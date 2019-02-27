import csv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#Carga y manejo de datos
id=pd.read_csv("BASE_ID.txt",delimiter="\t")
id.CLIENTE_CC=id.iloc[:,0].str.replace(',00', '').astype(int)
id=id.drop(id[id.FECHA_NACIMIENTO == '0001-01-01'].index)
id['FECHA_NACIMIENTO']=pd.to_datetime(id['FECHA_NACIMIENTO'], format='%Y%m%d')
id.fuga=id.fuga.fillna(0) 
id.MES_DE_FUGA=id.MES_DE_FUGA.fillna(0)
#id['FECHA_ALTA'] =pd.to_datetime(id['FECHA_ALTA'], format='%b%d%Y')
#Valores únicos
id['SEXO']=id['SEXO'].replace(['HOMBRE','masculino','varón','Masc.','M'], 'Hombre')
id['SEXO']=id['SEXO'].replace(['F','mujer','femenino','FEMENINO','MUJER'], 'Mujer')
id['ESTADO_CIVIL']=id['ESTADO_CIVIL'].replace(['SEPARADO'],'DIVORCIADO')
id['SITUACION_LABORAL']=id['SITUACION_LABORAL'].replace('otros','OTROS')
id['SITUACION_LABORAL']=id['SITUACION_LABORAL'].replace('Contrato fijo','CONTRATO FIJO')
id['SITUACION_LABORAL']=id['SITUACION_LABORAL'].replace('contrato autonomo.','CONTRATO AUTONOMO')
id['SITUACION_LABORAL']=id['SITUACION_LABORAL'].replace('temporal     ','CONTRATO TEMPORAL')
#Estandarización de valores
id.SITUACION_LABORAL = id.SITUACION_LABORAL.map({'OTROS' : 1,'CONTRATO FIJO' : 2,'CONTRATO AUTONOMO' : 3,' desconocido   ' : 4,'CONTRATO TEMPORAL' : 5,'SIN CLASIFICAR' : 6})
id.ESTADO_CIVIL = id.ESTADO_CIVIL.map({'CASADO' : 1,'UNION LIBRE' : 2,'SOLTERO' : 3,'DIVORCIADO' : 4, 'VIUDO' : 5})
id.SEXO = id.SEXO.map({'Mujer' : 1,'Hombre' : 2})
#Base movimientos
mov=pd.read_fwf("BASE_MOVIMIENTOS.txt")
mov['FECHA_INFORMACION'] =pd.to_datetime(mov['FECHA_INFORMACION'], format='%d%b%Y:%H:%M:%S')
mov.sort_values(['ID','FECHA_INFORMACION'])
vMov=mov.values

#Matriz de correlación movimientos
sns.heatmap(mov.corr(), annot=True, linewidths=.5, fmt= '.2f')
plt.show()
#Matriz de correlación clientes
sns.heatmap(id.corr(), annot=True, linewidths=.5, fmt= '.2f')
plt.show()

#Cruce de bases de datos
new=pd.merge(mov, id, left_on='ID', right_on='CLIENTE_CC')
new.drop(['CLIENTE_CC'], axis='columns', inplace=True)
new.sort_values(['ID','FECHA_INFORMACION'])
sns.heatmap(new.corr(), annot=True, linewidths=.5, fmt= '.2f')
plt.show()
new.to_csv('new.csv')
#Transacciones de los clientes
mov.plot(kind='scatter',x='ID',y='SALDO_AHORROS',color='red')
plt.show()


mov['FECHA_INFORMACION'].map(lambda d: d.year).plot(kind='hist')
#id['FECHA_ALTA']=id['FECHA_ALTA'].replace(['dic'], 'dec')
