import requests
import re
from bs4 import BeautifulSoup
import csv


def retrive_course(session_term: str, subject_abbr: str, catalog_number: str) -> list:
    """Retrive raw data from website"""
    result: str = ""
    session = requests.Session()

    # Initial page to get CSRF token
    initial_page = "https://reports.unc.edu/class-search/"
    response = session.get(initial_page, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # URL for course search
    search_url = "https://reports.unc.edu/class-search/"
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'term': session_term,
        'subject': subject_abbr,
        'catalog_number': catalog_number
    }
    response = session.post(search_url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})
    keys = [
        "Period",
        "Course_Number",
        "Intro",
        "Term",
        "Hours",
        "Date",
        "Time",
        "Building",
        "Format",
        "Instructor",
        "Seats"
    ]
    
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
            print(td)
            if td == "" and HL_Test:
                course_list.append(course_info)
                course_info = {
                    "Name": subject_abbr,
                    "Number": catalog_number,
                }
                loop = 0
    
            elif re.match("^[0-9].+[H,L]", td) and HL_Test:
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
                key = keys[loop] 
                course_info[key] = td
                loop += 1
        
        course_list.append(course_info)
        return course_list
    
    else:
        print("Failed to retrieve course information. Please check your inputs and the website.")

def write_dict_to_csv(data_list, filename):
    if not data_list:
        return 1
     
    fieldnames = data_list[0].keys()

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for row in data_list:
            writer.writerow(row)




data_list = retrive_course("2024 Sprint", "CHEM", "101")
print(data_list)
write_dict_to_csv(data_list, "output.csv")

