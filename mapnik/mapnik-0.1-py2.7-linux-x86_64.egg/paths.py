import os

mapniklibpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins")
inputpluginspath = os.path.join(mapniklibpath,'input')
fontscollectionpath = os.path.join(mapniklibpath,'fonts')
__all__ = [mapniklibpath,inputpluginspath,fontscollectionpath]
