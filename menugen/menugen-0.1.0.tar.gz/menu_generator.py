import operator
from fnmatch import fnmatch

# The menu generation works by taking in the following
# strings:
#
#        1) A string that represents the header, which 
#            is then printed at the top of the result-
#            -ing menu, along with a series of ASCII 
#            characters as a delimiter; that series of
#            characters is as long as the header.
#            
#        2) A list of strings or tuples that represent
#            the selectable options; for the time being
#            this method uses strict typing detection.
#           Because the class handles index printing,
#            the omission of index 0 should be invisi-
#            -ble to the calling component. 
#           Also, the class should be able to natively
#            deal in either strings or tuples without
#            the calling component being aware of the
#            handling process.
#
#        3) A list of tuples containing extra options,
#            usually alphabetical rather than numerical,
#            a convention which prevents overlap between
#            these indices and the indices of the main
#            option set.
#           An example use case of this might be an 'x'
#            for when the user wants to return to the
#            previous menu. The class will hand the
#            calling function the letter value, and 
#            any behavior relating to that option will
#            need to be handled by the calling function.


class Menu(object):

    def index_only(self, header, numbered, other):
        intake, target = self.loop(header, numbered, other)
        return intake

    def index_value(self, header, numbered, other):
        intake, target = self.loop(header, numbered, other)
        return intake, target

    # needs a string header, a list of typical numbered options, 
    # and a list of tuples of other options
    def loop(self, header, numbered, other):
        looping = True
        while looping == True:
            verify = ['None']                            # a list of valid indices
            print "\n", header, "\n", "="*len(header)
            # makes a list of tuples using the numbered options to 
            # simplify menu display code, then prints the list
            verify = self.print_numbered(numbered, verify)

            # print list of other options
            print ""
            for i in other:
                verify.append(i[0])                # adds the "index" to verify
                print "[%s]" % i[0], i[1]

            # get input and verify it is valid
            intake = raw_input("\n?")
            if intake in verify:
                looping = False
            elif intake not in verify:
                print "Option [%s]: Invalid selection." % intake

        assert intake in verify, "Invalid menu option error"

        # uses list of options to pick a target
        if intake.isalpha() == False:
            reticule = numbered[operator.sub(int(intake),1)]
            if type(reticule) is tuple:
                target = reticule[0]
            elif type(reticule) is str:
                target = reticule
        else:
            target = None
        return intake, target

    # makes a list of tuples using the numbered options to 
    # simplify menu display code, then prints the list
    def print_numbered(self, numbered, verify):
        for index, i in enumerate(numbered):
            i = operator.add(index,1), i
            verify.append(str(i[0]))        # adds the index to verify
            
            print "[%d]" % i[0],
            if type(i[1]) == tuple:
                for f in i[1]:
                    if f != i[0]:
                        print f,
            else:
                print i[1],
            print ''

        return verify


# a simple configurable-default yes/no menu
# returns false for 'no', true for 'yes'
class YN_Menu(object):

    def __init__(self, body='', base="Continue? ", default=None):
        """ Configuration for the Yes/No menu

        Arguments:
            base

        """
        if default == "yes":
            self.default = default
            self.string = base + "(Y/n)  "
        elif default == "no":
            self.default = default
            self.string = base + "(y/N)  "
        elif default == None:
            self.default = ''
            self.string = base + "(y/n)  "
        self.body = body


    def run(self):
        try_again = True
        if len(self.body) > 0:    
            print body.rstrip('\n') + "\n"
        while try_again:
            proceed = raw_input(self.string)
            if proceed == '':
                proceed = self.default
            if fnmatch(proceed, 'y*') or fnmatch(proceed, 'Y*'):
                return True
            elif fnmatch(proceed, 'n*') or fnmatch(proceed, 'N*'):
                return False
            else:
                print "Invalid response, try again."
