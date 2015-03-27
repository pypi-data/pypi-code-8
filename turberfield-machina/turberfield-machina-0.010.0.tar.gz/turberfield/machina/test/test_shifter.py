#!/usr/bin/env python3
# encoding: UTF-8

# This file is part of turberfield.
#
# Turberfield is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Turberfield is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with turberfield.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import asyncio
from collections import OrderedDict
from collections.abc import Callable
from collections.abc import Mapping
import decimal
from io import StringIO
import itertools
import json
import unittest
import uuid
import warnings

from turberfield.machina.demo.simulation import Simulation
from turberfield.machina.shifter import Shifter
from turberfield.machina.shifter import steadypace
from turberfield.machina.shifter import Fixed
from turberfield.machina.shifter import Mobile
from turberfield.machina.shifter import Tick
from turberfield.utils.expert import Expert
from turberfield.utils.homogeneous import point
from turberfield.utils.homogeneous import vector
from turberfield.utils.travel import Impulse
from turberfield.utils.travel import trajectory


class ShifterTests(unittest.TestCase):

    def create_theatre():
        rv = OrderedDict([
            (stage, Mobile(
                steadypace(trajectory(), routing, timing), 10))
            for stage, routing, timing in Simulation.patterns])
        rv.update(
            OrderedDict([
                (stage, Fixed(posn, reach))
                for stage, posn, reach in Simulation.static]))
        return rv

    def setUp(self):
        class_ = self.__class__
        class_.theatre = ShifterTests.create_theatre()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        warnings.simplefilter("ignore")

        # Plug in a StringIO object to the HATEOAS endpoints
        self._services = Shifter.options()
        class_._outputs = [StringIO(), StringIO()]
        self._services["positions"] = (
            self._services["positions"]._replace(
                dst=class_._outputs[0]
            )
        )
        self._services["bridging"] = (
            self._services["bridging"]._replace(
                dst=class_._outputs[1]
            )
        )
        class_.tick = Tick(0, 0, 0.3, 0.1, None)

    def test_has_provide(self):
        p = Expert()
        shifter = Shifter(
            self.theatre,
            loop=self.loop, **self._services
        )
        self.assertIsInstance(shifter, Expert)
        self.assertTrue(hasattr(shifter, "declare"))

    def test_has_services(self):
        shifter = Shifter(
            self.theatre,
            loop=self.loop, **self._services
        )
        self.assertEqual(7, len(shifter._services))

    def test_first_instantiation_defines_services(self):
        shifter = Shifter(
            self.theatre,
            loop=self.loop, **self._services
        )
        self.assertIsInstance(Shifter.options, Callable)
        self.assertIsInstance(
            shifter._services, Mapping)
        self.assertIsInstance(
            shifter._services["positions"].dst, StringIO)

        self.assertIsNot(Shifter.public, None)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.assertRaises(
                UserWarning,
                Shifter,
                ShifterTests.theatre,
                loop=self.loop,
                **Shifter.options()
            )

    def test_tick_attribute_service(self):
        shifter = Shifter(
            self.theatre,
            loop=self.loop, **self._services
        )
        task = asyncio.Task(
            shifter(0, 0.3, 0.1, loop=self.loop), loop=self.loop
        )

        self.loop.run_until_complete(task)
        self.tick = task.result()
        self.assertAlmostEqual(
            self.tick.stop,
            self.tick.t + self.tick.step, places=10
        )
        self.assertEqual(self.tick, Shifter.public.tick)

    def test_page_attribute_service(self):
        shifter = Shifter(
            self.theatre,
            loop=self.loop, **self._services
        )
        task = asyncio.Task(
            shifter(0, 0.3, 0.1, loop=self.loop), loop=self.loop
        )

        self.loop.run_until_complete(task)
        self.tick = task.result()
        self.assertEqual(4, len(Shifter.public.movement))

    def test_hateoas_attribute_service(self):
        shifter = Shifter(
            self.theatre,
            loop=self.loop, **self._services
        )
        task = asyncio.Task(
            shifter(0, 0.3, 0.1, loop=self.loop), loop=self.loop
        )

        self.loop.run_until_complete(task)
        self.tick = task.result()
        history = ShifterTests._outputs[0].getvalue()
        data = "{" + history.rpartition("}{")[-1]
        output = json.loads(data)
        self.assertIn("info", output)
        self.assertIn("nav", output)
        self.assertIn("items", output)
        self.assertIn("options", output)


class TaskTests(unittest.TestCase):

    def setUp(self):
        class_ = self.__class__
        class_.theatre = ShifterTests.create_theatre()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def test_tasks_for_queues(self):
        q = asyncio.Queue(loop=self.loop)
        shifter = Shifter(
            self.theatre, q, loop=self.loop
        )

        self.assertEqual(1, len(shifter._watchers))
        self.assertTrue(
            all(isinstance(i, asyncio.Task) for i in shifter._watchers)
        )

    def test_watcher_consumes_queues(self):

        @asyncio.coroutine
        def one_shot(q):
            # Collision id, actor, stage
            obj = (id(None), uuid.uuid4().hex, uuid.uuid4().hex)
            yield from q.put(obj)
            yield from q.put(None)

        q = asyncio.Queue(loop=self.loop)
        shifter = Shifter(
            self.theatre, q, loop=self.loop
        )

        listener = shifter._watchers[0]
        self.assertIsInstance(listener, asyncio.Task)
        self.loop.run_until_complete(asyncio.wait(
            [one_shot(q), listener], loop=self.loop, timeout=1
        ))

    def test_shifter_collisions_detected(self):
        theatre = self.theatre.copy()
        collider = Shifter.collision(theatre)
        collider.send(None)

        # During movement, c moves on to b's position
        infinity = decimal.Decimal("Infinity")
        items = list(theatre.items())
        (c, _), (b, fix) = items[-1], items[-2]
        imp = Impulse(
            1, infinity, vector(0, 0, 0), fix.posn
        )
        collisions = collider.send((c, imp, 5))
        self.assertEqual(5, collisions[frozenset((b, c))])


class SteadypaceTests(unittest.TestCase):

    def test_there_and_back_again(self):
        routes = [
            (point(160, 100, 0), point(484, 106, 0)),
            (point(484, 106, 0), point(160, 100, 0)),
        ]
        times = (2, 2)
        op = steadypace(trajectory(), iter(routes), iter(times))
        op.send(None)
        for n in range(42):
            imp = op.send(decimal.Decimal(n) / 10)
            if n == 21:
                with self.subTest(n=n):
                    self.assertEqual(2, imp.tBegin)
                    self.assertEqual(routes[0][1], imp.pos)
            elif n == 41:
                with self.subTest(n=n):
                    self.assertEqual(4, imp.tBegin)
                    self.assertEqual(routes[1][1], imp.pos)
