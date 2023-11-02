"""A file that store functions related to CSV files."""

from config import *
import csv
import os


def find_course_in_course_catalog(course_catalog: str, course_name: str, course_num: str):
    course_catalog = read_csv(course_catalog)
    left, right = 0, len(course_catalog) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_name = course_catalog[mid]['Name']
        if mid_name < course_name:
            left = mid + 1
        elif mid_name > course_name:
            right = mid - 1
        else:

            for i in range(mid, right + 1):
                if course_catalog[i]['Name'] == course_name and course_catalog[i]['Number'] == course_num:
                    return course_catalog[i]
            for i in range(mid, left - 1, -1):
                if course_catalog[i]['Name'] == course_name and course_catalog[i]['Number'] == course_num:
                    return course_catalog[i]

            break

    return {}



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



def write_dict_to_csv(data_list: list[dict], filename: str) -> None:
    """Import data to a csv file."""
    if not data_list:
        return 

    fieldnames = data_list[0].keys()
    
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in data_list:
            writer.writerow(row)


def check_values_in_same_csv_row(csv_file_path: str, abbr: str, number: str) -> bool:
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            if row['Name'] == abbr and row['Number'] == number:
                return True

    return False 