#Necessary Package
from imutils import paths
import numpy as np
import cv2
import os


def img_hash(image, hashSize=8):
	# convert the image to grayscale and resize the grayscale image,
	# adding a single column (width) so we can compute the horizontal
	# gradient
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (hashSize + 1, hashSize))

	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]

	# convert the difference image to a hash and return it
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


print("[Image Duplicate Detect and Remove]")
print()
IMG_DIR= input("Please Input the Image Directory :") or "D:\\FilteringDemoFile"
Path = list(paths.list_images(IMG_DIR))
print(Path)
hashes = {}
show_duplicate = 1
img_count = 0


for imagePath in Path:
	# load the input image and compute the hash
	image = cv2.imread(imagePath)
	h = img_hash(image)

	# grab all image paths with that hash, add the current image
	# path to it, and store the list back in the hashes dictionary
	p = hashes.get(h, [])
	p.append(imagePath)
	hashes[h] = p

for (h, hashedPaths) in hashes.items():
	# check to see if there is more than one image with the same hash
	if len(hashedPaths) > 1:
		# check to see if this is a dry run
		if show_duplicate == 1:
			# initialize a montage to store all images with the same
			# hash
			montage = None

			# loop over all image paths with the same hash
			for p in hashedPaths:
				# load the input image and resize it to a fixed width
				# and height
				
				
				image = cv2.imread(p)
				image = cv2.resize(image, (150, 150))

				# if our montage is None, initialize it
				if montage is None:
					montage = image

				# otherwise, horizontally stack the images
				else:
					montage = np.hstack([montage, image])

			# show the montage for the hash
			print("[INFO] hash: {}".format(h))
			cv2.imshow("Duplicated Image", montage)
			cv2.waitKey(0)

		# otherwise, we'll be removing the duplicate images
			# loop over all image paths with the same hash *except*
			# for the first image in the list (since we want to keep
			# one, and only one, of the duplicate images)
		for p in hashedPaths[1:]:
		 img_count = img_count +1
		 print("deleted : " + p)
		 os.remove(p)
		
if img_count == 0:
 print("no duplicate image found")
else:
 print("Operation Completed, deleted " +str(img_count)+ " Duplicated Image")
