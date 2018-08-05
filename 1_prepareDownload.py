"""
1_prepareDownload.py
This script searches for fanfiction on archiveofourown.org and extracts the identifier of each found text and saves it to a txt file.
The collected identifiers are used for downloading the texts.

Next script: 2_conductDownload.py
"""

#Imports
import os
import re

import requests
from bs4 import BeautifulSoup

#Folders
id_dir = os.path.join(os.getcwd(), "ID")

#Parameters
search_url = "https://archiveofourown.org/works/search?"
search_parameter = {
     "word_count": "&work_search[word_count]=5000-20000"
    ,"language": "&work_search[language_id]=1"
    ,"fandom_name": "&work_search[fandom_names]="
    ,"page_num": "page="
    }
novels = {
 "GOT" : "Game+of+Thrones+%28TV%29"
,"LOTR" : "The+Lord+of+the+Rings+-+J.+R.+R.+Tolkien"
,"HP" : "Harry+Potter+-+J.+K.+Rowling"
,"FB" : "Fantastic+Beasts+and+Where+to+Find+Them+%28Movies%29"
,"PJ" : "Percy+Jackson+and+the+Olympians+%26+Related+Fandoms+-+All+Media+Types"
,"TH" : "The+Hobbit+-+J.+R.+R.+Tolkien"
}
#Scroll through the result pages: 1 page = 20 results
pages = 10       


def get_work_IDs(search_url, search_parameter, novel, pages):
    
    ID_list = []

    for page in range(1, pages+1): 
        
        query_url = "".join((search_url, search_parameter["page_num"], str(page), search_parameter["word_count"], search_parameter["language"], search_parameter["fandom_name"], novel))
        
        result_page = requests.get(query_url)
        
        resultpage_soup = BeautifulSoup(result_page.text, "lxml")
        #first <a> element in <h4> always contains work-ID
        IDs = resultpage_soup.select("h4.heading > a:nth-of-type(1)") 

        for ID in IDs:
            if ID.attrs.get("href"):
                #extract the ID: from works/123456 to 123456
                ID_extracted = re.search("([0-9]+)", ID["href"]) 
                ID_list.append(ID_extracted.group(0))

    return ID_list

def write_work_IDs(IDs, novel):
    
    #Name ID file after novel name: LOTR.txt etc.
    with open(id_dir + "/" + novel + ".txt", "w", encoding="utf-8") as outfile:
        IDs_str = "\n".join(IDs)
        outfile.write(IDs_str)

def main(id_dir, search_url, search_parameter, novels, pages):
    
    if not os.path.exists(id_dir):
        os.makedirs(id_dir)
    
    for novel in novels:
        
        restart = True
        
        while restart:
            """
            This while-loop was needed, because often less IDs than expected were found (especially with queries that returned a lot of results).
            The loop will start over until the wanted amount of IDs has been collected.
            Sometimes duplicates are collected, therefore a condition with "set" is needed
            """
            restart = False

            IDs = get_work_IDs(search_url, search_parameter, novels[novel], pages)
            print(len(IDs), "IDs found for", novel)

            #Pages (=10) * 20 --> 200 texts per novel
            if (len(set(IDs)) == pages * 20):
                write_work_IDs(IDs, novel)
            else:
                print("Something went wrong. Not enough IDs gathered for: ", novel, ". Loop restarting!")
                restart = True

main(id_dir, search_url, search_parameter, novels, pages)
