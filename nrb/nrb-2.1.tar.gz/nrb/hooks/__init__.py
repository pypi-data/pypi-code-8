from nrb.hooks import commands
from nrb.hooks import files

def setup_hook(config):
    print "[setup_hook]: STARTED"
    print "[setup_hook]: ", config
    commands.CommandsConfig(config).run()
    files.FilesConfig(config, 'nrb').run()
    print "[setup_hook]: FINISHED"

