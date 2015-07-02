import time
import curses
import sys

from prettytable import PrettyTable

import pydcard


def dcard_terminal(window):
    while True:
        ts = TitlesTable()
        try:
            page_one = pydcard.get_all_new_posts(1)
            for p in page_one:
                got_title = p.get('version')[0].get('title').replace('\n', '')
                got_like_count = str(p.get('likeCount'))
                got_comment_count = str(p.get('commentCount'))
                got_post_id = str(p.get('id'))
                got_sex = '♂' if p.get('member').get('gender') == 'M' else '♀'
                got_author = got_sex + ' ' + p.get('member').get('school')

                got_forum_name = p.get('forum_name').title()

                ts.append_to_table(
                    title=got_title,
                    likes=got_like_count,
                    pid=got_post_id,
                    author=got_author,
                    forum=got_forum_name,
                    comments=got_comment_count
                )

                print_msg = str(ts.table_to_str())

            window.addstr(print_msg)
            window.refresh()
            window.erase()
            time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            sys.exit("Goodbye!")


class TitlesTable(object):
    def __init__(self):
        self.table = []
        header = [
            "Post ID",
            "Likes",
            "回覆",
            "文章主題",
            "作者",
            "討論區"
        ]
        self.x = PrettyTable(header)
        self.x.align["文章主題"] = "l"
        self.x.align["Post ID"] = "l"
        self.x.align["作者"] = "l"

    def append_to_table(self, *args, **kwargs):
        if kwargs:
            content = [
                kwargs['pid'],
                kwargs['likes'],
                kwargs['comments'],
                kwargs['title'],
                kwargs['author'],
                kwargs['forum']
            ]
            self.x.add_row(content)

    def table_to_str(self):
        return self.x

if __name__ == '__main__':
    curses.wrapper(dcard_terminal)
