import pandas as pd
from tqdm import tqdm,trange
from time import sleep
from ares_util.ares import call_ares
import os
import numpy

class FactureClass():
    def __init__(self,nazev,index,poc_cislo_faktury,excel_list):
        self._poc_cislo_faktury=poc_cislo_faktury
        self._nazev=nazev
        self._index=index
        self._excel = pd.read_excel("FACTURES/"+str(self._nazev)+".xlsx",sheet_name=excel_list) 
        self._df= pd.DataFrame(self._excel)
        datum_p=self._df.iloc[self._index].loc['Datum']
        self._castka=self._df.iloc[self._index].loc['Fremdwährung']
        self._cislo_faktury=self._df.iloc[self._index].loc['Referenz']
        self._poc_cislo_faktury=poc_cislo_faktury
        self._datum=str(datum_p.split(".")[2])+"-"+str(datum_p.split(".")[1])+"-"+str(datum_p.split(".")[0])

    def vlastnik_info(self):        
        self._V_company="GUSTAV KINDT GMBH"
        self._V_city="ELLERAU"
        self._V_street="Moortwiete"
        self._V_number="8"
        self._V_zip="254 79"
        self._V_ico ="682134908"
        self._V_dic="CZ682134908"
        self._V_acount_number="1390407379"
        self._V_bank_code="0800"
        self._V_note="-"
        
    def client_info(self):
        self._C_ico = self._df.iloc[self._index].loc['Ico']
        self._client_dict=call_ares(str(int(self._C_ico)))
        self._C_company=self._client_dict["legal"]["company_name"]
        self._C_city=self._client_dict["address"]["city"]
        self._C_street=self._client_dict["address"]["street"]
        self._C_zip=self._client_dict["address"]["zip_code"]
        self._C_dic=self._client_dict["legal"]["company_vat_id"]

    def export_prijata_xml(self):
        file_temp=open("TEMP/TEMP_prijata.xml","r")
        facture_file=open(str(self._nazev)+"_prijate.xml","a")
        for row in file_temp:
            zmena_dict={
                        "<typ:numberRequested>pohoda_facture_number</typ:numberRequested>": "<typ:numberRequested>"+str(self._poc_cislo_faktury)+"</typ:numberRequested>",
                        "<inv:symVar>facture_number</inv:symVar>":"<inv:symVar>"+str(self._cislo_faktury)+"</inv:symVar>",
                        "<inv:originalDocument>facture_number</inv:originalDocument>":"<inv:originalDocument>"+str(self._cislo_faktury)+"</inv:originalDocument>",
                        "<inv:date>datum</inv:date>":"<inv:date>"+str(self._datum)+"</inv:date>",
                        "<inv:dateTax>datum</inv:dateTax>":"<inv:dateTax>"+str(self._datum)+"</inv:dateTax>",
                        "<inv:dateDue>datum</inv:dateDue>":"<inv:dateDue>"+str(self._datum)+"</inv:dateDue>",
                        "<typ:company>C_firm</typ:company>":"<typ:company>"+str(self._C_company)+"</typ:company>",
                        "<typ:city>C_city</typ:city>":"<typ:city>"+str(self._C_city)+"</typ:city>",
                        "<typ:street>C_street</typ:street>":"<typ:street>"+str(self._C_street)+"</typ:street>",
                        "<typ:zip>C_zip</typ:zip>":"<typ:zip>"+str(self._C_zip)+"</typ:zip>",
                        "<typ:ico>C_ico</typ:ico>":"<typ:ico>"+str(self._C_ico)+"</typ:ico>",
                        "<typ:dic>C_dic</typ:dic>":"<typ:dic>"+str(self._C_dic)+"</typ:dic>",
                        "<typ:company>V_firm</typ:company>":"<typ:company>"+str(self._V_company)+"</typ:company>",
                        "<typ:city>V_city</typ:city>":"<typ:city>"+str(self._V_city)+"</typ:city>",
                        "<typ:street>V_street</typ:street>":"<typ:street>"+str(self._V_street)+"</typ:street>",
                        "<typ:number>V_number</typ:number>":"<typ:number>"+str(self._V_number)+"</typ:number>",
                        "<typ:zip>V_zip</typ:zip>":"<typ:zip>"+str(self._V_zip)+"</typ:zip>",
                        "<typ:ico>V_ico</typ:ico>":"<typ:ico>"+str(self._V_ico)+"</typ:ico>",
                        "<typ:dic>V_dic</typ:dic>":"<typ:dic>"+str(self._V_dic)+"</typ:dic>",
                        "<typ:accountNo>V_acount_number</typ:accountNo>":"<typ:accountNo>"+str(self._V_acount_number)+"</typ:accountNo>",
                        "<typ:bankCode>V_bank_code</typ:bankCode>":"<typ:bankCode>"+str(self._V_bank_code)+"</typ:bankCode>",
                        "<inv:note>V_note</inv:note>":"<inv:note>"+str(self._V_note)+"</inv:note>",
                        "<typ:amountHome>V_amount</typ:amountHome>":"<typ:amountHome>"+str(self._castka)+"</typ:amountHome>",
                        "<typ:priceNone>V_price</typ:priceNone>":"<typ:priceNone>"+str(self._castka)+"</typ:priceNone>"
                    }
            if row.strip() in zmena_dict: 
                novy_radek=row.replace(row.strip(),zmena_dict[row.strip()])
                facture_file.write(novy_radek)
            else:
                facture_file.write(row)
        facture_file.close()
        file_temp.close()
    def export_vydana_xml(self):
        file_temp=open("TEMP/TEMP_vydana.xml","r")
        facture_file=open(str(self._nazev)+"_vydane.xml","a")
        if len(str(self._cislo_faktury))==3:
               self._cislo_faktury = self._df.iloc[self._index].loc['Belegnr']
        for row in file_temp:
            zmena_dict={
                        "<typ:numberRequested>pohoda_facture_number</typ:numberRequested>":"<typ:numberRequested>"+str(self._poc_cislo_faktury)+"</typ:numberRequested>",
                        "<inv:symVar>pohoda_facture_number</inv:symVar>":"<inv:symVar>"+str(self._poc_cislo_faktury)+"</inv:symVar>",
                        "<inv:date>datum</inv:date>": "<inv:date>" + str(self._datum) + "</inv:date>",
                        "<inv:dateTax>datum</inv:dateTax>": "<inv:dateTax>" + str(self._datum) + "</inv:dateTax>",
                        "<inv:dateDue>datum</inv:dateDue>": "<inv:dateDue>" + str(self._datum) + "</inv:dateDue>",
                        "<inv:numberKHDPH>facture_number</inv:numberKHDPH>":"<inv:numberKHDPH>"+str(self._cislo_faktury)+"</inv:numberKHDPH>",
                        "<typ:company>C_firm</typ:company>":"<typ:company>" + str(self._C_company) + "</typ:company>",
                        "<typ:city>C_city</typ:city>": "<typ:city>" + str(self._C_city) + "</typ:city>",
                        "<typ:street>C_street</typ:street>": "<typ:street>" + str(self._C_street) + "</typ:street>",
                        "<typ:zip>C_zip</typ:zip>": "<typ:zip>" + str(self._C_zip) + "</typ:zip>",
                        "<typ:ico>C_ico</typ:ico>": "<typ:ico>" + str(self._C_ico) + "</typ:ico>",
                        "<typ:dic>C_dic</typ:dic>": "<typ:dic>" + str(self._C_dic) + "</typ:dic>",
                        "<typ:company>V_firm</typ:company>": "<typ:company>" + str(self._V_company) + "</typ:company>",
                        "<typ:city>V_city</typ:city>": "<typ:city>" + str(self._V_city) + "</typ:city>",
                        "<typ:street>V_street</typ:street>": "<typ:street>" + str(self._V_street) + "</typ:street>",
                        "<typ:number>V_number</typ:number>": "<typ:number>" + str(self._V_number) + "</typ:number>",
                        "<typ:zip>V_zip</typ:zip>": "<typ:zip>" + str(self._V_zip) + "</typ:zip>",
                        "<typ:ico>V_ico</typ:ico>": "<typ:ico>" + str(self._V_ico) + "</typ:ico>",
                        "<typ:dic>V_dic</typ:dic>": "<typ:dic>" + str(self._V_dic) + "</typ:dic>",
                        "<typ:date>V_date</typ:date>":"<typ:date>"+str(self._datum)+"</typ:date>",
                        "<typ:priceNone>V_price</typ:priceNone>":"<typ:priceNone>"+str(-1*(self._castka))+"</typ:priceNone>"
                    }
            if row.strip() in zmena_dict:
                novy_radek=row.replace(row.strip(),zmena_dict[row.strip()])
                facture_file.write(novy_radek)
            else:
                facture_file.write(row)
        facture_file.close()
        file_temp.close()

def start_info(facture_name):
    facture_file=open(str(facture_name)+".xml","w+")
    facture_file.write('<?xml version="1.0" encoding="Windows-1250"?>\n')
    facture_file.write('<dat:dataPack version="2.0" id="Usr01" ico="682134908" key="c63711ca-75a9-4c76-8fbf-f35940263e5a" programVersion="12804.4 (7.7.2021)" application="Transformace" note="Uživatelský export" xmlns:dat="http://www.stormware.cz/schema/version_2/data.xsd">\n')
    facture_file.close()
        
def end_info(facture_name):
    facture_file=open(str(facture_name)+".xml","a")
    facture_file.write('\n</dat:dataPack>')
    facture_file.close()
        
def excel_info(facture_name,excel_list):
    excel = pd.read_excel("FACTURES/"+str(facture_name)+".xlsx",sheet_name=excel_list)
    index_konce = excel.shape[0]
    return(index_konce)

def prijate_faktury(excel_list,poc_cislo_faktury_prijate,facture_name):
    index_zacatku_prijate=0
    index_konce_prijate=excel_info(facture_name,excel_list)
    start_info(facture_name+"_prijate")
    p_bar= tqdm([x for x in range(index_zacatku_prijate,index_konce_prijate-1)])
    for i in p_bar:
        info=f"Faktura prijata cislo: {i+2}"
        p_bar.set_description("Processing %s" %info)
        facture=FactureClass(facture_name,i,poc_cislo_faktury_prijate,excel_list)
        facture.vlastnik_info()
        facture.client_info()
        facture.export_prijata_xml()
        poc_cislo_faktury_prijate+=1
        sleep(0.02)
    end_info(facture_name+"_prijate")
    print("XML FILE EXPORT : prijate faktury - DONE")

def vydane_faktury(excel_list, poc_cislo_faktury_vydana,facture_name):
    index_zacatku_vydana=0
    index_konce_vydana=excel_info(facture_name,excel_list)
    start_info(facture_name+"_vydane")
    p_bar= tqdm([x for x in range(index_zacatku_vydana,index_konce_vydana-1)])
    for i in p_bar:
        info=f"Faktura vydana cislo: {i+2}"
        p_bar.set_description("Processing %s" %info)
        facture=FactureClass(facture_name,i,poc_cislo_faktury_vydana,excel_list)
        facture.vlastnik_info()
        facture.client_info()
        facture.export_vydana_xml()
        poc_cislo_faktury_vydana+=1
        sleep(0.02)
    end_info(facture_name+"_vydane")
    print("XML FILE EXPORT : vydane faktury - DONE")

def main():
    path=os.getcwd()
    facture_name=os.listdir(path+"\FACTURES")[0].split(".")[:-1][0]
    #   PRIJATE FAKTURY   #
    prijate_faktury(excel_list="EK RCH", poc_cislo_faktury_prijate=1,facture_name=facture_name)
    #   VYDANE FAKTURY   #
    vydane_faktury(excel_list="VK RCH", poc_cislo_faktury_vydana=1, facture_name=facture_name)

if __name__ == '__main__':
    main()