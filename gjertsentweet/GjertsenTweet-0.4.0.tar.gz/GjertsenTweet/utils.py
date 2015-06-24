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

import time
import datetime
import curses

__author__ = 'Fredrik Gjertsen'


month_names = ['Jan','Feb','Mar','Apr','May','Jun', 
               'Jul','Aug','Sep','Oct','Nov','Dec']

months = {month: i+1 for i, month in enumerate(month_names)}

def strip_leading_zero(month):
    if month.startswith('0'):
        print(month)
        return int(month[1:])
    return int(month)


def format_time(tweet_time):
    """Formats the time provided by twitter so it looks nice
       and show the right time"""
    tweet_time = tweet_time.split()
    month = months[tweet_time[1]]
    day = tweet_time[2]
    ttime = tweet_time[3]
    year = tweet_time[5]
    tweet_time = '{} {} {} {}'.format(ttime, month, day, year)
    time_format = '%H:%M:%S %m %d %Y'
    timestamp = time.mktime(datetime.datetime.strptime(tweet_time, time_format).timetuple())
    timestamp -= time.altzone
    tweet_time = datetime.datetime.fromtimestamp(timestamp).strftime(time_format)
    tweet_time = tweet_time.split()
    tweet_time[1] = month_names[strip_leading_zero(tweet_time[1])-1]
    return ' '.join(tweet_time)


def find_break_point(string, screen_width):
    """Finds the best index to split a string, in order
       to make it fit in a terminal. This is because npyscreen
       doesn't add a newline for you, instead it will continue
       writing the string outside the screen.
       :param screen_width: the width of the terminal"""
    last_space = 0
    for i in range(len(string)):
        if string[i] == ' ':
            last_space = i
        if i > screen_width-6:
            return last_space+1
    return screen_width


# npyscreen doesn't resize its widgets and forms when
# the screensize is <80
def format_tweet(string, screen_width):
    """Splits a tweet into two lines if it's too long
       to fit the screen"""
    index = find_break_point(string, screen_width)
    line1 = string[0:index]
    line2 = string[index:]
    if line2 == '':
        return [line1, '']
    return [line1, line2, '']

def parse_tweet(data, screen_width):
    """Parses the data to get the interesting data.
       Returns a list thats contains data we are interested in,
       or None if it got an keyError on any of the lookups."""
    try:
        username = '@'+data['user']['screen_name'].encode('utf8', 'replace')
        full_name = data['user']['name'].encode('utf8', 'replace')
        tweet_text = data['text'].encode('utf8', 'replace')
        time = data['created_at'].encode('utf8', 'replace')
        time = format_time(time)
        tweet_text = format_tweet(tweet_text, screen_width)
        parsed_tweet = [full_name, username, time]
        for text in tweet_text:
            parsed_tweet.append(text)
        return parsed_tweet
    except KeyError:
        return None

