import requests
import urllib3
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np


def contains_ip(URL):

    if re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",URL):
        return 1
    else:
        return 0


def URL_catcher(URL):
    try :

        http = urllib3.PoolManager(timeout=3.0,retries=False)
        page = http.request('GET', URL,
                        headers={'User-Agent':'Mozila/5.0'})

        soup = BeautifulSoup(page.data, "html.parser")
        soup_href = []
        soup_rel = []

        soup_h = soup.find_all('a',href=True)
        soup_l = soup.find_all('link',href=True)
        for i in soup_l :
            soup_rel.append(i.get('href'))

        for i in soup_h :
            soup_href.append(i.get('href'))

        return soup_href, soup_rel
    except:
        return [], []


def extract_domain(url):
    if contains_ip(url):
     return '','',''
    if re.findall("://",url):
        sub_domain_and_top_domain = url.split("//")[1].split('/')[0]
    else:
        sub_domain_and_top_domain = url.split('/')[0]
    split = sub_domain_and_top_domain.split('.')
    if split[0] != 'www':
      split = ['www'] + split
    top_domains = []
    domain = ''
    sub_domains = []
    if len(split) == 3 :
      return split[0], split[1], split[2]
    try:
      if len(split[-1])<5 and len(split[-2])<4:
          top_domains.append(split[-2])
          top_domains.append(split[-1])
          domain = split[-3]
          sub_domains = split[:-3].copy()
          return sub_domains,domain,top_domains
      if len(split[-1])<5:
          top_domains.append(split[-1])
          domain = split[-2]
          sub_domains = split[:-2].copy()


    except:
      print("error in extarcting domain")
    if not domain:
      domain = ''
    if not sub_domains:
      sub_domains = ''
    if not top_domains:
      top_domains = ''
    return sub_domains,domain,top_domains


def links_confermity_to_doamin(URL):
    list_of_links_where_domain_exists = []
    list_with_links = []
    if contains_ip(URL):
        return  0.01
    soup_href,soup_rel = URL_catcher(URL)
    #print(soup_rel+soup_href)

    sub_domain, domain, top_domain = extract_domain(URL)
    #print("###############################"+domain )
    #print(soup_href+soup_rel)
    for i in soup_href+soup_rel:
        if re.findall("https*://(www.)*",str(i)):
            list_with_links.append(str(i))
            #print(domain)
            if re.findall("https*://(www.)*"+domain,str(i)):
                list_of_links_where_domain_exists.append(str(i))

    if len(list_with_links) == 0:
    	return 0.333
    return len(list_of_links_where_domain_exists)/len(list_with_links)



df = pd.read_csv("dataset_url_70000/Dataset.csv", names=['URL','status'], header=0)
listt = list(df['URL'])

l = len(listt)
final = []

for j,i in enumerate(listt[6067:]):
    conf =links_confermity_to_doamin(i)
    print(conf)
    final.append(conf)
    f = open("confer.txt","a")
    f.write(str(conf)+'\n')
    f.close()

dff = df.iloc[6067,:].copy()
dff[["Conformity"]] = final
df.to_csv('rasi.csv')


