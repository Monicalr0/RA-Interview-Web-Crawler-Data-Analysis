from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import requests

PAGE_LIMIT = 3  # Set to small value considering Github rate limit
# This code is not perfect as the result from keywords search would requires
# some manual / automated data cleaning
# TODO: solve chinese encoding problem


def build_url(page=1, search="", sort="indexed"):
    base_url = "https://api.github.com/search/repositories"
    # Default using 100 repo per page
    # Default sort would be by best match (i.e. indexed)
    return f"{base_url}?q={search}&page={page}&per_page=100&sort={sort}"


def scrape(topic=""):
    """
    Function to scrape TOP 20 repo under topics
    """
    URL = "https://github.com/topics/" + topic
    # Current implementation can only scrape first 20 repo as there is a 'load more'
    # buttom block from further scraping.

    # Based on documentation seems like github REST API does not
    # provide function to scrape list of repos with certain tags.
    # Using BeautifulSoup w/ url instead.
    q_response = urlopen(URL)
    q_html = q_response.read()
    q_soup = BeautifulSoup(q_html)

    repos = q_soup.find_all(
        "article", class_="border rounded color-shadow-small color-bg-subtle my-4")
    repositories = []
    for r in repos:
        repo = {}
        repo["Title"] = r.div.div.div.h3.text.split()[2]
        # Some Repo may not have description, skip in this case and fill in NULL
        if len(r.findChildren("p")) >= 1:
            repo["Description"] = r.findChildren("p")[0].text
        else:
            repo["Description"] = ""
        repo["Topic"] = topic
        repositories.append(repo)

    return repositories


def scrape_search(keywords=""):
    """
    Function to scrape TOP 100 * PAGE_LIMIT Repo from search result 
    """
    # Create an API request, scrape up to page limit.
    repos = []
    i = 1
    while i <= PAGE_LIMIT:
        # Using default sort i.e. best match here beacause
        # the number of star may affected by large company.
        url = build_url(page=i, search=keywords)
        try:
            response = requests.get(url)

            # Process the result for data.
            response_dict = response.json()
            for r in response_dict["items"]:
                repo = {}
                repo["Title"] = r["full_name"]
                repo["Description"] = r["description"]
                repo["Topics"] = r["topics"]
                repo["Stars"] = r["stargazers_count"]
                repo["Language"] = r["language"]
                repo["search"] = keywords
                repos.append(repo)
        except:
            continue

        i += 1
    return repos


def export_data(topics=[], keywords=[]):
    data = []
    if topics:
        # TODO: check if can be done via api after analysis finished.
        for t in topics:
            data.extend(scrape(t))
        filename = "github.csv"
        with open(filename, "w", newline="") as data_file:
            fieldnames = ["Title", "Description", "Topic"]
            data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            data_writer.writeheader()
            for d in data:
                data_writer.writerow(d)
        print("Export Github tags finished")
    elif keywords:
        for k in keywords:
            data.extend(scrape_search(k))
        filename = "github_search.csv"
        with open(filename, "w", newline="") as data_file:
            fieldnames = ["Title", "Description",
                          "Topics", "Stars", "Language", "search"]
            data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            data_writer.writeheader()
            for d in data:
                data_writer.writerow(d)
        print("Export Github search finished")


if __name__ == "__main__":
    # Scraping Github TOP 20 Repo for each topic.
    topics = ["workflow-automation", "process-automation", "automation",
              "scraping", "crawling", "crawler", "scraping-websites"]
    # export_data(topics)
    # Not using full word
    # keywords = ["automation"]
    keywords = ["automation", "crawler", "scraping", "crawling", "spider"]
    export_data(keywords=keywords)

    # i = 1
    # url = build_url(page=i, search=keywords)
    # response = requests.get(url)
    # print(response.apparent_encoding)
