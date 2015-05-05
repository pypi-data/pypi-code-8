#!c:\Users\Uwe\Projects\emzed\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'emzed==2.11.1','console_scripts','emzed.console'
__requires__ = 'emzed==2.11.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('emzed==2.11.1', 'console_scripts', 'emzed.console')()
    )
