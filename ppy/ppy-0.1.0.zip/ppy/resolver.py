"""
ppy.resolver
~~~~~~~~~~~~

The local site packages resolver.
"""

import os


site_packages_dirname = 'site-packages'
requirements_filename = 'requirements.json'


def resolve_package_path(script_path):
    """Resolves the local site packages."""

    # Start with the base script path
    current_path = os.path.abspath(script_path)
    child_path = None

    while current_path != child_path:
        # TODO: If cwd is a/site-packages/b/ don't return a/site-packages

        # Check current directory for local site-package or requirements.json
        if os.path.exists(os.path.join(current_path, site_packages_dirname)):
            return current_path
        if os.path.exists(os.path.join(current_path, requirements_filename)):
            return current_path

        # Try parent directory
        child_path = current_path
        current_path = os.path.dirname(current_path)

    return None
