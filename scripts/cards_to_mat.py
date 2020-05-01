import sys
import json
import re
import numpy as np
import text_processing as tp


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

# create sets for all the parameters we care about keeping track of
ngram_set = set()
subtype_set = set()
type_set = set()
supertype_set = set()



# Loop 1 is to do all the text preprocessing and set up the matrix
print("preprocessing ",len(cards), " cards...")
for c in cards:
	# right now unigrams, maybe change latter
	ngrams = tp.rules_tokenize(c)

	for ng in ngrams:
		ngram_set.add(ng)
	for subty in c['subtypes']:
		subtype_set.add(subty)
	for ty in c['types']:
		type_set.add(ty)
	for supty in c['supertypes']:
		supertype_set.add(supty)

	# Store ngrams in card dict so you don't have to remake it
	c['ngrams'] = ngrams


# Now we will construct the matrix:
# num_cards by (ngramms + subtypes + 7/15(types) + 2/7(supertypes) + 5(colors) + 5(color_ids) + 1(cmc) + 1(pwr) + 1(tgh))
num_rows = len(cards)
num_cols = len(ngram_set) + len(subtype_set) + len(type_set) + len(supertype_set) + 13

print('setting up matrices:')
print('data_mat: ', num_rows, " x ", num_cols)
print('ngram: ', len(ngram_set))
print('subtype: ', len(subtype_set))
print('type: ', len(type_set))
print('supertype: ', len(supertype_set))


print("creating data_mat...")
data_mat = np.zeros((num_rows, num_cols))
card_names = [0]*(len(cards))
attr_map = {} # Map of attr name -> matrix col

# Now for the loops where we set attr_map
curr_col = 0
for ng in ngram_set:
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



# Now to populate the matrix and label the names
for i in range(0,len(cards)):
	c = cards[i]
	card_names[i] = c['name']

	for ng in c['ngrams']:
		data_mat[i][attr_map['ngram~'+ng]] += 1.0
	for subty in c['subtypes']:
		data_mat[i][attr_map['subty~'+subty]] += 1.0
	for ty in c['types']:
		data_mat[i][attr_map['ty~'+ty]] += 1.0
	for supty in c['supertypes']:
		data_mat[i][attr_map['supty~'+supty]] += 1.0
	for color in c['colors']:
		data_mat[i][attr_map['color~'+color]] += 1.0
	for colorid in c['colorIdentity']:
		data_mat[i][attr_map['colorid~'+colorid]] += 1.0
	data_mat[i][attr_map['cmc']] += c['convertedManaCost']
	data_mat[i][attr_map['power']] += c['power']
	data_mat[i][attr_map['toughness']] += c['toughness']



print(data_mat)


with open(dest_path, 'wb') as f:
	np.savez(f, data_mat=data_mat, card_names=np.array(card_names), attr_map=np.array(list(attr_map.items())))




