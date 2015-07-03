import unittest
import PyQPIC as _pq
import numpy as _np
import hashlib
import pkg_resources as pkg
import tempfile
import shutil
import os


class TestTemplateGeneration(unittest.TestCase):
    def setUp(self):
        pass

    def test_result(self):
        # =====================================
        # Default settings
        # =====================================
        qpic    = _pq.QuickPICSettings()
        magic   = _pq.MagicSettings()
        bunches = _np.array(
            [
                _pq.BunchSettings(beamtype='drive'), _pq.BunchSettings(beamtype='witness')
            ]).flatten()
        plasma  = _pq.PlasmaSettings(qpic=qpic, magic=magic, bunches=bunches)
        box     = _pq.BoxSettings()
        
        # =====================================
        # Generate rpinput file
        # =====================================
        md5_new = hashlib.md5()
        # with tempfile.TemporaryFile() as fid:
        with tempfile.TemporaryDirectory() as name:
            filename = os.path.join(name, 'rpinput')
            print(filename)
            fid = open(filename, 'w+', encoding='utf-8')
            _pq.deckgen(
                plasma  = plasma,
                bunches = bunches,
                box     = box,
                magic   = magic,
                qpic    = qpic,
                fid     = fid
                )

            # fid.flush()
            fid.seek(0)

            with open('copyrpinput', 'w+') as fid_copy:
                shutil.copyfileobj(fid, fid_copy)

            fid.close()

            fid = open(filename, 'rb')
        
            # =====================================
            # Hash file and compare to original
            # =====================================
            # fid.close()
            md5_new.update(fid.read())

            fid.close()
        
        hash_new = md5_new.hexdigest()
        
        md5_orig = hashlib.md5()
        with pkg.resource_stream('PyQPIC', 'tests/files/rpinput') as fid:
            md5_orig.update(fid.read())
        
        hash_orig = md5_orig.hexdigest()
        self.assertEqual(hash_orig, hash_new)


class TestBinaryHash(unittest.TestCase):
    def setUp(self):
        pass

    def test_result(self):
        # =====================================
        # Correct binary hash
        # =====================================
        hash_correct = '12596acb33eea0e2414a4e4f30ba15b9'
        print(hash_correct)

        # =====================================
        # Open binary and hash
        # =====================================
        md5_orig = hashlib.md5()
        with pkg.resource_stream('PyQPIC', 'resources/bin/qpic.e') as fid:
            md5_orig.update(fid.read())
        hash_current = md5_orig.hexdigest()
        self.assertEqual(hash_correct, hash_current)
