#!/usr/local/bin/python3.7
# -*- coding:utf-8 -*-

##### Import Modules #####
from __future__ import print_function
import time
import numpy as np
import pandas as pd
import subprocess as sp
from datetime import datetime, timedelta
import sys
import re
import os

TDIR='/home/ygin/skj/tmp/'
DIR='/home/ygin/skj/siteinfo_macro/'
today = datetime.strftime(datetime.now(),'%m%d')
ytd = datetime.strftime(datetime.now(),'%y')


 

def convert_dms2dd(x):
    dms = x.split(':')
    dd = np.around(int(dms[0]) + int(dms[1]) / 60 + float(dms[2]) / 3600,4)
    return dd

de = pd.DataFrame(columns=['date','gnb_ID','DU_Name','RRH_ID','CELL_ID','LATTITUDE','LONGITUDE','PCI','RU_TYPE','RANK_INDEX','HPW','VPW','ETILT','ERAB_ADD','SCG_SUM','DL_PRB'])

# date_list = ['0301','0302','0303']
# 3월 한달간 날짜 구하기
date_list = []
for i in range(51,20,-1):
    td = datetime.strftime(datetime.now()-timedelta(days=i),'%m%d')
    date_list.append(td)

for i in date_list:
    dt = pd.read_csv(DIR+i+'07_site_merge.csv',encoding='cp949',low_memory=False)
    dt['date']=ytd+i
    data = dt[['date','gnb_ID','DU_Name','RRH_ID','CELL_ID','LATTITUDE','LONGITUDE','PCI','RU_TYPE','RANK_INDEX','HPW','VPW','ETILT','ERAB_ADD','SCG_SUM','DL_PRB']]
    de = pd.concat([de,data])

# preprocessing
de.replace('-',np.nan,inplace=True)
de.dropna(inplace=True)
de = de.drop_duplicates(keep='first')
de['RU_TYPE'] = de['RU_TYPE'].map({'mt3201-780':32,'rt8801-780':8,'rra1-000':4})
de['RANK_INDEX'] = de['RANK_INDEX'].map({'rank4':4,'rank2':2,'rank1':1})
de['LAT'] = de['LATTITUDE'].str[2:].apply(convert_dms2dd)
de['LON'] = de['LONGITUDE'].str[1:].apply(convert_dms2dd)
de['HPW'] = de['HPW'].str[0:2]
de['VPW'] = de['VPW'].replace({'6degrees':6,'9degrees':9,'15degrees':15,'24degrees':24})
de2 = de.drop(['LATTITUDE','LONGITUDE'],axis=1)

## extract to csv
de2.to_csv(TDIR+'result_siteinfo.csv',index=False)