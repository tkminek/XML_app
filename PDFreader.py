from pdf2jpg import pdf2jpg
import shutil


facture_name="faktura1.pdf"
inputpath = "PDF/"+str(facture_name)
outputpath = r"PDF"
# To convert single page
result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="0")
print(result[0]["output_jpgfiles"][0])
shutil.move(result[0]["output_jpgfiles"][0], "PDF/faktura1.pdf.jpg")


