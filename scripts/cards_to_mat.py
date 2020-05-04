import sys
import json
import re
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

# Constant declaration
color_arr = ['W','U','B','R','G']

# what ngram values to use
ngram_vals = [1,3]

# weight for each feature/type of feature in the matrix
ngram_weights = [0.4, 0.6]
color_wieght = 0.5
colorid_weight = 0.5
subtype_weight = 1.0
type_weight = 1.0
supertype_weight = 1.0
cmc_weight = 0.2
pwr_tgh_weight = 1.0


# generate ngrams and save in card list
print("preprocessing ",len(cards), " cards ...")
matp.add_ngrams(cards, ngram_vals)

print("creating feature sets ...")
features = matp.generate_mat_features(cards)

# kind of a messy way to do this, I wonder if there's a better way...
ngram_doc_freq = features['ngram_doc_freq']
subtype_set = features['subtype_set']
type_set = features['type_set']
supertype_set = features['supertype_set']

# Now we will construct the matrix:
# num_cards by (ngramms + subtypes + 7/15(types) + 2/7(supertypes) + 5(colors) + 5(color_ids) + 1(cmc) + 1(pwr) + 1(tgh))
num_rows = len(cards)
num_cols = len(ngram_doc_freq) + len(subtype_set) + len(type_set) + len(supertype_set) + 13

print('setting up matrices:')
print('data_mat: ', num_rows, " x ", num_cols)
print('ngram: ', len(ngram_doc_freq))
print('subtype: ', len(subtype_set))
print('type: ', len(type_set))
print('supertype: ', len(supertype_set))


print("creating data_mat ...")
data_mat = np.zeros((num_rows, num_cols))
card_names = [""]*(len(cards))
attr_map = {} # Map of attr name -> matrix col

# Now for the loops where we set attr_map
curr_col = 0
for ng in ngram_doc_freq.keys():
	attr_map['ngram~'+ng] = curr_col
	curr_col += 1
for subty in subtype_set:
	attr_map['subty~'+subty] = curr_col
	curr_col += 1
for ty in type_set:
	attr_map['ty~'+ty] = curr_col
	curr_col += 1
for supty in supertype_set:
	attr_map['supty~'+supty] = curr_col
	curr_col += 1
for color in color_arr:
	attr_map['color~'+color] = curr_col
	curr_col += 1
for colorid in color_arr:
	attr_map['colorid~'+colorid] = curr_col
	curr_col += 1
attr_map['cmc'] = curr_col
curr_col += 1
attr_map['power'] = curr_col
curr_col += 1
attr_map['toughness'] = curr_col
curr_col += 1


print('populating feature matrix...')
# Now to populate the matrix and label the names
for i in range(0,len(cards)):
	c = cards[i]
	card_names[i] = c['name']

	# for each of the lists of ngrams add them in
	for j in range(0, len(c['ngrams'])):
		ngrams = c['ngrams'][j]
		for ng in ngrams:
			data_mat[i][attr_map['ngram~'+ng]] += (ngram_weights[j] / ngram_doc_freq[ng])

	for subty in c['subtypes']:
		data_mat[i][attr_map['subty~'+subty]] += subtype_weight

	for ty in c['types']:
		data_mat[i][attr_map['ty~'+ty]] += type_weight
	
	for supty in c['supertypes']:
		data_mat[i][attr_map['supty~'+supty]] += supertype_weight
	
	for color in c['colors']:
		data_mat[i][attr_map['color~'+color]] += color_wieght
	
	for colorid in c['colorIdentity']:
		data_mat[i][attr_map['colorid~'+colorid]] += colorid_weight
	
	data_mat[i][attr_map['cmc']] += c['convertedManaCost'] * cmc_weight
	data_mat[i][attr_map['power']] += c['power'] * pwr_tgh_weight
	data_mat[i][attr_map['toughness']] += c['toughness'] * pwr_tgh_weight

print("saving data to ", dest_path, " ...")
with open(dest_path, 'wb') as f:
	np.savez(f, data_mat=data_mat, card_names=np.array(card_names), attr_map=np.array(list(attr_map.items())))

print("finished successfully")


