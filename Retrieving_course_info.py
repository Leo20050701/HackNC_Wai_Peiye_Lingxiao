import requests
from bs4 import BeautifulSoup
import csv

def retrieve_course(session_term: str, subject_abbr: str, catalog_number: str) -> None:
    session = requests.Session()

    # Initial page to get CSRF token
    initial_page = "https://reports.unc.edu/class-search/"
    response = session.get(initial_page, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # URL for course search
    search_url = "https://reports.unc.edu/class-search/"
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'term': session_term,
        'subject': subject_abbr,
        'catalog_number': catalog_number
    }
    response = session.post(search_url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Specify the CSV file name
        csv_file = "output.csv"

        # Open the CSV file for writing
        with open(csv_file, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Find all <td> tags
            td_tags = soup.find_all('td')

            if not td_tags:
                print("No course information found.")
            else:
                for td in td_tags:
                    if td.text == "":
                        csv_writer.writerow("\n")
                    # Write the text inside the <td> tag to the CSV file
                    else:
                        csv_writer.writerow([td.text])

        print(f"CSV file '{csv_file}' created.")
    else:
        return 1

retrieve_course("2024 Spring", "COMP", "210")
retrieve_course("2024 Spring", "COMP", "110")
retrieve_course("2024 Spring", "MATH", "130")