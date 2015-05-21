"""
General infomation on the Project Free TV site
"""

from util import get_doc_root
from . import Show

class ShowNotFound(Exception):
    pass

class ProjectFreeTV:
    """
    Should just be a singleton because there should just be on instance of the
    site. Might be modified to conform to that fact in the future
    """
    site_url = "http://www.free-tv-video-online.info/"
    show_list = "http://www.free-tv-video-online.info/internet/"
    def __init__(self):
        self.shows = []
        self.show_set = set([])
        self.get_all_shows()

    @classmethod
    def get_show(cls, name):
        """get and return an instance of a show by its name
        """
        show_url = cls.show_list + name.lower().replace(" ", "_") + "/"
        try:
            return Show(name, show_url)
        except:
            raise ShowNotFound("this show is not on project free tv")

    @property
    def show_number(self):
        return len(self.show_set)

    def get_all_shows(self):
        """ get all shows, although including movies, on the site
        """
        root = get_doc_root(self.show_list)
        self.doc_root = root

        shows = []
        for tbl in root.xpath('//table[@cellspacing="1"]'):
            shows = tbl.xpath('.//tr//td//b//text()')[1:]

        self.show_set = set(shows)
        self.shows = shows
        return self.show_set

    def search_show(self, show):
        """ search a show by partial matching.
        returns all the shows with the text in their names
        """
        shows = []
        for tv_show in self.shows:
            if show.lower() in tv_show.lower():
                shows.append(tv_show)
        return shows
