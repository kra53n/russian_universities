import re
import requests as req
from bs4 import BeautifulSoup as bs


URL = "https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B"


def get_html(url):
    resp = req.get(url)

    if resp.status_code != 200:
        raise ConnectionError

    return resp.text

def find_number_of_pages(soup):
    return int(soup.find(id="pagination-wrapper").find_all("a")[-1].string)

def find_tags_with_classes_in_sequence(sequence, num_classes):
    result = []

    for tag in sequence:
        try:
            if len(tag["class"]) == num_classes:
                result.append(tag)
        except KeyError:
            pass

    return result

def parse_data_of_institute_row(row):
    """
    row - object of institute row in html on webpage
    """
    divs_with_class_institute_search_value = [
        div for div in find_tags_with_classes_in_sequence(
            row.find_all("div"), 1
         ) if div["class"][0] == "institute-search-value"
    ]

    try:
        university = {
            "rank"        : re.search(r"(?<=-)\w+", row.div["id"]).group(),
            "url"         : "https:" + row.a["href"],
            "logo"        : "https:" + row.a.img["src"],
            "name"        : row.find_all("a")[1].string,
            "city"        : divs_with_class_institute_search_value[1].a.string.replace(" ", ""),
            "average ege" : divs_with_class_institute_search_value[2].string,
            "students"    : divs_with_class_institute_search_value[0].string.replace(" ", ""),
        }
    except AttributeError:
        return None
    return university

def parse_institute_rows(soup):
    divs = [i for i in soup.find_all("div")]
    divs = find_tags_with_classes_in_sequence(divs, 1)
    divs = [div for div in divs if div["class"][0] == "institute-row"]

    result = []

    for row in divs:
        result.append(parse_data_of_institute_row(row))

    return result

def parse_vuzoteka():
    result = []

    html_doc = get_html(URL)
    soup = bs(html_doc, "html.parser")
    result.append(parse_institute_rows(soup))

    num_of_pages = find_number_of_pages(soup)

    for i in range(1, num_of_pages):
        print(f"{i}/{num_of_pages}")

        html_doc = get_html(URL + "?page=" + str(i + 1))
        soup = bs(html_doc, "html.parser")

        result.append(parse_institute_rows(soup))

    return result
