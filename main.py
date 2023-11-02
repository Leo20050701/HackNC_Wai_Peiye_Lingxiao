"""The main function!"""

import csv
from Retrieving_course_info import *
from Find_courses_tools import *
from Find_courses_GE_Info import *
from config import *
from csv_file_operator import *


if __name__ == "__main__":
    # Test the function

    #Your Session Term
    session_term = "2024 Spring"

    #Subject Abbr
    courses_abbr = ["MATH", "CHEM", "COMP", "ECON"]

    #Course Number
    course_number = ["381", "101", "210", "410"]

    #Course Period
    course_period = ["", "", "002", ""]
    #Time range
    earliest_time = "09:00 AM"
    latest_time = "09:00 PM"
    
    #retrieve_GE_and_put_in_csv(0, 500)

    for abbr, number in zip(courses_abbr, course_number):
        if not check_values_in_same_csv_row(CSV_FILENAME, abbr, number):
            write_dict_to_csv(retrieve_course(session_term, abbr, number), CSV_FILENAME)

    result = find_valid_schedule(CSV_FILENAME, courses_abbr, course_number, course_period, earliest_time, latest_time)
    
    for course_dict, schedule_sequence in zip(result, range(len(result))):
        credit_hour = 0
        print(f"\nSchedule {schedule_sequence+1}")
        for course in course_dict:
            credit_hour += float(course["Hours"])
            print(f"{course['Name']}{course['Number']} \t{course['Period']} \t {course['Time']} \t Seats: {course['Seats']} \t{course['Instructor']}")
        
        print(f"Credit Hour: {credit_hour}")
    
    print(find_course_in_course_catalog(COURSE_CATALOG_CSV_FILE_NAME, "CHIN", "101"))