import sys
import numpy as np

if len(sys.argv) != 2:
	print("Please put in src file.")
	quit()

src_path = sys.argv[1]

data_mat = 0
card_names = 0
attr_map = 0

with open(src_path, 'rb') as f:
	npy_file = np.load(f)
	data_mat = npy_file['data_mat']
	card_names = npy_file['card_names']
	attr_map = npy_file['attr_map']


for i in range(0,len(card_names)):
	for j in range(i+1,len(card_names)):
		# this is the way to find the euclidean distance between two matrices
		dist = np.linalg.norm(data_mat[i] - data_mat[j])
		print(card_names[i], " <-> ", card_names[j], ": ", dist)




