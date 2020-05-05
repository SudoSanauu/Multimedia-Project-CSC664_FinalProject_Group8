import sys
import numpy as np
import matplotlib.pyplot as plt
import mat_processing as matp


if len(sys.argv) != 2:
	print("Please put in src file.")
	quit()

src_path = sys.argv[1]

def is_value(in_str, cards_len):
	try: 
		x = int(in_str)
		return (x >= 0) and (x < cards_len)
	except ValueError:
		return False


data_mat = 0
card_names = 0
feature_map = 0

with open(src_path, 'rb') as f:
	npy_file = np.load(f)
	data_mat = npy_file['data_mat']
	card_names = npy_file['card_names']

	# the joys of renaming variables to things which make more sense
	feature_map = npy_file.get('feature_map')
	if not isinstance(feature_map, np.ndarray):
		feature_map = npy_file.get('attr_map')

# create distance matrix
dist_matrx = matp.create_distance_mat(data_mat)

in_str = ''
while in_str != 'q':
	in_str = input("Enter command (h or ? for help): ")
	if in_str == 'c': # get list of card names and indices
		for i in range(0,len(card_names)):
			print(i, ": ", card_names[i])

	elif is_value(in_str, len(card_names)): # print distances for one card
		i = int(in_str)
		print("distances for card ", i, " ", card_names[i])
		for j in range(0,len(card_names)):
			print("{0:30}{1:f}".format(card_names[j],dist_matrx[i][j]))
		
		fig = plt.figure()
		ax = fig.add_axes([0,0,1,1])
		ax.bar(card_names, dist_matrx[i])
		plt.show()

	elif in_str == 'p':  # print the distance matrix
		for i in range(0, len(dist_matrx)):
			print(['{:.2f}'.format(x) for x in dist_matrx[i]])

	elif in_str == 'd': # difference between mats
		print(matp.dist_mat_diff(dist_matrx))

	elif in_str == 'q':
		continue
	# if in_str == 'h' or in_str == '?':
	else: # help
		print("commands are: ")
		print('q: quit')
		print('h or ?: help menu')
		print('c: list the names and numbers of all the cards')
		print("a card's number: print the distances for that card")
		print("p: print table")



