"""
PageUp: A simple ReStructuredText based static page generator.

'It ain't supposed to be pretty, it's just supposed to work.'
    - me. right now.
"""

from docutils.core import publish_parts
from jinja2 import Environment, FileSystemLoader
from os import getcwd, path, makedirs
import requests


# Root directory of the app and where it is installed (system wide or in a
# virtual environment.
_ROOT = path.abspath(path.dirname(__file__))



def test_files():
    """
    Tests to see if all of the appropriate files re in the right places.
    """
    yell = ''
    needed = ['template.jinja', 'content.rst', 'style.css']
    for n in needed:
        if not path.isfile(n):
            yell += n + " does not appear to be available.\n"
    if yell:
        raise Exception(yell + " run `pageup init` to fix it.")
        exit(1)


def build():
    """
    Builds pages given template.jinja, style.css, and content.rst
    produces index.html.
    """
    test_files()
    with open('content.rst') as f:
        content = publish_parts(f.read(), writer_name='html')
        title = content['title']
        body =  content['html_body'].replace('\n',' ')

    with open('template.jinja', 'r') as f:
        loader = FileSystemLoader(getcwd())
        env= Environment(loader=loader)
        template = env.get_template('template.jinja')
        page =  template.render(title=title,
                                content=body)

    with open('index.html', 'w') as f:
        f.write(page)


def init(directory=None):
    """
    Initializes a new site in the `directory`
    Current working dir if directory is None.
    """
    if directory is not None and not path.exists(directory):
        makedirs(directory)
    else:
        print('%s already exists, populating with template files' % (directory))
        directory = ''

    if not path.isfile(path.join(directory,'style.css')):
        grab('style.css', directory)
        print('Added sample style')
    if not path.isfile(path.join(directory,'template.jinja')):
        grab('template.jinja', directory)
        print('Added sample template.jinja')
    if not path.isfile(path.join(directory,'content.rst')):
        grab('content.rst', directory)
        print('Added sample content.rst')

def grab(filename, directory):
    """
    Copy dist files from their installed path to cwd/directory/filename
    cwd is the current directory,
    directory is their custom site name dir,
    filename is the name of the example file being copied over.
    """
    r = requests.get('https://raw.githubusercontent.com/ElijahCaine/pageup/master/pageup/data/'+filename)
    with open(path.join(directory,filename), 'wb') as f:
        f.write(r.content)
