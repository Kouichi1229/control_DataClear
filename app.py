import imp
from itertools import count
import pandas as pd
import streamlit as st
from io import  StringIO
from strsimpy.jaro_winkler import JaroWinkler
from regex_data import *
from time import sleep
from stqdm import stqdm
import time

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
#replace_dt=pd.read_csv("./CompanyReplaceWords.csv") # 取代的詞彙
jarowinkler = JaroWinkler()

#參數
encoding='utf-8-sig'

#資料庫資料正規化
#regex_dataDB()
regex_sigle_db()

#讀取資料庫正規化資料
db_regex = pd.read_csv('./Single_db_regex.csv',encoding=encoding)
#db_regex.columns  Assignee_Name,AC,Assignee_Name_regex,AC_regex


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
     if st.button('開始比對'):

        with st.spinner('比對中請稍後...'):
            
            

            dataframe[str(option)+'regex']=dataframe[option].str.upper()
            dataframe[str(option)+'regex']=dataframe[str(option)+'regex'].apply(lambda words:' '.join(word.upper() for word in str(words).split() if word not in take_out_type))
            dataframe[str(option)+'regex']=dataframe[str(option)+'regex'].replace('[^A-Za-z0-9]+','',regex=True)
            dataframe[str(option)+'regex']=dataframe[str(option)+'regex'].replace(' ','',regex=True)
     
            list_vlue=[]#存入相似度數值
            ac_list=[]#存入權控值
            close_list=[]#存取最接近權控值
            similar_list=[]#存入最大相似度
            my_bar = st.progress(0)
            for percent_complete in range(100):
                 for i in range(0,len(dataframe[option])):
                     for j in range(0,len(db_regex['AC_regex'])):
                         similar=jarowinkler.similarity(str(dataframe[str(option)+'regex'][i]), str(db_regex['AC_regex'][j]))
                         list_vlue.append(similar)
                     if max(list_vlue) >=0.95:
                         index=list_vlue.index(max(list_vlue)) #最大相似度的位置
                         ac_list.append(db_regex['AC'][index]) #存入資料庫裡最大相似度的值
                         close_list.append(db_regex['AC'][index])
                         similar_list.append(max(list_vlue))
                         list_vlue.clear()#離開後清除所有值
                     else:
                         index=list_vlue.index(max(list_vlue))
                         ac_list.append(str(dataframe[option][i]).title()) #存入自己的值 並用title的方式存入
                         close_list.append(db_regex['AC'][index])
                         similar_list.append(max(list_vlue))
                         list_vlue.clear()
                     time.sleep(0.1)
                     my_bar.progress(percent_complete + 1)
        #stqdm.pandas()

            dataframe['AC']=pd.Series(ac_list)
            dataframe['Closest']=pd.Series(close_list)
            dataframe['Similarity'] = pd.Series(similar_list)
            time.sleep(5)
            st.success('比對完成，請下載')
                
            @st.cache
            def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode(encoding)

            csv = convert_df(dataframe)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='比對完後權控.csv',
                mime='text/csv',
                )
    
       