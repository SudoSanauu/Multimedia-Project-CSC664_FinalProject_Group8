import sys
import json

if len(sys.argv) != 3:
    print("Please put in src file and destination file.")
    quit()

src_path = sys.argv[1]
dest_path = sys.argv[2]

print(src_path)
print(dest_path)

with open(src_path, 'r', encoding="utf8") as f:
    set_json = json.load(f)

parsedCards = []
cards = []

for every in set_json["cards"]:
	cards.append(every)

deck = set_json.get("cards")

for i in cards:
	card = deck[i]
	if card.get("power") == "*":
		power = 0.0
	elif card.get("power") is None:
		power = -1
	else:
		power = card.get("power")

	if card.get("toughness") == "*":
		toughness = 0.0
	elif card.get("toughness") is None:
		toughness = -1
	else:
		toughness = card.get("toughness")

	card_info = {"colorIdentity": card.get("colorIdentity"),
	"colors": card.get("colors"),
	"convertedManaCost": card.get("convertedManaCost"),
	"name": card.get("name"),
	"power": power,
	"subtypes": card.get("subtypes"),
	"supertypes": card.get("supertypes"),
	"text": card.get("text"),
	"toughness": toughness,
	"type": card.get("type"),
	"types": card.get("types")
	}
	parsedCards.append(card_info)

with open(dest_path, 'w') as f:
		json.dump(parsedCards, f)