"""The main function!"""

from Retrieving_course_info import *
from Find_courses_tools import *
import csv

csv_fileName = "output.csv"

if __name__ == "__main__":
    print(find_subject(read_csv(csv_fileName), "MATH", "381"))
    #write_dict_to_csv(retrieve_course("2024 Spring", "IDS", "101"), csv_fileName)