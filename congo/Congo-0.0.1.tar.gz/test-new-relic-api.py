from pprint import pprint
from newrelic_api import Servers

API_KEY = "71cd4973f4cb867946257e44bc16f0950495d552e7024e0"

servers = Servers(api_key=API_KEY)

pprint(servers.list())