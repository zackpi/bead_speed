import cv2
from os import listdir
from os.path import isfile, join, dirname, realpath

# read files
currdir = dirname(realpath(__file__))
dir_suff = input("Directory of images: ")
img_dir = join(currdir, str(dir_suff))
img_files =sorted([join(img_dir, f) for f in listdir(img_dir) if isfile(join(img_dir, f))])

# function to mark beads
bead_index = 0
img_index = 0
MAX_BEADS = 10
bead_positions = [[(-1, -1) for j in range(MAX_BEADS)] for i in range(len(img_files))]

def bead_motion(event, x, y, flags, param):
	if event ==	cv2.EVENT_LBUTTONDOWN:
		bead_positions[img_index][bead_index] = (x, y)

cv2.namedWindow("bead_speed")
cv2.setMouseCallback("bead_speed", bead_motion)

# main loop
key = 0
while key != 27 and img_index < len(img_files):
	img = cv2.imread(img_files[img_index])
	cv2.putText(img, "img: " + str(img_index), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (64, 0, 64), 3)
	cv2.putText(img, "bead: " + str(bead_index), (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (64, 0, 64), 3)

	# draw bead positions
	if img_index > 0:
		for bi in range(MAX_BEADS):
			bead = bead_positions[img_index-1][bi]
			if bead != (-1, -1):
				cv2.putText(img, str(bi), (bead[0]+3, bead[1]+3), cv2.FONT_HERSHEY_SIMPLEX, .25, ((bi+1)*256/MAX_BEADS, 0, 0), 1)
				cv2.circle(img, bead, 2, ((bi+1)*256/MAX_BEADS, 0, 0))

		for bi in range(MAX_BEADS):
			bead1 = bead_positions[img_index-1][bi]
			bead2 = bead_positions[img_index][bi]
			if bead1 != (-1, -1) and bead2 != (-1, -1):
				cv2.line(img, bead1, bead2, ((bi+1)*256/MAX_BEADS, 0, 0))

	for bi in range(MAX_BEADS):
		bead = bead_positions[img_index][bi]
		if bead != (-1, -1):
			cv2.circle(img, bead, 5, ((bi+1)*256/MAX_BEADS, 0, 0), 2)

	cv2.imshow("bead_speed", img)
	key = cv2.waitKey(10)

	if (key == 83 or key == 100):
		img_index += 1
		bead_index = 0
	if (key == 81 or key == 97) and img_index > 0:
		img_index -= 1
		bead_index = 0
	if (key == 82 or key == 119) and bead_index < MAX_BEADS-1:
		bead_index += 1
	if (key == 84 or key == 115) and bead_index > 0:
		bead_index -= 1
	if key == 8 or key == 255:
		bead_positions[img_index][bead_index] = (-1, -1)

# print / save the data
print()
print("-- positions: -----------------")
print()

for bi in range(MAX_BEADS):
	pos_list = [bead_positions[i][bi] for i in range(len(img_files))]
	print("bead " + str(bi) + ":\t", ",\t".join(["\t---" if pos == (-1, -1) else str(pos) for pos in pos_list]))

print()
print("-- velocities: ----------------")
print()

for bi in range(MAX_BEADS):
	pos_list = [bead_positions[i][bi] for i in range(len(img_files))]
	vel_list = ["-"]
	for i in range(1, len(img_files)):
		if pos_list[i-1] != (-1, -1) and pos_list[i] != (-1, -1):
			velx = pos_list[i][0] - pos_list[i-1][0]
			vely = pos_list[i][1] - pos_list[i-1][1]
			vel_list.append((velx, vely))
		else:
			vel_list.append("\t---")
	print("bead " + str(bi) + ":\t", ",\t".join([str(vel) for vel in vel_list]))

print()
print("-------------------------------")
print()
