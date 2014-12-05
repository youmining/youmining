import sentiment_functions as sf
from nltk.tokenize import RegexpTokenizer
import sqlite3 as lite


def test_function():
    assert sf.sentiment_analysis({'good'}) == (1, 0, 0, 3, 1)
    assert sf.sentiment_analysis({'very good'}) == (1, 0, 0, 5, 1)
    assert sf.sentiment_analysis({'not very good'}) == (0, 1, 0, -5, 1)
    assert sf.sentiment_analysis({'I like this video!', 'This is so bad I hate it', 'not very good'}) == (1, 2, 0, -9, 3)
    assert sf.sentiment_analysis({'This is not great at all', 'so stupid but very nice and not bad'}) == (1, 1, 0, 3, 2)

#(no_of_pos, no_of_neg,  no_of_neu, video_sent_score, number_of_comments)