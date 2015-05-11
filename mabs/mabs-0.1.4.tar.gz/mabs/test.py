from mabs import *

a = TranTune(['192.168.1.1', '2', '23', '213', 'sdf'], gothreading=False)
a.send_file_support_shell('`date +%F`.bak')
