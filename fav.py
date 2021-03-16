import urllib3
from bs4 import BeautifulSoup
import re
import pandas as pd
def favicon(URL):
    try:
        http = urllib3.PoolManager()
        page = http.request('GET', URL,
                            headers={'User-Agent':'Mozila/5.0'})
        soup = BeautifulSoup(page.data, "html.parser")
        soup = soup.find_all('link')
        soup_rel = []

        for i in soup :
            soup_rel.append(i.get('rel'))
        for i,row in enumerate(soup_rel):
            if row :
                if len(row) >1:
                    j = row[0]+" "+row[1]#check for a string composed from two words
                    if re.findall('^shortcut icon$',j):
                        print(soup[i])
                        return 1 , soup[i]
                else:
                    if re.findall('^icon$',row[0]):

                        return 1 ,soup[i]
        return 0 , ''
    except:
        return 0,''

df = pd.read_csv("dataset_url_70000/Dataset.csv", names=['URL','status'], header=0)
listt = list(df['URL'])

l = len(listt)
final_num = []
final_link = []



for j,i in enumerate(listt[2690:35000]):
    print(favicon(i))
    a,b =favicon(i)
    final_num.append(a)
    final_link.append(b)
    print(j)
    f = open("favicon.txt","a")
    f.write(str(a)+str(b)+'\n')
    f.close()
dff = df.iloc[2690:35000,:].copy()
dff[["favicon"]] = final_num
dff[["url_fav"]] = final_link
dff.to_csv('favicon.csv')

