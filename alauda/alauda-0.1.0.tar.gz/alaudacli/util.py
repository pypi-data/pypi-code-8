import sys


def parse_image_name_tag(image):
    result = image.split(':')
    if len(result) == 1:
        return image, 'latest'
    elif len(result) == 2:
        return result[0], result[1]
    else:
        print 'Invalid image name'
        sys.exit(1)


def parse_target_state(do_not_start):
    if do_not_start:
        return 'STOPPED'
    else:
        return 'STARTED'


def parse_instance_ports(port_list):
    def _parse_instance_port(_port):
        result = _port.split('/')
        if len(result) != 2:
            print 'Invalid port description. (Example of valid description: 80/tcp)'
            sys.exit(1)

        port = int(result[0])
        protocol = result[1]

        if protocol not in ['tcp']:
            print 'Invalid port protocal. Supported protocols: {tcp}'
            sys.exit(1)
        if port < 0 or port > 65535:
            print 'Invalid port number'
            sys.exit(1)

        return port, protocol

    parsed_ports = []
    if port_list is not None:
        for port_desc in port_list:
            port, protocol = _parse_instance_port(port_desc)
            parsed_ports.append({"container_port": port, "protocol": protocol})
    return parsed_ports


def parse_envvars(envvar_list):
    def _parse_envvar(_envvar):
        result = _envvar.split('=')
        if len(result) != 2:
            print 'Invalid environment variable'
            sys.exit(1)
        return result[0], result[1]

    parsed_envvars = {}
    if envvar_list is not None:
        for envvar in envvar_list:
            key, value = _parse_envvar(envvar)
            parsed_envvars[key] = value
    return parsed_envvars
