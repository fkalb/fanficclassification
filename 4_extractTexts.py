"""
This script uses the previously downloaded .html files to extract the contained texts
"""

#Imports
import glob
import os
from bs4 import BeautifulSoup
import re

#Folders
html_dir = os.path.join(os.getcwd(), "html")
text_dir = os.path.join(os.getcwd(), "texts")

if not os.path.exists(text_dir):
    os.makedirs(text_dir)


for html_file in glob.glob(html_dir + "/*.html"):
    print("Now extracting", html_file)
    
    filename = os.path.splitext(os.path.basename(html_file))[0]
    
    with open(html_file, 'r', encoding="utf-8") as infile:

        #Extracting text
        html_content = BeautifulSoup(infile.read(), "lxml")
        relevant_div = html_content.find_all("div", class_="userstuff")
        extracted_text_as_list = [div.find_all('p') for div in relevant_div]
        #Cleaning text
        extracted_text = "".join([str(string) for string in extracted_text_as_list])
        extracted_text = re.sub("</p>", "\n", extracted_text)
        extracted_text = re.sub("<br/>", "\n", extracted_text)
        extracted_text = re.sub("<[^<]+?>", " ", extracted_text)
        #Writing text
        with open(text_dir + "\\" + filename + ".txt", 'w', encoding='utf-8') as outfile:
            outfile.write(extracted_text)


