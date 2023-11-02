"""Functions to find desired courses."""
from config import *
import csv
import re
from itertools import product
from typing import List, Dict
from csv_file_operator import *

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


def find_subject(course_data: list[dict], subject_abbr: str, subject_number: str, subject_period) -> list[dict]:
    """Find course with chosen subject."""
    new_data: list[dict] = list()
    for course in course_data:
        if course["Name"] == subject_abbr and course["Number"] == subject_number:
            if not subject_period:
                new_data.append(course)
            else:
                if course["Period"] == subject_period:
                    new_data.append(course)
    
    if new_data:
        return new_data
    return


def convert_time_to_float(time_str: str) -> float:
    """Converts a 12-hour format time string to a float representing the time in 24-hour format."""
    
    # Use regex to find time part
    time_match = re.search(r"([0-9]{2}:[0-9]{2} (AM|PM))", time_str)
    if time_match:
        time_str = time_match.group(1)
        
        if "PM" in time_str and "12" not in time_str:
            return float(time_str[0:2]) + 12.0 + float(time_str[3:5]) / 60
        else:
            return float(time_str[0:2]) + float(time_str[3:5]) / 60
    else:
        return None  


def check_conflict(courses: List[Dict[str, str]]) -> bool:
    """Check if there is a time conflict between courses."""
    for i, course1 in enumerate(courses):
        for j, course2 in enumerate(courses):
            if i >= j:
                continue
            intersecting_days = set(find_course_date(course1)["Days"]) & set(find_course_date(course2)["Days"])
            if intersecting_days:
                start_time1_str, end_time1_str = course1["Time"].split('-')
                start_time2_str, end_time2_str = course2["Time"].split('-')

                start_time1, end_time1 = map(convert_time_to_float, [start_time1_str, end_time1_str])
                start_time2, end_time2 = map(convert_time_to_float, [start_time2_str, end_time2_str])
                
                if (start_time1 < end_time2 + 15/60 and end_time1 + 15/60 > start_time2):
                    return True
    return False


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


def find_valid_schedule(all_course_data: str, courses_abbr: List[str], course_number: List[str], course_period: list[str], earliest_time: str, latest_time: str) -> List[List[Dict]]:
    if len(courses_abbr) != len(course_number):
        return
    
    all_course_data = read_csv(all_course_data)
    course_by_subject: list[list[dict]] = list()
    potential_valid_schedules: list[list[dict]] = list()
    final_valid_schedules: list[list[dict]] = list()

    all_course_data = find_time_between(all_course_data, earliest_time, latest_time)

    for abbr, number, period in zip(courses_abbr, course_number, course_period):
        course = find_subject(all_course_data, abbr, number, period)
        if course:
            course_by_subject.append(course)
    
    def find_combinations(picked_so_far: list[dict], remaining_subjects: list[list[dict]]):
        # Base case: no more subjects to consider
        if not remaining_subjects:
            potential_valid_schedules.append(picked_so_far)
            return
        
        # Recursive case
        current_subject = remaining_subjects[0]
        for course in current_subject:
            find_combinations(picked_so_far + [course], remaining_subjects[1:])

    find_combinations([], course_by_subject)
    if potential_valid_schedules:
        for i in range(0, len(potential_valid_schedules)):
            if not check_conflict(potential_valid_schedules[i]):
                final_valid_schedules.append(potential_valid_schedules[i])

    return final_valid_schedules


def find_course_date(course_data: dict[str: str]) -> list[dict]:
    date_match = re.search(r"^([MTWHF]+)", course_data["Time"])
    if date_match:
        course_data['Days'] = date_match.group(1)
    
    return course_data  