import csv
import sys
from bs4 import BeautifulSoup
import re

from strip_classes import strip_html_classes

def parse_for_fb(html_file):
    # Read the HTML file
    try:
        with open(html_file, 'r') as file:
            html = file.read()
    except IOError:
        print(f"Error: Unable to read the HTML file '{html_file}'.")
        sys.exit(1)

    cleaned_html = strip_html_classes(html)

    soup = BeautifulSoup(cleaned_html, 'html.parser')

    # Find all <div> elements containing an email
    email_elements = soup.find_all('div', string=re.compile(r'[\w\.-]+@[\w\.-]+'))

    # Extract the associated name for each email
    names_emails = []
    for email_element in email_elements:
        # Find the preceding <a> element that contains the name
        name_element = email_element.find_previous('a', href=re.compile('/user'), attrs={"aria-label": True})
        if name_element:
            aria_label = name_element['aria-label']
            # Extract first and last name from the aria-label
            match = re.match(r'^(.*?)\s(.*)$', aria_label)
            if match:
                first_name = match.group(1)
                last_name = match.group(2)
                email = email_element.text.strip()
                names_emails.append((first_name, last_name, email))

    # Print the extracted names and associated emails
    for name_email in names_emails:
        print(f"First Name: {name_email[0]}, Last Name: {name_email[1]}, Email: {name_email[2]}")

    return names_emails

def write_output(output_file, names_emails):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Email'])
        writer.writerows(names_emails)

# Check if the HTML file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the HTML file path as a command-line argument.")
    sys.exit(1)

html_files = sys.argv[1:]

all_names_emails = []

for html_file in html_files:
    all_names_emails += parse_for_fb(html_file)

write_output('output.csv', all_names_emails)
