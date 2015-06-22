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


__author__ = 'Fredrik Gjertsen'

def find_break_point(string, screen_width):
    """Finds the best index to split a string, in order
       to make it fit in a terminal. This is because npyscreen
       doesn't add a newline for you, instead it will continue
       writing the string outside the screen.
       :param screen_width: the width of the terminal"""
    last_space = 0
    for i in range(len(string)):
        if i > screen_width-6:
            return last_space+1
        if string[i] == ' ':
            last_space = i
    return screen_width-6
