import sys
import subprocess
import tempfile
import shutil
import os
import filecmp

from msdiff import diff_files, DifferentNrOfStavesError

def main():
    
    
    # If the user hasn't passed exactly 2 arguments, we terminate the program \
    # with a helpful message.
    try:
        assert(len(sys.argv) == 3)
        old_path_ = sys.argv[1]
        new_path_ = sys.argv[2]
    except:
        print ">>> Invalid input."
        print "msdiff must be called with exactly 2 file names"
        return
    
    # Test the paths for validity. Concretely:
    for path in [old_path_, new_path_]:
        
        # - test if the path exists
        if not os.path.exists(path):
            print "'{}' - Invalid Path; path does not exist.".format(path)
            return
        
        # - test if the path points to a file (and not to a directory, for example)
        if not os.path.isfile(path):
            print "'{}' - Invalid Path; path is not a file.".format(path)
            return
    
    # If the files are equal, there is no need to call Musescore.
    # The user is best served with a message that says the files are equal.
    if filecmp.cmp(old_path_, new_path_, shallow=True):
        print "Files are equal."
        return
    
    
    # Create temporary files so that users can't accidetlly shoot \
    # themselves in the foot by modifying files that are not to de modified.
    # 
    # The `tempfile.mkstemp` will generate a filename with random characters \
    # between the supplied prefix and suffix. \
    # This could be handled in a different way by creating a temporary directory \
    # and using file names without random characters, but I think the random \
    # characters remind the user that these are not the original files, \
    # but copies.
    handle, diff_path = tempfile.mkstemp(suffix='.mscx', prefix='diff__')
    handle, old_path = tempfile.mkstemp(suffix='.mscx', prefix='new__')
    handle, new_path = tempfile.mkstemp(suffix='.mscx', prefix='old__')
    
    shutil.copy(old_path_, old_path)
    shutil.copy(new_path_, new_path)
    
    # Try to diff the files:
    try:
        diff_files(old_path, new_path, diff_path)
    
    # If the files have different numbers of staves, we can't compare them.
    except DifferentNrOfStavesError as e:
        print "Files with different number of staves ({} and {}, respectively)".\
                 format(e.old_nr, e.new_nr)
        print "msdiff can't (yet) diff files with different number of staves."
        return
    except:
        print "An error has occurred. Files could not be diffed."
        return
    
    
    # Finally, if all goes well, open the three files in Musescore.
    #
    # By default, the files are shown in different tabs, with the first tab \
    # in focus. This brings the `diff_path`, containing the diffed file, into focus.
    subprocess.call(['musescore', diff_path, old_path, new_path])
    
    
