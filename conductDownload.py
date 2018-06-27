"""
This script uses the collected work-IDs and downloads the fanfictions as HTML
"""

#Imports
import glob
import os
import re
import requests

#Folders
id_dir = os.path.join(os.getcwd(), "id")
html_dir = os.path.join(os.getcwd(), "html")

#URLs
base_url = "https://archiveofourown.org/works/"
url_suffix = "?view_full_work=true"
  
if not os.path.exists(html_dir):
    os.makedirs(html_dir)

for idfile in glob.glob(id_dir + "/HP.txt"):
    
    file_prefix = os.path.splitext(os.path.basename(idfile))[0] #prefix: LOTR, HP...
    print("Downloading texts from:", file_prefix)

    with open(idfile, 'r', encoding="utf-8") as infile:
        
        id_import = infile.read().splitlines() #remove \n 
        
        for ID in id_import:

            """
            The corresponding HTML file for every ID is requested and downloaded
            """
            
            fanfic = requests.get(base_url + ID + url_suffix)
            
            with open(html_dir + "\\" + file_prefix + "_" + str(ID) + ".html", "w", encoding="utf-8") as outfile:
                outfile.write(fanfic.text)
    print("Finished downloading texts from:", file_prefix)

    