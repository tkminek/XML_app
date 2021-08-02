import fitz
import cv2 
import pytesseract
import numpy as np
from pytesseract import Output




def create_jpg(name):
    pdffile = "PDF/"+str(name)+".pdf"
    doc = fitz.open(pdffile)
    page = doc.loadPage(0)  # number of page
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

def vypis_txt(text,name):
    file_text=open("PDF/"+str(name)+".txt","w+",encoding='utf-8')
    file_text.write(text)
    file_text.close()
    


def main():
    name="faktura1"
    jpg=create_jpg(name)
    jpg_upravene=uprava_jpg(jpg)
    #cv2.imshow('image',jpg_upravene)
    #cv2.waitKey(0)
    text=pytesseract.image_to_string(jpg_upravene,lang='ces',config='--psm 6')
    vypis_txt(text,name)
    print("DONE")



        



if __name__ == '__main__':
    main()