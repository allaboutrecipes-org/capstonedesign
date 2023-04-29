import numpy as np
from pytesseract import Output
import pytesseract
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
filename = 'C:\\Users\\JUNYEOP\\allaboutrecipes\\receipt\\nc.jpg'
img_nparray=np.array(Image.open(filename))
text=pytesseract.image_to_string(Image.open(filename), lang="kor")

'''
norm_img = np.zeros((img_nparray.shape[0],img_nparray.shape[1]))
img=cv2.normalize(img_nparray,norm_img,0.255,cv2.NORM_MINMAX)
img=cv2.threshold(img,100,255,cv2.THRESH_BINARY)[1]
img=cv2.GaussianBlur(img,(1,1),0)
print(img)'''

print(text)