import ndex.client as nc

devNdex = nc.Ndex("http://dev.ndexbio.org", "test", "ndex")

network = devNdex.get_complete_network('166a0e51-1a16-11e5-8169-0aa4c1de39d1', debug=True)

ns = devNdex.save_new_network(network, debug=True)

id_to_delete = ns['externalId']

devNdex.delete_network(id_to_delete, debug=True)
