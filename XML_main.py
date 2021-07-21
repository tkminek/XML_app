import pandas as pd



class FactureClass():
    def __init__(self,nazev,index,poc_cislo_faktury):
        self._nazev=nazev
        self._index=index
        self._excel = pd.read_excel("FACTURES/"+str(self._nazev)+".xlsx",sheet_name='EK RCH') 
        self._df= pd.DataFrame(self._excel)
        datum_p=self._df.iloc[index].loc['Datum']
        self._castka=self._df.iloc[index].loc['Fremdwährung']
        self._cislo_faktury=self._df.iloc[index].loc['Referenz']
        self._poc_cislo_faktury=poc_cislo_faktury
        self._datum=str(datum_p.split(".")[2])+"-"+str(datum_p.split(".")[1])+"-"+str(datum_p.split(".")[0])

    def client_info(self):
        self._C_ico = self._df.iloc[self._index].loc['Ico']
        self._C_company="Pepa Novotny .sro"
        self._C_city="Frýdeku-Místek"
        self._C_street="Zelena 328"
        self._C_zip="987654321"
        self._C_dic="999999"

    def export_xml(self):
        file_temp=open("TEMP/TEMP_prijata.xml","r")
        facture_file=open(str(self._nazev)+".xml","w+")
        for row in file_temp:
            zmena_dict={
                        "<typ:numberRequested>21F0742</typ:numberRequested>": "<typ:numberRequested>1</typ:numberRequested>",
                        "<inv:symVar>110210043</inv:symVar>":"<inv:symVar>"+str(self._cislo_faktury)+"</inv:symVar>",
                        "<inv:originalDocument>110210043</inv:originalDocument>":"<inv:originalDocument>"+str(self._cislo_faktury)+"</inv:originalDocument>",
                        "<inv:date>2021-06-04</inv:date>":"<inv:date>"+str(self._datum)+"</inv:date>",
                        "<inv:dateTax>2021-06-04</inv:dateTax>":"<inv:dateTax>"+str(self._datum)+"</inv:dateTax>",
                        "<inv:dateDue>2021-07-04</inv:dateDue>":"<inv:dateDue>"+str(self._datum)+"</inv:dateDue>",
                        "<typ:company>Statek Miroslav, a.s.</typ:company>":"<typ:company>"+str(self._C_company)+"</typ:company>",
                        "<typ:city>Miroslav</typ:city>":"<typ:city>"+str(self._C_city)+"</typ:city>",
                        "<typ:street>Kašenec 870</typ:street>":"<typ:street>"+str(self._C_street)+"</typ:street>",
                        "<typ:zip>671 72</typ:zip>":"<typ:zip>"+str(self._C_zip)+"</typ:zip>",
                        "<typ:ico>46983775</typ:ico>":"<typ:ico>"+str(self._C_ico)+"</typ:ico>",
                        "<typ:dic>CZ682134908</typ:dic>":"<typ:dic>"+str(self._C_dic)+"</typ:dic>"
                    }

            if row.strip() in zmena_dict:
                novy_radek=row.replace(row.strip(),zmena_dict[row.strip()])
                facture_file.write(novy_radek)
                print(novy_radek)
            else:
                facture_file.write(row)



        facture_file.close()
        file_temp.close()


def main():
    facture_name="doklady-CZ-06_2021-DPH"
    poc_cislo_faktury="1"
    index_zacatku=14
    facture=FactureClass(facture_name,index_zacatku,poc_cislo_faktury)
    facture.client_info()
    facture.export_xml()
    print("DONE")





if __name__ == '__main__':
    main()