import os
import urllib2
from django.core.management.base import BaseCommand, CommandError
from lor.settings import FILES_URLS, STATIC_DIR


def _ask_yes_no(prompt_text):
    """
    Prompt for ask 'yes' or 'no' to user. Default response is 'yes'.
    'No' matches when first letter is `n` or `N`.

    :param prompt_text: Text to display
    :type prompt_text: `str`

    :returns: Boolean matching with user's answer
    :rtype: `bool`
    """
    res = raw_input("%s [Y/n]: " % prompt_text)
    return not res.lower().startswith('n')


class Command(BaseCommand):
    help = 'Download defined static files'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--noinput', action='store_true',
            help="Tells Django to NOT prompt the user for input of any kind.")
        # parser.add_argument('-o', '--noinput', action='store_true')
        # parser.add_argument('-f', '--files')

    def _create_static_directory(self, noinput):
        """
        Create LOR static directory.

        :param noinput: Disable user's questions
        :type noinput: `bool`
        """
        if not os.path.exists(STATIC_DIR):
            if noinput or _ask_yes_no('Create %s' % STATIC_DIR):
                os.makedirs(STATIC_DIR)
                self.stdout.write('Created %s' % STATIC_DIR)

    def _check_destination(self, noinput, file_path):
        """
        Check if a file is writable on filesystem.

        :param noinput: Disable user's questions
        :type noinput: `bool`

        :param file_path: Path where to write file
        :type file_path: `str`

        :returns: True or false if writable
        :rtype: `bool`
        """
        if os.path.exists(file_path):
            if not noinput and not _ask_yes_no('Overwrite %s' % file_path):
                return False
            elif noinput:
                self.stdout.write("No create %s" % file_path)
                return False
        return True

    def _get_remote_file(self, url):
        """
        Get remote file from an url.

        :param url: URL where file is
        :type url: `str`

        :returns: Response object or nothing if there's a problem.
        :rtype: class:`urllib.addinfourl` or `NoneType`
        """
        try:
            res = urllib2.urlopen(url)
            if res.code != 200:
                msg = "Can't get '%s' (%i)" % (url, res.code)
                self.stderr.write(msg)
                return None
        except IOError as ex:
            self.stderr.write("Can't get '%s': %s" % (url, ex.args[0]))
            return None
        return res

    def _create_local_file(self, response, file_path):
        """
        Write file to local filesystem.

        :param response: File to write
        :type response: class:`urllib.addinfourl` or `file`

        :param file_path: Where to write the file
        :type file_path: `str`
        """
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'wb') as fd:
            fd.write(response.read())
            self.stdout.write('Created %s' % file_path)

    def handle(self, *args, **opts):
        noinput = opts.get('noinput', False)
        self._create_static_directory(noinput)
        if not FILES_URLS:
            self.stdout.write("No file defined.")
        for static in FILES_URLS.keys():
            url = FILES_URLS[static][1]
            file_path = os.path.join(STATIC_DIR + FILES_URLS[static][0])
            if not self._check_destination(noinput, file_path):
                continue
            response = self._get_remote_file(url)
            if response is None:
                continue
            self._create_local_file(response, file_path)
