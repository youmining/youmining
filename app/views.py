"""View handler.

.. module:: views

.. module authors:: Mattias Nasman, s132062
                    Glebs Rjabovs, s107142
"""
from flask import render_template, request
from app import app
import sentiment_functions as sf
app.jinja_env.add_extension("chartkick.ext.charts")


@app.route('/', methods=['POST', 'GET'])
@app.route('/index')
def index():
    """Method for index.html.

    Returns:
        if input button is pressed: results.html
        else: index.html

    """
    if request.method == 'POST':
        input_string = request.form['input_string']
        (comment_data) = sf.get_comments(input_string)
        (likes, dislikes,
            viewcount,
            video_title) = sf.get_video_info(input_string)
        comments = [d['comment'] for d in comment_data]
        (no_of_pos, no_of_neg,
            no_of_neu, video_sent_score,
            number_of_comments) = sf.sentiment_analysis(comments)
        (percentage, positive,
            negative) = sf.make_statistics(no_of_pos,
                                                     no_of_neg,
                                                     no_of_neu,
                                                     video_sent_score,
                                                     number_of_comments)
        dates = [d['date'] for d in comment_data]
        date_count = sf.count_frequency(dates)
        (likes_percent, dislikes_percent) = sf.percentage(likes, dislikes)
        return render_template("results.html", title='Home',
                               input=input_string, pos=positive,
                               neg=negative, posN=no_of_pos,
                               negN=no_of_neg, neuN=no_of_neu,
                               percent_data=percentage,
                               N=number_of_comments, time_data=date_count,
                               likes=likes, dislikes=dislikes,
                               likes_p=likes_percent,
                               dislikes_p=dislikes_percent,
                               viewcount=viewcount, vtitle=video_title)
    return render_template("index.html", title='Home')


@app.route('/results')
def results():
    """Method for results.html.

    Returns:
        if input button is pressed: results.html

    """
    if request.method == 'POST':
        input_string = request.form['input_string']
        (comment_data, likes,
            dislikes, viewcount,
            video_title) = sf.get_comments(input_string)
        comments = [d['comment'] for d in comment_data]
        (no_of_pos, no_of_neg,
            no_of_neu, video_sent_score,
            number_of_comments) = sf.sentiment_analysis(comments)
        (percentage, positive,
            negative, percent_pos_vs_neg,
            percent_neg_vs_pos) = sf.make_statistics(no_of_pos,
                                                     no_of_neg,
                                                     no_of_neu,
                                                     video_sent_score,
                                                     number_of_comments)
        dates = [d['date'] for d in comment_data]
        date_count = sf.count_frequency(dates)
        print date_count
        (likes_percent, dislikes_percent) = sf.percentage(likes, dislikes)
        return render_template("results.html", title='Home',
                               input=input_string, pos=positive,
                               neg=negative, posN=no_of_pos,
                               negN=no_of_neg, neuN=no_of_neu,
                               percent_data=percentage,
                               N=number_of_comments, time_data=date_count,
                               likes=likes, dislikes=dislikes,
                               likes_p=likes_percent,
                               dislikes_p=dislikes_percent,
                               viewcount=viewcount, vtitle=video_title)
