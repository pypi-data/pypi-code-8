import sys
if sys.platform == 'win32':
    from tzlocal.win32 import get_localzone, reload_localzone
else:
    from tzlocal.unix import get_localzone, reload_localzone
    
