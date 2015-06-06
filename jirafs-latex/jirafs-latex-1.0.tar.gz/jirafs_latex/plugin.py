import os
import subprocess

import six

from jirafs.plugin import Plugin, PluginOperationError, PluginValidationError


class Latex(Plugin):
    """ Converts Latex documents into PDFs when uploading to JIRA.

    """
    MIN_VERSION = '1.10.0'
    MAX_VERSION = '1.99.99'

    LATEX_EXTENSIONS = ['tex']

    def get_command_args(self, original_filename):
        command = [
            'xelatex',
            original_filename
        ]

        return command

    def alter_file_upload(self, info):
        metadata = self.get_metadata()
        filename, file_object = info

        basename, extension = os.path.splitext(filename)
        if extension[1:] not in self.LATEX_EXTENSIONS:
            return filename, file_object
        new_filename = '.'.join([basename, 'pdf'])

        proc = subprocess.Popen(
            self.get_command_args(filename),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(file_object.read())

        if proc.returncode:
            raise PluginOperationError(
                "%s encountered an error while compiling PDF for %s: %s" % (
                    self.plugin_name,
                    filename,
                    stderr,
                )
            )

        with open(new_filename, 'rb') as temp_output:
            content = six.BytesIO(temp_output.read())

        for extension in ['pdf', 'log', 'aux']:
            os.unlink(
                '.'.join([basename, extension])
            )

        filename_map = metadata.get('filename_map', {})
        filename_map[new_filename] = filename
        metadata['filename_map'] = filename_map
        self.set_metadata(metadata)

        return new_filename, content

    def validate(self):
        try:
            subprocess.check_call(
                ['xelatex', '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, IOError, OSError):
            raise PluginValidationError(
                "%s requires xelatex to be installed." % (
                    self.plugin_name,
                )
            )
