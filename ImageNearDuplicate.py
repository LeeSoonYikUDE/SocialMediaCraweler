# USAGE
# python compare.py

# import the necessary packages
from imutils import paths
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import cv2
import os

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB,Path1,Path2):
	# compute the mean squared error and structural similarity
	# index for the images
	#m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	m=1
	title="image compare"
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("%s, %s , Similarity: %.2f" % (Path1,Path2,s))

	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")

	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")

	# show the images
	#plt.show()
	return s

IMG_DIR= input("Please Input the Image Directory :") or "D:\FilteringDemoFile"
Path = list(paths.list_images(IMG_DIR))
show_duplicate = 1
img_count = 0

list_len = len(Path)
rmlist= []
for i in range(0,list_len):
	print('--------------------')
	print('round', i)

	current_idx = i + 1
	if current_idx < list_len:
		for j in range(current_idx,list_len):
			print(Path[i], "compare with", Path[j])
			img1 = cv2.imread(Path[i])
			img2 = cv2.imread(Path[j])
			img1= cv2.resize(img1, (200,200))
			img2= cv2.resize(img2, (200,200))
			img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
			img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
			result= compare_images(img1,img2,os.path.basename(Path[i]),os.path.basename(Path[j]))
			print(result)
			if result > 0.9 :
				rmlist.append(Path[j])
rmlist= set(rmlist)
for r in rmlist:
	os.remove(r)
	