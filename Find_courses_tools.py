"""Functions to find desired courses."""
from config import *
import csv

def read_csv(csv_fileName) -> list[dict]:
    """Read .csv file and store the data into list[dict]."""
    data: list[dict] = list()
    with open(csv_fileName, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
        
    return data


def find_subject(course_data: list, subject_abbr: str, subject_number: str) -> list:
    """Find course with chosen subject."""
    new_data: list[dict] = list()
    for course in course_data:
        if course["Name"] == subject_abbr and course["Number"] == subject_number:
            new_data.append(course)

    return new_data
