"""Search for a test."""
import os, sys

class Search(object):
    """A search for tests that matches both test modules and test filenames."""
    def __init__(self, directory, text):
        self.directory = directory
        self.text = text

    def run(self):
        """Actually do the search."""
        module_names = []       # All found module_names
        file_names = []         # All discovered tests

        # List of filenames (e.g. 'tests/my_test_group/test_something.py' that match the search
        self.file_matches = []

        # List of test module names (e.g. 'tests.my_test_group.test_something' that match the search)
        self.module_matches = []

        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in [f for f in filenames if f.endswith(".py") and f.startswith("test_")]:
                file_path = os.path.join(dirpath, filename).replace(self.directory + os.sep, "")
                file_names.append(file_path)
                module_names.append(file_path.replace(".py", "").replace("/", "."))

        for potential_name in file_names:
            if self.text in potential_name:
                self.file_matches.append(potential_name)

        for potential_name in module_names:
            if self.text in potential_name:
                self.module_matches.append(potential_name)

    def just_one(self):
        """Return the only matching test, if there was just one."""
        if len(self.file_matches) == 1 and len(self.module_matches) < 2:
            return self.file_matches[0]
        elif len(self.module_matches) == 1 and len(self.file_matches) < 2:
            return self.module_matches[0].replace(".", os.sep) + ".py"
        return None

    def none(self):
        """Return true if there were no matches, otherwise false."""
        return len(self.file_matches) == 0 and len(self.module_matches) == 0

    def matching(self):
        """Return a list of the tests matching the search, along with their type."""
        if len(self.file_matches) > len(self.module_matches):
            return ("filename", self.file_matches)
        else:
            return ("module", self.module_matches)