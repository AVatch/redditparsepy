import urllib2
import csv
import sys
from bs4 import BeautifulSoup

# stupid encoding check
reload(sys)
sys.setdefaultencoding('utf-8')

# Define source and container
data = []
n = 1000
url = 'https://www.reddit.com/r/AskReddit/comments/3pwjuz/who_can_you_not_believe_is_still_alive/?limit=' + str(n)

# Get data
req = urllib2.Request(url)
res = urllib2.urlopen(req)

# Parse content
soup = BeautifulSoup(res.read(), 'html.parser')
commentarea = soup.find('div', class_='commentarea')
listings = commentarea.find('div', class_='sitetable nestedlisting')
# only look at the top level comments
comments = listings.find_all('div', class_='comment', recursive=False)


for comment in comments:
    thing = {}

    # Get comment meta data
    tagline = comment.find('p', class_='tagline')
    author = tagline.find('a', class_='author')
    
    thing['author'] = author.string if author is not None else ''

    score = tagline.find_all('span', class_='score')
    if not score:
        continue
    thing['dislikes'] = score[0].string.replace('points', '').replace('point', '').strip() if score[0] is not None else ''
    thing['unvoted'] = score[1].string.replace('points', '').replace('point', '').strip() if score[1] is not None else ''
    thing['likes'] = score[2].string.replace('points', '').replace('point', '').strip() if score[2] is not None else ''
    
    time = tagline.find('time')
    thing['time'] = time.attrs['datetime'] if time is not None else ''

    # Get comment content
    content = comment.find('form').find('p')
    if not content.string:
        continue
    thing['content'] = content.string if content is not None else ''

    data.append(thing)

with open('reddit_comments.csv', 'wb') as csvfile:
    ideawriter = csv.writer(csvfile, delimiter=',')
    ideawriter.writerow(['author', 'dislikes', 'unvoted', 'likes', 'time', 'content'])
    for point in data:
        ideawriter.writerow([point['author'], point['dislikes'], point['unvoted'], point['likes'],
                             point['time'], point['content']])