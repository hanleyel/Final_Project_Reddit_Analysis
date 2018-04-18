# To Do:
# scrape fox comments
# file w/ reddit comment text?
# file w/ fox comment/article text?
# count frequencies of words in each
# input frequencies/post times to SQL
# test cases


import praw
import random
import json
import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re
from nltk.corpus import stopwords
import datetime


# FILE_NAME = 'harry_text.txt'
subreddit = 'The_Donald'
fox_url = 'http://www.foxnews.com/politics.html'
db_name = 'text.db'
comment_limit = 10


#############################
##### IMPLEMENT CACHING #####
#############################

# Ok... I know it's not efficient to essentially repeat this function twice and I'll fix it if I have time

def make_fox_request_using_cache(baseurl): ## 1

    unique_ident = baseurl

    CACHE_FNAME = 'cache.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    except:
        CACHE_DICTION = {}

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        response = scrape_fox_news()
        response = json.dumps(response)
        loaded_response = json.loads(response)
        # print(type(loaded_response))
        CACHE_DICTION[unique_ident] = loaded_response
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def make_reddit_request_using_cache(baseurl):  ## 1

    unique_ident = baseurl

    CACHE_FNAME = 'cache.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    except:
        CACHE_DICTION = {}

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        response = get_reddit_info(comment_limit, subreddit)
        response = json.dumps(response)
        loaded_response = json.loads(response)
        # print(type(loaded_response))
        CACHE_DICTION[unique_ident] = loaded_response
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()  # Close the open file
        return CACHE_DICTION[unique_ident]


####################################
##### Create a Reddit instance #####
####################################

def get_reddit_info(limit, subreddit):

    reddit_dict = {'comment': [], 'submission': []}

    reddit = praw.Reddit(client_id='pjgL2F9jwdUDGg',
                         client_secret='88YOfEa8lWM6dv5PsgUg_Al32To',
                         username='HexMouse',
                         password='LePetitPrince',
                         user_agent='HexChat')

    subreddit = reddit.subreddit(subreddit)

    hot_python = subreddit.hot(limit=limit) # Gets hot posts
    # print(hot_python)

    # comment_str = ''

    fhand = open('trump_text.txt', 'w')

    for submission in hot_python:

        submission_dict = {}

        if not submission.stickied: # skips stickied posts

            submission_dict['archived'] = str(submission.archived)
            submission_dict['author'] = str(submission.author)
            submission_dict['distinguished'] = str(submission.distinguished)
            submission_dict['edited'] = str(submission.edited)
            submission_dict['fullname'] = str(submission.fullname)
            submission_dict['gild'] = str(submission.gilded)
            submission_dict['id'] = str(submission.id)
            submission_dict['likes'] = str(submission.likes)
            reddit_dict['media'] = str(submission.media)
            submission_dict['name'] = str(submission.name)
            submission_dict['permalink'] = str(submission.permalink)
            submission_dict['save'] = str(submission.saved)
            submission_dict['selftext'] = str(submission.selftext)
            submission_dict['score'] = str(submission.score)
            submission_dict['stickied'] = str(submission.stickied)
            submission_dict['subreddit'] = str(submission.subreddit)
            submission_dict['title'] = str(submission.title)
            submission_dict['ups'] = str(submission.ups)
            reddit_dict['submission'].append(submission_dict)

            submission.comments.replace_more(limit=0)

            for comment in submission.comments.list():

                comment_dict = {}

                ##### ATTRIBUTES TO CACHE #####

                comment_id = comment.id

                comment_dict['archived'] = str(comment.archived)
                comment_dict['author'] = str(comment.author)
                comment_dict['body'] = str(comment.body)
                comment_dict['controversiality'] = str(comment.controversiality)
                comment_dict['created'] = str(datetime.datetime.fromtimestamp(comment.created).strftime('%Y-%m-%d %H:%M:%S'))
                comment_dict['depth'] = str(comment.depth)
                comment_dict['distinguished'] = str(comment.distinguished)
                comment_dict['downs'] = str(comment.downs)
                comment_dict['edited'] = str(comment.edited)
                comment_dict['fullname'] = str(comment.fullname)
                comment_dict['gild'] = str(comment.gilded)
                comment_dict['id'] = str(comment.id)
                comment_dict['likes'] = str(comment.likes)
                comment_dict['name'] = str(comment.name)
                comment_dict['permalink'] = str(comment.permalink)
                comment_dict['save'] = str(comment.saved)
                comment_dict['score'] = str(comment.score)
                comment_dict['stickied'] = str(comment.stickied)
                comment_dict['submission'] = str(comment.submission)
                comment_dict['submission_id'] = str(submission.id)
                comment_dict['subreddit'] = str(comment.subreddit)
                comment_dict['ups'] = str(comment.ups)

                reddit_dict['comment'].append(comment_dict)

    fhand.close()

    return reddit_dict


###################################
#####     SCRAPE FOX NEWS     #####
###################################

def scrape_fox_news():
    # Would be interesting to get comments as well

    fox_dict = {'webpage': [],
                fox_url: []}  ##### This is for class checkpoint purposes; grabbing raw data
    link_lst = []  # category links on front page
    article_lst = []  # individual articles to scrape

    response = requests.get('http://www.foxnews.com/')
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    ##### GET NEWS STORIES #####

    inner_class = soup.findAll('div', class_='inner')
    for ele in inner_class:
        li_class = ele.findAll('li', class_='nav-item')
        for li in li_class:
            link = li.find('a')['href']
            if 'category' in link:
                link_lst.append(link[2:])

    for ele in link_lst:

        soup_dict = {}

        response = requests.get('http://' + ele)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')

        ##### FIND ARTICLES #####
        article_class = soup.findAll('article', class_=re.compile('story-*'))
        for item in article_class:
            try:
                link = item.find('a')['href']
                if link[1:9] != 'category' and 'video' not in link:
                    article_lst.append('http://foxnews.com' + link)
            except:
                pass
    print(article_lst)
    print('Article list length: ', len(article_lst))

    ##### FIND TITLE #####

    for article in article_lst[0:5]:
        response = requests.get(article)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')

        title = soup.find('h1', class_='headline').text
        print(title)

        ##### FIND CATEGORY #####
        category_class = soup.find('div', class_='eyebrow')
        category = category_class.find('a').text
        print(category)

        ##### FIND AUTHOR #####
        author_class = soup.find('div', class_='author-byline')
        # print(author_class)
        # print(author_class)
        author_span = author_class.find('span')
        author = author_span.find('a').text.strip()
        # print(author)

        ##### FIND BODY #####
        body = ''
        body_class = soup.find('div', class_='article-body')
        p_tags = body_class.findAll('p')
        for tag in p_tags:
            body += tag.text
        body = body.strip()
        # print(body)

        ##### FIND PUBLISHED TIME #####
        time_tag = soup.findAll('time')
        time_tag = str(time_tag)
        pub_time = time_tag[28:53]

        time.sleep(5)

        soup_dict['title'] = str(title)
        soup_dict['category'] = str(category)
        soup_dict['author'] = str(author)
        soup_dict['body'] = str(body)
        soup_dict['time'] = str(pub_time)

        fox_dict['webpage'].append(soup_dict)

        time.sleep(5)

    return fox_dict

# def get_text_from_file():
#     fhand = open(FILE_NAME, 'r')
#     comment_str = fhand.read()
#     fhand.close()
#     return comment_str


####################################
#####     CREATE DATABASES     #####
####################################

def create_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        print(sqlite3.version)
    except 'Error' as e:
        print(e)

def populate_database(db_name):

    ##### DROP PRE-EXISTING TABLES #####

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'RedditSubmissionWords';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'RedditSubmissions';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'RedditCommentWords';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'RedditComments';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'FoxArticleWords';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'FoxArticles';
    '''
    cur.execute(statement)

    ##### CREATE TABLES #####

    statement = '''
    CREATE TABLE RedditSubmissionWords(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Word' TEXT,
    'Count' INTEGER,
    'Frequency' REAL
    )'''

    cur.execute(statement)

    statement = '''
    CREATE TABLE RedditSubmissions(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'SubmissionUniqueId' TEXT,
    'Archived' TEXT,
    'Author' TEXT,
    'Distinguished' TEXT,
    'Edited' TEXT,
    'Fullname' TEXT,
    'Gild' INTEGER,
    'Likes' INTEGER,
    'Name' TEXT,
    'Permalink' TEXT,
    'Save' TEXT,
    'Selftext' INTEGER,
    'Score' INTEGER,
    'Stickied' TEXT,
    'Subreddit' TEXT,
    'Title' TEXT,
    'Ups' INTEGER
    )'''

    cur.execute(statement)

    statement = '''
    CREATE TABLE RedditCommentWords(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Word' TEXT,
    'Count' INTEGER,
    'Frequency' REAL
    )'''

    cur.execute(statement)

    statement = '''
    CREATE TABLE RedditComments(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'CommentUniqueId' TEXT,
    'SubmissionId' TEXT,
    'Archived' TEXT,
    'Author' TEXT,
    'Body' TEXT,
    'Controversiality' TEXT,
    'Created' REAL,
    'Depth' INTEGER,
    'Distinguished' TEXT,
    'Downs' INTEGER,
    'Edited' TEXT,
    'Fullname' TEXT,
    'Gild' INTEGER,
    'Likes' INTEGER,
    'Name' TEXT,
    'Permalink' TEXT,
    'Save' TEXT,
    'Score' INTEGER,
    'Stickied' TEXT,
    'Submission' TEXT,
    'Subreddit' TEXT,
    'Ups' INTEGER
    )'''

    cur.execute(statement)

    statement = '''
    CREATE TABLE FoxArticleWords(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Word' TEXT,
    'Count' INTEGER,
    'Frequency' REAL
    )
    '''

    cur.execute(statement)

    statement = '''
    CREATE TABLE FoxArticles(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Title' TEXT,
    'CategorY' TEXT,
    'Author' TEXT,
    'Body' TEXT,
    'Time' TEXT
    )
    '''

    cur.execute(statement)

    ##### POPULATE TABLES WITH DATA #####

    ##### REDDIT SUBMISSION WORDS DATA #####

    reddit_submission_data = make_reddit_request_using_cache(subreddit)

    # print(reddit_submission_data['submission'][0].keys())

    reddit_submission_dict = {}
    reddit_submission_freq_dict = {}
    reddit_submission_vocab = 0
    for ele in reddit_submission_data['submission']:
        # print("Submission: ", ele)
        pass

    ##### REDDIT SUBMISSION DATA #####

    for ele in list(reddit_submission_data['submission']):

        reddit_comment_params = [None, ele['id'], ele['archived'], ele['author'], ele['distinguished'], ele['edited'], ele['fullname'],
                                 ele['gild'], ele['likes'], ele['name'], ele['permalink'], ele['save'], ele['selftext'], ele['score'],
                                 ele['stickied'], ele['subreddit'], ele['title'], ele['ups']]

        insert_statement = 'INSERT INTO "RedditSubmissions"'
        insert_statement += 'Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        cur.execute(insert_statement, reddit_comment_params)

    ##### REDDIT COMMENT WORDS DATA #####

    reddit_comment_data = make_reddit_request_using_cache(subreddit)
    reddit_comment_dict = {}
    reddit_comment_freq_dict = {}
    reddit_comment_vocab = 0
    for ele in reddit_comment_data['comment']:
        # print("Comment", ele)
        words = ele['body'].split()
        for word in words:
            if word not in stopwords.words('english'): ##### FILTER OUT FILLER WORDS #####
                if word not in reddit_comment_dict:
                    reddit_comment_dict[word] = 1
                else:
                    reddit_comment_dict[word] += 1
                    reddit_comment_vocab += 1 # Increment the vocab

    for word in list(reddit_comment_dict.keys()):
        reddit_comment_freq_dict[word] = reddit_comment_dict[word]/reddit_comment_vocab

    # print(reddit_comment_dict)
    # print(reddit_comment_freq_dict)
    # print(reddit_comment_vocab)

    # print(reddit_comment_data['comment'][0].keys())

    for ele in list(reddit_comment_dict.keys()):

        reddit_comment_params = [None, ele, reddit_comment_dict[ele], reddit_comment_freq_dict[ele]]

        insert_statement = 'INSERT INTO "RedditCommentWords"'
        insert_statement += 'Values (?, ?, ?, ?)'

        cur.execute(insert_statement, reddit_comment_params)

    ##### REDDIT COMMENTS DATA #####

    for ele in list(reddit_comment_data['comment']):

        reddit_comment_params = [None, ele['id'], ele['submission_id'], ele['archived'], ele['author'], ele['body'], ele['controversiality'], ele['created'],
                                 ele['depth'], ele['distinguished'], ele['downs'], ele['edited'], ele['fullname'],
                                 ele['gild'], ele['likes'], ele['name'], ele['permalink'], ele['save'], ele['score'],
                                 ele['stickied'], ele['submission'], ele['subreddit'], ele['ups']]

        insert_statement = 'INSERT INTO "RedditComments"'
        insert_statement += 'Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        cur.execute(insert_statement, reddit_comment_params)

    ##### FOX ARTICLES DATA #####

    fox_submission_data = make_fox_request_using_cache(fox_url)

    print(fox_submission_data)

    for ele in list(fox_submission_data['webpage']):

        fox_article_params = [None, ele['title'], ele['category'], ele['author'], ele['body'], ele['time']]

        insert_statement = 'INSERT INTO "FoxArticles"'
        insert_statement += 'Values (?, ?, ?, ?, ?, ?)'

        cur.execute(insert_statement, fox_article_params)


    ##### FOX ARTICLE WORDS DATA #####

    print(fox_submission_data['webpage'][0].keys())

    fox_submission_dict = {}
    fox_submission_freq_dict = {}
    fox_submission_vocab = 0
    for ele in list(fox_submission_data['webpage']):
        # print("Article: ", ele)
        words = ele['body'].split()
        for word in words:
            if word not in stopwords.words('english'): ##### FILTER OUT FILLER WORDS #####
                if word not in fox_submission_dict:
                    fox_submission_dict[word] = 1
                else:
                    fox_submission_dict[word] += 1
                    fox_submission_vocab += 1  # Increment the vocab

    for word in list(fox_submission_dict.keys()):
        fox_submission_freq_dict[word] = fox_submission_dict[word]/fox_submission_vocab

    print(fox_submission_dict)
    print(fox_submission_freq_dict)
    print(fox_submission_vocab)

    for ele in list(fox_submission_dict.keys()):

        fox_submission_params = [None, ele, fox_submission_dict[ele], fox_submission_freq_dict[ele]]

        insert_statement = 'INSERT INTO "FoxArticleWords"'
        insert_statement += 'Values (?, ?, ?, ?)'

        cur.execute(insert_statement, fox_submission_params)

    conn.commit()
    conn.close()