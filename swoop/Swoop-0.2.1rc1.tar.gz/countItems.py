#!/usr/bin/env python

import Swoop
import argparse
import shutil
import EagleTools
import GadgetronConfig

class Counter(EagleTools.EagleFilePartVisitor):
    def __init__(self, root=None):
        EagleTools.EagleFilePartVisitor.__init__(self,root)
        self.count = 0;
        self.elementCount = 0
        self.layerCount = 0
    def default_pre(self, efp):
        self.count += 1
    def Element_pre(self, e):
        self.count += 1
        self.elementCount += 1
    def Layer_pre(self, l):
        self.count += 1
        self.layerCount += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple test for visitor")
    parser.add_argument("--file", required=True,  type=str, nargs='+', dest='file', help="files to process")
    args = parser.parse_args()
    
    for f in args.file:

        ef = Swoop.EagleFile.from_file(f)

        r =Counter(ef).go()
        print f, r.count, r.layerCount, r.elementCount
        
        ef.write(f)
