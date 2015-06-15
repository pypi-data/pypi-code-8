import os.path
import sys


__BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CHROMEDRV_PATH = os.path.join(__BASE_PATH, 'bin')

# little hack to have chrome driver in sys path
sys.path.insert(1, __BASE_PATH)
