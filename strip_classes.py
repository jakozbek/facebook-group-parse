import sys
from bs4 import BeautifulSoup


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
