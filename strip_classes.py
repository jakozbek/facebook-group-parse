import sys
from bs4 import BeautifulSoup

def strip_html_classes(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with the class attribute
    elements = soup.find_all(attrs={'class': True})
    elements2 = soup.find_all(attrs={'style': True})

    for meta in soup.find_all('meta'):
        meta.extract()

    for style in soup.find_all('style'):
        style.extract()

    for script in soup.find_all('script'):
        script.extract()

    for link in soup.find_all('link'):
        link.extract()

    for path in soup.find_all('path'):
        path.extract()

    for img in soup.find_all('image'):
        img.extract()

    # Remove the class attribute from each element
    for element in elements:
        del element['class']

    for element in elements2:
        del element['style']

    # Return the modified HTML
    return str(soup)


def strip_html_file(file_path):
    # Read the HTML file
    with open(file_path, 'r') as file:
        html = file.read()

    # Strip HTML classes
    stripped_html = strip_html_classes(html)

    # Write the modified HTML back to the file
    with open('test_file.html', 'w') as file:
        file.write(stripped_html)


# Check if the filename is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python strip_html_classes.py <filename>")
    sys.exit(1)

# Get the filename from the command line argument
html_file_path = sys.argv[1]

# Strip HTML classes from the file
strip_html_file(html_file_path)
print("HTML classes stripped from the file:", html_file_path)

