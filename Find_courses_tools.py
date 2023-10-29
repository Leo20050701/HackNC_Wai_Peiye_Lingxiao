"""Functions to find desired courses."""
from config import *
import csv
import re
from itertools import product
from typing import List, Dict

def read_csv(csv_fileName) -> list[dict]:
    """Read .csv file and store the data into list[dict]."""
    data: list[dict] = list()
    with open(csv_fileName, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
        
    if data:
        return data
    return


def find_subject(course_data: list[dict], subject_abbr: str, subject_number: str) -> list[dict]:
    """Find course with chosen subject."""
    new_data: list[dict] = list()
    for course in course_data:
        if course["Name"] == subject_abbr and course["Number"] == subject_number:
            new_data.append(course)
    
    if new_data:
        return new_data
    return


def convert_time_to_float(time_str: str) -> float:
    """Converts a 12-hour format time string to a float representing the time in 24-hour format."""
    if "PM" in time_str and "12" not in time_str:
        return float(time_str[0:2]) + 12.0 + float(time_str[3:5]) / 60
    else:
        return float(time_str[0:2]) + float(time_str[3:5]) / 60


<<<<<<< HEAD
=======
def check_conflict(courses: List[Dict[str, str]]) -> bool:
    """Check if there is a time conflict between courses."""
    for i, course1 in enumerate(courses):
        for j, course2 in enumerate(courses):
            if i >= j:
                continue
            intersecting_days = set(course1["Day"]) & set(course2["Day"])
            if intersecting_days:
                start_time1_str, end_time1_str = course1["Time"].split('-')
                start_time2_str, end_time2_str = course2["Time"].split('-')

                start_time1, end_time1 = map(convert_time_to_float, [start_time1_str, end_time1_str])
                start_time2, end_time2 = map(convert_time_to_float, [start_time2_str, end_time2_str])
                
                if (start_time1 < end_time2 + 15/60 and end_time1 + 15/60 > start_time2):
                    return True
    return False


>>>>>>> development_visualization
def find_time_between(course_data: list[dict], earliest_time: str, latest_time: str) -> list[dict]:
    """Filter course between time A and B."""
    new_data: list[dict] = list()
    start_time: float = 0.0
    end_time: float = 0.0
    
    if earliest_time != "":
        earliest_time = convert_time_to_float(earliest_time)
    else:
        earliest_time = 8.0
    if latest_time != "":
        latest_time = convert_time_to_float(latest_time)
    else:
        latest_time = 24.0


    for course in course_data:
        if course["Time"] == None:
            pass
        else:
            start_time = re.search(r"^[A-Z]+ ([0-9][0-9]:[0-9][0-9] (PM|AM))", course["Time"])
            end_time = re.search(r"([0-9][0-9]:[0-9][0-9] (PM|AM))$", course["Time"])
            if start_time and end_time:
                start_time = start_time.group(1)
                end_time = end_time.group(1)

            if start_time and end_time:
                start_time = convert_time_to_float(start_time)
                end_time = convert_time_to_float(end_time)

                if earliest_time <= start_time and latest_time >= end_time:
                    new_data.append(course)

    return new_data


def find_course_date(course_data: list[dict]) -> list[dict]:
    for course in course_data:
        date_match = re.search(r"^([MTWUF]+)", course["Time"])
        if date_match:
            course['Days'] = date_match.group(1)
    return course_data  


def find_course(course_data: list[dict], subject_abbr: str, course_number: str, start_Time: str, end_Time: str) -> list[dict]:
    """Find course that met all criteria"""
    #Build input check
    return find_time_between(find_subject(read_csv(course_data), subject_abbr, course_number), start_Time, end_Time)