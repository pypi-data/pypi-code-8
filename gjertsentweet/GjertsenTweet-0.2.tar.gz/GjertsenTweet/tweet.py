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


from twitter import Twitter, TwitterStream, read_token_file, OAuth, oauth_dance
import os

from consumer import CONSUMER_KEY, CONSUMER_SECRET


__author__ = 'Fredrik Gjertsen'

def authenicate():
    twitter_credentials = os.path.expanduser('~/.GjertsenTweet')
    if not os.path.exists(twitter_credentials):
        oauth_dance('GjertsenTweet', CONSUMER_KEY, CONSUMER_SECRET, twitter_credentials)
    
    token, token_secret = read_token_file(twitter_credentials)

    return OAuth(token, 
                 token_secret, 
                 CONSUMER_KEY, 
                 CONSUMER_SECRET)


