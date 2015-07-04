"""
A command line clipboard manager
"""
from pyperclip import copy, paste
import cPickle as pickle
import argparse, sys, os

class ClipboardMemo(object):

    def __init__(self):

        #Create directory to save dump file
        if not os.path.exists(os.path.expanduser('~/.clipboard_memo/')):
            os.makedirs(os.path.expanduser('~/.clipboard_memo/'))

        self.dbpath = os.path.expanduser('~/.clipboard_memo/dump.p')

        try:
            self.memos = pickle.load(open(self.dbpath, 'rb'))   #Load saved memos
        except IOError:
            #If dump doesn't exist create new
            self.memos = []

    def run(self):
        """Parse and run"""

        parser = argparse.ArgumentParser(
            description='Save clipboard data as memos',
            usage='''clipboard_memo <command> [<args>]
Available commands are:
    save                Save the contents of clipboard
    delete INDEX        Delete a memo of given index number
    delete -a | --all   Delete all saved memos
    ls                  List all saved memos
    yank INDEX          Copy a memo to clipboard
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2]) #Parse only the first argument

        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)

        #Execute the given command
        getattr(self, args.command)()


    def commit(self):
        """Save the current memos to memory."""
        pickle.dump(self.memos, open(self.dbpath, 'wb'))

    def save(self):
        """Save a new memo to the memos list."""
        text = str(paste()) #Data from clipboard
        if not bool(text):
            exit()  #Nothing to save

        text = text.encode('utf-8') #Clean string
        text = text.strip() #Get rid of whitespaces
        self.memos.append(text)
        self.commit()

    def delete(self):
        """Deletes the memos of the given index number."""
        parser = argparse.ArgumentParser(
            description='Delete memo of the given index number from clipboard')
        parser.add_argument('-i', '--index', type=int, help='Index of the memo to delete')
        parser.add_argument('-a', '--all', help='Delete all memos', action='store_true')
        args = parser.parse_args(sys.argv[2:])

        #Delete all memos
        if args.all:
            self.memos = []    #Delete all memos
            self.commit()
            exit(0)

        #If index number is provided then delete the particular memo
        if args.index:
            try:
                del self.memos[args.index - 1]   #Since we enumerate from 1 instead of 0
            except TypeError:
                print 'Integer required'
                self.commit()
        
        else:
            print 'Too few arguments. Provide the index number of memo to delete'

        

    def ls(self):
        """Lists all saved memos."""
        print '\n'.join(str(i) for i in enumerate(self.memos, start=1))

    def yank(self):
        """Copy the memo corresponding to the given index number to clipboard."""
        parser = argparse.ArgumentParser(
            description='''Copy the memo corresponding to the given index number
                to clipboard''')
        parser.add_argument('index', type=int)
        args = parser.parse_args(sys.argv[2:])

        try:
            copy(str(self.memos[args.index - 1]))    #Since we enumerate from 1 instead of 0
        except TypeError:
            pass    #Oops

def main():
    c = ClipboardMemo()
    c.run()

if __name__ == '__main__':
    main()
