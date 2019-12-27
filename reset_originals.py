import os
import shutil

def get_originals():

    dropbox = '/Users/austinrose/Dropbox (PASSUR Aerospace)/A. Rose Files/Projects/diversion-analysis'
    mv_path = '/Users/austinrose/development/python/tmp-all'
    
    # get a list of all the folders in the drobox directory
    for directory in os.listdir(dropbox):
        if directory[0] == '2':
            for region in os.listdir(dropbox + '/' + directory):
                if region[0] == 'D' or region[0] == 'G':
                    for file in os.listdir(dropbox + '/' + directory + '/' + region):
                        if 'Original' in file:
                            new_file = file[0:file.index('_')] + file[file.index('.')::]
                            shutil.copy((dropbox + '/' + directory + '/' + region + '/' + file), (mv_path + '/' + new_file))
                        
if __name__ == "__main__":
    get_originals()