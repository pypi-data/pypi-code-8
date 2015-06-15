import os.path
import sys


__BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin')
CHROMEDRV_PATH = os.path.join(__BASE_PATH, 'chromedriver')

# little hack to have chrome driver in sys path
sys.path.insert(1, __BASE_PATH)
