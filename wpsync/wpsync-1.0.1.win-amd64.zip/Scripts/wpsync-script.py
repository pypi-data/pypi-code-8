#!C:\Python34\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'wpsync==1.0.1','console_scripts','wpsync'
__requires__ = 'wpsync==1.0.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('wpsync==1.0.1', 'console_scripts', 'wpsync')()
    )
