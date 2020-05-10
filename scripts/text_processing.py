import re

# declare constants & compile res
no_reminder = re.compile("\([^)]*\)")
no_useless = re.compile("[\.,'\"!—%]")
no_newline = re.compile("\n")
space_colon = re.compile(":")
split_pattern = re.compile(' ')
mana_split = re.compile('\}\{')

rules_stoplist = ['the', 'of', '', 'with']
r_slist_fun = lambda f: not f in rules_stoplist

flavor_stoplist = ['the', '', 'a', 'to', 'an', 'it', 'its']
f_slist_fun = lambda f: not f in flavor_stoplist


def rules_tokenize(card):
	# replace cardname with @ and makes all lowercase
	# TODO: Find a way to remove shortened legendary names too
	new_rules = card['text'].replace(card['name'], "@").lower()

	# remove all reminder text in parens
	new_rules = no_reminder.sub("", new_rules)

	# get rid of useless characters
	new_rules = no_useless.sub("", new_rules)

	# replace \n with ' '
	new_rules = no_newline.sub(" ", new_rules)

	# edit : to be separated with spaces so it becomes its own token
	new_rules = space_colon.sub(' :', new_rules)

	# split tokens and remove stop words
	return list(filter(r_slist_fun, split_pattern.split(new_rules)))

def flavor_tokenize(card):
	# all lowercase
	new_flavor = card['flavorText'].lower()

	# get rid of useless characters
	new_flavor = no_useless.sub("", new_flavor)

	# replace \n with ' '
	new_flavor = no_newline.sub(" ", new_flavor)

	# split tokens and remove stop words
	return list(filter(f_slist_fun, split_pattern.split(new_flavor)))

def manacost_tokenize(card):
	mc = card['manaCost']
	if mc == '':
		return []

	# since manacost appears as '{a}{b}...{c}' removing 1st & last brace and then
	# splitting on }{ separates all the tokens 
	return mana_split.split(mc[1:-1])

def add_img_url(card):
	if card["scryfallId"] != "" :
		card["imgUrl"] = 'https://img.scryfall.com/cards/normal/front/' + \
			card["scryfallId"][0] + '/' + card["scryfallId"][1] + '/' + \
			card["scryfallId"] + '.jpg'
	else:
		card['imgUrl'] = "https://images.all-free-download.com/images/graphiclarge/frowny_face_clip_art_13121.jpg"

def is_num(in_str):
	try:
		x = float(in_str)
		return True
	except ValueError:
		return False


def token_to_bigram(tokens):
	return token_to_ngrams(tokens,2)

def token_to_ngrams(tokens, ngram_size):
	# S & E are start and end tokens for n>1
	if ngram_size > 1:
		new_tok = ['S'] + tokens + ['E']
	else:
		if tokens == []:
			return ["()"]
		new_tok = tokens

	# catch case of too small to prevent out of index errors
	if len(new_tok) <= ngram_size:
		ngram = ','.join(new_tok)
		return ['(' + ngram + ')']

	# allocate list for performance
	outlist = ['']*(len(new_tok)-(ngram_size-1))

	for i in range(0, len(new_tok)-(ngram_size-1)):
		ngram = ','.join( new_tok[i:(i+ngram_size)] )
		outlist[i] = '(' + ngram + ')'
	return outlist	


def clean_card_json(card):
	if ('names' in card) and (card['names'] != []):
		return None

	power = card.get("power", -1.0)
	if power == "*":
		power = 0.0
	else:
		power = float(power)

	toughness = card.get("toughness", -1.0)
	if toughness == "*":
		toughness = 0.0
	else:
		toughness = float(toughness)

	return {
		"colorIdentity": card.get("colorIdentity",[]),
		"colors": card.get("colors",[]),
		"convertedManaCost": card.get("convertedManaCost",0),
		"manaCost": card.get("manaCost", ""),
		"name": card.get("name",""),
		"power": power,
		"scryfallId": card.get("scryfallId", ""),
		"subtypes": card.get("subtypes",[]),
		"supertypes": card.get("supertypes",[]),
		"text": card.get("text",""),
		"toughness": toughness,
		"type": card.get("type"),
		"types": card.get("types",[])
	}
