import argparse
import os
import stat
import yaml
import subprocess
import jinja2
from reseasdk import info, error, generating

START_C_TEMPLATE = """\

{% for app in start_order %}
void {{ app }}_startup();
{% endfor %}

void start_apps(void){

{% for app in start_order %}
    {{ app }}_startup();
{% endfor %}
}
"""

MAKEFILE_TEMPLATE = """\

.PHONY: default
BUILD_DIR = build/{{ target }}
default: $(BUILD_DIR)/executable

# keep blank not to delete intermediate file (especially stub files)
.SECONDARY:
$(VERBOSE).SILENT:
CMDECHO = ./$(BUILD_DIR)/cmdecho


#
#  Global build config
#
{% for k,v in config.items() -%}
{{ k }} ?= {{ v }}
{% endfor %}

# start.o
# FIXME: ugly
{%- for ext,compile,genstub,stub_prefix,stub_suffix in langs %}
{% if ext == 'c' %}
$(BUILD_DIR)/start.o: $(BUILD_DIR)/start.c
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'COMPILE({{ ext }})' $@
	{{ compile }} $@ $<
{% endif %}
{% endfor %}

# executable
$(BUILD_DIR)/executable: \\
                         {% for name,v in build_packages.items() -%}
                         $(BUILD_DIR)/{{name}}/__package__.o \\
                         {% endfor -%}
                         $(BUILD_DIR)/start.o
	$(CMDECHO) LINK $@
	$(HAL_LINK) $@ $^

#
#  stub
#
{%- for ext,compile,genstub,stub_prefix,stub_suffix in langs %}
$(BUILD_DIR)/stubs/{{ ext }}/{{ stub_prefix }}%{{ stub_suffix }}: packages/%/package.yml
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'GENSTUB({{ ext }})' $@
	{{ genstub }} $@ $<
{% endfor %}

#
#  Packages
#
LD_R ?= ld -r -o
MKDIR ?= mkdir

{% for name,v in build_packages.items() -%}
# -- {{ name }} --

{%- for ext,compile,genstub,stub_prefix,stub_suffix in v['langs'] %}

# compile
$(BUILD_DIR)/{{ name }}/%.o: packages/{{ name }}/%.{{ ext }} $(BUILD_DIR)/Makefile \\
  $(addsuffix {{ stub_suffix }},$(addprefix $(BUILD_DIR)/stubs/{{ ext }}/{{ stub_prefix }},{{ v['depends'] | join(' ') }}))
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'COMPILE({{ ext }})' $@
	{{ compile }} $@ $<
{%- endfor %}

# __package__.o
$(BUILD_DIR)/{{ name }}/__package__.o: {{ v['objs'] | join(' ') }}
	$(CMDECHO) GEN $@
	$(LD_R) $@ $(filter %.o, $^)
{% endfor %}
"""

CMDECHO = """\
#!/usr/bin/env zsh
autoload -Uz colors; colors

cmd=$1; shift
pad=${(r:$((16-${#cmd})):: :)}
echo "  ${fg[magenta]}$cmd$reset_color$pad$*"
"""


current_package = ''
package_ymls = {}


def load_package_yml(package):
    global package_ymls

    if package in package_ymls:
        return package_ymls[package]
    else:
        if not os.path.exists('packages/{}'.format(package)):
            get_package(package)
        yml = yaml.load(open('packages/{}/package.yml'.format(package)))
        package_ymls[package] = yml
        return yml


class RecursiveDependencyError(Exception):
    pass


def tsort(deps):
    """ Topological sorting by Kahn's algorithm """
    l = []  # the result
    num = 0 # the number of all edges
    ins = {x: 0 for x in deps} # the number of in-degree edges

    # count in-degree edges
    for x in deps:
        for y in deps[x]:
            ins[y] += 1
            num += 1

    s = [] # a list of nodes with no in-defree edges
    for x in deps:
        if ins[x] == 0:
            s.append(x)

    while s:
        x = s.pop()
        l.insert(0, x)
        for d in deps[x]:
            num -= 1
            ins[d] -= 1
            if ins[d] == 0:
                s.append(d)

    if num > 0:
        raise RecursiveDependencyError()

    return l
          

def get_required_packages(packages, added=None):
    """ Returns a dict of required packages: `{package_name: [dependencies]}` """

    if added is None:
        added = []

    deps = {}
    for package in packages:
        deps[package] = load_package_yml(package).get('requires', [])
        unadded = list(filter(lambda r: r not in added, deps[package]))
        added += unadded + [package]
        deps.update(get_required_packages(unadded, added=added))
    return deps


def resolve_required_packages(packages, types=None, include_themselves=None):
    """ Returns a list of package names, ordered by dependency."""

    # TODO: add tests

    if types is None:
        types = ['application', 'library', 'interface', 'group']

    l = []
    for x in tsort(get_required_packages(packages)):
        if load_package_yml(x).get('category') in types:
            l.append(x)

    if not include_themselves:
        # remove the elements in `packages` from `l`
        l2 = []
        for x in l:
            if x not in packages:
                l2.append(x)
        l = l2

    return l


def _get_package(package, method, symlink_from=None):
    # Note: we're in the `packages` directory
    if method == 'symlink':
        os.symlink(symlink_from, package)
    elif method == 'git-clone':
        uri = 'https://github.com/resea/{}'.format(package) # XXX
        info('git: cloning {} ({})'.format(package, uri))
        p = subprocess.Popen(['git', 'clone', uri])
        p.wait()
    else:
        error("unknown method to get a package: '{}'".format(method))


def get_package(package):
    """ Prepare the package in `packages` directory. """
    os.makedirs('packages', exist_ok=True)
    os.chdir('packages')

    kwargs = {}
    if package == current_package:
        kwargs['symlink_from'] = os.path.normpath(os.getcwd() + '/..')
        method = 'symlink'
    else:
        method = 'git-clone'

    _get_package(package, method, **kwargs)

    os.chdir('..')


def load_global_config(packages):
    config = {}
    for package in packages:
        config_path = 'packages/{}/config.global.yml'.format(package)
        if os.path.exists(config_path):
            config.update(yaml.load(open(config_path)))
    return config


def load_build_config(target):
    return yaml.load(open('config.{}.yml'.format(target)))


def load_packages(package_yml, target):
    # load config.<target>.yml
    config = load_build_config(target)
    builtin_apps = config.get('APPS', [])
    if package_yml.get('category') == 'application':
        builtin_apps.append(package_yml['name'])

    required = resolve_required_packages(package_yml['requires'] +
                                         [config['HAL']],
                                         include_themselves=True)

    # load all config.global.yml
    config.update(load_global_config(required))
    return config, required, builtin_apps


def load_current_package_yml():
    return yaml.load(open('package.yml'))


def generate_makefile(target):
    global current_package

    package_yml = load_current_package_yml()
    current_package = package_yml['name']

    # resolve packages dependencies, load their build config and prepare them
    config, required, builtin_apps = load_packages(package_yml, target)
    hal = config['HAL']

    # generate the build directory
    build_dir = 'build/{}'.format(target)
    if not os.path.exists(build_dir):
        generating('MKDIR', build_dir)
        os.makedirs(build_dir, exist_ok=True)

    # generate start.c
    start_c_path = 'build/{}/start.c'.format(target)
    generating('GEN', start_c_path)
    order = resolve_required_packages(builtin_apps, types=['application'],
                                      include_themselves=True)
    start_c = jinja2.Template(START_C_TEMPLATE).render(start_order=order)
    open(start_c_path, 'w').write(start_c)

    # create log file
    log_path = 'build/{}/boot.log'.format(target)
    if not os.path.exists(log_path):
        generating('GEN', log_path)
        open(log_path, 'w').close()

    # generate cmdecho
    cmdecho_path = 'build/{}/cmdecho'.format(target)
    if not os.path.exists(cmdecho_path):
        generating('GEN', cmdecho_path)
        with open(cmdecho_path, 'w') as f:
            f.write(CMDECHO)
        os.chmod(cmdecho_path, 0o777)

    generating('GEN', 'Makefile')

    # convert a list in `config` to a string
    for k,v in config.items():
        if isinstance(v, list):
            config[k] = ' '.join(v)

    # langs
    langs = []
    for lang in filter(lambda s: s.startswith('LANG_COMPILE_'),
                       config.keys()):
        ext = lang.split('LANG_COMPILE_')[1]
        try:
            l = (ext.lower(),
                 config['LANG_COMPILE_' + ext],
                 config['LANG_GENSTUB_' + ext],
                 config['LANG_STUB_PREFIX_' + ext],
                 config['LANG_STUB_SUFFIX_' + ext]
                )
        except KeyError as e:
            error('lang_{} does not define {} in its config'.format(ext.lower(), e))
        langs.append(l)

    # build rules of __package__.o
    libs = resolve_required_packages([current_package], types=['library'])
    build_packages = {}
    for name in builtin_apps + libs + [hal]:
        if package_ymls[name].get('build') and \
           len(package_ymls[name]['build'].get('sources', [])) > 0:
            build_dir = 'build/{}/{}'.format(target, name)
            sources = package_ymls[name]['build']['sources']
            objs = list(map(lambda source:
                            '{}/{}.o'.format(build_dir, os.path.splitext(source)[0]),
                            sources))
            build_packages[name] = {
                'objs': objs,
                'langs': langs,
                'depends': resolve_required_packages([name], include_themselves=True)
            }

    # let's generate Makefile
    makefile = jinja2.Template(MAKEFILE_TEMPLATE).render(**locals())
    open('build/{}/Makefile'.format(target), 'w').write(makefile)


def build(target, regenerate=False):
    """ Builds an executable. """
    if regenerate or not os.path.exists('build/{}/Makefile'.format(target)):
        generate_makefile(target)

    # execute make(1)
    try:
        r = subprocess.call(['make', '-f', 'build/{}/Makefile'.format(target)])
    except Exception as e:
        error('failed to execute make: ' + str(e))

    if r != 0:
        error('error occurred during make')


def main(args_):
    parser = argparse.ArgumentParser(prog='resea build',
                                     description='build an executable')
    parser.add_argument('-r', action='store_true', help='regenerate Makefile')
    parser.add_argument('--target', default='release', help='the build target')
    args = parser.parse_args(args_)

    build(args.target, args.r)
