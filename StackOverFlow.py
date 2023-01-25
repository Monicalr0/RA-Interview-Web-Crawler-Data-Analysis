from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

URL = "https://stackoverflow.com/questions?"  # Default URL to scrape questions
TAGGED_URL = "https://stackoverflow.com/questions/tagged/"
Q_URL = "https://stackoverflow.com"  # Base URL to get question detail.
# Using 50 question per page & limit rate to 3 page for daily rate limit consideration.
PAGE_LIMIT = 2
CURR_PAGE_LIMIT = 2


def build_url(base_url=URL, tab="Frequent", page=1, tag="", question_href=""):
    if tag:
        base_url = TAGGED_URL + tag
        print('added tag')
    if question_href:
        return Q_URL + question_href
    # Default using 50 post per page here to calculate max page.
    # Using 50 here because that's how many get scraped no matter what pagesize is specified in link.
    return f"{base_url}?tab={tab}&page={page}&pagesize=50"


def scrape_question(href):
    """
    Function to scrape all info about a single question.
    """
    q_URL = build_url(question_href=href)
    q_response = urlopen(q_URL)
    q_html = q_response.read()
    q_soup = BeautifulSoup(q_html)

    # Add prpoperties (Title, Description, Vote, Views) of questions.
    question = {}
    try:
        question["Title"] = q_soup.find(
            "h1", class_="fs-headline1 ow-break-word mb8 flex--item fl1").text
        question["Description"] = q_soup.find(
            "div", class_="s-prose js-post-body").text
        question["Views"] = q_soup.select_one(
            "div[title*=Viewed]").text.split()[1]
        question["Votes"] = q_soup.find(
            "div", class_="js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title").text
    except:
        pass

    answers = q_soup.find_all("div", class_="answercell post-layout--right")
    for i in range(len(answers)):
        answers[i] = answers[i].div.text
    question["Answers"] = answers

    return question


def scrape_page(page=1, tag=""):
    """
    Function to scrape a single page in stack overflow
    """
    # Get page and read HTML from the page
    update_URL = build_url(page=page, tag=tag)
    response = urlopen(update_URL)
    html = response.read()
    soup = BeautifulSoup(html)

    if page == 1:
        global CURR_PAGE_LIMIT
        # Get maximum number of page under the tag to update number of page to be scraped.
        page_numbers = soup.find_all(
            "a", class_="s-pagination--item js-pagination-item")
        if len(page_numbers) >= 2:
            max_page = int(page_numbers[-2].text)
        else:
            max_page = 1
        CURR_PAGE_LIMIT = min(PAGE_LIMIT, max_page)

    questions_list = soup.find_all(
        "h3", class_="s-post-summary--content-title")

    page_questions = []
    for q in questions_list:
        # For each question, get url to the question and scrape the actual description and answer
        question = scrape_question(href=q.a['href'])
        page_questions.append(question)
    return page_questions


def scrape(tag=""):
    """
    Function to scrape to PAGE_LIMIT
    """
    questions = []
    for i in range(1, CURR_PAGE_LIMIT + 1):
        # An issue need to be fixed later for maximum page.
        if i > CURR_PAGE_LIMIT:
            break
        questions.extend(scrape_page(i, tag))
    return questions


def export_data(tag=""):
    data = scrape(tag)
    if tag:
        filename = tag + ".csv"
    else:
        filename = "question.csv"
    with open(filename, "w", newline="") as data_file:
        fieldnames = ["Title", "Description", "Views", "Votes", "Answers"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    print("Export tag: " + tag + " finished")


if __name__ == "__main__":
    # Scraping Stackoverflow using existing tags related to web automation, ui automation, data scraping etc.
    #tags = ["ui-automation", "webautomation", "web-scraping"]
    tags = ["automation", "screen-scraping", "web-crawler"]
    for t in tags:
        export_data(t)
