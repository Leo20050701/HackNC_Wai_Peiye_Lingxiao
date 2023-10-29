"""Functions to find desired courses."""
from config import *
import csv
import re

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


def find_time_between(course_data: list[dict], earliest_time: str, latest_time: str) -> list[dict]:
    """Filter course between time A and B."""
    new_data: list[dict] = list()
    start_time: float = 0.0
    end_time: float = 0.0
    #Process the begin and end time, from str to float, from 12h to 24h
    if "PM" in earliest_time and "12" not in earliest_time:
        earliest_time = float(earliest_time[0:2]) + 12.0 + float(earliest_time[3:5]) / 60
    elif not earliest_time:
        earliest_time = 8.0
    else:
        earliest_time = float(earliest_time[0:2]) + float(earliest_time[3:5]) / 60

    if "PM" in latest_time and "12" not in latest_time:
        latest_time = float(latest_time[0:2]) + 12.0 + float(latest_time[3:5]) / 60
    elif not latest_time:
        latest_time = 24.0
    else:
        latest_time = float(latest_time[0:2]) + float(latest_time[3:5]) / 60


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
                #Process the start and end time, from str to float, from 12h to 24h
                if "PM" in start_time and "12" not in start_time:
                    start_time = float(start_time[0:2]) + 12.0 + float(start_time[3:5]) / 60
                else:
                    start_time = float(start_time[0:2]) + float(start_time[3:5]) / 60
            
                if "PM" in end_time and "12" not in end_time:
                    end_time = float(end_time[0:2]) + 12.0 + float(end_time[3:5]) / 60
                else:
                    end_time = float(end_time[0:2]) + float(end_time[3:5]) / 60


                if earliest_time <= start_time and latest_time >= end_time:
                    new_data.append(course)

    return new_data


def find_course(course_data: list[dict], subject_abbr: str, course_number: str, start_Time: str, end_Time: str) -> list[dict]:
    """Find course that met all criteria"""
    #Build input check
    return find_time_between(find_subject(read_csv(course_data), subject_abbr, course_number), start_Time, end_Time)