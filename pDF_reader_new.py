import fitz
import cv2 
import pytesseract
import numpy as np
from pytesseract import Output
import re
from re import finditer

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def pdf_page_number(name):
    doc = fitz.open(open("PDF/"+str(name)+".pdf"))
    number=doc.pageCount
    return(number)


def create_jpg(name,index):
    pdffile = "PDF/"+str(name)+".pdf"
    doc = fitz.open(pdffile)
    page = doc.loadPage(index)  # number of page
    pix = page.getPixmap(matrix=fitz.Matrix(300/72, 300/72))
    output = "PDF/"+str(name)+".jpg"
    pix.writePNG(output)
    return(output)


def uprava_jpg(jpg):
    image = cv2.imread(jpg)    
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    return(image)



def prijata_faktura_txt(name):
    number_pages=pdf_page_number(name)
    number_pages=1
    for index in range(0,number_pages):
        jpg=create_jpg(name,index)
        jpg_upravene=uprava_jpg(jpg)
        my_config=r'--oem 3 --psm 6 '
        text = pytesseract.image_to_string(jpg_upravene,lang='ces',config=my_config)
        #only for spyder start#
        arr = text.split('\n')[0:-1]        
        text = '\n'.join(arr)
        #only for spyder end#
        print(text)
        #print("---------------")
        #print(f"TXT file - Page number: {index} is DONE")    


   


def main():
    name="faktura1"
    prijata_faktura_txt(name)



if __name__ == '__main__':
    main()