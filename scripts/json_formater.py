import sys
import json

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
	c = set_json[cname]
	if 'names' in c and c['names'] != []: continue

	if c.get("power") == "*":
		power = 0.0
	elif c.get("power") is None:
		power = -1
	else:
		power = float(c.get("power"))

	if c.get("toughness") == "*":
		toughness = 0.0
	elif c.get("toughness") is None:
		toughness = -1
	else:
		toughness = float(c.get("toughness"))

	card_info = {
		"colorIdentity": c.get("colorIdentity"),
		"colors": c.get("colors"),
		"convertedManaCost": c.get("convertedManaCost"),
		"name": c.get("name"),
		"power": power,
		"subtypes": c.get("subtypes"),
		"supertypes": c.get("supertypes"),
		"text": c.get("text"),
		"toughness": toughness,
		"type": c.get("type"),
		"types": c.get("types")
	}
	parsedCards.append(card_info)

with open(dest_path, 'w') as f:
		json.dump(parsedCards, f)