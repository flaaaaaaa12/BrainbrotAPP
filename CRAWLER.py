import praw
import json
import unicodedata

def cleanupstring(string):
    words={
        "AITA for " : "Am I the asshole for ",
        "AITAH for " : "Am I the asshole for ",
        "AITA" : "Am I the asshole ",
        "AITAH" : "Am I the asshole ",   
        "." : ". ",
        " H ": " ",
        " - " : " ",
        "\u2019" : "'"
    }
    string = "".join(c for c in string if c.isprintable())
    string = unicodedata.normalize("NFKC", string)
    for word,replace in words.items() :
        if word.lower() in string.lower() :
            string = string.replace(word,replace)
    return string

class CRAWLER:
    def __init__(self,savefile="media/posts.json"):
        self.reddit = praw.Reddit(
            client_id="8ds4wDv4AlrUakzKXhzFGQ",
            client_secret="7aP3HtDGu4vTnXvcNzAMMbnXhUlWhw",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
        )
        self.savefile=savefile
   
    def appendposts(self,subreddit,postamount):
        subreddit = self.reddit.subreddit(subreddit)
        posts = []
        with open(self.savefile, "r", encoding="utf-8") as file:
            posts=json.load(file)
        for submission in subreddit.hot(limit=postamount):  # "hot", "new", "top" sont des options
            posts.append({
                "title": cleanupstring(submission.title),
                "content": cleanupstring(submission.selftext),
                "url": submission.url, 
                "posted": False,
                "postcount":0
            })
        with open(self.savefile, "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4, ensure_ascii=False)