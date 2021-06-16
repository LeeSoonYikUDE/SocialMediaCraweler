import easyocr
from langdetect import detect, language
from imutils import paths
import os

def lang_detect(img_path):
 result = reader.readtext( img_path ,detail = 0, paragraph=True)
 if result == [] :
     print("[]")
     return 1
 language = detect(str(result))
 print(result)
 if language == "de":
  return 0
 else:
  return 1


print("[Image Text Detect and Remove]")
print()
IMG_DIR= input("Please Input the Image Directory :") or "D:\\test3"
reader = easyocr.Reader(['de','en'], gpu = False)
Path = list(paths.list_images(IMG_DIR))
show_duplicate = 1
img_count = 0


for imagePath in Path:
 # load the input image and compute the hash
 image = lang_detect(imagePath)
 if image == 1:
     print("this is either not german or no text")
     os.remove(imagePath)
 else :
     print("this is german")
     










