__author__ = 'hvishwanath'

import os
import sys
import tempfile
import zipfile
import tarfile
from planparser import PlanParser

class PDPParser(object):
    def __init__(self, pdpfile):
        # PDP File can actually be a pdp archive
        # alternately it can be a folder that contains required contents of a PDP
        self.pdpfile = pdpfile
        self.pdpdir = None

        if os.path.isdir(self.pdpfile):
            self.pdpdir = self.pdpfile

        elif os.path.isfile(self.pdpfile):
            # This is a pdp archive. depending on the type, extract it somewhere.
            tmpdir = tempfile.mkdtemp(prefix="libpaas_")
            if zipfile.is_zipfile(pdpfile):
                with zipfile.ZipFile(pdpfile) as z:
                    z.extractall(tmpdir)
                self.pdpdir = tmpdir
            elif tarfile.is_tarfile(pdpfile):
                with tarfile.open(pdpfile) as t:
                    t.extractall(tmpdir)
                self.pdpdir = tmpdir
            else:
                raise ValueError("Unsupported PDP file type : %s" % pdpfile)

        if not self.validate_integrity():
            raise RuntimeError("PDP Archive couldn't be validated for content integrity")

        if not self.validate_signature():
            raise RuntimeError("Signature used to sign the PDP archive couldn't be verified")


        self.planfile = os.path.join(self.pdpdir, "camp.yaml")
        if not os.path.isfile(self.planfile):
            raise RuntimeError("Malformed PDP archvie. Missing manifest file")

        self.plan = PlanParser.parse(self.planfile)


    def validate_integrity(self):
        return True

    def validate_signature(self):
        return True

