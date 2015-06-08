import re

def get_version_from_setup_py():
    """get_version_from_setup_py() -> string

    Extract and return the version form the setup.py file."""
    with file("setup.py") as f:
        for line in f:
            if line.startswith("version"):
                return re.split("version = '(.*)'", line)[1]