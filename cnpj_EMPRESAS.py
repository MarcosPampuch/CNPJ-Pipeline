# -*- coding: utf-8 -*-

##Marcos Pampuch

## FOR "CNPJ EMPRESAS" ##

import sys
import os
import pandas as pd

url = "http://200.152.38.155/CNPJ/K3241.K03200Y0.D20108.EMPRECSV.zip"
path = r"D:\Users\Marcos\Documents\teste"

sys.path.append(path)
#from database_class import Database, download_unzip
from auxi_file import Database, download_unzip

host="localhost" 
user = "root"
pw = "Pampuch" ### password to access MySQL server

db='roit_exercise'
table="cnpj_empresas"


#DOWNLOADING and UNZIPPING FILEs FROM LINK
file_path = download_unzip(url, path, path)


#STANDARDIZING: CREATING DATAFRAME AND STORING IT AS .csv

## Decoding .EMPRECSV file using ISO-8859-1
df_cnpj = pd.read_csv(file_path, sep=";", encoding = "ISO-8859-1", index_col=False, header=None)

n_rows = len(df_cnpj)


## Storing raw file in .csv format
raw_csv_path = os.path.join(path, "raw_cnpj_empresas.csv")
df_cnpj.to_csv(raw_csv_path, sep=";")

print("\nRaw CSV file stored in %s\n"%raw_csv_path)

########CONFORMING DATA
print("CONFORMING DATA..\n")

df_cnpj[5] = df_cnpj[5].fillna(0)        ##filling null values of field "5" with 0
df_cnpj[6] = df_cnpj[6].fillna("-")

# searcingh for null values in NOT NULL contraint columns
if df_cnpj.iloc[:,0:-2].isnull().values.any():
    print("\n Null values found in main columns \n")
    sys.exit(0)
    

## Transforming 4th column from "100,00" to "100.00" 
for ind in range(n_rows):
    df_cnpj.iloc[ind,4] = df_cnpj.iloc[ind,4].replace(",",".")
    

df_cnpj = df_cnpj.astype({4 : "float64"}) ## converting 4th column to float64


## Setting dataTypes of each column
df_cnpj = df_cnpj.astype({
        0 : "int32",
        1 : "object",
        2 : "int16",
        3 : "int8",
        4 : "int64",
        5 : "int8",
        6 : "object"})


# ### Naming columns
df_cnpj.rename(columns={0 : "cnpj_básico", 
                        1 : "razão_social", 
                        2 : "natureza_juridica",
                        3 : "qualificação_do_responsável",
                        4 : "capital_social_da_empresa",
                        5 : "porte_da_empresa",
                        6 : "ente_federativo_responsavel"}, inplace = True)



df_cnpj.sort_values("porte_da_empresa", inplace=True) ### Sorting by "PORTE DA EMPRESA"


df_cnpj.reset_index(inplace=True, drop=True)    ## reseting index

## APLICAÇÃO

print("\nSending to Database...\n")

##  Store dataframe in SQL database
connection = Database(db, host, user, pw)

connection.empty_table(table)

## Creating chunks or not depending on the size of the file
if n_rows > 1000000:
    chunks = connection.create_chunks(df_cnpj)
    connection.send_to_database(df_cnpj, table, chunks)
else:
    connection.send_to_database(df_cnpj, table)










