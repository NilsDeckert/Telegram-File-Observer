import os
import filecmp
import urllib.request
import datetime
from config import settings

# This file downloads the file from the given link in config/settings.py, then compares it to the file previously downloaded file
# if changes were found, it renames the old file with the current date and time and moves the new file from the temporary directory
# to another folder were the files are stored permanently.

file = settings.file
v_tmp = 'tmp/v.pdf'                                         # Directory for temporary storing the last downloaded file
v_prm = 'v/v.pdf'                                           # Directory to permanently store all files (except last downloaded file)
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)
def check_v():
    urllib.request.urlretrieve(file, v_tmp)
    if not filecmp.cmp(v_tmp,v_prm):
        os.rename(v_prm, datetime.datetime.now().strftime('v/'+'%Y-%m-%d--%H-%M')+'.pdf') # renames latest file in permanent storing directory
        os.rename(v_tmp, v_prm)                                                           # moves latest file to permanent storing directory
        return True
    else:
        return False
