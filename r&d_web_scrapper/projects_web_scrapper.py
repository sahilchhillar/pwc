from bs4 import BeautifulSoup
import requests
import json

def get_responses(hmrc_url, chatgpt_qualifying_url, chatgpt_non_qualifying_url):
    hmrc_response = requests.get(url=hmrc_url)
    chatgpt_qualifying_response = requests.get(url=chatgpt_qualifying_url)
    chatgpt_non_qualifying_response = requests.get(url=chatgpt_non_qualifying_url)

    return [hmrc_response, chatgpt_qualifying_response, chatgpt_non_qualifying_response]

def get_soup_object(hmrc_response, chatgpt_qualifying_response, chatgpt_non_qualifying_response):
    hmrc_soup = BeautifulSoup(markup=hmrc_response.text, features="html.parser")
    chatgpt_qualifying_soup = BeautifulSoup(markup=chatgpt_qualifying_response.text, features="html.parser")
    chatgpt_non_qualifying_soup = BeautifulSoup(markup=chatgpt_non_qualifying_response.text, features="html.parser")

    return [hmrc_soup, chatgpt_qualifying_soup, chatgpt_non_qualifying_soup]

def scrap_web(hmrc_soup, chatgpt_qualifying_soup, chatgpt_non_qualifying_soup):
    hmrc_paragraphs = hmrc_soup.find_all(['p', 'ul', 'li'])
    chatgpt_qualifying_paragraphs = chatgpt_qualifying_soup.find_all('p')
    chatgpt_non_qualifying_paragraphs = chatgpt_non_qualifying_soup.find_all('p')

    return [hmrc_paragraphs, chatgpt_qualifying_paragraphs, chatgpt_non_qualifying_paragraphs]

def create_data(hmrc_paragraphs, chatgpt_qualifying_paragraphs, chatgpt_non_qualifying_paragraphs):
    paragraphs_details = []
    for p in hmrc_paragraphs:
        paragraphs_details.append(p.get_text().lower())

    for p in chatgpt_qualifying_paragraphs:
        paragraphs_details.append(p.get_text().lower())

    for p in chatgpt_non_qualifying_paragraphs:
        paragraphs_details.append(p.get_text().lower())

    return paragraphs_details

def create_dict_data(paragraphs_details):
    keyword = "case study"
    qualifying_keywords = ["qualifying activity", "not"]
    para_len = len(paragraphs_details)

    proj_details = {}

    i = 0
    proj_number = 0
    while i < para_len:
        while i < para_len and keyword not in paragraphs_details[i]:
            i += 1
        
        j = i+1
        proj_data = ""
        non_qualifying = False
        while j < para_len and keyword not in paragraphs_details[j]:
            if all(word in paragraphs_details[j] for word in qualifying_keywords):
                non_qualifying = True                
            proj_data += paragraphs_details[j]
            j += 1
        
        if non_qualifying:
            proj_details[str(proj_number)] = [proj_data, "non_qualifying"]
        else:
            proj_details[str(proj_number)] = [proj_data, "qualifying"]

        proj_number += 1

        i = j 
    
    return proj_details

def create_json(proj_details):
    with open('output.json', 'w') as json_file:
        json.dump(proj_details, json_file, indent=4)

def main(hmrc_url, chatgpt_qualifying_url, chatgpt_non_qualifying_url):
    hmrc_response, chatgpt_qualifying_response, chatgpt_non_qualifying_response = \
        get_responses(hmrc_url, chatgpt_qualifying_url, chatgpt_non_qualifying_url)
    
    hmrc_soup, chatgpt_qualifying_soup, chatgpt_non_qualifying_soup = \
        get_soup_object(hmrc_response, chatgpt_qualifying_response, chatgpt_non_qualifying_response)

    hmrc_paragraphs, chatgpt_qualifying_paragraphs, chatgpt_non_qualifying_paragraphs = \
        scrap_web(hmrc_soup, chatgpt_qualifying_soup, chatgpt_non_qualifying_soup)
    
    paragraphs_details = create_data(hmrc_paragraphs, chatgpt_qualifying_paragraphs, chatgpt_non_qualifying_paragraphs)

    proj_details = create_dict_data(paragraphs_details)

    create_json(proj_details)

if __name__ == "__main__":
    hmrc_url = "https://www.gov.uk/hmrc-internal-manuals/corporate-intangibles-research-and-development-manual/cird81980"
    chatgpt_qualifying_url = "http://127.0.0.1:5500/index_qualifying.html"
    chatgpt_non_qualifying_url = "http://127.0.0.1:5500/index_non_qualifying.html"
    main(hmrc_url, chatgpt_qualifying_url, chatgpt_non_qualifying_url)

