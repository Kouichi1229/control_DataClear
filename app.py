import imp
from itertools import count
import pandas as pd
import streamlit as st
from io import  StringIO
from strsimpy.jaro_winkler import JaroWinkler
from regex_data import *

stop_words = ["THE","AND"] # 去掉無意義的詞
replace_dt=pd.read_csv("./CompanyReplaceWords.csv") # 取代的詞彙
jarowinkler = JaroWinkler()

#參數
encoding='utf-8-sig'

#資料庫資料正規化
regex_dataBD()
#讀取資料庫正規化資料
db_regex = pd.read_csv('./Control_db_Regex.csv',encoding=encoding)
#db_regex.columns  Assignee_Name,AC,Assignee_Name_regex,AC_regex

just_regex_db= db_regex[["Assignee_Name_regex","AC"]]
just_regex_db.drop_duplicates()

#資料庫字典
dic_1={} #Assignee&AC
#dic_2={} #Assignee_regex&AC
#dic_3={} #AC_regex&AC

for i in range(0,len(db_regex["AC"])):
    dic_1[db_regex["Assignee_Name"][i]]=db_regex["AC"][i]
    #dic_2[db_regex["Assignee_Name_regex"][i]]=db_regex["AC"][i]
    #dic_3[db_regex["AC_regex"][i]]=db_regex["AC"][i]


#正規化資料庫
dic_2={}

for i in range(0,len(just_regex_db['AC'])):
    dic_2[just_regex_db["Assignee_Name_regex"][i]]=just_regex_db['AC'][i]

uploaded_file = st.file_uploader("清選擇清洗目標比對檔案 CSV檔")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     #st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_file.getvalue().decode(encoding))
     #st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     #st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
     dataframe = pd.read_csv(uploaded_file,encoding=encoding)
     st.write(dataframe)

     
    # 選擇清洗欄位
     option = st.selectbox(
     '選擇要比對的欄位',
     (dataframe.columns))

     st.write('你的比對欄位', dataframe[option]) #option type str
     #比對欄位正規化

     #先對應資料庫裡有的欄位

     dataframe["AC"] = dataframe[option].map(dic_1)
     #原本是NULL的填入
     for i in range(0,len(dataframe[option])):
        if dataframe[option][i]=='NULL':
            dataframe['AC'][i]=dataframe[option][i]
            

     #判斷資料裡是否有null
     if dataframe['AC'].isnull().sum()>0:
        
        if st.button('沒有對應到的資料'):
            st.write("共有"+str(dataframe['AC'].isnull().sum())+"筆",dataframe[dataframe.isnull().T.any()]) 

            #未比對的正規化
            dataframe["Assignee_regex"]=dataframe[option].astype(str).str.upper()
     
    
            for i in range(0,len(replace_dt['Replace'])):
                dataframe["Assignee_regex"]=dataframe["Assignee_regex"].astype(str).str.replace(replace_dt['Replace'][i],replace_dt['Replace Words'][i],regex=True)
        
                dataframe["Assignee_regex"]=dataframe["Assignee_regex"].apply(lambda words:' '.join(word.upper() for word in words.split() if word not in stop_words))
        
                dataframe["Assignee_regex"]=dataframe["Assignee_regex"].replace('[^A-Za-z0-9]+','',regex=True)
        
                dataframe["Assignee_regex"]=dataframe["Assignee_regex"].replace(' ','',regex=True)

            dataframe['AC']=dataframe['Assignee_regex'].map(dic_2)

            st.subheader("正規化後配對")
            st.write(dataframe[dataframe.isnull().T.any()],"剩下"+str(dataframe['AC'].isnull().sum())+"筆") 

            if dataframe['AC'].isnull().sum() >0:
                st.subheader("Jaro-Winkler 模糊比對 填入資料")        

                compare_dt = dataframe[dataframe.isnull().T.any()]
                for i in range(0,len(compare_dt['AC'])):
                    for j in range(0,len(just_regex_db['AC'])):
                        similar=jarowinkler.similarity(compare_dt['Assignee_regex'].iloc[i], just_regex_db['Assignee_Name_regex'][j])
                        #st.write(compare_dt['Assignee_regex'].iloc[i],just_regex_db['Assignee_Name_regex'][j],similar)
                        if similar >= 0.90:
                            index = compare_dt['AC'].index[0]
                            dataframe['AC'][index]=just_regex_db['AC'][j]
                        else:
                            index = compare_dt['AC'].index[0]
                            #insert_db=pd.read_csv("./Control_db.csv",encoding=encoding)
                            #insert_db.append(dataframe[option][index],dataframe[option][index].str.title())

                            #st.write(index,type(index),dataframe['AC'][index],type(dataframe['AC'][index]))
                
                st.write(dataframe[[option,'AC']])
            
     

    #st.write(null_df)
    #  for i in range(0,len(null_df['AC'])):
    #     for j in range(0,len(db_regex['AC'])):
    #         #st.write(db_regex['Assignee_Name_regex'][j],type(db_regex['Assignee_Name_regex'][j]))
    #         similar=jarowinkler.similarity(null_df['Assignee_regex'].iloc[i], db_regex['Assignee_Name_regex'][j])
    #         #st.write(similar)
    #         if similar >=0.95:
    #             index=null_df['AC'].index[0]
    #             dataframe['AC'][index]=db_regex['AC'][j]
    #         else:
    #             index=null_df['AC'].index[0]
    #             dataframe['AC'][index]=dataframe[option][index].title()
     
    #  null_df2=dataframe[dataframe.isnull().T.any()]
     #st.write("共有"+str(len(null_df2['AC']))+"筆",null_df2[[option,'AC']])
     #st.write(dataframe)
