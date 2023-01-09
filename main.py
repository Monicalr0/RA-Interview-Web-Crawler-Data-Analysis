from bs4 import BeautifulSoup
from urllib.request import urlopen
# import requests
# import csv

URL = "https://stackoverflow.com/questions?"  # Default URL to scrape questions
TAGGED_URL = "https://stackoverflow.com/questions/tagged/"
Q_URL = "https://stackoverflow.com"  # BASE URL to get question detail.
# build = "https://stackoverflow.com/questions/tagged/ui-automation?tab=frequent&page=1&pagesize=15"
# Using 50 question per page & limit rate to 3 page for rate limit consideration.
PAGE_LIMIT = 3
CURR_PAGE_LIMIT = 3


def build_url(base_url=URL, tab="Frequent", page=1, tag="", question_href=""):
    if tag:
        base_url = TAGGED_URL + tag
        print('added tag')
    if question_href:
        return Q_URL + question_href
    # Default using 50 post per page here to calculate max page.
    return f"{base_url}?tab={tab}&page={page}&pagesize=15"


# # Get page and read HTML from the page
# update_URL = build_url(tag="ui-automation")
# print(update_URL)
# response = urlopen(update_URL)
# html = response.read()
# soup = BeautifulSoup(html)

# # Get maximum number of page under the tag to update number of page to be scraped.
# max_page = int(soup.find_all(
#     "a", class_="s-pagination--item js-pagination-item")[-2].text)
# CURR_PAGE_LIMIT = min(PAGE_LIMIT, max_page)


# questions_list = soup.find_all("h3", class_="s-post-summary--content-title")

# new_URL = build_url(question_href=questions_list[0].a['href'])
# print(new_URL)

# for q in questions_list:
#     print(q.a['href'])

def scrape_question(href):
    """
    Function to scrape all info about a single question.
    """
    q_URL = build_url(question_href=href)
    q_response = urlopen(q_URL)
    q_html = q_response.read()
    q_soup = BeautifulSoup(q_html)

    # One of the answer
    print(q_soup.find("div", class_="answercell post-layout--right").div.text)
    # Add detail to question.
    question = {}
    question["Title"] = q_soup.find(
        "h1", class_="fs-headline1 ow-break-word mb8 flex--item fl1").text
    question["Description"] = q_soup.find(
        "div", class_="s-prose js-post-body").text
    print(question)


def scrape_page(page=1, tag=""):
    """
    Function to scrape a single page in stack overflow
    """
    # Get page and read HTML from the page
    update_URL = build_url(tag=tag)
    response = urlopen(update_URL)
    html = response.read()
    soup = BeautifulSoup(html)

    if page == 1:
        global CURR_PAGE_LIMIT
        # Get maximum number of page under the tag to update number of page to be scraped.
        max_page = int(soup.find_all(
            "a", class_="s-pagination--item js-pagination-item")[-2].text)
        CURR_PAGE_LIMIT = min(PAGE_LIMIT, max_page)

    questions_list = soup.find_all(
        "h3", class_="s-post-summary--content-title")

    page_questions = []
    # for q in questions_list:

    # For each question, get url to the question and scrape the actual description and answer
    question = scrape_question(href=questions_list[0].a['href'])

    # for summary in question_summary:
    #     question = summary.find(class_="question-hyperlink").text
    #     vote_count = summary.find(class_="vote-count-post").find("strong").text
    #     answers_count = summary.find(class_="status").find("strong").text
    #     view_count = summary.find(class_="views").text.split()[0]
    #     page_questions.append({
    #         "question":  question,
    #         "answers": answers_count,
    #         "views": view_count,
    #         "votes": vote_count
    #     })

    # return page_questions


def scrape(tag=""):
    """
    Function to scrape to PAGE_LIMIT
    """
    questions = []
    # for i in range(1, CURR_PAGE_LIMIT + 1):
    scrape_page(1, tag)
    # page_questions = scrape_page(i)
    # questions.extend(page_questions)
    return questions


scrape("ui-automation")
# # def export_data():
# #     data = scrape()
# #     with open("questions.csv", "w") as data_file:
# #         fieldnames = ["answers", "question", "views", "votes"]
# #         data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
# #         data_writer.writeheader()
# #         for d in data:
# #             data_writer.writerow(d)
# #         print("Done")


# if __name__ == "__main__":
#     from pprint import pprint
#     pprint(scrape())
# #     # export_data()
