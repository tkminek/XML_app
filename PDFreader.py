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
    for index in range(0,number_pages):
        jpg=create_jpg(name,index)
        jpg_upravene=uprava_jpg(jpg)
        #my_config='--psm 1'
        my_config='--psm 6'
        text=pytesseract.image_to_string(jpg_upravene,lang='ces',config=my_config)
        #only for spyder start#
        arr = text.split('\n')[0:-1]        
        text = '\n'.join(arr)
        #only for spyder end#
        vypis_txt(text,name)
        print("---------------")
        print(f"TXT file - Page number: {index} is DONE")


   

def cisla_faktury(name):
    file_text=open("PDF/"+str(name)+".txt","r",encoding='utf-8')
    cisla_faktury=[]
    cisla_faktury_ident=["daňový doklad","danovy doklad","danový doklad","číslo faktury","cislo faktury","císlo faktury"]
    for index,line in enumerate(file_text):        
        if any(x in line.lower() for x in cisla_faktury_ident):
            cisla_faktury_n=[int(s) for s in [char for char in line] if s.isdigit()]            
            cisla_faktury_n=''.join(str(e) for e in cisla_faktury_n)
            if cisla_faktury_n!="":
                cisla_faktury.append(cisla_faktury_n)
    file_text.close()             
    return(cisla_faktury) 

def dodavatel(name):
    file_text=open("PDF/"+str(name)+".txt","r",encoding='utf-8')
    dodavatel=[]
    file_text.close()             
    return(dodavatel)


def ica_faktury(name,d_start,d_konec):
    file_text=open("PDF/"+str(name)+".txt","r",encoding='utf-8')
    ica_faktury=[]
    ica_faktury_ident=["ič:","ic:","ičo:","ico:"]
    for index,line in enumerate(file_text):      
        if any(x in line.lower() for x in ica_faktury_ident) and index>=d_start and index<=d_konec:
            ica_faktury_n=[s for s in line.split() if s.isdigit()]
            if ica_faktury_n!=[] and ica_faktury_n[0] not in ica_faktury:
                ica_faktury.append(ica_faktury_n[0])
            
    file_text.close()     
    return(ica_faktury) 

def faktura_zpracovani(name):
    d_start=600
    d_konec=1000
    cisla_faktury_list=cisla_faktury(name)
    ica_faktury_list=ica_faktury(name,d_start,d_konec)
    print(cisla_faktury_list)
   


def main():
    name="faktury_prijate"
    #prijata_faktura_txt(name)
    faktura_zpracovani(name)

    #cv2.imshow('image',jpg_upravene)
    #cv2.waitKey(0)


if __name__ == '__main__':
    main()