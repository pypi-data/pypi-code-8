
import radical.utils as ru
import radical.pilot as rp
import sys
import pprint

dh = ru.DebugHelper()

session = rp.Session()

pm = rp.PilotManager(session=session)

cpd = rp.ComputePilotDescription()
cpd.resource = "local.localhost"
cpd.cores    = 1
cpd.runtime  = 1
cpd.sandbox  = "/tmp/radical.pilot.sandbox.unittests"
cpd.cleanup  = True

pilot = pm.submit_pilots(pilot_descriptions=cpd)

assert pilot is not None
assert pilot.start_time is None
assert pilot.stop_time is None

pilot.wait(state=[rp.ACTIVE, rp.DONE, rp.CANCELED, rp.FAILED], timeout=60)
assert pilot.submission_time is not None
assert pilot.state == rp.ACTIVE
assert pilot.start_time is not None
assert pilot.log is not None
assert pilot.sandbox == "file://localhost%s/radical.pilot.sandbox/%s-%s/" % (cpd.sandbox, session.uid, pilot.uid)

# the pilot should finish after it has reached run_time

pilot.wait(timeout=5*60)
assert pilot.state == rp.DONE
assert pilot.stop_time is not None

session.close()

