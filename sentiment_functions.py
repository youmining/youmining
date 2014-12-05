"""Functions for the sentiment analysis.

..  module:: sentiment_functions

..  functions::
        bla bla.

..  module authors:: Mattias Nasman, s132062
                    Glebs Rjabovs, s107142
"""
from __future__ import division
import gdata.youtube
import gdata.youtube.service
from nltk.tokenize import RegexpTokenizer
import pafy
import sqlite3 as lite


def get_video_info(video_url):
    """Retrieve the basic information about a video.

    Args:
        video_id (str):    YouTube video url.

    Returns:
        likes (int):       Number of likes.
        dislikes (int):    Number of dislikes.
        viewcount (int):   Number if views.
        video_title (str): Title of the video.

    """
    video = pafy.new(video_url)
    likes = video.likes
    dislikes = video.dislikes
    viewcount = video.viewcount
    video_title = video.title
    return (likes, dislikes, viewcount, video_title)


def get_comments(video_url):
    """Download comments from a youtube video.

    Args:
        video_url (str):  http url string

    Returns:
        data (array):  comment (str)
                       date (str)

    """
    video_id = video_url[-11:]  # Extract the video_id from the url
    comments = []
    dates = []
    data = []
    yts = gdata.youtube.service.YouTubeService()
    index = 1
    urlpattern = 'http://gdata.youtube.com/feeds/api/videos/'+video_id+'/comments?start-index=%d&orderby=published&max-results=50'
    url = urlpattern % index  # MAKE TRY FUNCTION if commenting is disabled
    ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url)
    while ytfeed is not None:  # Make sure there is something to read from
        for comment in ytfeed.entry:
            comments = comment.content.text
            dates = comment.published.text.split("T")[0]
            d = dict()
            d['comment'] = comments
            d['date'] = dates
            data.append(d)
        next_url = ytfeed.GetNextLink()  # Get next page of comments
        if next_url is not None:
            ytfeed = yts.GetYouTubeVideoCommentFeed(next_url.href)
        else:
            ytfeed = None
    return (data)


def sentiment_analysis(comments):
    """The function makes a sentiment analysis of obtained comments.

    Args:
        comments (str):    unformatted strings of comments.

    Returns:
        video_sent_score (int):    total sentiment score for video.

    The function stores the words that has a sentiment value
    in two tables of the database statistics.db.

    """
    index_counter_p = 0
    index_counter_n = 0
    video_sent_score = 0
    no_of_pos = 0
    no_of_neg = 0
    no_of_neu = 0
    video_sent_score = 0
    number_of_comments = 0
    tokenizer = RegexpTokenizer(r'\w+')
    afinn = dict(map(lambda (k, v): (k, int(v)),
                     [line.split('\t') for line in open("AFINN-111.txt")]))
    incrementers = dict(map(lambda (k, v): (k, int(v)),
                            [line.split('\t') for line in open("inc.txt")]))
    decrementers = dict(map(lambda (k, v): (k, int(v)),
                            [line.split('\t') for line in open("dec.txt")]))
    inverters = dict(map(lambda (k, v): (k, int(v)),
                         [line.split('\t') for line in open("inv.txt")]))
    connection = lite.connect('statistics.db')
    with connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Words_pos")
        cursor.execute("CREATE TABLE Words_pos(Id INT, Word TEXT)")
        cursor.execute("DROP TABLE IF EXISTS Words_neg")
        cursor.execute("CREATE TABLE Words_neg(Id INT, Word TEXT)")
    for comment_post in comments:
        if comment_post is not None:
            number_of_comments += 1
            words = tokenizer.tokenize(str(comment_post))
            sent_value = 0
            previous_word = 0
            previous_word2 = 0
            for word in words:
                if word in afinn:
                    sent_value = afinn.get(word, 0)
                    if previous_word in incrementers:
                        inc_value = incrementers.get(previous_word, 0)
                        if (sent_value > 0):
                            sent_value += inc_value
                        if (sent_value < 0):
                            sent_value += inc_value
                    if previous_word in decrementers:
                        dec_value = decrementers.get(previous_word, 0)
                        if (sent_value > 0):
                            sent_value -= dec_value
                        if (sent_value < 0):
                            sent_value += dec_value
                    if previous_word in inverters:
                        sent_value -= (2*sent_value)
                    if previous_word2 in inverters:
                        sent_value -= (2*sent_value)
                    if sent_value > 0:
                        with connection:
                            cursor.execute("INSERT INTO Words_pos VALUES(?,?)",
                                           (index_counter_p, word))
                            index_counter_p += 1
                    if sent_value <= 0:
                        with connection:
                            cursor.execute("INSERT INTO Words_neg VALUES(?,?)",
                                           (index_counter_n, word))
                            index_counter_n += 1
                    video_sent_score += sent_value
                previous_word2 = previous_word
                previous_word = word
            if (sent_value > 0):
                no_of_pos += 1
            if (sent_value < 0):
                no_of_neg += 1
            if (sent_value == 0):
                no_of_neu += 1
    return (no_of_pos, no_of_neg,
            no_of_neu, video_sent_score,
            number_of_comments)


def count_frequency(data):
    """Count the frequency of a string from a list.

    Args:
        data (list):  container for list of strings.

    Returns:
        sorted_list (list): list sorted by frequency.

    """
    sorted_list = {}
    for i in data:
        sorted_list[i] = sorted_list.get(i, 0)+1
    return sorted_list


def make_statistics(no_of_pos, no_of_neg, no_of_neu,
                    video_sent_score, number_of_comments):
    """The function creates statistics for web presentation.

    Args:
        video_sent_score (int):    total sentiment score for video.

    Returns:
        percent_data (list): percentage of positive, negative
                             and neutral comments.
        pos (list):          top 5 positive words from sentiment
        neg (list):          top 5 negative words from sentiment
        percent_pos_vs_neg (float): percentage positive vs negative
        percent_neg_vs_pos (float):

    (This is where all the statistics should be implemented).

    """
    percent_pos = round((no_of_pos/(number_of_comments))*100, 1)
    percent_neg = round((no_of_neg/(number_of_comments))*100, 1)
    percent_neu = round((no_of_neu/(number_of_comments))*100, 1)
    percent_labels = ['Neutral', 'Negative', 'Positive']
    percent = []
    percent.append(percent_neu)
    percent.append(percent_neg)
    percent.append(percent_pos)
    percent_data = dict(zip(percent_labels, percent))
    counter = 0
    positive = []
    negative = []
    neg = [0]*5
    pos = [0]*5
    connection = lite.connect('statistics.db')
    with connection:  # Order the words by number of times it has been found
        c = connection.cursor()
        c.execute("SELECT Word, count(Word) FROM Words_pos GROUP BY Word ORDER BY count(Word) DESC")
        positive = c.fetchmany(size=5)
        c.execute("SELECT Word, count(Word) FROM Words_neg GROUP BY Word ORDER BY count(Word) DESC")
        negative = c.fetchmany(size=5)
    for post in positive:  # copy to new lists to avoid sending empty lists
        pos[counter] = post
        counter += 1
    counter = 0
    for post in negative:
        neg[counter] = post
        counter += 1
    return (percent_data, pos, neg)


def percentage(likes, dislikes):
    """Calculate the percentage representation of two values.

    Args:
        likes:    number of likes for the video.
        dislikes: number of dislikes for the video.

    Returns:
        likes_percent:     percentage of the total likes/dislikes
        dislikes_percent:  percentage of the total likes/dislikes

    """
    total = likes + dislikes
    likes_percent = round((likes/(total))*100, 1)
    dislikes_percent = round((dislikes/(total))*100, 1)
    return (likes_percent, dislikes_percent)
