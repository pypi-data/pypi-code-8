class SymfonyProject(object):
        
    def __init__(self, instance, dir):
        self.instance = instance
        self.dir = dir

    def init(self, **parameters):
        self.instance.run_commands(
            'cd ' + self.dir,
            'composer install --no-scripts',
            'cp app/config/parameters.yml.dist app/config/parameters.yml'
        )
        
        if parameters:
            self.set_parameters(**parameters)
        
    def set_parameters(self, **kwargs):
        for arg in kwargs:
            self.set_parameter(arg, kwargs[arg])
        
    def set_parameter(self, name, value):
        value = value.replace('/', '\/')
        
        self.instance.run_commands(
            'cd ' + self.dir,
            "sed -i -e 's/" + name + ": .*$/" + name + ": " + value + "/g' app/config/parameters.yml"
        )