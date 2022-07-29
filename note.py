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
        
