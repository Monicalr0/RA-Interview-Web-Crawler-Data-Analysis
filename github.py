from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv


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


def export_data(topics=[]):
    data = []
    for t in topics:
        data.extend(scrape(t))
    filename = "github.csv"
    with open(filename, "w", newline="") as data_file:
        fieldnames = ["Title", "Description", "Topic"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    print("Export Github finished")


if __name__ == "__main__":
    # Scraping Github TOP 20 Repo for each topic.
    topics = ["workflow-automation", "process-automation", "automation",
              "scraping", "crawling", "crawler", "scraping-websites"]
    export_data(topics)
