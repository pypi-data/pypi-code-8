class SecurityGroup(object):
    
    def __init__(self, infrastructure, id):
        self.infrastructure = infrastructure
        self.id = id
    
    def allow_inbound_port_for_group(self, port):
        self.infrastructure.aws(
            'ec2', 'authorize-security-group-ingress',
            '--group-id', self.id,
            '--source-group', self.id,
            '--port', str(port),
            '--protocol', 'tcp'
        )