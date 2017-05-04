#!/usr/bin/env python

import os
import re
import types
import zipfile
import shutil
from datetime import datetime

def get_tid_file(path='.'):
    filectime = datetime.fromtimestamp(os.path.getmtime(path))
    tid = '_{0:%Y%m%d_%H%M}'.format(filectime)
    return tid

def get_tid_time(ctime=(datetime.now())):
    if type(ctime) is types.FloatType:
        ctime = datetime.fromtimestamp(ctime)
    tid = '_{0:%Y%m%d_%H%M}'.format(ctime)
    return tid

def pycode_backup_zip(src_path='.',dst_path='..'):
    """
    backup the pycode to name_yyyymmdd_hhmm.zip

    Parameters:
    ----------
    images_path : foilder path for search image under it.

    Returns:
    ----------
    list of image name with path in format [img0, img1...] 
    """
    assert os.path.exists(src_path), "No valid src_path: {}".format(src_path)
    assert os.path.exists(dst_path), "No valid src_path: {}".format(dst_path)

    count = 0
    total = 0
    image_list = []
    m_ctime = os.path.getmtime(src_path)
    list_dirs = os.walk(src_path)
    for root, _, files in list_dirs:
        for f in files:
            if re.match(r'.+\.(py|pkl|txt|ods)$', f):
                filename = os.path.join(root, f)
                ctime = os.path.getmtime(filename)
                if ctime>m_ctime : m_ctime =ctime
                count += 1
                image_list.append(filename)
            total += 1
            '''
            if count%1000 == 0:
                print '[I]:{0:4} files Processed. {1:<8}:{2}'.format(count, root, f)
            '''
    # get the zip file name
    tid = get_tid_time(m_ctime)
    work_path =  os.path.basename(os.path.abspath(src_path))
    zip_filename = os.path.join(dst_path,work_path+tid+'.zip')
    print '--  Total {} files, {} pycode files will backup into : {}'.format(total, count,zip_filename)       

    # zip and backup files
    with zipfile.ZipFile(zip_filename, 'w') as myzip:
        for filename in image_list :
            myzip.write(filename)
            #    shutil.copyfileobj(f_in, f_out)

    return image_list


if __name__ == '__main__':
    print '# Begin pycode backup... at: ', get_tid_time()
    file_list = pycode_backup_zip()
    # for fname in file_list :         print fname
