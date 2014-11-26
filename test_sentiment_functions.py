import pandas as pd
from nltk.tokenize import RegexpTokenizer

incrementers = ['very']
decrementers = pd.read_csv("Dec.csv")
afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("AFINN-111.txt") ]))
tokenizer = RegexpTokenizer(r'\w+')

def compute(comment_post):
	# comment_post = ["This is very bad"]
	words = tokenizer.tokenize(str(comment_post))
	print words
	sentence_score = 0
	previous_word = 0
	for word in words:
		if word in afinn:
			if previous_word in incrementers:
				if (afinn.get(word, 0) > 0):
					sentence_score += afinn.get(word, 0) + 1
				if (afinn.get(word, 0) < 0):
					sentence_score += afinn.get(word, 0) - 1
			elif previous_word in decrementers:
				if (afinn.get(word, 0) > 0):
					decrement_value = (decrementers.loc[decrementers['word'] == 'barely'])
					print "---> word score: " + str(decrement_value)
					sentence_score += afinn.get(word, 0) - 1
				if (afinn.get(word, 0) < 0):
					sentence_score += afinn.get(word, 0) + 1
			else:
				print word
				sentence_score += afinn.get(word, 0)
			# print sentence_score
		previous_word = word
			# previous_word = word
			# print "Sentence score: " + str(sentence_score)
	print "Sentence score: ", sentence_score
	return sentence_score
def test_compute():
	assert compute('good') == 3
	assert compute('This is very bad and very good. This is a wonderful day. The sun is so awesome.') ==  8
	# assert 0