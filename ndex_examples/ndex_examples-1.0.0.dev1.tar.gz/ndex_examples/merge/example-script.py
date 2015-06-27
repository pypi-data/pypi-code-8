import ndex.client as nc
import ndex.client.example.merge.bindingdb_merger as merger

devNdex = nc.Ndex("http://dev.ndexbio.org", "drh", "drh")

reactome_network = devNdex.getCompleteNetwork('f8cddf73-1c49-11e5-8169-0aa4c1de39d1')
# large 54,877
# bindingdb_network = devNdex.getCompleteNetwork('13f083ad-1c32-11e5-8169-0aa4c1de39d1')
# small 201
bindingdb_network = devNdex.getCompleteNetwork('5cf1ae26-1c1d-11e5-8169-0aa4c1de39d1')

merger.merge_network(bindingdb_network, reactome_network)

reactome_network['name'] = "merge_demo 5"
reactome_network['description'] = "merge_demo 5"

localNdex = nc.Ndex("http://localhost:8080", "test", "ndex_examples")

localNdex.saveNewNetwork(reactome_network)