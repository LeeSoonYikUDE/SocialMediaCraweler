import argparse
from imutils import paths
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import cv2
import os
import easyocr
from langdetect import detect, language
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree
from scipy.misc import face
import timeit

start = timeit.default_timer()


#Function to compare to images and show the SSIM result
def compare_images(imageA, imageB,Path1,Path2,shw):
    # compute the structural similarity
    s = ssim(imageA, imageB)
    title="image compare"
    if shw == 1:
        fig = plt.figure(title)
        plt.suptitle("%s, %s , Similarity: %.2f" % (Path1,Path2,s))
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(imageA, cmap = plt.cm.gray)
        plt.axis("off")
        ax = fig.add_subplot(1, 2, 2)
        plt.imshow(imageB, cmap = plt.cm.gray)
        plt.axis("off")
        plt.show()    
    return s


#function to detect the duplication and near duplication in images
def duplicate_remove(rem,path):
 print(rem)
 print("Executing duplication and near duplication")
 if rem == True:
     print("Delete once detected : True")
 else:
     print("Delete once detected : False")
 
 #List out every images in the directory
 Path = list(paths.list_images(path))

 #If you dont't want to show the duplicate, put 0
 show_duplicate = 0
 # change the tolerance when necessary, 1 is duplicate, the less the number, the less the similarity
 d_limit= 0.9


 list_len = len(Path)
 rmlist= []
 #Compare every images in the specified directory
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
             result= compare_images(img1,img2,os.path.basename(Path[i]),os.path.basename(Path[j]),show_duplicate)
             print("SSIM :" + str(result))
             if result > d_limit :
                 rmlist.append(Path[j])
 
 #Part to remove or not remove detected images
 rmlist= set(rmlist)
 if rem == "y":
     for r in rmlist:
         print("Duplication detected and removed : " + r)
         os.remove(r)
 else:
     for r in rmlist:
         print("Duplication detected : " + r)





def only_text_remove(rem,path):
    print("Executing only text image detection")

    #tolerance index

    cmax = 115

    # borrow a list of named colors from matplotlib
    use_colors = colors.cnames
    # translate hexstring to RGB tuple
    named_colors = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3*(16,)))
                for k, v in use_colors.items()}
    ncol = len(named_colors)
    # make an array containing the RGB values 
    color_tuples = list(named_colors.values())
    color_tuples = np.array(color_tuples)
    color_names = list(named_colors)

    
    Path = list(paths.list_images(path))
    for imagePath in Path:
        # get example picture
        img = cv2.imread(imagePath)
        img = cv2.resize(img, (150,150))
        tree = KDTree(color_tuples[:-1])
        # tolerance for color match `inf` means use best match no matter how bad it may be
        tolerance = np.inf
        # find closest color in tree for each pixel in picture
        dist, idx = tree.query(img, distance_upper_bound=tolerance)
        # count and reattach names
        counts = dict(zip(color_names, np.bincount(idx.ravel(), None, ncol+1)))
        #count the number of color element which are 0
        a= list(counts.values())
        elm_count = a.count(0)
        print(imagePath + " index ： " + str(elm_count))
        if elm_count > cmax:
            print(imagePath + "  Potentially contain only text with index of " + str(elm_count) )
            if rem =='y':
                os.remove(imagePath)


def lang_detect(img_path):
 result = reader.readtext( img_path ,detail = 0, paragraph=True)
 #check the text, return 1(not german) if no text or less word is detected
 if result == [] :
     print("No text detected")
     return 1

 
 count = 0
 print(result)
 for item in result:
      count = count + len(item.split())
 print("total number of words : "  + str(count))
 if count >30 :
     return 1
 if count < 2 :
     return 1

 try:
        language = detect(str(result))
 except:
        language = "error"
        return 1
 


 if language == "de":
  return 0
 else:
  return 1




#function to detect non-german text or no text in images
def nonGermantext_remove(rem,path):
    print("Executing non German or no text image detection")

 
    Path = list(paths.list_images(path))

    
    for imagePath in Path:
        image = lang_detect(imagePath)
        if image == 1:
            print(imagePath +" contain either non German or no text")
            print("-------------------------")
            if rem == 'y':
                os.remove(imagePath)
        else :
            print(imagePath + " contain german text")
            print("-------------------------")



# Argument Parser statement
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str, required=True,
    help="Directory path to the images")
ap.add_argument("-r", "--remove", type=str.lower, required=True,default="N",
    choices=["Y", "N","y","n"],
    help="Option whether to remove once dirtiness of image data detected")
ap.add_argument("-d", "--duplicate", action='store_true',
    help="Detect duplicates and near duplicates in the directory")
ap.add_argument("-l", "--language",action='store_true',
    help="Remove images that are not in German language")
ap.add_argument("-t", "--text", action='store_true',
    help="Remove images with only text")

args = ap.parse_args()



if __name__ == '__main__':
    if args.duplicate == True:
        duplicate_remove(args.remove, args.path)
    if args.text == True:
        only_text_remove(args.remove, args.path)
    if args.language == True:
        #if you have GPU supported PC, change gpu to True
        reader = easyocr.Reader(['de','en'], gpu = False)
        nonGermantext_remove(args.remove, args.path)


stop = timeit.default_timer()


#to calculate run time for better efficiency
print('Total Time Taken: ', stop - start)  
        
