import datetime
import os

from backupfolders import (create_copy_for_each_folder,
                           get_directories_with_backup)
from updatedbf import transfer_rows

# delete folder pylogs if exists including files
if os.path.exists("pylogs"):
    for file in os.listdir("pylogs"):
        os.remove(os.path.join("pylogs", file))
    os.rmdir("pylogs")
# create folder logs 
os.mkdir("pylogs")

create_copy_for_each_folder()
directories_with_backup = get_directories_with_backup()
# iterate over directories with backup
for directory in directories_with_backup:
    # copy the files from 'clona' folder to the current folder
    # overwrite the existing files
    clona_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clona')
    for file in os.listdir(clona_folder):
        if os.path.isfile(os.path.join(clona_folder, file)):
            with open(os.path.join(clona_folder, file), 'rb') as f:
                with open(os.path.join(directory, file), 'wb') as new_f:
                    new_f.write(f.read())

    # iterate over files in directory
    for file in os.listdir(directory):
        #check if file exists in backup folder
        if not os.path.exists(os.path.join(f"_{directory}_", file)):
            continue
        if(file.lower().endswith('.dbf') and not file.lower().endswith('_conf.dbf')):
            # transfer rows from the backup file to the current file
            transfer_rows(os.path.join(f"_{directory}_", file), os.path.join(directory, file))
            # if file is societ.dbf
        else:
            # write into a skippedfiles.txt the name of the file, the date and time
            with open("pylogs/skippedfiles.csv", "a", encoding='utf-8') as logs_file:
                logs_file.write(f"{datetime.datetime.now().strftime('%H:%M:%S')},{file}\n")

with open("free.txt", "w") as file:
    pass

