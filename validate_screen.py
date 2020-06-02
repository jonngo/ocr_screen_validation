import argparse
import os
import cv2
from PIL import Image
from fuzzywuzzy import fuzz
from pytesseract import pytesseract

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, help="path to input image", required=True)
ap.add_argument("-t", "--text", type=str, help="text to match")
args = vars(ap.parse_args())

tesseract_path = 'C:\Program Files\Tesseract-OCR\\tesseract'
image_path = args["image"]
preprocess = ["blur",]
temp_img = "temp_img.jpg"
text_ref = args["text"]

# load the image and convert it to grayscale
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
if "thresh" in preprocess:
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
elif "blur" in preprocess:
    gray = cv2.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
cv2.imwrite(temp_img, gray)

# set path of tessaract
pyt = pytesseract
pyt.tesseract_cmd = tesseract_path

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pyt.image_to_string(Image.open(temp_img))
text = " ".join(text.split())

os.remove(temp_img)

#print the text extracted
print("Actual       : "+text)
print("Expected     : "+text_ref)

#get ratio
print("Accuracy     : "+str(fuzz.ratio(text_ref,text)))
