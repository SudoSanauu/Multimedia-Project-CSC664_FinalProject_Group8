import sys
import json
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

# what ngram values to use
ngram_vals = [1,3]

# weight for each feature/type of feature in the matrix
weights = {
	'ngram_weights': [0.4, 0.6],
	'ngram_idf?': True,
	'color_weight': 0.5,
	'colorid_weight': 0.5,
	'subtype_weight': 1.0,
	'type_weight': 1.0,
	'supertype_weight': 1.0,
	'cmc_weight': 0.1,
	'mana_cost_weight': 0.1,
	'pwr_tgh_weight': 1.0
}

# generate ngrams and save in card list
print("preprocessing ",len(cards), " cards ...")
matp.add_features(cards, ngram_vals)

print("creating feature sets ...")
features = matp.generate_mat_features(cards)

print('setting up matrix ...')
matrix_data = matp.prepare_mat(features, cards)

print('data_mat: ', len(matrix_data['data_mat']), " x ", len(matrix_data['data_mat'][0]))
print('ngram: ', len(features['ngram_doc_freq']))
print('manacosts: ', 1 + len(features['manacost_set']))
print('subtype: ', len(features['subtype_set']))
print('type: ', len(features['type_set']))
print('supertype: ', len(features['supertype_set']))


print('populating matrix ...')
matp.populate_mat(cards, features, matrix_data, weights)

print("saving data to ", dest_path, " ...")
with open(dest_path, 'wb') as f:
	np.savez(f, 
		data_mat=matrix_data['data_mat'], 
		card_names=np.array(matrix_data['card_names']), 
		feature_map=np.array( list(matrix_data['feature_map'].items()) )
	)

print("finished successfully")


