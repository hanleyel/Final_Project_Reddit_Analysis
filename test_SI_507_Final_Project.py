import unittest
from SI_507_Final_Project import *

class TestDatabase(unittest.TestCase):

    def test_fox_articles_table(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        select_statement = '''
        SELECT COUNT(*), Author
        FROM FoxArticles
        '''

        results = cur.execute(select_statement)
        result = results.fetchall()
        self.assertGreaterEqual(int(result[0][0]), 100) # Checking that there are more than 100 entries in the table
        self.assertIs(type(result[0][1]), str) # Checking that authors are input as strings

        conn.close()

    def test_reddit_submissions_table(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        select_statement = '''
        SELECT Author, Subreddit
        FROM RedditSubmissions
        '''

        results = cur.execute(select_statement)
        result = results.fetchall()
        self.assertIs(type(result[0][0]), str) # Checking that authors are input as strings
        self.assertEqual(result[0][1], subreddit) # Checking that it's drawing from the correct subreddit

        conn.close()

    def test_reddit_comments_table(self):

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        select_statement = '''
        SELECT Count(*), Author
        FROM RedditComments
        '''

        results = cur.execute(select_statement)
        result = results.fetchall()
        self.assertGreaterEqual(int(result[0][0]), 100) # Checking that there are more than 100 entries in the table
        self.assertIs(type(result[0][1]), str)

        conn.close()

    def test_associative_table(self):

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        select_statement = '''
        SELECT DayHour
        FROM FoxRedditDetails
        '''

        results = cur.execute(select_statement)
        result = results.fetchall()
        self.assertIs(type(result[0][0]), str)

        conn.close()

class TestClasses(unittest.TestCase):

    def test_fox_articles_class(self):
        results = FoxArticle(123, 'test')
        self.assertEqual(results.author, 'test')
        self.assertEqual(results.post_time, 123)

    def test_reddit_comments_class(self):
        results = RedditComment(123, 'test')
        self.assertEqual(results.author, 'test')
        self.assertEqual(results.post_time, 123)

class TestQueries(unittest.TestCase):

    def test_fox_articles_queries(self):
        results = create_fox_instance_lst()
        self.assertIs(type(results[0].author), str)
        self.assertIs(type(results[0].post_time), str)

    def test_reddit_comments_queries(self):
        results = create_reddit_comment_instance_lst()
        self.assertIs(type(results[0].author), str)
        self.assertIs(type(results[0].post_time), str)

unittest.main()