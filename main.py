"""The main function!"""

from Retrieving_course_info import *
from Find_courses_tools import *
import csv

csv_fileName = "output.csv"


if __name__ == "__main__":
    # Test the function

    #Your Session Term
    session_term = "2024 Spring"

    #Subject Abbr
    courses_abbr = ["MATH", "CHEM", "COMP", "BUSI", "ECON"]

    #Course Number
    course_number = ["381", "101", "210", "100", "410"]

    #Time range
    earliest_time = "09:00 AM"
    latest_time = "06:00 PM"
    
    # This is to check wether the course that we search already in the .csv file, if not, retrieve it online.
    for abbr, number in zip(courses_abbr, course_number):
        if not check_values_in_same_csv_row(csv_fileName, abbr, number):
            write_dict_to_csv(retrieve_course(session_term, abbr, number), csv_fileName)

    result = find_valid_schedule(csv_fileName, courses_abbr, course_number, earliest_time, latest_time)
    
    for course_dict, schedule_sequence in zip(result, range(len(result))):
        credit_hour = 0
        print(f"\nSchedule {schedule_sequence+1}")
        for course in course_dict:
            credit_hour += float(course["Hours"])
            print(f"{course['Name']}{course['Number']} \t{course['Period']} \t {course['Time']} \t Seats: {course['Seats']} \t{course['Instructor']}")
        
        print(f"Credit Hour: {credit_hour}")