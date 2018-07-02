# CSPC Recalls Bot

# Syntax for secret.txt
# Line 1: Reddit Client ID
# Line 2: Reddit Client Secret
# Line 3: Reddit Username
# Line 4: Reddit Password

import praw, feedparser

feed = feedparser.parse("https://www.cpsc.gov/Newsroom/CPSC-RSS-Feed/Recalls-RSS")



secretFile = open("secret.txt").read().split("\n")

reddit = praw.Reddit(user_agent='CSPCRecallsBot', client_id=secretFile[0], client_secret=secretFile[1], username=secretFile[2], password=secretFile[3])
subreddit = reddit.subreddit('CPSCRecalls')

