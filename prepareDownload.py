"""
This script searches for fanfiction on archiveofourown.org and extracts the identifier of each found text and saves it to a txt file
"""
#########
#Imports#
#########
from bs4 import BeautifulSoup
import os
import re
import requests

############
#Parameters#
############
id_dir = os.path.join(os.getcwd(), "ID")
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
pages = 10       #   1 page = 20 results


###########
#Functions#
###########

def get_work_IDs(search_url, search_parameter, novel, pages):
    
    ID_list = []

    for page in range(1, pages+1): 
        
        query_url = "".join((search_url, search_parameter["page_num"], str(page), search_parameter["word_count"], search_parameter["language"], search_parameter["fandom_name"], novel))
        
        result_page = requests.get(query_url)
        
        resultpage_soup = BeautifulSoup(result_page.text, "lxml")
        IDs = resultpage_soup.select("h4.heading > a:nth-of-type(1)")

        for ID in IDs:
            if ID.attrs.get("href"):
                ID_extracted = re.search("([0-9]+)", ID["href"])
                ID_list.append(ID_extracted.group(0))

    return ID_list

def write_word_IDs(IDs, novel):
    with open(id_dir + "/" + novel + "_IDs.txt", "w", encoding="utf-8") as outfile:
        IDs_str = "\n".join(IDs)
        outfile.write(IDs_str)

def main(id_dir, search_url, search_parameter, novels, pages):
    
    if not os.path.exists(id_dir):
        os.makedirs(id_dir)
    
    for novel in novels:
        
        restart = True

        while restart:
            restart = False

            IDs = get_work_IDs(search_url, search_parameter, novels[novel], pages)
            print(len(IDs), "IDs found for", novel)
            #print(IDs)
            if (len(IDs) == pages * 20):
                write_word_IDs(IDs, novel)
            else:
                print("Something went wrong. Not enough IDs gathered for: ", novel, ". Loop restarting!")
                restart = True 
main(id_dir, search_url, search_parameter, novels, pages)