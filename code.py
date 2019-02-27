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
#id.SEXO = id.SEXO.map({'Mujer' : 1,'Hombre' : 2})
id.MES_DE_FUGA = id.MES_DE_FUGA.map({1: 'Enero',2: 'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'})
#Base movimientos
mov=pd.read_fwf("BASE_MOVIMIENTOS.txt")
mov['FECHA_INFORMACION'] =pd.to_datetime(mov['FECHA_INFORMACION'], format='%d%b%Y:%H:%M:%S')
mov.sort_values(['ID','FECHA_INFORMACION'])

#Matriz de correlación movimientos
#sns.heatmap(mov.corr(), annot=True, linewidths=.5, fmt= '.2f')
plt.show()
#Matriz de correlación clientes
#sns.heatmap(id.corr(), annot=True, linewidths=.5, fmt= '.2f')
plt.show()

#Cruce de bases de datos
mat=pd.merge(mov, id, left_on='ID', right_on='CLIENTE_CC')
mat.drop(['CLIENTE_CC','ID'], axis='columns', inplace=True)
matHeat=sns.heatmap(mat.corr(), annot=True, linewidths=.5, fmt= '.2f',vmin=-0.9, vmax=0.9)
plt.show()

new=pd.merge(mov, id, left_on='ID', right_on='CLIENTE_CC')
new.sort_values(['ID','FECHA_INFORMACION'])

job=sns.boxplot(x="MES_DE_FUGA", y="fuga", data=new)
plt.show()

sns.lmplot("fuga", "SALDO_AHORROS", hue="MES_DE_FUGA", data=new)
plt.show()

new.groupby(['SITUACION_LABORAL','fuga'])['CLIENTE_CC'].size().unstack().plot(kind='bar',stacked=True)
plt.show()

#Transacciones de los clientes
mov.plot(kind='scatter',x='ID',y='SALDO_AHORROS',color='red')
plt.show()
#Relacion Situacion laboral - fuga
id.groupby(['SITUACION_LABORAL','fuga'])['CLIENTE_CC'].size().unstack().plot(kind='bar',stacked=True)
#Relacion Indicador mora - fuga
new.groupby(['INDICADOR_MORA','fuga'])['ID'].size().unstack().plot(kind='bar',stacked=True)
id.groupby(['SEXO','fuga'])['CLIENTE_CC'].size().unstack().plot(kind='bar',stacked=True)

#
ax = plt.gca()
a=new[new.fuga==1]
a.plot(kind='line',x='ID',y='MONTO_ABONOS_NOMINA',ax=ax)
plt.show()

#Distribución temporal de tx
mov['FECHA_INFORMACION'].map(lambda d: d.year).plot(kind='hist')
