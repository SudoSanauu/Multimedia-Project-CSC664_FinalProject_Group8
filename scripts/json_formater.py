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
	if ('names' in c) and (c['names'] != []):
		continue

	power = c.get("power", -1.0)
	if power == "*":
		power = 0.0
	else:
		power = float(power)

	toughness = c.get("toughness", -1.0)
	if toughness == "*":
		toughness = 0.0
	else:
		toughness = float(toughness)

	card_info = {
		"colorIdentity": c.get("colorIdentity",[]),
		"colors": c.get("colors",[]),
		"convertedManaCost": c.get("convertedManaCost",0),
		"manaCost": c.get("manaCost", ""),
		"name": c.get("name",""),
		"power": power,
		"subtypes": c.get("subtypes",[]),
		"supertypes": c.get("supertypes",[]),
		"text": c.get("text",""),
		"toughness": toughness,
		"type": c.get("type"),
		"types": c.get("types",[])
	}
	parsedCards.append(card_info)

with open(dest_path, 'w') as f:
		json.dump(parsedCards, f)