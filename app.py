import imp
from itertools import count
import pandas as pd
import streamlit as st
from io import  StringIO
from strsimpy.jaro_winkler import JaroWinkler
from regex_data import *
from action import *
from time import sleep
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
#regex_sigle_db()

#讀取資料庫正規化資料
db_regex = pd.read_csv('./Single_db_regex.csv',encoding=encoding)
#db_regex.columns  Assignee_Name,AC,Assignee_Name_regex,AC_regex

#database dict
dic_db={}
#AC,AC_regex
for i in range(0,len(db_regex['AC'])):
    dic_db[db_regex['AC_regex'][i]]=db_regex['AC'][i]

#st.write(dic_db)

upload_type= st.radio(
     "請選擇上傳檔案類型",
     ('Csv', 'Excel'))

if upload_type == 'Csv':
     st.write('上傳CSV檔')
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
        dataframe[str(option)+'regex']=dataframe[option].str.upper()
        dataframe[str(option)+'regex']=dataframe[str(option)+'regex'].apply(lambda words:' '.join(word.upper() for word in str(words).split() if word not in take_out_type))
        dataframe[str(option)+'regex']=dataframe[str(option)+'regex'].replace('[^A-Za-z0-9]+','',regex=True)
        dataframe[str(option)+'regex']=dataframe[str(option)+'regex'].replace(' ','',regex=True)
        
        dataframe['AC']=dataframe[str(option)+'regex'].map(dic_db)
        
        not_Null= pd.notnull(dataframe['AC'])
     
        st.write("總共有",len(dataframe[option]),"與資料庫配對到的有",len(dataframe[not_Null]))
        st.write(dataframe[[option,'AC']])
        
        if st.button('下載目前與資料庫比對到的資料'):
            csv = convert_df(dataframe)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='比對完後權控.csv',
                mime='text/csv',
            )
        
        elif st.button('比對資料(建議未配對到資料少於50在按下此按鈕)'):

            with st.spinner('比對中請稍後...'):
            
            

                
                list_index=dataframe[dataframe['AC'].isnull()].index.tolist()

                list_vlue=[]
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    for i in range(0,len(list_index)):
                        for j in range(0,len(db_regex['AC'])):
                            similar=jarowinkler.similarity(str(dataframe[str(option)+'regex'].iloc[list_index[i]]), str(db_regex['AC_regex'][j]))
                            list_vlue.append(similar)
                        if max(list_vlue) >=0.95:
                            index=list_vlue.index(max(list_vlue))
                            dataframe['AC'][list_index[i]]=db_regex['AC_regex'][index]
                            list_vlue.clear()
                        else:
                            index=list_vlue.index(max(list_vlue))
                            dataframe['AC'][list_index[i]]=str(dataframe[str(option)+'regex'].iloc[list_index[i]]).title()
                            list_vlue.clear()
                        time.sleep(0.00000000000000000000000000000001)
                        my_bar.progress(percent_complete + 1)
        


                time.sleep(0.1)
                st.success('比對完成，請下載')
                
            

                csv = convert_df(dataframe)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='比對完後權控.csv',
                    mime='text/csv',
                    )
    
else:
     st.write("上傳Excel檔")

     uploaded_file = st.file_uploader("清選擇清洗目標比對檔案 Excel檔",type='xlsx')
     if uploaded_file is not None:
     # To read file as bytes:
        #bytes_data = uploaded_file.getvalue()
     #st.write(bytes_data)

     # To convert to a string based IO:
        #stringio = StringIO(uploaded_file.getvalue().decode())
     #st.write(stringio)

     # To read file as string:
        #string_data = stringio.read()
     #st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_excel(uploaded_file,sheet_name=1)
        st.write(dataframe)

       