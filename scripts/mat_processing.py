import numpy as np
import text_processing as tp

# Lots of this should be done with classes and object eventually, I'm just doing
# it with dictionaries for the time being because JS has poisoned my brain and
# its faster/easier for quick iteration to start out. If I continue this project
# and try to make the api more usable I should do that.

# Constants
color_arr = ['W','U','B','R','G']

hand_train_weights_17 = np.matrix([
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

hand_test_weights_17 = np.matrix([
	[0.00, 9.00, 3.25, 6.50, 5.00, 9.00, 9.00, 8.50, 6.00, 5.00, 4.00, 9.00, 1.50, 7.50, 9.00, 7.25, 7.00],
	[9.00, 0.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 8.50, 9.00, 9.00, 9.00, 9.00, 8.50, 9.00, 3.75, 7.50],
	[3.25, 9.00, 0.00, 9.00, 7.75, 7.50, 7.50, 7.75, 6.50, 7.75, 8.50, 7.50, 3.75, 7.75, 7.50, 9.00, 7.00],
	[6.50, 9.00, 9.00, 0.00, 7.00, 9.00, 3.25, 8.50, 9.00, 7.00, 7.00, 9.00, 6.25, 9.00, 3.00, 5.50, 7.00],
	[5.00, 9.00, 7.75, 7.00, 0.00, 9.00, 9.00, 9.00, 7.25, 0.00, 2.50, 9.00, 5.50, 7.25, 9.00, 8.00, 9.00],
	[9.00, 9.00, 7.50, 9.00, 9.00, 0.00, 7.00, 2.50, 8.50, 9.00, 9.00, 1.00, 9.00, 8.50, 7.00, 8.00, 9.00],
	[9.00, 9.00, 7.50, 3.25, 9.00, 7.00, 0.00, 7.50, 9.00, 9.00, 9.00, 7.00, 9.00, 9.00, 0.25, 9.00, 9.00],
	[8.50, 9.00, 7.75, 8.50, 9.00, 2.50, 7.50, 0.00, 9.00, 9.00, 9.00, 2.00, 9.00, 9.00, 7.50, 8.50, 9.00],
	[6.00, 8.50, 6.50, 9.00, 7.25, 8.50, 9.00, 9.00, 0.00, 7.25, 7.75, 8.50, 6.50, 1.50, 9.00, 8.50, 8.50],
	[5.00, 9.00, 7.75, 7.00, 0.00, 9.00, 9.00, 9.00, 7.25, 0.00, 2.45, 9.00, 5.50, 7.25, 9.00, 8.00, 9.00],
	[4.00, 9.00, 8.50, 7.00, 2.50, 9.00, 9.00, 9.00, 7.75, 2.45, 0.00, 9.00, 4.50, 7.75, 9.00, 8.50, 9.00],
	[9.00, 9.00, 7.50, 9.00, 9.00, 1.00, 7.00, 2.00, 8.50, 9.00, 9.00, 0.00, 9.00, 8.50, 7.00, 8.50, 9.00],
	[1.50, 9.00, 3.75, 6.25, 5.50, 9.00, 9.00, 9.00, 6.50, 5.50, 4.50, 9.00, 0.00, 8.00, 9.00, 7.00, 8.50],
	[7.50, 8.50, 7.75, 9.00, 7.25, 8.50, 9.00, 9.00, 1.50, 7.25, 7.75, 8.50, 8.00, 0.00, 9.00, 8.50, 9.00],
	[9.00, 9.00, 7.50, 3.00, 9.00, 7.00, 0.25, 7.50, 9.00, 9.00, 9.00, 7.00, 9.00, 9.00, 0.00, 9.00, 9.00],
	[7.25, 3.75, 9.00, 5.50, 8.00, 8.00, 9.00, 8.50, 8.50, 8.00, 8.50, 8.50, 7.00, 8.50, 9.00, 0.00, 8.00],
	[7.00, 7.50, 7.00, 7.00, 9.00, 9.00, 9.00, 9.00, 8.50, 9.00, 9.00, 9.00, 8.50, 9.00, 9.00, 8.00, 0.00]
	])

# helper function for dictionary insertion
def insert_incr_dict(inDict, token):
	if token in inDict:
		inDict[token] += 1
	else:
		 inDict[token] = 1


# take in a list of cards (dicts), and the ngrams to each card
def add_features(card_list, ngram_vals):
	for c in card_list:
		add_card_features(c, ngram_vals)

def add_card_features(card, ngram_vals):
	tokens = tp.rules_tokenize(card)
	ngrams = []

	for n in ngram_vals:
		# make a list of ngrams for this n
		ngs = tp.token_to_ngrams(tokens, n)
		# give a prefix to show what they are an ngram of
		ngs = list(map(lambda x: '%' + str(n) + x, ngs))
		# append those ngs to the master list
		ngrams.append(ngs)

	manacost_tkns = tp.manacost_tokenize(card)


	# put that list in the card
	tp.add_img_url(card)
	card['ngrams'] = ngrams
	card['ngramVals'] = ngram_vals
	card['manaCostTkns'] = manacost_tkns

def generate_mat_features(card_list):
	ngram_doc_freq = {}
	subtype_set = set()
	type_set = set()
	supertype_set = set()
	manacost_set = set()


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
		for mc in set(c['manaCostTkns']):
			if not tp.is_num(mc):
				manacost_set.add(mc)

	# compile findings into one data structure to return
	features = {
		'ngram_doc_freq': ngram_doc_freq,
		'subtype_set': subtype_set,
		'type_set': type_set,
		'supertype_set': supertype_set,
		'manacost_set': manacost_set
	}
	return features

def prepare_mat(features, card_list):
	# this is still really ugly but keeps my variables names just too long
	# instead of way too long
	ngram_doc_freq = features['ngram_doc_freq']
	subtype_set = features['subtype_set']
	type_set = features['type_set']
	supertype_set = features['supertype_set']
	manacost_set = features['manacost_set']

	# Now we will construct the matrix:
	# num_cards by (ngramms + subtypes + 7/15(types) + 2/7(supertypes) +
	# 5(colors) + 5(color_ids) + 6/22(mana tokens) + 1(cmc) + 1(pwr) + 1(tgh))
	num_rows = len(card_list)
	## TODO add manacost tokens
	num_cols = len(ngram_doc_freq) + len(subtype_set) + len(type_set) + \
		len(supertype_set) + (len(manacost_set) + 1) + 13

	# initialize matrix
	empty_mat = np.zeros((num_rows, num_cols))
	card_names = [""]*(len(card_list))
	feature_map = {}

	# populate col values
	curr_col = 0
	for ng in ngram_doc_freq.keys():
		feature_map['ngram~'+ng] = curr_col
		curr_col += 1
	for subty in subtype_set:
		feature_map['subty~'+subty] = curr_col
		curr_col += 1
	for ty in type_set:
		feature_map['ty~'+ty] = curr_col
		curr_col += 1
	for supty in supertype_set:
		feature_map['supty~'+supty] = curr_col
		curr_col += 1
	for color in color_arr:
		feature_map['color~'+color] = curr_col
		curr_col += 1
	for colorid in color_arr:
		feature_map['colorid~'+colorid] = curr_col
		curr_col += 1
	# This is the int generic mana cost
	feature_map['manacost~#'] = curr_col
	curr_col +=1
	# this is all the tokens
	for mc in manacost_set:
		feature_map['manacost~'+mc] = curr_col
		curr_col += 1
	feature_map['cmc'] = curr_col
	curr_col += 1
	feature_map['power'] = curr_col
	curr_col += 1
	feature_map['toughness'] = curr_col
	curr_col += 1

	matrix_data = {
		'data_mat': empty_mat,
		'card_names': card_names,
		'feature_map': feature_map
	}
	return matrix_data

def populate_mat(card_list, features, matrix_data, weights):
	data_mat = matrix_data['data_mat']
	card_names = matrix_data['card_names']
	feature_map = matrix_data['feature_map']

	ngram_doc_freq = features['ngram_doc_freq']


	for i in range(0,len(card_list)):
		c = card_list[i]
		card_names[i] = c['name']

		# for each of the lists of ngrams add them in
		for j in range(0, len(c['ngrams'])):
			ngrams = c['ngrams'][j]
			for ng in ngrams:
				divisor = ngram_doc_freq[ng] if weights['ngram_idf?'] else 1.0
				data_mat[i][feature_map['ngram~'+ng]] += (weights['ngram_weights'][j] / divisor)

		for subty in c['subtypes']:
			data_mat[i][feature_map['subty~'+subty]] += weights['subtype_weight']

		for ty in c['types']:
			data_mat[i][feature_map['ty~'+ty]] += weights['type_weight']
		
		for supty in c['supertypes']:
			data_mat[i][feature_map['supty~'+supty]] += weights['supertype_weight']
		
		for color in c['colors']:
			data_mat[i][feature_map['color~'+color]] += weights['color_weight']
		
		for colorid in c['colorIdentity']:
			data_mat[i][feature_map['colorid~'+colorid]] += weights['colorid_weight']

		for mc in c['manaCostTkns']:
			if tp.is_num(mc):
				data_mat[i][feature_map['manacost~#']] += weights['mana_cost_weight'] * float(mc)
			else:
				data_mat[i][feature_map['manacost~'+mc]] += weights['mana_cost_weight']
		
		data_mat[i][feature_map['cmc']] += c['convertedManaCost'] * weights['cmc_weight']
		data_mat[i][feature_map['power']] += c['power'] * weights['pwr_tgh_weight']
		data_mat[i][feature_map['toughness']] += c['toughness'] * weights['pwr_tgh_weight']


def create_distance_mat(data_mat):
	dimension = len(data_mat)
	dist_matrx = np.zeros( (dimension,dimension) )
	for i in range(0, dimension):
		# we get to cheat since (n,n) = 0 and (n,m) = (m,n)
		for j in range(i+1, dimension):
			# this is the way to find the euclidean distance between two matrices
			dist_matrx[i][j] = dist_matrx[j][i] = np.linalg.norm(data_mat[i] - data_mat[j])
	return dist_matrx

def dist_mat_diff(dist_mat1, dist_mat2):
	return np.sum( np.absolute(dist_mat1 - dist_mat2) )

def square_diff(dist_mat1, dist_mat2):
	return np.sum( (dist_mat1 - dist_mat2) ** 2 )