#finds all my collected firefox bookmarks and merges them!
#from __future__ import print_function
from six import print_

bookmark_dir='.'

import bookmark_pyparser as bpp


#finds a list (recursively) of all html (bookmark) files in the chosen directory
import os
htmlfiles=[]
for root,dirs,files in os.walk(bookmark_dir):
	print_(root)
	htmlfiles_tmp=[os.path.join(root,fils) for fils in files if fils.split('.')[-1].lower()=='html']
	htmlfiles.extend(htmlfiles_tmp)

print_()
result={}
numhref=0
for bookmarkfile in htmlfiles:
        print_('############################## parsing ', bookmarkfile)
        parsedfile=bpp.bookmarkshtml.parseFile(open(bookmarkfile))
        numhref+=len(bpp.hyperlinks(parsedfile))
        print_('############################## creating a bookmarkDict ')
        bmDict=bpp.bookmarkDict(parsedfile)
        print_('############################## merging latest file into result')
        result=bpp.merge_bookmarkDict(result,bmDict)
    

finalfile=open('merged bookmarks.html', 'w')
finalstr=bpp.serialize_bookmarkDict(result)
finalfile.write(finalstr)
finalfile.close()

print_('total nunber of hyperlinks found = ', numhref)
print_('number of hyperlinks in final file=', len(bpp.hyperlinks_bookmarkDict(result)))
print_('number of unique hyperlinks =', len(set(bpp.hyperlinks_bookmarkDict(result))))
print_('number of folders =', bpp.count_folders(result))