"""Retrive course info from unc course search and put them into a csv file at certain format."""
import requests
import re
from bs4 import BeautifulSoup
import csv
import os
from config import *
from typing import Dict
from csv_file_operator import *


def retrieve_course(session_term: str, subject_abbr: str, catalog_number: str) -> list:
    """Retrive raw data from website"""
    #input type check
    if not isinstance(session_term, str) or not isinstance(subject_abbr, str) or not isinstance(catalog_number, str):
        return
    
    if not re.match("^[0-9]{2,3}(H|I|L|$)", catalog_number):
        return
    
    if session_term not in VALID_SESSIONTERM or not re.match("^[A-Z]{3,4}$", subject_abbr) or int(catalog_number) <= 10 or int(catalog_number) >= 1000:
        return 
    
    result: str = ""
    session = requests.Session()

    initial_page = "https://reports.unc.edu/class-search/"
    response = session.get(initial_page, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    search_url = "https://reports.unc.edu/class-search/"
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'term': session_term,
        'subject': subject_abbr,
        'catalog_number': catalog_number
    }
    response = session.post(search_url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})

    print(f"Retrieving {subject_abbr} {catalog_number}......")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        course_list: list[dict] = list()

        td_tags = soup.find_all('td')
        loop = 0
        course_info = {
            "Name": subject_abbr,
            "Number": catalog_number,
        }
        HL_Test: bool = True
        for td in td_tags[3:]:
            td = td.text
            if td == "" and HL_Test:
                course_list.append(course_info)
                course_info = {
                    "Name": subject_abbr,
                    "Number": catalog_number,
                }
                loop = 0
    
            elif re.match("^[0-9].+[H,L,I]", td) and HL_Test:
                course_list.append(course_info)
                HL_Test = False
                moditifed_number: str = td
                course_info = {
                    "Name": subject_abbr,
                    "Number": moditifed_number,
                }
                loop = 0
    
            elif td == "" and not HL_Test:
                loop = 0
                if "Period" in course_info:
                    course_list.append(course_info)

                course_info = {
                    "Name": subject_abbr,
                    "Number": moditifed_number,
                }

            else:
                key = KEYS_CSV[loop] 
                course_info[key] = td
                loop += 1
        
        course_list.append(course_info)
        if "Period" in course_list[0]:
            return course_list
    
    else:
        print(f"Fail to retrieve {subject_abbr} {catalog_number}......")
        return

    return


def check_values_in_same_csv_row(csv_file_path: str, abbr: str, number: str) -> bool:
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            if row['Name'] == abbr and row['Number'] == number:
                return True

    return False 