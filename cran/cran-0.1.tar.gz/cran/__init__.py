import pandas as pd
from cran import settings

def crantastic():
    return (u'''Clean is better than cluttered.
              Code documentation in markdown.
              Compatibility layer with R traditions.
              Idiomatic Pandas code inside.''')

def install_packages(package, repos='https://github.com/lovestats/', local=settings.CRAN_ROOT):
    if isinstance(package, basestring):
        # 1. Check if the 'package' exists in repositories of 'repos'
        # 2. Download or update the source code to 'local' (git clone)
        # 3. Reload
        pass
    elif isinstance(package, list):
        pass
    else:
        pass

def library(package):
    if isinstance(package, basestring):
        pass
    elif isinstance(package, list):
        pass
    else:
        pass

def max(it):
    if isinstance(it, pd.DataFrame):
        return it.values.max()
    else:
        pass
