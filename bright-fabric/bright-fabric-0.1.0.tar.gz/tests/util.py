# -*- coding: utf-8 -*-
# (c) 2015 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from fabric.state import env


class ArgumentCaptor(object):

    def __eq__(self, argument):
        self.argument = argument
        return True


class OverrideFabricConfig(object):

    def __init__(self, **kwargs):
        self.initial_config = env.copy()
        self.overrides = env.copy()
        self.overrides.update(kwargs)

    def __enter__(self):
        env.clear()
        env.update(self.overrides)

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.clear()
        env.update(self.initial_config)
