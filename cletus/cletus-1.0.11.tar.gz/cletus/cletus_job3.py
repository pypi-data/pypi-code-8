--- cletus_job.py	(original)
+++ cletus_job.py	(refactored)
@@ -16,6 +16,7 @@
     See the file "LICENSE" for the full license governing use of this file.
     Copyright 2013, 2014 Ken Farmer
 """
+from __future__ import absolute_import
 
 
 import os
@@ -116,7 +117,7 @@
         """
         try:
             self.pidfd = open(pid_fqfn, 'a')
-        except IOError, e:
+        except IOError as e:
             self.logger.critical('Could not open pidfile: %s - permissions? missing dir?' % e)
             raise
         else:
@@ -187,7 +188,7 @@
             else:
                 err_msg = 'app_name must be provided if pid_dir is not'
                 self.logger.critical(err_msg)
-                raise ValueError, err_msg
+                raise ValueError(err_msg)
 
         # next try to create it, just in case it isn't there
         try:
