import ndex.client as nc
import json

devNdex = nc.Ndex("http://dev.ndexbio.org", "test", "ndex")

devNdex.set_debug_mode(True)

network = devNdex.get_complete_network('166a0e51-1a16-11e5-8169-0aa4c1de39d1')

provenance = devNdex.get_provenance('166a0e51-1a16-11e5-8169-0aa4c1de39d1')

print json.dumps(provenance, sort_keys=True, indent=4, separators=(',', ': '))

devNdex.set_provenance('166a0e51-1a16-11e5-8169-0aa4c1de39d1', provenance)