import unittest

from commandRunner import *

# tmp_id = ''
# tmp_path = ''
# in_glob = ''
# out_glob = ''
# command = ''


class RunnerTestCase(unittest.TestCase):

    r = ''
    id_string = "INTERESTING_ID_STRING"
    tmp_path = "/tmp/"
    in_glob = ".in"
    out_glob = ".out"
    cmd = "ls /tmp > $OUTPUT"
    data = "SOME EXAMPLE DATA"

    def setUp(self):
        self.r = commandRunner(self.id_string, self.tmp_path,
                        self.in_glob, self.out_glob, self.cmd, self.data)

    def tearDown(self):
        path = self.tmp_path+self.id_string
        file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
        out = self.tmp_path+self.id_string+"/"+self.id_string+self.out_glob
        if os.path.exists(file):
            os.remove(file)
        if os.path.exists(out):
            os.remove(out)
        if os.path.exists(path):
            os.rmdir(path)

    def testInitialisation(self):
        """
            Just reasserts that initialising works
        """
        self.assertEqual(self.r.tmp_id, self.id_string)
        self.assertEqual(self.r.in_glob, "in")
        self.assertEqual(self.r.out_glob, "out")

    def testPathExistsWorks(self):
        """
            Check the path looks right
        """
        self.assertEqual(self.r.tmp_path, "/tmp")

    def testPathDoesNotExistWorks(self):
        """
            Test the non-existing path raises and exception
        """
        self.assertRaises(OSError, commandRunner, self.id_string,
                          "/Blarghelblarghel/", self.in_glob, self.out_glob,
                          self.cmd, self.data)

    def test_translate_command_correctly_interpolate_output(self):
        """
            test __translated_command works as expected
        """
        test_string = "ls /tmp > /tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.out"
        self.assertEqual(self.r.command, test_string)

    def test_translate_command_correctly_interpolate_input(self):
        """
            test __translated_command works as expected
        """
        self.r = commandRunner(self.id_string, self.tmp_path,
                        self.in_glob, self.out_glob, "ls /tmp > $INPUT",
                        self.data)
        test_string = "ls /tmp > /tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.in"
        self.assertEqual(self.r.command, test_string)

    def test_translate_command_correctly_interpolate_both(self):
        self.r = commandRunner(self.id_string, self.tmp_path,
                        self.in_glob, self.out_glob, "ls /tmp > $INPUT $OUTPUT",
                        self.data)
        test_string = "ls /tmp > /tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.in /tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.out"
        self.assertEqual(self.r.command, test_string)

    def test_translate_command_correctly_handles_globs_without_periods(self):
        self.r = commandRunner(self.id_string, self.tmp_path,
                        "in", "out", self.cmd, self.data)
        test_string = "ls /tmp > /tmp/INTERESTING_ID_STRING/INTERESTING_ID_STRING.out"
        self.assertEqual(self.r.command, test_string)

    def test_prepare_correctly_makes_directory_and_file(self):
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file), True)

    def test_prepare_without_data(self):
        self.r = commandRunner(self.id_string, self.tmp_path,
                        self.in_glob, self.out_glob, "ls /tmp > $INPUT $OUTPUT",
                        None)
        self.r.prepare()
        path = self.tmp_path+self.id_string
        file = self.tmp_path+self.id_string+"/"+self.id_string+self.in_glob
        self.assertEqual(os.path.isdir(path), True)
        self.assertEqual(os.path.exists(file), False)

    def test_run(self):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.assertEqual(exit_status, 0)
        self.assertNotEqual(self.r.output_data, None)
    # TODO: more thorough testing of failure states and sensible behaviour if
    # we are not producing files

    def test_tidy_removes_all_files_and_dirs(self):
        self.r.prepare()
        exit_status = self.r.run_cmd()
        self.r.tidy()
        self.assertEqual(os.path.exists(self.r.path), False)
        self.assertEqual(os.path.exists(self.r.in_path), False)
        self.assertEqual(os.path.exists(self.r.out_path), False)


if __name__ == '__main__':
    unittest.main()
