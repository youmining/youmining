"""Functions for the sentiment analysis.

.. module:: sentiment_functions

.. module authors:: Mattias Nasman, s132062
					Glebs Rjabovs, s107142
"""
import re
import gdata.youtube
import gdata.youtube.service
import nltk
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import sqlite3 as lite
import sys

tokenizer = RegexpTokenizer(r'\w+')
afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("AFINN-111.txt") ]))

def get_comments(video_id):
	"""The function downloads video comments from a youtube video.

	Args:
		video_id (str): 	unique id for a chosen YouTube video.
	
	Returns:
		comments (str): 	unformatted strings of comments.

	"""
	comments = []
	yts = gdata.youtube.service.YouTubeService()
	index = 1
	urlpattern = 'http://gdata.youtube.com/feeds/api/videos/' + video_id + '/comments?start-index=%d&orderby=published&max-results=50'
	url = urlpattern % index
	ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url)  # Get first page of comments
	while ytfeed is not None: # Make sure there is something to read from
		comments.extend([ comment.content.text for comment in ytfeed.entry ]) # Extract comments from current url
		next_url = ytfeed.GetNextLink() # Get next page of comments
		if next_url is not None: # Check if the next comment page exists. If not, break the loop.
			ytfeed = yts.GetYouTubeVideoCommentFeed(next_url.href)
		else: 
			ytfeed = None
	return comments

def sent_analyzes_sentence(comments):
	"""The function makes a sentiment analysis of obtained comments.

	Args:
		comments (str): 			unformatted strings of comments.
	
	Returns:
		video_sent_score (int): 	total sentiment score for video.

	The function stores the words that has a sentiment value in two tables of the database statistics.db.

	"""
	index_counter_p=0
	index_counter_n=0
	video_sent_score=0
	incrementers = ['very'] # This will be implemented in a larger database
	decrementers = pd.read_csv("Dec.csv")
	connection = lite.connect('statistics.db')
	with connection:
	    cursor = connection.cursor()
	    cursor.execute("DROP TABLE IF EXISTS Words_pos")
	    cursor.execute("CREATE TABLE Words_pos(Id INT, Word TEXT)")
	    cursor.execute("DROP TABLE IF EXISTS Words_neg")
	    cursor.execute("CREATE TABLE Words_neg(Id INT, Word TEXT)")
	for comment_post in comments:
		if comment_post is not None:
			words = tokenizer.tokenize(str(comment_post))
			sent_value=0
			previous_word=0
			for word in words:
				if word in afinn:
					if previous_word in incrementers:
						if (afinn.get(word, 0) > 0):
							sent_value = afinn.get(word, 0) + 1
						if (afinn.get(word, 0) < 0):
							sent_value = afinn.get(word, 0) - 1
					elif previous_word in decrementers:
						if (afinn.get(word, 0) > 0):
							sent_value = afinn.get(word, 0) - 1
						if (afinn.get(word, 0) < 0):
							sent_value = afinn.get(word, 0) + 1
					else:
						sent_value = afinn.get(word, 0)
					if sent_value > 0:
						with connection:
							cursor.execute("INSERT INTO Words_pos VALUES(?,?)", (index_counter_p, word))
							index_counter_p+=1
					if sent_value <= 0:
						with connection:
							cursor.execute("INSERT INTO Words_neg VALUES(?,?)", (index_counter_n, word))
							index_counter_n+=1
					video_sent_score += sent_value
				previous_word = word
	return video_sent_score

def make_statistics(video_sent_score):
	"""The function creates statistics for web presentation.

	Args:
		video_sent_score (int): 	total sentiment score for video.
	
	Returns:
		Nothing yet.
		
	(This is where all the statistics should be implemented).

	"""
	print 'Sent score: ' + str(video_sent_score)
	connection = lite.connect('statistics.db')
	names = 0
	no_of_words = 0
	with connection: # Order the words by number of times it has been found
		cursor = connection.cursor()
    	cursor.execute("SELECT Word, count(Word) FROM Words_pos GROUP BY Word ORDER BY count(Word) DESC")
    	rows = cursor.fetchall()
    	print 'Positive---->'
    	for row in rows:
    		if no_of_words < 5:
    			print row[0], row[1]
    			no_of_words += 1
    	cursor.execute("SELECT Word, count(Word) FROM Words_neg GROUP BY Word ORDER BY count(Word) DESC")
    	rows = cursor.fetchall()
    	print 'Negative---->'
    	no_of_words = 0
    	for row in rows:
    		if no_of_words < 5:
    			print row[0], row[1]
    			no_of_words += 1