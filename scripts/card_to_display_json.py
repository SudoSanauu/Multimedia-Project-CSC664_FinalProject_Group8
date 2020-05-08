import numpy as np
import mat_processing as matp
import text_processing as tp
import sys
import json

# CONSTANTS
ngram_vals = [1, 3]

weights = {
	'ngram_weights': [0.33, 1],
	'ngram_idf?': True,
	'color_weight': 0.33,
	'colorid_weight': 0.33,
	'subtype_weight': 0.33,
	'type_weight': 1.0,
	'supertype_weight': 0.33,
	'cmc_weight': 0.33,
	'mana_cost_weight': 0.33,
	'pwr_tgh_weight': 0.33
}

if len(sys.argv) != 3:
	print("Please put in src file and destination file.")
	quit()

card_path = sys.argv[1]
dest_path = sys.argv[2]

print("reading from ", card_path)
with open(card_path, 'r') as f:
	cards = json.load(f)



print("preprocessing ",len(cards), " cards ...")
cleaned_cards = []

# Eventually I need to figure out how to parse the json correctly depending on
# which type it is and such
for c in cards.values():

	new_c = tp.clean_card_json(c)
	if new_c == None:
		continue

	matp.add_card_features(new_c, ngram_vals)
	cleaned_cards.append(new_c)

print("finished preprocessing with ", len(cleaned_cards), " cards")

print("setting up matrix ...")
features = matp.generate_mat_features(cleaned_cards)
matrix_data = matp.prepare_mat(features, cleaned_cards)

print('data_mat: ', len(matrix_data['data_mat']), " x ", len(matrix_data['data_mat'][0]))
print('ngram: ', len(features['ngram_doc_freq']))
print('manacosts: ', 1 + len(features['manacost_set']))
print('subtype: ', len(features['subtype_set']))
print('type: ', len(features['type_set']))
print('supertype: ', len(features['supertype_set']))

print("populating matrix ...")
matp.populate_mat(cleaned_cards, features, matrix_data, weights)

print("creating distance matrix ...")
dist_mat = matp.create_distance_mat(matrix_data['data_mat'])

print("saving to ", dest_path, " ...")
out_json = {
	'distMat': dist_mat.tolist(),
	'cards': cleaned_cards
}

with open(dest_path, 'w') as f:
	json.dump(out_json, f)

print('Finished successfully')


