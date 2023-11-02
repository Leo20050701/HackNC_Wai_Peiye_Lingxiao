"""Find course Gen-ed info on UNC Course Catalog."""

import re
from bs4 import BeautifulSoup
import requests
from config import *
import time
from Retrieving_course_info import *
from Find_courses_tools import *
from csv_file_operator import *

def find_course_ge(course: dict, min_num: int = 10, max_num: int = 999) -> dict:
    """Find course gen-ed info."""
    subject_abbr: str = ""
    course_num: str = ""
    
    if remove_HLI(course["Number"]) >= min_num and remove_HLI(course["Number"]) <= max_num:
        if (course["Name"] != subject_abbr or course["Number"] != course_num):
            print(f"Finding GE for {course['Name']} {course['Number']} .....")
            subject_abbr = course["Name"]
            course_num = course["Number"]
            genEd_info = parse_genEd_info(retrieve_course_ge(subject_abbr, course_num))
    
        course["Number_of_GenEd"] = len(genEd_info)
        for i in range(0, NUM_OF_GENED_IN_CSV_TITLE):
            key_name = f"Gen_Ed_{i+1}"
            if i < len(genEd_info):
                course[key_name] = genEd_info[i]
            else:
                course[key_name] = ""
    else:
        return 1

    return course



def remove_HLI(init: str) -> int:
    """Change Honor, Lab, I class to int for comparison."""
    if re.match("[0-9]{2,3}[H|L|I]",init):
        return int(init[:-1])
    else:
        return int(init)


def retrieve_course_ge(subject_abbr: str, subject_num: str) -> str:
    """Retrieve gen-ed info from website."""
    search_url = f"https://catalog.unc.edu/search/?search={subject_abbr}+{subject_num}"
    find_Gened: str = ""
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        parsed_response = soup.find_all('span')
    else:
        return
    
    for i in parsed_response:
        i = re.search("(FC-.+).$", i.text)
        if i:
            find_Gened = i.group(1)
    
    return find_Gened


def parse_genEd_info(raw_info: str) -> list[str]:
    """Distinguish each Gen-ed from raw info."""
    genEd_list: list[str] = list()
    temp_list: list[str] = list()
    #Seperite two GenEd
    if "," in raw_info:
        genEd_list  = raw_info.split(",")
        for i in range(0, len(genEd_list)):
            if genEd_list[i][0] == " ":
                genEd_list[i] = genEd_list[i][1:]
    
    else:
        genEd_list.append(raw_info)
    
    #Eliminate HI

    for i in range(0, len(genEd_list)):
        if "FC" in genEd_list[i]:
            temp_list.append(genEd_list[i])

    return temp_list


def build_course_catalog(subject: str) -> list[dict]:
    """Retrieve all course abbr and number from website."""
    #abbr_list= ["COMP", "MATH", "ECON"]
    unc_course_list: list[dict] = list()
    temp_course: dict[str, str] = dict()
    search_url = f"https://catalog.unc.edu/search/?search={subject}"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    parsed_response = soup.find_all('h2')
    for line in parsed_response:
        temp_course = {}
        course_info = re.search(f"^({subject} .+)$", line.text)
        if course_info and re.match("^[A-Z]{4} [0-9]{2,3}(H|L|I)? .+$", course_info.group(1)):
            temp_subject = re.search(r"^([A-Z]{4}) ([0-9]{2,3}[H|L|I]?) (.+)$", course_info.group(1))
            temp_course["Name"] = temp_subject.group(1)
            temp_course["Number"] = temp_subject.group(2)
            temp_course["Full_Name"] = temp_subject.group(3)
            print(f"Found course {temp_course['Name']} {temp_course['Number']} {temp_course['Full_Name']}")
            unc_course_list.append(temp_course)
        
    return unc_course_list


def find_all_subject_abbr() -> list:
    """Retrieve all subject abbr"""
    search_url = "https://catalog.unc.edu/courses/"
    response = requests.get(search_url)
    abbr_list: list[str] = list()
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        parsed_response = soup.find_all('li')
 
    else:
        return
    
    for line in parsed_response:
        abbr = re.search("^[A-Z, ].+\(([A-Z]{4})\)$", line.text)            
        if abbr:
            if abbr.group(1) in abbr_list:
                break
            abbr_list.append(abbr.group(1))


    return sorted(abbr_list)


def retrieve_GE_and_put_in_csv(min_num: int = 10, max_num: int = 999) -> None:
    """Main for this section."""
    course_abbr_list = find_all_subject_abbr()
    temp_list: list[dict] = [{}]
    for subject in course_abbr_list:
        course_catalog = build_course_catalog(subject)
        for i in course_catalog:
            #time.sleep(1)
            temp_list[0] = find_course_ge(i, min_num, max_num)
            if temp_list[0] != 1:
                write_dict_to_csv(temp_list, COURSE_CATALOG_CSV_FILE_NAME)
                
    return
