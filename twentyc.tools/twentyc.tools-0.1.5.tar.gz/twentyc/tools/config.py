from ConfigParser import ConfigParser
def dict_conf(filename):
  """
  Return dict object for *.conf file
  """
  config = ConfigParser()
  config.read(filename)
  rv = {}
  for section in config.sections():
    rv[section] = {}
    for key,value in config.items(section):
      rv[section][key] = value.strip('"').strip("'").decode("string_escape")
  return rv
