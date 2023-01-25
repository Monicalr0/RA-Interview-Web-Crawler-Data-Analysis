from bs4 import BeautifulSoup
import csv
import requests

# Current implementations are using manually inspectation for maximum page number & link
# because the corresponding topics number is not sure.
# TODO: update to automatically get data if needed
# TODO: clean up function, now using simple for loop


def scrape():
    """
    Function to scrape UiPath with manually inspected url and page limit.
    """
    data = []
    for i in range(0, 9):
        url = "https://forum.uipath.com/c/build/it-automation/111.json?page=" + \
            str(i)
        response = requests.get(url)
        response = response.json()

        for t in response["topic_list"]["topics"]:
            post = {}
            post["Title"] = t["title"]
            post["PostCount"] = t["posts_count"]
            post["ReplyCount"] = t["reply_count"]
            post["Excerpt"] = t["excerpt"]
            post["tag"] = "it-automation"
            data.append(post)

    for i in range(0, 2):
        url = "https://forum.uipath.com/c/build/automation-suite/222.json?page=" + \
            str(i)
        response = requests.get(url)
        response = response.json()

        for t in response["topic_list"]["topics"]:
            post = {}
            post["Title"] = t["title"]
            post["PostCount"] = t["posts_count"]
            post["ReplyCount"] = t["reply_count"]
            post["Excerpt"] = t["excerpt"]
            post["tag"] = "automation-suite"
            data.append(post)
    return data


def export_data():
    data = scrape()
    filename = "UiPath.csv"
    with open(filename, "w", newline="") as data_file:
        fieldnames = ["Title",
                      "PostCount", "ReplyCount", "Excerpt", "tag"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    print("Export UiPath finished")


if __name__ == "__main__":
    export_data()
