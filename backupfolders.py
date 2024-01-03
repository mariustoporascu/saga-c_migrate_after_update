import os


def create_copy_for_each_folder():
    """
    Create a copy for each folder which is named as an int ex: 0001.
    The copy should contain all files from the original folder.
    The new folder should be named like so _<original_name>_
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directories = os.listdir(script_dir)
    for item in directories:
        if(directories.__contains__('_'+item+'_')):
            continue

        if os.path.isdir(os.path.join(script_dir, item)):
            if item.isdigit():
                new_folder_name = f"_{item}_"
                new_folder_path = os.path.join(script_dir, new_folder_name)
                os.mkdir(new_folder_path)
                for file in os.listdir(os.path.join(script_dir, item)):
                    file_path = os.path.join(script_dir, item, file)
                    new_file_path = os.path.join(new_folder_path, file)
                    with open(file_path, 'rb') as f:
                        with open(new_file_path, 'wb') as new_f:
                            new_f.write(f.read())
                            
def get_directories_with_backup():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directories = os.listdir(script_dir)
    directories_with_backup = []
    for item in directories:
        if os.path.isdir(os.path.join(script_dir, item)):
            if item.isdigit() and directories.__contains__('_'+item+'_'):
                directories_with_backup.append(item)
    print("Created backup for the following folders: ")
    print(directories_with_backup)
    return directories_with_backup
# test
#create_copy_for_each_folder()
#get_directories_with_backup()