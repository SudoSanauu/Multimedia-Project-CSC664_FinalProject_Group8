import numpy as np
import mat_processing as matp
import text_processing as tp
import sys
import json

# CONSTANTS
ngram_vals = [1]


# # try one
# weights = {
# 	'ngram_weights': #[0.67], val is [2]
# 	'ngram_idf?': False,
# 	'color_weight': 1.0,
# 	'colorid_weight': 1.0,
# 	'subtype_weight': 0.33,
# 	'type_weight': 1.0,
# 	'supertype_weight': 1.0,
# 	'cmc_weight': 0.67,
# 	'mana_cost_weight': 1.0,
# 	'pwr_tgh_weight': 1.0
# }

# try two
weights = {
  "ngram_weights": [0.66], # val is [1]
  "ngram_idf?": False,
  "color_weight": 1.25,
  "colorid_weight": 1.25,
  "subtype_weight": 0.5,
  "type_weight": 1.25,
  "supertype_weight": 1.25,
  "cmc_weight": 0.75,
  "mana_cost_weight": 1.25,
  "pwr_tgh_weight": 0.75
}

if len(sys.argv) != 3:
	print("Please put in src file and destination file.")
	quit()

card_path = sys.argv[1]
dest_path = sys.argv[2]

print("reading from ", card_path)
with open(card_path, 'r') as f:
	in_json = json.load(f)

# to try and make this work for the different files someone may want to run it
# on. Note, will only make imgUrl for specific printings.
if type(in_json) == list:
	cards = in_json
elif type(in_json) == dict:
	first = next(iter(in_json))
	# if its just 
	if in_json[first].get('cards') == None:
		cards = list(in_json.values())
	else:
		cards = []
		for mtg_set in in_json.values():
			cards = cards + mtg_set['cards']



print("preprocessing ",len(cards), " cards ...")
cleaned_cards = []

# for c in cards.values():
for c in cards:

	new_c = tp.clean_card_json(c)
	if new_c == None:
		continue

	matp.add_card_features(new_c, ngram_vals)
	cleaned_cards.append(new_c)

cleaned_cards.sort(key=lambda c: c['name'])

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

with open(dest_path + '.json', 'w') as f:
	json.dump(out_json, f)

with open(dest_path + '.npz', 'wb') as f:
	np.savez_compressed(f,
		data_mat=matrix_data['data_mat'], 
		card_names=np.array(matrix_data['card_names']), 
		feature_map=np.array( list(matrix_data['feature_map'].items()) ),
		dist_mat=dist_mat
	)

print('Finished successfully')


