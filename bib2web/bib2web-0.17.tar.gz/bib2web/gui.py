from Tkinter import *
import main
from bibtexparser.bibdatabase import BibDatabase
import ConfigParser
import os
import bibtexparser
import subprocess
import ttk
import urllib2
import time

class GUI():
    #GUI initation function
    def __init__(self):
        self.file_list = []
        self.tree = None
        self.win = self.makeWindow()
        self.bib_dir = None
        self.personal_website_bib = None
        self.personal_website_html = None
        self.personal_link = None
        self.group_website_bib = None
        self.group_website_html = None
        self.group_link = None
        self.bibtex_files = None

    #Find the selected rows
    def whichSelected(self, website):
        select = self.tree.selection()
        selected = []
        #Items are hexadecimal starting with an 'I', 
        #for instance 'I00D' for row number 13
        #This needs to be parsed to and int
        for item in select:
            index = int(item.replace('I', ''), 16) - 1
            selected.append(self.file_list[index])
        self.write_selected_to_file(selected, website)

    #Write selected rows to personal or group bib file
    #from this bib file a website is created using BibBase.org
    def write_selected_to_file(self, selected, website):
        db = BibDatabase()
        result = []
        for item in selected:
            path = str(self.bib_dir) + str(item)
            with open(path, 'r') as f:
                db = bibtexparser.load(f)
                result.append(db.entries[0])
        db.entries = result
        if website == 'personal':
            with open(self.personal_website_bib, 'w') as f:
                bibtexparser.dump(db, f)
        elif website == 'group':
            with open(self.group_website_bib, 'w') as f:
                bibtexparser.dump(db, f)

        #Make sure the file is uploaded to Dropbox before it is send to BibBase
        time.sleep(1)
        
        #Query to BibBase with the right URL
        if website == 'personal':
            html = urllib2.urlopen("http://bibbase.org/show?bib=" + str(self.personal_link)).read()
        elif website == 'group':
            html = urllib2.urlopen("http://bibbase.org/show?bib=" + str(self.group_link)).read()
        #The html does not contain styling and jquery or javascript
        html = '<head>' + \
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>' + \
            '<script src="http://bibbase.org/js/bibbase.min.js" type="text/javascript"></script>' + \
            '<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">' + \
            '<link rel="stylesheet" href="http://bibbase.org/css/bootstrap.min.css" type="text/css" media="screen">' + \
            '<link rel="stylesheet" href="http://bibbase.org/css/styles/default.css" type="text/css" media="screen">' + \
            '<link rel="stylesheet" href="http://bibbase.org/css/styles/common.css" type="text/css" media="screen">' + \
            '<link rel="stylesheet" href="http://bibbase.org/css/styles/hide_text.css" type="text/css" media="screen">' + str(html)

        if website == 'personal':
            with open(self.personal_website_html, 'w') as website:
                website.write(html)    
        elif website == 'group':
            with open(self.group_website_html, 'w') as website:
                website.write(html)    

    #Update the table with new entries
    def update_table(self):
        print "Updating table with new entries"
        self.tree.delete(*self.tree.get_children());
        self.file_list = []
        count = 0
        for f in os.listdir(self.bib_dir):
            if f.endswith(".bib"):
                self.file_list.append(f)
                split = f.split('_')
                split[-1] = split[-1].split('.')[0]
                self.tree.insert("", count, values=(split[0], split[1], split[2:]))
                count += 1

    #Define and create the GUI
    def makeWindow(self):
        global select
        win = Tk()
        win.geometry('{}x{}'.format(1250, 700))
        
        
        frame2 = Frame(win)       # Row of buttons
        frame2.pack()
        b1 = Button(frame2,text="Search for new entries",command=lambda: main.search_new(self.config, self.bib_dir, self, self.bibtex_files))
        b2 = Button(frame2,text="Generate personal website",command=lambda: self.whichSelected('personal'))
        b3 = Button(frame2,text="Generate group website",command=lambda: self.whichSelected('group'))
        b1.pack(side=LEFT); b2.pack(side=LEFT); b3.pack(side=LEFT)

        frame1 = Frame(win)
        frame1.pack()

        Label(frame1, text="Select the BibTex entries you want to publish on website. Hold down the CTRL-key to select multiple entries.").grid(row=1, column=0, sticky=W)

        frame3 = Frame(win)       # select of names
        frame3.pack(expand=True)
        scroll = Scrollbar(frame3, orient=VERTICAL)
        self.tree = ttk.Treeview(frame3, selectmode='extended', yscrollcommand=scroll.set, height=50)
        scroll.config(command=self.tree.yview)
        scroll.pack(side=RIGHT, fill=Y)

        self.tree['show'] = 'headings'
        self.tree['selectmode'] = "extended"
        self.tree["columns"]=("Type", "Year", "Title")
        self.tree.column("Type", width=200)
        self.tree.column("Year", width=100)
        self.tree.column("Title", width=1000)
        self.tree.heading("Type", text="Type")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Title", text="Title")
         
        self.tree.pack()
        return win