"""The main function!"""

from Retrieving_course_info import *
from Find_courses_tools import *
import csv

csv_fileName = "output.csv"


if __name__ == "__main__":
    # Testing...
    # Main script

    # Sample course data
    # print(find_course_date(test_data))
    # Test the function
    session_term = "2024 Spring"
    courses_abbr = ["ECON", "CHEM", "COMP", "CHEM", "BUSI"]
    course_number = ["410", "101", "210", "101L", "100"]
    earliest_time = "10:00 AM"
    latest_time = "06:00 PM"
    
    # This is to check wether the course that we search already in the .csv file, if not, retrieve it online.
    for abbr, number in zip(courses_abbr, course_number):
        if not check_values_in_same_csv_row(csv_fileName, abbr, number):
            write_dict_to_csv(retrieve_course(session_term, abbr, number), csv_fileName)

    result = find_valid_schedule(csv_fileName, courses_abbr, course_number, earliest_time, latest_time)
    print(result)

    for course_dict, schedule_sequence in zip(result, range(len(result))):
        print(f"\nSchedule {schedule_sequence+1}")
        for course in course_dict:
            print(f"{course['Name']} - {course['Number']}   {course['Time']}")