# CNPJ pipeline creation

Project aiming the creation of a pipeline to import files from the site "https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj", treat them all and send to a database of choice.

# The Database

The database chose was a MYSQL 8.0 local server hosted by my own computer.
Due to the size of the file sent, an automated function to split and send the data in chunks was created (by defaut each chunk has 1000000 rows).

# FILE cnpj_empresas.py

It is the main file, coordenating the follow activities: 

  - Download of zip file through the URL;
  - Creation of file "raw_cnpj_empresas.csv" with raw data in csv format;
  - Treatment of data(setting column names, filling NULL values, setting column DataTypes...);
  - Send data to a SQL database; 

# FILE auxi_file.py

It's an auxiliary file which contains the functions and class needed to make cnpj_empresas.py run.

  - Class Database(): Set the connection with MYSQL server. It allows through its methods: table cleanning, creation of chunks and send data from python to the database;
  - Function download_unzip(): It is responsable for downloading the zip file through an URL and unziping it in the path chose.  


# FILE CNPJ_empresas.bat

This file can be used on windows task scheduler to set a periodical execution.

To execute the whole code, double click this file.


## FILE Requirements.txt

Execute this file in CMD to install the libraries needed to run the code.

The versions used were:
  - Python3.8
  - Pandas 1.4.1
  - wget 3.2
  - mysql-connector-python 2.2.9
  - pymysql 1.0.2

## Observations

The list below shows some topics that were not yet implemented:

  - Create .py files to treat and send data from SOCIOS and ESTABELECIMENTOS zip files to the database**

** Since tuesday, the download files from the URL provided(https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj) are offline. This problem kept me from downloading and consequently treating the SOCIO and ESTABELECIMENTO files.



