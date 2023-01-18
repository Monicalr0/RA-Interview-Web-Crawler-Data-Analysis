import praw
import config
# This file is created referenced to this article
# https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

LIMIT = 10

# Create a read-only reddit instance to access data.
# TOKEN is saved in seperate file, need to ask for file
# or create your own application on reddit to get TOKEN.
reddit = praw.Reddit(client_id=config.CLIENT_ID_TOKEN,
                     client_secret=config.SECRET, user_agent=config.REDDIT_NAME)

subreddit = 'webscraping'
hot_posts = reddit.subreddit(subreddit).hot(limit=LIMIT)
posts = []
for p in hot_posts:
    post = {}
    post['Title'] = p.title
    post['URL'] = p.url
    post['Subreddit'] = p.subreddit
    post['Body'] = p.selftext
    posts.append(post)

# Only Scraping Top-Level Comment for now as we just want to focus on post content
# instead of follow up discussion
for po in posts:
    submission = reddit.submission(url=po['URL'])
    submission.comments.replace_more(limit=0)
    comments = []
    for comment in submission.comments:
        comments.append(comment.body)
    po["Comments"] = comments

print(posts)


# if __name__ == "__main__":
#     # Scraping reddit
