import sys
import json
import re
import copy
import numpy as np
import text_processing as tp
import mat_processing as matp


if len(sys.argv) != 3:
	print("Please put in src file and destination file.")
	quit()

card_path = sys.argv[1]
dest_path = sys.argv[2]

print("reading from ", card_path)
with open(card_path, 'r') as f:
	cards = json.load(f)

ngram_vals = [1, 2, 3, 4]

# generate ngrams and save in card list
print("preprocessing ", len(cards), " cards ...")
matp.add_features(cards, ngram_vals)

print("creating feature sets ...")
features = matp.generate_mat_features(cards)

print('setting up matrix ...')
matrix_data = matp.prepare_mat(features, cards)

print('data_mat: ', len(matrix_data['data_mat']),
	  " x ", len(matrix_data['data_mat'][0]))
print('ngram: ', len(features['ngram_doc_freq']))
print('manacosts: ', 1 + len(features['manacost_set']))
print('subtype: ', len(features['subtype_set']))
print('type: ', len(features['type_set']))
print('supertype: ', len(features['supertype_set']))


print('iterating through')


# what ngram values to use


# weight for each feature/type of feature in the matrix
weights_arr = [0, 1/8, 2/8, 3/8, 4/8, 5/8, 6 /
	8, 7/9, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]


# for a, b, c, d, e, f, g, h, i, j, k, l in weights_arr:
# 	weights = {
# 		'ngram_weights': [a, b, c, d],
# 		'ngram_idf?': True,
# 		'color_weight': e,
# 		'colorid_weight': f,
# 		'subtype_weight': g,
# 		'type_weight': h,
# 		'supertype_weight': i,
# 		'cmc_weight': j,
# 		'mana_cost_weight': k,
# 		'pwr_tgh_weight': l
# 	}
# 	matp.populate_mat(cards, features, matrix_data, weights)
# 	dist_matrx = matp.create_distance_mat(matrix_data['data_mat'])
# 	print(matp.dist_mat_diff(dist_matrx))
min_dist = float("inf")
min_dist_weights = {}

for a in weights_arr:
	for b in weights_arr:
		for c in weights_arr:
			for d in weights_arr:
				for e in weights_arr:
					for f in weights_arr:
						for g in weights_arr:
							for h in weights_arr:
								for i in weights_arr:
									for j in weights_arr:
										for k in weights_arr:
											for l in weights_arr:
												for m in [True, False]:
													weights = {
														'ngram_weights': [a, b, c, d],
														'ngram_idf?': m,
														'color_weight': e,
														'colorid_weight': f,
														'subtype_weight': g,
														'type_weight': h,
														'supertype_weight': i,
														'cmc_weight': j,
														'mana_cost_weight': k,
														'pwr_tgh_weight': l
													}
													matp.populate_mat(cards, features, matrix_data, weights)
													dist_matrx = matp.create_distance_mat(matrix_data['data_mat'])
													if matp.dist_mat_diff(dist_matrx) < min_dist:
														min_dist = matp.dist_mat_diff(dist_matrx)
														min_dist_weights = copy.deepcopy(weights)
														print(min_dist)

with open(dest_path, 'w') as f:
	json.dump(min_dist_weights, f)