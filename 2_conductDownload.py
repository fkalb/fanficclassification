"""
2_conductDownload.py
This script uses the collected work-IDs and downloads the fanfictions as HTML files for further processing.

Next script: 3_generateMetadata.py
"""

#Imports
import glob
import os
import re

import requests

#Folders
id_dir = os.path.join(os.getcwd(), "id")
html_dir = os.path.join(os.getcwd(), "html")

#Parameters
base_url = "https://archiveofourown.org/works/"
url_suffix = "?view_full_work=true"


if not os.path.exists(html_dir):
    os.makedirs(html_dir)

for id_file in glob.glob(id_dir + "/*.txt"):
    
    #File prefix determines the novel: LOTR, HP...
    file_prefix = os.path.splitext(os.path.basename(id_file))[0]
    print("Downloading texts from:", file_prefix)

    with open(id_file, 'r', encoding="utf-8") as infile:
        
        #Use splitlines() to remove '\n'
        id_import = infile.read().splitlines()
        
        for ID in id_import:

            #The corresponding HTML file for every ID is requested and downloaded
            fanfic = requests.get(base_url + ID + url_suffix)
            
            with open(html_dir + "\\" + file_prefix + "_" + str(ID) + ".html", "w", encoding="utf-8") as outfile:
                outfile.write(fanfic.text)

    print("Finished downloading texts from:", file_prefix)
