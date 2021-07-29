import pandas as pd
from tqdm import tqdm,trange
from time import sleep
from ares_util.ares import call_ares
import os
import numpy

class ExcelInfo():
    def __init__(self,nazev,index,excel_list):
        self._nazev = nazev
        self._index = index
        self._excel = pd.read_excel("FACTURES/" + str(self._nazev) + ".xlsx", sheet_name=excel_list)
        self._df = pd.DataFrame(self._excel)
        self._datum_p = self._df.iloc[self._index].loc['Datum']
        self._castka= self._df.iloc[self._index].loc['Fremdwährung']
        self._cislo_faktury= self._df.iloc[self._index].loc['Referenz']
        self._datum= str(self._datum_p.split(".")[2]) + "-" + str(self._datum_p.split(".")[1]) + "-" + str(self._datum_p.split(".")[0])
        self._cislo_faktury2 = self._df.iloc[self._index].loc['Belegnr']

    def main_info(self):
        return {
                "datum":self._datum,
                "castka":self._castka,
                "cislo_faktury":self._cislo_faktury,
                "cislo_faktury2":self._cislo_faktury2,
                "nazev":self._nazev,
                "index":self._index
                }

    def vlastnik_info(self):
        return {
                "V_company":"GUSTAV KINDT GMBH",
                "V_city" : "ELLERAU",
                "V_street" : "Moortwiete",
                "V_number" : "8",
                "V_zip" : "254 79",
                "V_ico" : "682134908",
                "V_dic": "CZ682134908",
                "V_acount_number": "1390407379",
                "V_bank_code": "0800",
                "V_note" : "-"
                }
        
    def client_info(self):
        self._C_ico= self._df.iloc[self._index].loc['Ico']
        self._client_dict= call_ares(str(int(self._C_ico)))
        self._C_company= self._client_dict["legal"]["company_name"]
        self._C_city= self._client_dict["address"]["city"]
        self._C_street= self._client_dict["address"]["street"]
        self._C_zip= self._client_dict["address"]["zip_code"]
        self._C_dic= self._client_dict["legal"]["company_vat_id"]
        return {
                "C_ico":self._C_ico,
                "C_company": self._C_company,
                "C_city": self._C_city,
                "C_street": self._C_street,
                "C_zip": self._C_zip,
                "C_dic": self._C_dic
                }

class ExportXML():
    def __init__(self,main_dic,client_dic,vlastnik_dic,poc_cislo_faktury):
        self._poc_cislo_faktury=poc_cislo_faktury
        self._cislo_faktury=main_dic["cislo_faktury"]
        self._cislo_faktury2 = main_dic["cislo_faktury2"]
        self._datum = main_dic["datum"]
        self._nazev= main_dic["nazev"]
        self._index=main_dic["index"]
        self._castka = main_dic["castka"]
        self._C_ico = client_dic["C_ico"]
        self._C_company = client_dic["C_company"]
        self._C_city = client_dic["C_city"]
        self._C_street = client_dic["C_street"]
        self._C_zip = client_dic["C_zip"]
        self._C_dic = client_dic["C_dic"]
        self._V_ico = vlastnik_dic["V_ico"]
        self._V_company = vlastnik_dic["V_company"]
        self._V_city = vlastnik_dic["V_city"]
        self._V_street = vlastnik_dic["V_street"]
        self._V_number = vlastnik_dic["V_number"]
        self._V_zip = vlastnik_dic["V_zip"]
        self._V_dic = vlastnik_dic["V_dic"]
        self._V_note = vlastnik_dic["V_note"]
        self._V_acount_number = vlastnik_dic["V_acount_number"]
        self._V_bank_code = vlastnik_dic["V_bank_code"]

    def export_prijata_xml(self):
        file_temp=open("TEMP/TEMP_prijata.xml","r")
        facture_file=open("OUTPUT/"+str(self._nazev)+"_prijate.xml","a")
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
        facture_file=open("OUTPUT/"+str(self._nazev)+"_vydane.xml","a")
        if len(str(self._cislo_faktury))==3:
               self._cislo_faktury = self._cislo_faktury2
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
    facture_file=open("OUTPUT/"+str(facture_name)+".xml","w+")
    facture_file.write('<?xml version="1.0" encoding="Windows-1250"?>\n')
    facture_file.write('<dat:dataPack version="2.0" id="Usr01" ico="682134908" key="c63711ca-75a9-4c76-8fbf-f35940263e5a" programVersion="12804.4 (7.7.2021)" application="Transformace" note="Uživatelský export" xmlns:dat="http://www.stormware.cz/schema/version_2/data.xsd">\n')
    facture_file.close()
        
def end_info(facture_name):
    facture_file=open("OUTPUT/"+str(facture_name)+".xml","a")
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
        facture=ExcelInfo(facture_name,index_zacatku_prijate,excel_list)
        main_dic=facture.main_info()
        vlastnik_dic=facture.vlastnik_info()
        client_dic=facture.client_info()
        export_xml=ExportXML(main_dic,client_dic,vlastnik_dic,poc_cislo_faktury_prijate)
        export_xml.export_prijata_xml()
        poc_cislo_faktury_prijate+=1
        index_zacatku_prijate += 1
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
        facture = ExcelInfo(facture_name, index_zacatku_vydana, excel_list)
        main_dic = facture.main_info()
        vlastnik_dic = facture.vlastnik_info()
        client_dic = facture.client_info()
        export_xml = ExportXML(main_dic, client_dic, vlastnik_dic, poc_cislo_faktury_vydana)
        export_xml.export_vydana_xml()
        poc_cislo_faktury_vydana+=1
        index_zacatku_vydana+=1
        sleep(0.02)
    end_info(facture_name+"_vydane")
    print("XML FILE EXPORT : vydane faktury - DONE")

def main():
    path=os.getcwd()
    try:
        facture_name=os.listdir(path+"\FACTURES")[0].split(".")[:-1][0]
    except:
        print("NO FACTURE EXCEl FILE IN ...\FACTURES")
    #   PRIJATE FAKTURY   #
    prijate_faktury(excel_list="EK RCH", poc_cislo_faktury_prijate=1,facture_name=facture_name)
    #   VYDANE FAKTURY   #
    vydane_faktury(excel_list="VK RCH", poc_cislo_faktury_vydana=1, facture_name=facture_name)

if __name__ == '__main__':
    main()