"""Main file for the sentiment analysis and statistics.

.. module:: main

.. module authors:: Mattias Nasman, s132062
					Glebs Rjabovs, s107142
"""
import re
import gdata.youtube
import gdata.youtube.service
import nltk
import pandas as pd
import sentiment_functions as sf

#comments = ["This is cool sucks sucks sucks bad bad terrible horrible bad bad bad very good, happy. Hello how awesome good is happy. Very good indeed.","Bad, nice good, barely good","lovely lovely lovely lovely"]
#comments = ["very terrible horrible","very good"]

video_id = 'd89qJSU_r44'
comments = sf.get_comments(video_id)
video_sent_score = sf.sent_analyzes_sentence(comments)
sf.make_statistics(video_sent_score)