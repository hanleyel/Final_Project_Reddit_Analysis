# To Do:

# scrape fox comments

# file w/ reddit comment text?
# file w/ fox comment/article text?

# count frequencies of words in each
# get post times?

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


FILE_NAME = 'harry_text.txt'
subreddit = 'The_Donald'
fox_url = 'http://www.foxnews.com/politics.html'
db_name = 'text.db'
comment_limit = 10

#############################
##### IMPLEMENT CACHING #####
#############################

## 1 need to figure out how baseurl should be represented (e.g., comment id? subreddit name?)

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


# pdf_reader = PyPDF2.PdfFileReader(open('complete_harry_potter.pdf', 'rb'))

# #import text from PDF into txt file
# fhand = open('harry_text.txt', 'w')
#
# for page_number in range(pdf_reader.numPages):
#     page_obj = pdf_reader.getPage(page_number)
#     fhand.write(page_obj.extractText())
#
# fhand.close()

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


        # comment_attr_lst = ['archived', 'author', 'block', 'body', 'collapse', 'collapsed', 'controversiality',
        #                     'created', 'delete', 'depth', 'distinguished', 'downs', 'downvote', 'edit', 'edited',
        #                     'fullname', 'gild', 'gilded', 'id', 'likes', 'mod', 'name', 'parent', 'parse', 'permalink',
        #                     'refresh', 'replies', 'reply', 'report', 'save', 'saved', 'score', 'stickied', 'submission',
        #                     'subreddit', 'uncollapse', 'unsave', 'ups', 'upvote']

        if not submission.stickied: # skips stickied posts

            submission_dict['archived'] = str(submission.archived)
            submission_dict['author'] = str(submission.author)
            # reddit_dict['block'] = comment.block
            # submission_dict['body'] = submission.body
            # reddit_dict['collapse'] = comment.collapse
            # reddit_dict['collapsed'] = comment.collapsed
            # submission_dict['controversiality'] = submission.controversiality
            # submission_dict['created'] = submission.created
            # reddit_dict['delete'] = comment.delete
            # submission_dict['depth'] = submission.depth
            submission_dict['distinguished'] = str(submission.distinguished)
            # submission_dict['downs'] = submission.downs
            # reddit_dict['downvote'] = comment.downvote
            # reddit_dict['edit'] = comment.edit
            submission_dict['edited'] = str(submission.edited)
            # submission_dict['flair'] = submission.flair
            submission_dict['fullname'] = str(submission.fullname)
            submission_dict['gild'] = str(submission.gilded)
            submission_dict['id'] = str(submission.id)
            submission_dict['likes'] = str(submission.likes)
            reddit_dict['media'] = str(submission.media)
            # reddit_dict['mod'] = comment.mod
            submission_dict['name'] = str(submission.name)
            # reddit_dict['parent'] = comment.parent
            # reddit_dict['parse'] = comment.parse
            submission_dict['permalink'] = str(submission.permalink)
            # reddit_dict['refresh'] = comment.refresh
            # reddit_dict['replies'] = comment.replies
            # reddit_dict['reply'] = comment.reply
            # reddit_dict['report'] = comment.report
            submission_dict['save'] = str(submission.saved)
            submission_dict['selftext'] = str(submission.selftext)
            submission_dict['score'] = str(submission.score)
            submission_dict['stickied'] = str(submission.stickied)
            # submission_dict['submission'] = submission.submission
            submission_dict['subreddit'] = str(submission.subreddit)
            # reddit_dict['uncollapse'] = comment.uncollapse
            # reddit_dict['unsave'] = comment.unsave
            submission_dict['title'] = str(submission.title)
            submission_dict['ups'] = str(submission.ups)
            # reddit_dict['upvote'] = comment.upvote

            reddit_dict['submission'].append(submission_dict)

            # print(submission)

            # for ele in dir(submission):
            #     if '_' not in ele:
            #         print(ele)

            #         attr_lst.append(ele)
                    # print(getattr(submission, 'body'))
            #print(submission.title)
            # print('Title: {}, ups: {}, downs: {}, Have we visited: {}'.format(submission.title,
            #                                                                   submission.ups,
            #                                                                   submission.downs,
            #                                                                   submission.visited))
            submission.comments.replace_more(limit=0)


            for comment in submission.comments.list():

                comment_dict = {}

                ##### ATTRIBUTES TO CACHE #####

                comment_id = comment.id

                comment_dict['archived'] = str(comment.archived)
                comment_dict['author'] = str(comment.author)
                # reddit_dict['block'] = comment.block
                comment_dict['body'] = str(comment.body)
                # reddit_dict['collapse'] = comment.collapse
                # reddit_dict['collapsed'] = comment.collapsed
                comment_dict['controversiality'] = str(comment.controversiality)
                comment_dict['created'] = str(datetime.datetime.fromtimestamp(comment.created).strftime('%Y-%m-%d %H:%M:%S'))
                # reddit_dict['delete'] = comment.delete
                comment_dict['depth'] = str(comment.depth)
                comment_dict['distinguished'] = str(comment.distinguished)
                comment_dict['downs'] = str(comment.downs)
                # reddit_dict['downvote'] = comment.downvote
                # reddit_dict['edit'] = comment.edit
                comment_dict['edited'] = str(comment.edited)
                comment_dict['fullname'] = str(comment.fullname)
                comment_dict['gild'] = str(comment.gilded)
                comment_dict['id'] = str(comment.id)
                comment_dict['likes'] = str(comment.likes)
                # reddit_dict['mod'] = comment.mod
                comment_dict['name'] = str(comment.name)
                # reddit_dict['parent'] = comment.parent
                # reddit_dict['parse'] = comment.parse
                comment_dict['permalink'] = str(comment.permalink)
                # reddit_dict['refresh'] = comment.refresh
                # reddit_dict['replies'] = comment.replies
                # reddit_dict['reply'] = comment.reply
                # reddit_dict['report'] = comment.report
                comment_dict['save'] = str(comment.saved)
                comment_dict['score'] = str(comment.score)
                comment_dict['stickied'] = str(comment.stickied)
                comment_dict['submission'] = str(comment.submission)
                comment_dict['submission_id'] = str(submission.id)
                comment_dict['subreddit'] = str(comment.subreddit)
                # reddit_dict['uncollapse'] = comment.uncollapse
                # reddit_dict['unsave'] = comment.unsave
                comment_dict['ups'] = str(comment.ups)
                # reddit_dict['upvote'] = comment.upvote

                reddit_dict['comment'].append(comment_dict)


                # for ele in attr_lst:
                #     try:
                #         print(getattr(comment, ele)())
                #     except:
                #         pass
                # print(20*'-')
                # print('Parent ID', comment.parent())
                # print('Comment ID', comment.id)
                # print(comment.body)
                # comment_str += comment.body
                # fhand.write(comment.body)
                # print(comment.body)
            # print(reddit_dict)
    fhand.close()

    return reddit_dict

    # return submission.comments.list()

###################################
#####     SCRAPE FOX NEWS     #####
###################################

def scrape_fox_news():
    # Would be interesting to get comments as well

    fox_dict = {'webpage': [],
                fox_url: []}  ##### FOX URL IS FOR CLASS CHECKPOINT PURPOSES TO PROVE I CAN GRAB THE RAW DATA
    link_lst = []  # category links on front page
    article_lst = []  # individual articles to scrape

    response = requests.get('http://www.foxnews.com/')
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    # print(soup)

    # print(soup)

    ##### GET NEWS STORIES #####

    inner_class = soup.findAll('div', class_='inner')
    for ele in inner_class:
        li_class = ele.findAll('li', class_='nav-item')
        for li in li_class:
            link = li.find('a')['href']
            if 'category' in link:
                link_lst.append(link[2:])

    for ele in link_lst:
        # print(ele)

        soup_dict = {}

        response = requests.get('http://' + ele)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        # print(soup)
        #
        #     fox_dict[fox_url] = str(soup) ##### THIS IS FOR CLASS CHECKPOINT PURPOSES TO PROVE I CAN GRAB THE RAW DATA
        #
        ##### FIND ARTICLES #####
        article_class = soup.findAll('article', class_=re.compile('story-*'))
        # print(article_class)
        for item in article_class:
            try:
                link = item.find('a')['href']
                if link[1:9] != 'category' and 'video' not in link:
                    # print(link)
                    # print(link)
                    # if link[0] == '/':
                    #    print(link)
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

    # # Would be interesting to get comments as well
    #
    # fox_dict = {'webpage': [], fox_url:[]} ##### FOX URL IS FOR CLASS CHECKPOINT PURPOSES TO PROVE I CAN GRAB THE RAW DATA
    # link_lst = []
    #
    # response = requests.get('http://www.foxnews.com/politics.html')
    # data = response.text
    # soup = BeautifulSoup(data, 'html.parser')
    #
    # # print(soup)
    #
    # ##### GET TRENDING NEWS STORIES     #####
    #
    # trending_class = soup.findAll('section', class_='collection collection-trending')
    # # print(trending_class)
    #
    # for ele in trending_class:
    #     a_tag = ele.select('a')
    #     # print(a_tag)
    #     for a in a_tag:
    #         # print(a)
    #         link = a['href']
    #         if link not in link_lst:
    #             link_lst.append(link)
    # # print(link_lst)
    #
    # for ele in link_lst:
    #
    #     soup_dict = {}
    #
    #     response = requests.get(ele)
    #     data = response.text
    #     soup = BeautifulSoup(data, 'html.parser')
    #
    #     fox_dict[fox_url] = str(soup) ##### THIS IS FOR CLASS CHECKPOINT PURPOES TO PROVE I CAN GRAB THE RAW DATA
    #
    #     ##### FIND TITLE #####
    #     title = soup.find('title').text
    #     # print(title)
    #
    #     ##### FIND AUTHOR #####
    #     author_class = soup.find('div', class_='author-byline')
    #     # print(author_class)
    #     author_span = author_class.find('span')
    #     author = author_span.find('a').text.strip()
    #
    #     ##### FIND BODY #####
    #     body = ''
    #     body_class = soup.find('div', class_='article-body')
    #     p_tags = body_class.findAll('p')
    #     for tag in p_tags:
    #         body += tag.text
    #     # print(body)
    #
    #     soup_dict['title'] = str(title)
    #     soup_dict['author'] = str(author)
    #     soup_dict['body'] = str(body)
    #
    #
    #
    #     fox_dict['webpage'].append(soup_dict)
    #
    #
    #
    # return fox_dict

#def get_text_from_file():
    fhand = open(FILE_NAME, 'r')
    comment_str = fhand.read()
    fhand.close()
    return comment_str

# A variety of options for getting text data:
# comment_str = get_reddit_info().strip()


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

    ############################################
    #####     DROP PRE-EXISTING TABLES     #####
    ############################################

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

    #################################
    #####     CREATE TABLES     #####
    #################################

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

    #############################################
    #####     POPULATE TABLES WITH DATA     #####
    #############################################

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




#################################
#####     CHATBOT STUFF     #####
#################################

def create_dictionaries (test_str, two_dict = {}, one_dict = {}):

    test_str = test_str.split()

    count1 = 0
    count2 = 1
    count3 = 2

    while count3 < len(test_str):
        two_key = (test_str[count1], test_str[count2])
        one_key = test_str[count1]
        if two_key in two_dict:
            two_dict[two_key].append(test_str[count3])
        else:
            two_dict[two_key] = [test_str[count3]]
        if one_key in one_dict:
            one_dict[one_key].append(test_str[count2])
        else:
            one_dict[one_key] = [test_str[count2]]
        count1 += 1
        count2 += 1
        count3 += 1

    return (two_dict, one_dict)

# print(two_dict)
# print(one_dict)

# print(two_dict)
# print(one_dict)

def get_first_word():
    first_word = 'word'
    while first_word[0].istitle() == False:
        first_word = random.choice(list(one_dict.keys()))
    return first_word

def create_sentence(count, two_dict, one_dict, first_word):
    sentence = first_word.capitalize()

    second_word = random.choice(one_dict[first_word])
    sentence += ' ' + second_word

    count1 = 0
    count2 = 1

    fhand = open('output_file', 'w')

    while len(sentence.split()) < count:
    # while sentence[-1] != '.':

        current_key = (sentence.split()[count1], sentence.split()[count2])
        # print(current_key)

        if current_key in two_dict:
            next_word = random.choice(two_dict[current_key])
            sentence += ' ' + next_word
            if next_word[-1]=='.':
                count = count
            # print('two',next_word)
            # print(next_word)
        # elif current_key[1] in one_dict:
        else:
            next_word = random.choice(one_dict[current_key[1]])
            sentence += ' ' + next_word
            if next_word[-1]=='.':
                count = count
            # print(next_word)
            # print('key',current_key[0])
            # print('one',next_word)
        if sentence[-1]=='.':
            sentence += '\n'

        count1 += 1
        count2 += 1

    # sentence = sentence.replace('.', '\n')

    fhand.write(sentence)
    fhand.close

    return sentence

if __name__ == "__main__":

    populate_database(db_name)

    # scrape_fox_news()
    # fox_results = make_fox_request_using_cache(fox_url)
    # reddit_results = make_reddit_request_using_cache(subreddit)

    create_db(db_name)




    # get_reddit_info(2)

    # response = get_reddit_info(3, subreddit)

    # for ele in response['comment']:
    #     print("comment", ele)
    # for ele in response['submission']:
    #     print("submission", ele)

    # comment_str = get_text_from_file()
    # two_dict = create_dictionaries(comment_str)[0]
    # one_dict = create_dictionaries(comment_str)[1]
    # first_word = get_first_word()
    # print(create_sentence(500, two_dict, one_dict, first_word))