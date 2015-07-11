import os
import yaml
import shutil
import pytest
import reseasdk
from reseasdk.commands.build import tsort, RecursiveDependencyError


def test_tsort():
    deps = {
        'a': ['b', 'c'],
        'b': ['c'],
        'c': []
    }
    assert tsort(deps) == ['c', 'b', 'a']

    deps = {
        'a': ['b', 'c'],
        'b': ['c'],
        'c': [],
        'd': ['a'],
    }
    assert tsort(deps) == ['c', 'b', 'a', 'd']

    deps = {
        'a': ['b', 'c'],
        'b': ['c', 'd'],
        'c': [],
        'd': ['b'], # recursion!!!
    }
    with pytest.raises(RecursiveDependencyError):
        tsort(deps)


def test_build(package):
    build_dir = 'build/release'
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    package_yml = yaml.load(open('package.yml'))
    package_yml['category'] = 'application'
    package_yml['requires'] = ['c_lang', 'discovery', 'log']
    package_yml['build']['sources'] = ['src/startup.c']
    yaml.dump(package_yml, open('package.yml', 'w'))

    config_build_yml = yaml.load(open('config.release.yml'))
    config_build_yml['HAL'] = 'userspace'
    config_build_yml['APPS'] = ['log', 'discovery']
    yaml.dump(config_build_yml, open('config.release.yml', 'w'))

    config_test_yml = yaml.load(open('config.test.yml'))
    config_test_yml['HAL'] = 'userspace'
    config_test_yml['APPS'] = ['log', 'discovery']
    yaml.dump(config_test_yml, open('config.test.yml', 'w'))

    open('src/startup.c', 'w').write("""\
#include <resea.h>

Result sandbox_startup(void){

  return OK;
}
""")

    reseasdk.main(['build'])
    assert os.path.exists('build/release/executable')

