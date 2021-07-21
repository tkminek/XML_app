import pandas as pd


class FactureClass():
    def __init__(self,nazev,index):
        self._nazev=nazev
        self._index=index
        self._excel = pd.read_excel("FACTURES/"+str(self._nazev)+".xlsx",sheet_name='EK RCH') 
        df= pd.DataFrame(self._excel)
        self._datum=df.iloc[index].loc['Datum']
        self._belegrn=df.iloc[index].loc['Belegnr']
        self._text=df.iloc[index].loc['Text']
        self._gegenkto=df.iloc[index].loc['Gegenkto']
        self._fremdwahrung=df.iloc[index].loc['Fremdwährung']
        self._betrag=df.iloc[index].loc['Betrag']
        self._stsatz=df.iloc[index].loc['Stsatz']
        self._konto=df.iloc[index].loc['Konto']
        self._Jahr=df.iloc[index].loc['Jahr']
        self._Periode=df.iloc[index].loc['Periode']

        
    def export_xml(self):
        file_temp=open("TEMP/TEMP1.xml","r")
        facture_file=open(str(self._nazev)+".xml","w+")
        for row in file_temp:
            zmena="<inv:text>Nákup zboží</inv:text>"
            if zmena in row:
                row_novy=row.replace("Nákup zboží","testiiiicek")
                print(row_novy)
                facture_file.write(row_novy)
            else:    
                facture_file.write(row)
        
        facture_file.close()
        file_temp.close()


def main():
    print("ahoj")
    #facture_name="doklady-CZ-06_2021-DPH"
    #facture=FactureClass(facture_name,14)
    #facture.export_xml()





if __name__ == '__main__':
    main()