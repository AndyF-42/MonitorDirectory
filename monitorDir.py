"""
Syntax: monitorDir.py (dir_to_monitor) (final_dir)

1. Check for files that exist in dir_to_monitor

2. temporarily save size of each file in dir_to_monitor that is >=101.9 GB (save as candidate_list)
	2.1 sleep 30 seconds
	2.2 for each item in candidate_list, check if each of those files hasn’t changed file size at all since when we checked in step 2. 
	2.3 if file size has changed, remove this file name from candidate_list 
	2.4 sleep 30 seconds
	2.5 check again if any files in candidate_list are unchanged since step  2.2
		2.6 if file still hasn’t changed then copy it to final dir
		2.7 if file has changed, skip it
2.8 sleep 60 seconds, go back to Step 1
"""

import sys
import time
import glob
import os
import shutil

# get command line args
dir_to_monitor = sys.argv[1]
final_dir = sys.argv[2]

while True:
    # initialize the dictionary (maps files to their size if greater than value)
    candidate_list = {}
    count = 0
    for file in glob.glob(dir_to_monitor + "/**.*", recursive=True):
        size = os.path.getsize(file)
        if size > 2000:
            candidate_list[file] = size

    time.sleep(30)

    # remove files that changed size
    candidate_list = {file:candidate_list[file] for file in candidate_list if os.path.getsize(file) == candidate_list[file]}

    time.sleep(30)

    # copy files that didn't change size
    for file in candidate_list:
        if os.path.getsize(file) == candidate_list[file]:
            shutil.copy(file, final_dir)
            count += 1
    print(count + " files copied")
    time.sleep(60)