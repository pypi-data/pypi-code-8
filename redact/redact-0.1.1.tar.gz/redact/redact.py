import sys
from os import path
import re
import json
from opster import command
from cliui import prompt, sigint


var_pattern = r'#\{([a-zA-Z0-9_.-]+)\}'


def render(tmpl, names):
    def get_val_by_name(obj):
        key = obj.group(1)
        if key in names:
            return names[key]
        else:
            return ''
    return re.sub(var_pattern, get_val_by_name, tmpl)


def get_in(d, keys):
    for k in keys:
        if d is not None and k in d:
            d = d[k]
        else:
            return None
    return d


def set_in(d, keys, val):
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    d[keys[-1]] = val


def ensure_vars(template, kvs):
    vars = [var.split(".") for var in re.findall(var_pattern, template)]
    for var in vars:
        if None is get_in(kvs, var):
            try:
                set_in(kvs, var, prompt(".".join(var) + " > "))
            except Exception:
                print("quit")
                sys.exit(1)


def render_from_tmpl(pth, kvs):
    pth = path.expanduser(pth)
    print("processing %s" % pth)
    if not path.exists(pth):
        print("%s not found" % pth)
        return False
    with open(pth) as i:
        template = i.read()
        ensure_vars(template, kvs)
        result = render(template, kvs)
        (output, _) = path.splitext(pth)
        if path.isfile(output):
            with open(output, 'r') as original:
                if original.read() == result:
                    return False
        with open(output, 'w') as o:
            o.write(result)
            return True


def load_template_pathes(pth):
    pth = path.expanduser(pth)
    if path.exists(pth):
        with open(pth) as fp:
            return fp.read().splitlines()
    return []


def dump_template_pathes(pth, pathes):
    pth = path.expanduser(pth)
    with open(pth, 'w') as fp:
        fp.writelines(pathes)


def load_secrets(pth):
    pth = path.expanduser(pth)
    if path.exists(pth):
        with open(pth) as fp:
            try:
                return json.load(fp)
            except Exception:
                pass
    return {}


def dump_secrets(pth, kvs):
    pth = path.expanduser(pth)
    with open(pth, 'w') as fp:
        return json.dump(kvs, fp)


@command(usage='[-t templates.txt] [-s secrets.json] [file]')
def main(template=None,
         templates=('t', '',
                    'file containing location of template files'),
         secrets=('s', '',
                  'file to store secrets')):
    '''rendering dotfiles from template

examples:

  render ~/.muttrc and enter the variables interactively:

    redact ~/.muttrc.tpl

  render ~/.muttrc and save/load variables to ~/.passwords:

    redact -s ~/.passwords ~/.muttrc.tpl

  render a list of files in templates.txt and save/load variables from secrets:

    redact -t templates.txt -s ./secrets

    '''
    if secrets:
        secrets_store = load_secrets(secrets)
    else:
        secrets_store = {}

    if templates:
        template_pathes = load_template_pathes(templates)
    else:
        template_pathes = []

    if template:
        (target, _) = path.splitext(template)
        if render_from_tmpl(template, secrets_store):
            print("%s updated" % target)
        else:
            print("%s not changed" % target)
        if templates:
            if template not in template_pathes:
                template_pathes.append(template)
                dump_template_pathes(templates, template_pathes)

    elif templates:
        if not template_pathes:
            print("no templates found")
            sys.exit(1)
        for pth in template_pathes:
            if render_from_tmpl(pth, secrets_store):
                print("processed %s" % pth)
            else:
                print("skiped %s" % pth)
    else:
        print("redact -h for help")
        sys.exit(1)

    if secrets:
        dump_secrets(secrets, secrets_store)


@sigint
def on_int(signal, frame):
    print("quit")
    sys.exit(1)


def redact():
    main.command()
