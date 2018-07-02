# CSPC Recalls Bot

# Syntax for secret.txt
# Line 1: Reddit Client ID
# Line 2: Reddit Client Secret
# Line 3: Reddit Username
# Line 4: Reddit Password

import praw, feedparser, re
from datetime import timedelta, datetime

yesterdayTime = datetime.now() - timedelta(days=1)
feed = feedparser.parse("https://www.cpsc.gov/Newsroom/CPSC-RSS-Feed/Recalls-RSS")

# See if the first element is a new one
Break = False
index = 0
indexList = []
while (Break == False):
    eventDate = datetime.strptime(feed['entries'][index]['published'], "%B %d, %Y")
    if eventDate > yesterdayTime:
        indexList.append(index)
    else:
        Break = True
    index+=1

if len(indexList) == 0:
    logFile = open("logFile.txt", "a")
    logFile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t0")
    logFile.close()
    exit(0)

secretFile = open("secret.txt").read().split("\n")

reddit = praw.Reddit(user_agent='CSPCRecallsBot', client_id=secretFile[0], client_secret=secretFile[1], username=secretFile[2], password=secretFile[3])
subreddit = reddit.subreddit('CPSCRecalls')

logFile = open("logFile.txt", "a")

submissionsList = []

for index in indexList:
    # Check to see if it's already been submitted
    search = list(subreddit.search("url:"+feed['entries'][index]['link']))
    if len(search) == 0:
        subTitle = feed['entries'][index]['title']
        subTitle = re.sub(r'\([^)]*\)', '', subTitle).rstrip()
        submission = subreddit.submit(subTitle, url=feed['entries'][index]['link'])
        submission.reply("> " + str(feed['entries'][index]['summary']) + "\n\n^(This message was posted by a bot. [source](https://github.com/etnguyen03/CPSCRecallsBot/)")
        submissionsList.append(str(submission))

logFile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t" + len(submissionsList) + "\t" + str(submissionsList))
logFile.close()
