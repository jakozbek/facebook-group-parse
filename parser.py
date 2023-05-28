import csv
import sys
from bs4 import BeautifulSoup
import re

# Check if the HTML file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the HTML file path as a command-line argument.")
    sys.exit(1)

html_file = sys.argv[1]

# Read the HTML file
try:
    with open(html_file, 'r') as file:
        html = file.read()
except IOError:
    print(f"Error: Unable to read the HTML file '{html_file}'.")
    sys.exit(1)

soup = BeautifulSoup(html, 'html.parser')

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

# Write the extracted names and emails to a CSV file
output_file = "output.csv"
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['First Name', 'Last Name', 'Email'])
    writer.writerows(names_emails)
