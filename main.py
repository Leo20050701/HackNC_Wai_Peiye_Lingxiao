"""The main function!"""

from Retrieving_course_info import *
from Find_courses_tools import *
import csv

csv_fileName = "output.csv"

course_criteria: list[dict] = [{
    "subject": "MATH",
    "number": "381",
    "start_Time": "08:00",
    "end_Time": "10:00",
    },
    {
    "subject": "COMP",
    "number": "210",
    "start_Time": "08:00",
    "end_Time": "10:00",
    }]

if __name__ == "__main__":
    #Testing...
    #search_result = find_subject(read_csv(csv_fileName), course_criteria["subject"], course_criteria["number"])
    #search_result = find_time_between(search_result, course_criteria["start_Time"], course_criteria["end_Time"])
    #print(find_course_date(find_course(csv_fileName, course_criteria[0]["subject"], course_criteria[0]["number"], course_criteria[0]["start_Time"],course_criteria[0]["end_Time"])))
    #write_dict_to_csv(retrieve_course("2024 Spring", "IDS", "101"), csv_fileName)
    
    # Main script

    # Sample course data
    #print(find_course_date(test_data))
    # Test the function
