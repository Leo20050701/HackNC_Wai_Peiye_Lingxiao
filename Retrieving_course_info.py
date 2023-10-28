import requests
from bs4 import BeautifulSoup
import csv

def append_to_csv(data, csv_file):
    with open(csv_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

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

        # Find all <tr> tags
        tr_tags = soup.find_all('tr')

        if not tr_tags:
            print("No course information found.")
        else:
            # Specify the CSV file name
            csv_file = "output.csv"
            
            for tr in tr_tags:
                data = [subject_abbr, catalog_number]  # Add subject abbreviation and catalog number as the first two columns
                td_tags = tr.find_all('td')
                for td in td_tags:
                    strong_tag = td.find('strong')
                    if strong_tag is None:  # Ignore <td> elements containing <strong> tags
                        text = td.text.strip()  # Remove leading/trailing whitespace
                        if text:  # Check if the text is not empty
                            data.append(text)
                # Append the data to the CSV file for each <tr> tag
                append_to_csv(data, csv_file)

            print("Data appended to CSV file.")

    else:
        print("Failed to retrieve course information. Please check your inputs and the website.")

# Example usage:
retrieve_course("2024 Spring", "COMP", "210")
retrieve_course("2024 Spring", "MATH", "110")
