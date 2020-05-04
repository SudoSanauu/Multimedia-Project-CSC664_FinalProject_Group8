import numpy as np
import text_processing as tp

# Constants
color_arr = ['W','U','B','R','G']

hand_weights_17 = np.matrix([
	[0.00, 7.50, 3.00, 5.00, 0.50, 6.00, 6.00, 7.75, 7.50, 0.50, 7.00, 6.00, 7.50, 8.50, 4.00, 7.50, 6.00],
	[7.50, 0.00, 6.50, 6.50, 7.50, 4.50, 8.00, 3.00, 2.00, 7.50, 4.00, 8.50, 2.00, 8.50, 7.50, 1.00, 9.00],
	[3.00, 6.50, 0.00, 2.00, 2.75, 7.50, 4.50, 6.00, 6.00, 2.75, 6.50, 5.50, 6.50, 7.00, 4.50, 6.50, 9.00],
	[5.00, 6.50, 2.00, 0.00, 4.75, 7.50, 4.50, 6.00, 6.00, 4.75, 6.50, 5.50, 6.50, 7.00, 6.00, 6.50, 9.00],
	[0.50, 7.50, 2.75, 4.75, 0.00, 6.00, 6.00, 7.75, 7.50, 0.50, 7.00, 5.75, 7.50, 8.50, 4.00, 7.50, 6.00],
	[6.00, 4.50, 7.50, 7.50, 6.00, 0.00, 9.00, 5.50, 4.00, 6.00, 6.00, 9.00, 4.00, 9.00, 4.00, 4.00, 3.75],
	[6.00, 8.00, 4.50, 4.50, 6.00, 9.00, 0.00, 7.50, 7.00, 6.00, 8.00, 6.00, 9.00, 4.00, 8.00, 8.00, 9.00],
	[7.75, 3.00, 6.00, 6.00, 7.75, 5.50, 7.50, 0.00, 1.50, 7.75, 3.00, 9.00, 3.00, 8.50, 8.00, 2.50, 8.00],
	[7.50, 2.00, 6.00, 6.00, 7.50, 4.00, 7.00, 1.50, 0.00, 7.50, 3.50, 9.00, 2.00, 9.00, 7.00, 1.50, 6.00],
	[0.50, 7.50, 2.75, 4.75, 0.50, 6.00, 6.00, 7.75, 7.50, 0.00, 7.00, 5.75, 7.50, 8.50, 4.00, 7.50, 6.00],
	[7.00, 4.00, 6.50, 6.50, 7.00, 6.00, 8.00, 3.00, 3.50, 7.00, 0.00, 6.00, 2.50, 6.00, 7.50, 3.75, 8.00],
	[6.00, 8.50, 5.50, 5.50, 5.75, 9.00, 6.00, 9.00, 9.00, 5.75, 6.00, 0.00, 5.75, 5.50, 7.50, 9.00, 8.50],
	[7.50, 2.00, 6.50, 6.50, 7.50, 4.00, 9.00, 3.00, 2.00, 7.50, 2.50, 5.75, 0.00, 6.00, 7.00, 1.75, 8.00],
	[8.50, 8.50, 7.00, 7.00, 8.50, 9.00, 4.00, 8.50, 9.00, 8.50, 6.00, 5.50, 6.00, 0.00, 9.00, 9.00, 8.50],
	[4.00, 7.50, 4.50, 6.00, 4.00, 4.00, 8.00, 8.00, 7.00, 4.00, 7.50, 7.50, 7.00, 9.00, 0.00, 8.75, 6.50],
	[7.50, 1.00, 6.50, 6.50, 7.50, 4.00, 8.00, 2.50, 1.50, 7.50, 3.75, 9.00, 1.75, 9.00, 8.75, 0.00, 7.00],
	[6.00, 9.00, 9.00, 9.00, 6.00, 3.75, 9.00, 8.00, 6.00, 6.00, 8.00, 8.50, 8.00, 8.50, 6.50, 7.00, 0.00]
	])

# helper function for dictionary insertion
def insert_incr_dict(inDict, token):
	if token in inDict:
		inDict[token] += 1
	else:
		 inDict[token] = 1


# take in a list of cards (dicts), and the ngrams to each card
def add_ngrams(card_list, ngram_vals):
	for c in card_list:
		tokens = tp.rules_tokenize(c)
		ngrams = []

		for n in ngram_vals:
			# make a list of ngrams for this n
			ngs = tp.token_to_ngrams(tokens, n)
			# give a prefix to show what they are an ngram of
			ngs = list(map(lambda x: '%' + str(n) + x, ngs))
			# append those ngs to the master list
			ngrams.append(ngs)

		# put that list in the card
		c['ngrams'] = ngrams
		c['ngramVals'] = ngram_vals
		# NOTE: a better api would be to have an ngram dictionary with elements
		# key=n and value=ngs for each n.

def generate_mat_features(card_list):
	ngram_doc_freq = {}
	subtype_set = set()
	type_set = set()
	supertype_set = set()


	for c in card_list:
		for i in range(0, len(c['ngramVals'])):
			n = c['ngramVals'][i]
			ngrams = c['ngrams'][i]

			# now insert them into doc freq dictionary
			for ng in set(ngrams):
				insert_incr_dict(ngram_doc_freq, ng)
		
		# insert the types into their sets
		for subty in c['subtypes']:
			subtype_set.add(subty)
		for ty in c['types']:
			type_set.add(ty)
		for supty in c['supertypes']:
			supertype_set.add(supty)
	# compile findings into one data structure to return
	return_dict = {
		'ngram_doc_freq': ngram_doc_freq,
		'subtype_set': subtype_set,
		'type_set': type_set,
		'supertype_set': supertype_set
	}
	return return_dict



