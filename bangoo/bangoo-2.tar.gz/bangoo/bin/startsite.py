from optparse import OptionParser
from django.core import management

PROJECT_TEMPLATE_URL = 'http://bangoo.lovasb.com/project_template.zip'

def create_site():
    parser = OptionParser(usage="usage: %prog [options] project_name")
    parser.add_option("-t", "--template", dest="template",
        help="Place where the project template is located")
    (options, args) = parser.parse_args()


    if len(args) != 1:
        parser.error("project_name must be specified")
    project_name = args[0]
    management.call_command('startproject', project_name, template=options.template or PROJECT_TEMPLATE_URL)


if __name__ == '__main__':
    create_site()