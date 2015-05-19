def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('standard', parent_package, top_path,'.')
    print "ok"
    config.version = '1.0'
    config.description = """A python package for Bayesian estimation \
    using Markov chain Monte Carlo"""
    config.author = "Christopher Strickland"
    config.author_email = 'christopher.strickland@qut.edu.au'
    config.license = "GNU GPLv3"
    config.add_data_files('glm_helper.py','glm.py', 'mix_model.py', 'tobit.py', '__init__.py')
    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
    
