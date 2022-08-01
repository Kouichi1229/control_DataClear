# dic對上後 找到NULL的位置田

from bitarray import test
from strsimpy.jaro_winkler import JaroWinkler
jarowinkler = JaroWinkler()

test_db=[]
db=[]

list_index=test_db[test_db['AC'].isnull()].index.tolist()

list_vlue=[]

for i in range(0,len(list_index)):
    for j in range(0,len(db['AC'])):
        similar=jarowinkler.similarity(str(test_db['Assignee_regex'].iloc[list_index[i]]), str(db['AC_regex'][j]))
        list_vlue.append(similar)
    if max(list_vlue) >=0.95:
        index=list_vlue.index(max(list_vlue))
        test_db['AC'][list_index[i]]=db['AC_regex'][index]
        list_vlue.clear()
    else:
        index=list_vlue.index(max(list_vlue))
        test_db['AC'][list_index[i]]=str(test_db['Assignee_regex'].iloc[list_index[i]]).title()
        list_vlue.clear()
        



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
        

dataframe['AC']=pd.Series(ac_list)
dataframe['Closest']=pd.Series(close_list)
dataframe['Similarity'] = pd.Series(similar_list)
time.sleep(1)
st.success('比對完成，請下載')
                
            

csv = convert_df(dataframe)

st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='比對完後權控.csv',
                    mime='text/csv',
                    )