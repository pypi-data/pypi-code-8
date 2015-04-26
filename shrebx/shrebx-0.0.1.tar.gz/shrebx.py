from random import sample
from string import ascii_letters, digits
from configparser import ConfigParser, NoOptionError

def shrebx(file_name,
           section_name = 'secrets', key_length = 62,
           random_fields = ['DATABASE_PASSWORD'],
           manual_fields = ['SECRET_KEY']):
    'Load secrets from a configuration file, generating them if needed.'

    c = ConfigParser()
    c.read(file_name)
    if section_name not in c.sections():
        c.add_section(section_name)
    section = c[section_name]

    output = {}
    for manual_field in manual_fields:
        if manual_field in section.keys():
            output[manual_field] = section[manual_field]
        else:
            output[manual_field] = None

    for random_field in random_fields:
        if random_field not in section.keys():
            key = ''.join(sample(ascii_letters + digits, key_length))
            c.set(section_name, random_field, key)
        output[random_field] = c.get(section_name, random_field)

    with open(file_name, 'w') as fp:
        c.write(fp)

    return output
