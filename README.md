##############################
#####    Data Sources    #####
##############################

1. Reddit, The_Donald subreddit (API)

	In order to access the Reddit API you'll need to sign up for a Reddit account if you don't already have one. Access the developer tools to make a user agent as well as to sign up for a client id and client secret: https://www.reddit.com/prefs/apps

2. Fox News

	This program scrapes Fox News to get the latest articles in every category listed on the Fox News front page.


#####################################
#####    Running the program    #####
#####################################

1. Required packages can be found in the requirements.txt file

	Install these to your virtual environment before running.

2. Plotly signup/Python info: https://plot.ly/python/getting-started/

	You'll need to sign up for an account on Plotly in order to run the visualizations portion.


##################################
#####     Data structures    #####
##################################

Main data structures:

Classes:

FoxArticle
- Author and post time of fox article

RedditComment
- Author and post time of reddit comment

Functions:

create_reddit_instance
- Accesses the Reddit API

scrape_fox_news
- Scrapes Fox News website

populate_database
- Inputs data from Reddit and Fox News into database

Series of functions to create Plotly graphs

get_input_from_user
- Makes the program interactive


######################################
#####     Running the program    #####
######################################

When the program runs, you will be presented with the option to select one of four graphs to view. Enter the number that appears next to the graph that you would like to see. The graph should pop up in Plotly (this may take a moment to load). After the graph appears you can choose another graph to view. If you want to quit the program at any point, type 
"exit."

