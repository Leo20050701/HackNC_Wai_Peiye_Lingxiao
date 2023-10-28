"""For retrieving course information from UNC website."""
import requests
from bs4 import BeautifulSoup
import re

def retrive_course(session_term: str, subject_abbr: str, catalog_number: str) -> str:
    """Retrive raw data from website"""
    result: str = ""
    session = requests.Session()

    initial_page = "https://reports.unc.edu/class-search/" 
    response = session.get(initial_page, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']


    search_url: str = "https://reports.unc.edu/class-search/" 
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'term': session_term,
        'subject': subject_abbr,
        'catalog_number': catalog_number
    }
    response = session.post(search_url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        td_tags = soup.find_all('td')
        if not td_tags: 
            return
        
        for td in td_tags:
            result = result + " " + str(td.text)

        return result
    
    else:
        return 1
    
print(retrive_course("2024 Spring", "COMP", "210"))
print(retrive_course("2024 Spring", "COMP", "10"))
print(retrive_course("2024 Spring", "MATH", "233"))
