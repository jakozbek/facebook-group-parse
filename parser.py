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

# Find all <a> elements with '/user' in the href and extract the first and last name from the aria-label
name_elements = soup.find_all('a', href=re.compile('/user'), attrs={"aria-label": True})
names = []
for name_element in name_elements:
    aria_label = name_element['aria-label']
    # Extract first and last name from the aria-label
    match = re.match(r'^(.*?)\s(.*)$', aria_label)
    if match:
        first_name = match.group(1)
        last_name = match.group(2)
        names.append((first_name, last_name))

# Print the extracted names
for name in names:
    print(f"First Name: {name[0]}, Last Name: {name[1]}")
