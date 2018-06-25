"""
This script is used for downloading fanfiction from archiveofourown.com and saving those as .html files
"""
#########
#Imports#
#########
from bs4 import BeautifulSoup
import os
import re
import requests

#########
#Folders#
#########
work_dir = os.getcwd()
html_dir = os.path.join(work_dir, "html")
id_dir = os.path.join(work_dir, "ID")

############
#Parameters#
############
base_url = "https://archiveofourown.org/works/"
search_url = "https://archiveofourown.org/works/search?"
search_parameter = {"word_count": "&work_search[word_count]=5000-20000", "language": "&work_search[language_id]=1", "fandom_name": "&work_search[fandom_names]=", "page_num": "page="}
movies = {"LOTR" : "The+Lord+of+the+Rings+-+J.+R.+R.+Tolkien", "HP" : "Harry+Potter+-+J.+K.+Rowling"}
pages = 5       #   1 page = 20 results

###########
#Functions#
###########

def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_work_IDs(search_url, movie, result_pages):
    
    ID_list = []

    for page in range(1, result_pages+1): 
        
        query_url = "".join((search_url, search_parameter["page_num"], str(page), search_parameter["word_count"], search_parameter["language"], search_parameter["fandom_name"], movie))
        
        try:
            result_page = requests.get(query_url)
        except requests.exceptions.RequestException as e:
            print("Error ", e,  "at: ", query_url)

        resultpage_soup = BeautifulSoup(result_page.text, "lxml")
        IDs = resultpage_soup.select("h4.heading > a:nth-of-type(1)")

        for ID in IDs:
            if ID.attrs.get("href"):
                ID_extracted = re.search("([0-9]+)", ID["href"])
                ID_list.append(ID_extracted.group(0))

    return ID_list

def write_word_IDs(IDs, movie):
    with open(id_dir + "/" + movie + "_IDs.txt", "w", encoding="utf-8") as outfile:
        IDs_str = "\n".join(IDs)
        outfile.write(IDs_str)

def main(html_dir, id_dir, base_url, search_url, pages, movies):
    createFolder(html_dir)
    createFolder(id_dir)

    for movie in movies:
        IDs = get_work_IDs(search_url, movies[movie], pages)
        print(len(IDs), "IDs found for", movie)

        if (len(IDs) == pages * 20):
            write_word_IDs(IDs, movie)
        
        else:
            print("Not enough IDs gathered for ", movie, "... Please restart this script!")
    
main(html_dir, id_dir, base_url, search_url, pages, movies)