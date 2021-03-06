# CSPC Recalls Bot

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Syntax for secret.txt
# Line 1: Reddit Client ID
# Line 2: Reddit Client Secret
# Line 3: Reddit Username
# Line 4: Reddit Password

import praw, feedparser, re
from datetime import timedelta, datetime

yesterdayTime = datetime.now() - timedelta(days=5)
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
    logFile = open("/var/log/CPSCRecallsBot/CPSCRecallsBotLog.txt", "a")
    logFile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t0\n")
    logFile.close()
    exit(0)

secretFile = open("secret.txt").read().split("\n")

reddit = praw.Reddit(user_agent='CSPCRecallsBot', client_id=secretFile[0], client_secret=secretFile[1], username=secretFile[2], password=secretFile[3])
subreddit = reddit.subreddit('CPSCRecalls')

logFile = open("/var/log/CPSCRecallsBot/CPSCRecallsBotLog.txt", "a")

submissionsList = []

for index in indexList:
    # Check to see if it's already been submitted
    # searchFor = re.sub(".*[/]", "", feed['entries'][index]['link'])
    searchFor = "url:"+str(feed['entries'][index]['link'])
    search = list(subreddit.search(searchFor))
    if len(search) == 0:
        subTitle = feed['entries'][index]['title']
        subTitle = re.sub(r'\([^)]*\)', '', subTitle).rstrip()
        submission = subreddit.submit(subTitle, url=feed['entries'][index]['link'])
        submission.reply("> " + str(feed['entries'][index]['summary']) + "\n\n^(This message was posted by a bot. [source](https://github.com/etnguyen03/CPSCRecallsBot/))")
        submissionsList.append(str(submission))

logFile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t" + str(len(submissionsList)) + "\t" + str(submissionsList) + "\n")
logFile.close()
