import unittest
from . import ProjectFreeTV, ShowNotFound


class Test(unittest.TestCase):

    def setUp(self):
        self.pft = ProjectFreeTV()
        self.friends = ProjectFreeTV.get_show('Friends')

    def testSeason(self):
        self.failUnlessEqual(self.friends.season_count, 10)

    def testShowNumber(self):
        self.assertGreater(self.pft.show_number, 2840)

    def testShowNotFound(self):
        self.assertRaises(ShowNotFound, ProjectFreeTV.get_show, 'this awesome show is too awesome')

    def testRange(self):
        ydl_links = self.friends.get_ydl_links_in_range(1, -5, 8)
        self.assertEqual(len(ydl_links), 8)
        ydl_links = self.friends.get_ydl_links_in_range(1, 3, 20)
        self.assertEqual(len(ydl_links), 18)
        ydl_links = self.friends.get_ydl_links_in_range(1, 3, 26)
        self.assertEqual(len(ydl_links), 22)


    def tearDown(self):
        del self.friends

if __name__ == '__main__':
    unittest.main()
