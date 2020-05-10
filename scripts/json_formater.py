import sys
import json
import text_processing as tp

if len(sys.argv) != 3:
	print("Please put in src file and destination file.")
	quit()

src_path = sys.argv[1]
dest_path = sys.argv[2]

with open(src_path, 'r', encoding="utf8") as f:
	set_json = json.load(f)

parsedCards = []
# cards = []

# for every in set_json["cards"]:
# 	cards.append(every)

# deck = set_json.get("cards")

# for i in cards:

# above code works for different json files than we're using

for cname in set_json:
	c = tp.clean_card_json(set_json[cname])
	if c != None:
		parsedCards.append(c)
	
with open(dest_path, 'w') as f:
	json.dump(parsedCards, f)