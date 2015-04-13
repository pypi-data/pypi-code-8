from pyatom import AtomFeed
from datetime import datetime
from sinor.html_content import from_file
from sinor.posts import sorted_posts, no_drafts
from sinor.config import config
import sys


def render_atom_feed(files):
    feed = AtomFeed(title=config.feed_title(),
                    subtitle=config.feed_subtitle(),
                    feed_url=config.feed_url(),
                    author=config.author(),
                    url=config.feed_url())

    posts = map(from_file, files)
    for post in no_drafts(sorted_posts(posts)):
        try:
            feed.add(title=post['title'],
                     content=post['content'],
                     author=config.author(),
                     url=post['absolute_url'],
                     updated=datetime.strptime(post['date'],
                                               config.blog_date_format()).date())
        except:
            print('Failed adding post {} to feed'.format(post))
            sys.exit(-1)

    return feed.to_string()
