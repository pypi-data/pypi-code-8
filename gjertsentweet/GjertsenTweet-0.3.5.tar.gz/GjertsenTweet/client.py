# GjertsenTweet is a simple twitter client
# Copyright (C) 2015  Fredrik Gjertsen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from threading import Thread

from npyscreen import ActionForm, SplitForm, TitleText, Pager, NPSAppManaged,\
                      notify_confirm, notify_yes_no

import tweet
from utils import find_break_point


__author__ = 'Fredrik Gjertsen'


class GTweet(ActionForm, SplitForm):
    """This is the form that contains the feed, 
       including the fields to write a tweet
       or search."""
    
    def create(self):
        """initiliazed the form, adds the widgets and fires up the feed."""
        self.tweet = self.add(TitleText, name="What's happening?", 
                              use_two_lines=False, begin_entry_at=18)
        self.search = self.add(TitleText, name="Search", begin_entry_at=18)
        self.draw_line_at = 5
        self.nextrely += 4
        self.feed = self.add(Pager, name='Feed', ascii=False)
        self.populate()
        # Since npyscreen is poorly documented, this is how
        # we do it, just fire up a new thread

        self.thread = Thread(target=self.stream)
        self.thread.daemon = True
        self.thread.start()

    def on_ok(self):
        """Checks wether you have a tweet to post
           or a query to search for. Notifies the uses
           if the tweet is too long, or if the user
           has something to post."""
        post = self.tweet.value
        query = self.search.value

        if len(post) > 140:
            notify_confirm('Your tweet is too long!', title='Error')
        elif len(post) > 0:
            yes = notify_yes_no('Are you sure you want to post:\n' + post, 
                                title='Post')
            if yes:
                self.post_tweet(post)
        elif len(query) > 0:
            self.mysearch(query)
        
        self.tweet.value = ''
        self.search.value = ''

    def on_cancel(self):
        """Askes the user if he/she really wants to quit when the cancel 
        button is pressed. Terminates if yes, else continue."""
        yes = notify_yes_no('Are you sure you wanna quit?', title='Quit')
        # This is really ugly, but since the
        # twitter stream won't shut down this
        # was the quickest/dirtiest solution
        if yes:
            exit()

    def post_tweet(self, post):
        """Posts a tweet.
           :param post: Your tweet."""
        twittr = tweet.Twitter(auth=tweet.authenicate())
        twittr.statuses.update(status=post)

    def parse_tweet(self, data):
        """Parses the data to get the interesting data.
           This is the actual tweet, username, full name, 
           and the time the tweet was posted.
           Returns a list thats contains data we are interested in,
           or None if it got an keyError on any of the lookups."""
        try:
            username = '@'+data['user']['screen_name'].encode('utf8', 'replace')
            full_name = data['user']['name'].encode('utf8', 'replace')
            tweet_text = data['text'].encode('utf8', 'replace')
            time = data['created_at'].encode('utf8', 'replace')
            index = find_break_point(tweet_text, self.max_x)
            tweet1 = tweet_text[0:index]
            tweet2 = tweet_text[index:]
            return [full_name, username, time, tweet1, tweet2]
        except KeyError:
            return None

    def update_feed(self, data):
        """Updates the feed, new tweets go first, the rest
           gets pushed down. The will at most contain the
           100 newest tweets.
           Returns the updated feed."""
        twit =  self.parse_tweet(data)
        feed = self.feed.values
        if twit != None:
            full_name, username, time, tweet1, tweet2 = twit
            feed.insert(0, full_name)
            feed.insert(1, username + ' ' + time)
            feed.insert(2, tweet1)
            if tweet2 != '':
                feed.insert(3, tweet2)
                feed.insert(4, '')
            else:
                feed.insert(3, '')

        if len(self.feed.values) >= 100:
            feed = feed[0:100]
        
        return feed

    def populate(self):
        """Populates the the feed with the last 20 tweets from
           your feed when the client starts."""
        twittr = tweet.Twitter(auth=tweet.authenicate())
        tweets = reversed(twittr.statuses.home_timeline(count=20))

        for data in tweets:
            self.feed.values = self.update_feed(data)

    def stream(self):
        """Listens to your feed, and updates it whenever
           someone posts a new tweet.
           Note, if you for some reason exits with ctrl-c, the
           twitterstream will still be running. So use the cancel button 
           to exit."""
        twittr_stream = tweet.TwitterStream(auth=tweet.authenicate(), 
                                            domain='userstream.twitter.com')       
        tweets = twittr_stream.user()

        for data in tweets:
            self.feed.values = self.update_feed(data)

    def mysearch(self, query):
        """Searches for tweets and adds them to the feed
           :param query: what you are searching for."""
        twittr = tweet.Twitter(auth=tweet.authenicate())
        tweets = twittr.search.tweets(q=query)
        tweets = reversed(tweets['statuses'])
        for data in tweets:
            self.feed.vaules = self.update_feed(data)            


class TwitterClient(NPSAppManaged):
    """This is the client. It only loads the
       form where you can post tweets, search, 
       and see your feed."""
    
    def onStart(self):
        self.addForm('MAIN', GTweet, name='GjertsenTweet')


def main():
    tweet.authenicate()
    TwitterClient().run()


if __name__ == '__main__':
    main()

