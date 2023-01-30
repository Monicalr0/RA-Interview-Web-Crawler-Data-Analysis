from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

# This program needs manually inspect the corresponding value for each topic
# Currently only scraping topic "Data Extraction and Web Screen Scraping which is f = 7"
URL = "https://forum.imacros.net/viewforum.php?f=7"
# PAGE_LIMIT = 2


def build_url(base_url=URL, page=1, question_href=""):
    # iMacros use start to jump between dfferent pages. Each page has 50 posts
    if question_href:
        return f"https://forum.imacros.net{question_href}"
    else:
        start = (page-1)*50
        return f"{base_url}&start={start}"


def scrape_question(href):
    """
    Function to scrape detail about a single question.
    """
    q_URL = build_url(question_href=href)
    q_response = urlopen(q_URL)
    q_html = q_response.read()
    q_soup = BeautifulSoup(q_html)

    # Add prpoperties (Title, Description, Vote, Views) of questions.
    question = {}
    try:
        question["Title"] = q_soup.find(
            "h2", class_="topic-title").text
        question["Description"] = q_soup.find(
            "div", class_="content").text
        # Number of posts(reply), due to special format need split
        question["PostsNum"] = q_soup.find(
            "div", class_="pagination").text.split()[0]
        question["URL"] = q_URL
    except:
        pass
    return question


def scrape_page(page=1):
    """
    Function to scrape a single page of questions in iMacros
    50 questions per page.
    """
    # Get page and read HTML from the page
    update_URL = build_url(page=page)
    response = urlopen(update_URL)
    html = response.read()
    soup = BeautifulSoup(html)

    questions_list = soup.find_all(
        "a", class_="topictitle")

    page_questions = []
    for q in questions_list:
        # For each question, get url to the question and scrape the actual description and answer
        question = scrape_question(href=q['href'][1:])
        page_questions.append(question)
    return page_questions


def scrape():
    """
    Function to scrape page within given range
    """
    questions = []
    for i in range(1, 16):
        questions.extend(scrape_page(i))
        print("page " + str(i) + " finished scraping")
    return questions


def export_data():
    """
    Function to export data, note the data may need cleaning due to edge cases after exported
    """
    data = scrape()
    filename = "iMacro11-15.csv"
    with open(filename, "w", newline="") as data_file:
        fieldnames = ["Title", "Description", "PostsNum", "URL"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    print("Export iMacros finished")


if __name__ == "__main__":
    export_data()
