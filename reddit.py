import praw
import config
import csv
# This file is created referenced to this article
# https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

# Limit for number of questions to be scraped in each subreddit.
LIMIT = 300  # Reddit rate limit is around 2 sec/posts


def scrape(subreddit=""):
    """
    Function to scrape to LIMIT, sorted by hottest question. 
    """
    # Create a read-only reddit instance to access data.
    # TOKEN is saved in seperate file, need to ask for file
    # or create your own application on reddit to get TOKEN.
    reddit = praw.Reddit(client_id=config.CLIENT_ID_TOKEN,
                         client_secret=config.SECRET, user_agent=config.REDDIT_NAME)

    subreddit = subreddit
    hot_posts = reddit.subreddit(subreddit).hot(limit=LIMIT)

    posts = []
    for p in hot_posts:
        post = {}
        post['Title'] = p.title
        post['URL'] = p.url
        post['Subreddit'] = p.subreddit
        post['Body'] = p.selftext
        posts.append(post)

    # Scraping comments for each questions.
    # Only Scraping Top-Level Comment for now as we just want to focus on post content
    # instead of follow up discussion
    for po in posts:
        # To handle unexpected URL
        try:
            submission = reddit.submission(url=po['URL'])
            # Remove "View More Comments" to prevemt execepton
            submission.comments.replace_more(limit=0)
            comments = []
            for comment in submission.comments:
                comments.append(comment.body)
            po["Comments"] = comments
        except:
            print("error" + str(IOError))
            pass

    return posts


def export_data_seperate(subreddit="all"):
    """
    Function to export scraped data.
    If not specify subreddit, export hottest post from all subreddits
    """
    data = scrape(subreddit)
    filename = subreddit + ".csv"
    with open(filename, "w", newline="") as data_file:
        fieldnames = ["Title", "URL", "Subreddit", "Body", "Comments"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    print("Export subreddit: " + subreddit + " finished")


def export_data_concat(subreddit=["all"]):
    """
    Function to export scraped data all in one table.
    If not specify subreddit array, export hottest post from all subreddits
    """
    data = []
    for sr in subreddits:
        data.extend(scrape(sr))

    filename = "AllRedditData" + ".csv"
    with open(filename, "w", newline="") as data_file:
        fieldnames = ["Title", "URL", "Subreddit", "Body", "Comments"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    print("Export all subreddits in one file finished")


if __name__ == "__main__":
    # Scraping reddit
    # Members of selected subreddits: 11.5k, 87.9k, 14.2k, 10.7k
    subreddits = ["webscraping", 'Automate', 'Automation', 'Selenium']
    export_data_concat(subreddits)
    # for sr in subreddits:
    #     export_data_seperate(sr)
