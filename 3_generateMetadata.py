"""
3_generateMetadata.py
This script extracts metadata from the previously downloaded html files and saves them in a csv file for further use.

Next script: 4_extractTexts.py
"""

#Imports
import glob
import os
import re

import pandas as pd
from bs4 import BeautifulSoup

#Folders
html_dir = os.path.join(os.getcwd(), "html")


def extract_metadata(html_dir):
    
    print("Extracting metadata...")
    
    metadata = {}

    for html_file in glob.glob(html_dir + "/*.html"):
        
        #Extract novel and ID from filename
        filename = os.path.splitext(os.path.basename(html_file))[0]
        novel, ID = filename.split("_")

        #Initialize nested dictionary
        metadata[filename] = {"Novel" : novel, "Genre" : "", "ID": ID}

        #Determine genre: Either 'High Fantasy' or 'Contemporary Fantasy'
        if novel == "LOTR" or novel == "GOT" or novel == "TH":
            metadata[filename].update({"Genre" : "HF"})

        else:
            metadata[filename].update({"Genre" : "CF"})

        #Extract metadata from each html file
        with open(html_file, 'r', encoding="utf-8") as infile:
            
            html_contents = infile.read()
            html_soup = BeautifulSoup(html_contents, "lxml")
            
            #Find author
            try:
                author_soup = html_soup.find("a", attrs={"rel": "author"})
                author = author_soup.get_text(strip=True)
            except:
                #NB: There are actually anonymous authors!
                author = "Anonymous"
            metadata[filename].update({"Author" : author})

            #Find title
            title_soup = html_soup.find("h2", class_="title heading")
            title = title_soup.get_text(strip=True)
            title = re.sub("\*", "", title)   
            metadata[filename].update({"Title" : title})

            #Find text_length
            text_length_soup = html_soup.find("dd", class_="words")
            text_length = text_length_soup.get_text(strip=True)
            metadata[filename].update({"Length" : text_length})

    return metadata

def create_DataFrame(metadata_dict):
    
    meta_df = pd.DataFrame.from_dict(metadata_dict, orient="index")
    meta_df.index.rename('Filename', inplace=True)
    
    print("DataFrame created!")

    return meta_df

def write_metadata(metadata_dataframe):

    with open("metadata.csv", "w", encoding="utf-8") as outfile:
        metadata_dataframe.to_csv(outfile, sep="\t")

    print("Metadata file created!")

def main(html_dir):

    metadata_dict = extract_metadata(html_dir)
    metadata_dataframe = create_DataFrame(metadata_dict)
    write_metadata(metadata_dataframe)

main(html_dir)
