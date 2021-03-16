import urllib3
from bs4 import BeautifulSoup
import pandas as pd
def iframe(URL):
    try:
        http = urllib3.PoolManager(timeout=3.5,retries=False)
        page = http.request('GET', URL,
                        headers={'User-Agent':'Mozila/5.0'})

        soup = BeautifulSoup(page.data, "html.parser")
        soup = soup.find_all('iframe')
        if soup:
            return 1
        else:
            return  0
    except:
        return 0.01
df = pd.read_csv("new_phising_websites_online.csv", names=['URL'], header=0)
listt = list(df['URL'])

l = len(listt)
final = []
#print(listt)
for j,i in enumerate(listt):
    ifram = iframe(i)
    final.append(ifram)
    f = open("iframe.txt","a")
    f.write(str(ifram)+'\n')
    f.close()

dff = df.iloc[:-20,:].copy()
df[["iframe"]] = final
df.to_csv('iframe.csv')

