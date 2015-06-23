import os
from django.core.files.storage import DefaultStorage
from lor.settings import FILES_URLS


class LorStorage(DefaultStorage):
    """
    Fake Storage using class:`django.core.files.storage.DefaultStorage`,
    for handle files. It deletes files listed in ``LOR_FILES_URLS`` before
    make its meth:`post_process`.
    """
    def post_process(self, paths, *args, **kwargs):
        """
        Delete files in ``LOR_FILES_URLS`` and launch
        meth:`DefaultStorage.post_process`.

        :param paths: List of tuple with Storage class and file path
        :type paths: ``list`` of ``(:class:`Storage`, str)

        :returns: List of files to post process
        :rtype: ``list``
        """
        lor_files_paths = [v[0] for v in FILES_URLS.values()]
        for file_path, value in paths.copy().items():
            if file_path in lor_files_paths:
                paths.pop(file_path)
                full_path = os.path.join(self.location, file_path)
                if not kwargs.get('dry_run'):
                    os.remove(full_path)
                    print("Deleting '%s'" % full_path)
        print("Copied and deleted %s files" % len(lor_files_paths))
        files = [] if not hasattr(DefaultStorage, 'post_process') else \
            super(LorStorage, self).post_process(paths, *args, **kwargs)
        return files

    def url(self, path):
        return self.__class__().url(path)
