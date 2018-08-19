import pandas as pd
import numpy as np
import xlsxwriter

workbook = pd.ExcelFile("dcs.xls")
worksheet = workbook.parse("tabvInfo")
exclude =['BYOL', 'SPLA8', 'STD', 'MGMT']

df1 = worksheet[ ['VM','CPUs','Memory','Cluster','Host'] ]
df2 = df1[df1['Cluster'].str.contains(r'(.*) SPLA [1-7]{1}$')] 

ratio = (df2.Memory/df2.CPUs/1000).astype(int)

df2.insert(3,'Memory CPU Ratio',ratio)

df2['Cluster Recommendation'] = np.where(df2['Memory CPU Ratio']>5,'SPLA7',np.where(df2['Memory CPU Ratio']>3, 'SPLA1 or SPLA6', 'SPLA3 or SPLA4 or SPLA5'))


df2['Memory CPU Ratio'] = df2['Memory CPU Ratio'].astype(str)+':1'

print df2

writer = pd.ExcelWriter('simple.xlsx', engine='xlsxwriter')

df2.to_excel(writer, index=False, sheet_name="Sheet1")

writer.save()