"""The main function!"""

from Retrieving_course_info import *
from Find_courses_tools import *
import csv

csv_fileName = "output.csv"

course_criteria: dict[str: str] = {
    "subject": "MATH",
    "number": "381",
    "start_Time": "08:00",
    "end_Time": "13:00",
    "Date": "MTWTHF"
}

if __name__ == "__main__":
    #Testing...
    search_result = find_subject(read_csv(csv_fileName), course_criteria["subject"], course_criteria["number"])
    search_result = find_time_between(search_result, course_criteria["start_Time"], course_criteria["end_Time"])
    print(search_result)
    #write_dict_to_csv(retrieve_course("2024 Spring", "IDS", "101"), csv_fileName)
