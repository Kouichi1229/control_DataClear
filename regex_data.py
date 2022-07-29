import pandas as pd

take_out_type=['INCORPORATED',
 'CORPORATION',
 'CORP.',
 'CORP',
 'INC',
 'INC.',
 '& CO.',
 'CO.',
 'CO',
 'CO.,',
 'COMPANY',
 'KABUSHIKI KAISHA',
 'KABUSHIKI', 'KAISHA',
 'KK',
 'K.K.',
 'K.K',
 'PTY. LTD.',
 'PTY LTD',
 'LTD',
 'L.T.D.',
 'LTD.',
 'LIMITED',
 'LLC',
 'L.L.C.',
 "THE","AND"]
stop_words = ["THE","AND"] # 去掉無意義的詞
replace_dt=pd.read_csv("./CompanyReplaceWords.csv") # 取代的詞彙


#權控表正規化
encoding = 'utf-8-sig'


def regex_sigle_db():
    dt=pd.read_csv('./Single_db.csv',encoding=encoding)
    dt['AC_regex']=dt['AC'].str.upper()

    #dt['AC_rgex']=dt['AC_rgex'].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in stop_words))
    dt['AC_regex']=dt['AC_regex'].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in take_out_type))
    dt['AC_regex']=dt['AC_regex'].replace('[^A-Za-z0-9]+','',regex=True)
    dt['AC_regex']=dt['AC_regex'].replace(' ','',regex=True)

    dt.to_csv('Single_db_regex.csv',encoding=encoding)


def regex_dataDB():
    dt=pd.read_csv("./Control_db.csv",encoding=encoding)
    dt['Assignee_Name_regex']=dt['Assignee_Name'].str.upper()
    dt['AC_regex']=dt['AC'].str.upper()
    
    for i in range(0,len(replace_dt['Replace'])):
        dt['Assignee_Name_regex']=dt['Assignee_Name_regex'].str.replace(replace_dt['Replace'][i],replace_dt['Replace Words'][i],regex=True)
        dt['AC_regex']=dt['AC_regex'].str.replace(replace_dt['Replace'][i],replace_dt['Replace Words'][i],regex=True)
        
    dt['Assignee_Name_regex']=dt['Assignee_Name_regex'].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in stop_words))
    dt['AC_regex']=dt['AC_regex'].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in stop_words))
    
    dt['Assignee_Name_regex']=dt['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)
    dt['AC_regex']=dt['AC_regex'].replace('[^A-Za-z0-9]+','',regex=True)
    
    dt['Assignee_Name_regex']=dt['Assignee_Name_regex'].replace(' ','',regex=True)
    dt['AC_regex']=dt['AC_regex'].replace(' ','',regex=True)
    
    dt.to_csv("Control_db_Regex.csv",encoding=encoding)
        
    

def regex_null_data(dt,option):
    dt["Assignee_regex"]=dt[option].astype(str).str.upper()
    dt["Assignee_regex"]=dt["Assignee_regex"].replace('[^A-Za-z0-9]+',' ',regex=True)

    for i in range(0,len(replace_dt['Replace'])):
        dt["Assignee_regex"]=dt["Assignee_regex"].astype(str).str.replace(replace_dt['Replace'][i].upper(),replace_dt['Replace Words'][i].upper(),regex=True)
        
        dt["Assignee_regex"]=dt["Assignee_regex"].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in stop_words))
        
        dt["Assignee_regex"]=dt["Assignee_regex"].replace('[^A-Za-z0-9]+','',regex=True)
        
        dt["Assignee_regex"]=dt["Assignee_regex"].replace(' ','',regex=True)
        






#比對資料正規化
def regex_data(dt,row:str):
    #dt=pd.read_csv(fileName+".csv",encoding=endcoding)
    dt[row+"_regex"]=dt[row].astype(str).str.upper()
    
    for i in range(0,len(replace_dt['Replace'])):
        dt[row+"_regex"]=dt[row+"_regex"].astype(str).str.replace(replace_dt['Replace'][i],replace_dt['Replace Words'][i],regex=True)
        
        dt[row+"_regex"]=dt[row+"_regex"].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in stop_words))
        
        dt[row+"_regex"]=dt[row+"_regex"].replace('[^A-Za-z0-9]+','',regex=True)
        
        dt[row+"_regex"]=dt[row+"_regex"].replace(' ','',regex=True)
        

