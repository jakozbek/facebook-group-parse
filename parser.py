#!/usr/bin/env python

import csv
import sys
from typing import TypedDict
from bs4 import BeautifulSoup
import re
import argparse
from datetime import datetime

from upload import upload_subscriber

parser = argparse.ArgumentParser(
    description="Parse HTML files for email addresses and names"
)
parser.add_argument("html_files", nargs="+", help="HTML file paths to parse")
parser.add_argument("--ml", action="store_true", help="Upload to mailing list")
parser.add_argument("--csv", action="store_true", help="Write output to CSV file")
parser.add_argument(
    "--csv-filename", default=None, help="Custom CSV filename (default: YYMMDD.csv)"
)

args = parser.parse_args()


def strip_html_classes(html):
    soup = BeautifulSoup(html, "html.parser")

    # Find all elements with the class attribute
    elements = soup.find_all(attrs={"class": True})
    elements2 = soup.find_all(attrs={"style": True})

    for meta in soup.find_all("meta"):
        meta.extract()

    for style in soup.find_all("style"):
        style.extract()

    for script in soup.find_all("script"):
        script.extract()

    for link in soup.find_all("link"):
        link.extract()

    for path in soup.find_all("path"):
        path.extract()

    for img in soup.find_all("image"):
        img.extract()

    # Remove the class attribute from each element
    for element in elements:
        del element["class"]

    for element in elements2:
        del element["style"]

    # Return the modified HTML
    return str(soup)


class UserInfo(TypedDict):
    email: str
    fname: str
    lname: str


def parse_for_fb(html_file):
    # Read the HTML file
    try:
        with open(html_file, "r") as file:
            html = file.read()
    except IOError:
        print(f"Error: Unable to read the HTML file '{html_file}'.")
        sys.exit(1)

    cleaned_html = strip_html_classes(html)

    soup = BeautifulSoup(cleaned_html, "html.parser")

    # Find all <div> elements containing an email
    email_elements = soup.find_all("div", string=re.compile(r"[\w\.-]+@[\w\.-]+"))

    # Extract the associated name for each email
    users = []
    for email_element in email_elements:
        # Find the preceding <a> element that contains the name
        name_element = email_element.find_previous(
            "a", href=re.compile("/user"), attrs={"aria-label": True}
        )
        if name_element:
            aria_label = name_element["aria-label"]
            # Extract first and last name from the aria-label
            match = re.match(r"^(.*?)\s(.*)$", aria_label)
            if match:
                first_name = match.group(1)
                last_name = match.group(2)
                email = email_element.text.strip()
                userinfo = UserInfo(email=email, fname=first_name, lname=last_name)
                users.append(userinfo)

    length_of_emails = len(users)

    print(f"Parsed {length_of_emails} emails in file")

    return users


def write_output(output_file, names_emails):
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Email"])
        writer.writerows(names_emails)


if not args.html_files:
    print("Please provide HTML file paths as command-line arguments.")
    sys.exit(1)

all_names_emails = []

for html_file in args.html_files:
    all_names_emails += parse_for_fb(html_file)

# Upload via API
if args.ml:
    print("Uploading to mailing list...")
    if not all_names_emails:
        print("No emails found to upload.")
        sys.exit(0)

    for user in all_names_emails:
        upload_subscriber(user["email"], user["fname"], user["lname"])


if args.csv:
    if args.csv_filename:
        output_filename = args.csv_filename
    else:
        output_filename = f"{datetime.now().strftime('%y%m%d')}.csv"

    write_output(
        output_filename,
        [[user["fname"], user["lname"], user["email"]] for user in all_names_emails],
    )
    print(f"Data written to {output_filename}")
