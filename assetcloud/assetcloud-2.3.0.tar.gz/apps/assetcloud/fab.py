from bright_fabric.fab import tag_matches_package_version, abs_path
from fabric.api import env, local
from fabric.utils import error, abort
import bright_vc
import re


def test():
    test_app_string = ''
    if 'test_apps' in env:
        test_app_string = ' '.join(env.get('test_apps'))
    local('./manage test %s' % test_app_string)


def git_tag(tag):
    """
    Create a tag, push it to github and then roll it out

    Example: fab -R test tag_and_rollout:tag=v0.2.0
    """
    try:
        bright_vc.check_tag(tag)
    except Exception as e:
        abort(str(e))

    if 'app_version' in env and not tag_matches_package_version(tag, env.app_version):
        error("Package version and tag must match to continue")

    if not 'skip_tests' in env:
        test()

    # "v1.2.3" -> "version 1.2.3"
    version_description = re.sub('^v', 'version ', tag)
    local('git tag -a "%s" -m "%s"' % (tag, version_description))
    local('git push origin "%s"' % tag)


def touch_static():
    """
    Hit the timestamp on every file in static to bust any erroneous '304' not
    modified responses.
    """
    local('find static -exec touch {} \;')


def start_solr():
    """
    Start the Apache Solr indexing server.
    """
    SOLR_HOME = abs_path('solr')
    local('''cd '%s' && '''
          '''java -Dsolr.solr.home='%s' -jar start.jar''' % (env.solr_config, SOLR_HOME))


def build_solr_schema():
    """
    Update the Solr schema.xml files from the model and index declarations.
    """
    local('./manage build_solr_schema -v 0 > solr/main/conf/schema.xml')
    local('cp -p solr/main/conf/schema.xml solr/test/conf/schema.xml')


def teardown():
    """
    Destroy the current database and media files.
    """
    for dir in ('databases', 'media'):
        local('rm -rf %s/*' % dir)


def clean():
    """
    Remove all temporary build and .pyc files.
    """
    for dir in ('build', 'static/CACHE'):
        local('rm -rf %s/*' % dir)
    local('''find . -name '*.pyc' -exec rm -f {} \;''')


def upload():
    """
    Perform local (django-)compression of js/css files, then upload to epio
    """
    local('./manage compress --force')
    local('epio upload')
    local('epio django -a assetcloud migrate')
