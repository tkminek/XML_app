import fitz
import cv2 
import pytesseract
import numpy as np
from pytesseract import Output

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

def vypis_txt(text,name):
    file_text=open("PDF/"+str(name)+".txt","a+",encoding='utf-8')
    file_text.write(text)
    file_text.close()

def prijata_faktura_txt(name):
    number_pages=pdf_page_number(name)
    number_pages=1
    for index in range(0,number_pages):
        jpg=create_jpg(name,index)
        jpg_upravene=uprava_jpg(jpg)
        my_config=r"--psm 4"
        #my_config='--psm 6'
        text=pytesseract.image_to_string(jpg_upravene,lang='ces',config=my_config)
        #only for spyder start#
        arr = text.split('\n')[0:-1]        
        text = '\n'.join(arr)
        #only for spyder end#
        vypis_txt(text,name)
        print("---------------")
        print(f"TXT file - Page number: {index} is DONE")    

def info_txt(name):    
    file_text=open("PDF/"+str(name)+".txt","r",encoding='utf-8')
    dodavatel_list=[]
    odberatel_list=[]
    odberatel_ident=["odberatel","odběratel"]
    dodavatel_ident=["dodavatel"]
    for index,line in enumerate(file_text):        
        if any(x in line.lower() for x in odberatel_ident):
            odberatel_list.append(index)
        elif any(x in line.lower() for x in dodavatel_ident):
            dodavatel_list.append(index)   
            
    return(dodavatel_list,odberatel_list)        

def faktura_zpracovani(name):
    dodavatel,odberatel=info_txt(name)
    print(f"dodavatel : {dodavatel}")
    print(f"odberatel : {odberatel}")
   


def main():
    name="faktury_prijate"
    prijata_faktura_txt(name)
    #faktura_zpracovani(name)

    #cv2.imshow('image',jpg_upravene)
    #cv2.waitKey(0)


if __name__ == '__main__':
    main()