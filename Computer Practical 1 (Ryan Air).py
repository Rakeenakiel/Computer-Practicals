#!/usr/bin/env python
# coding: utf-8

# ### Import Cell

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re 
import os


# ### Importing Data

# In[2]:


def year(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
    txt= soup.find_all('h3')
    clean = []
    for i in txt:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', str(i))
        clean.append(cleantext)
    asd = clean[0:-2]
    qwe = [i.rstrip() for i in asd]
    qwe[19]= "1999-00"
    return qwe
def People(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
    txt = soup.find_all('p')
    new_list = []
    for x in txt:
        new_list.append(str(x))
    fin_list = []
    for i in new_list:
        if "People (y/e):" in i:
            fin_list.append(i)
    ans = []
    for i in fin_list:
        b = i.replace('<p>',"").replace("</p>","")
        ans.append(b)
    anj = []
    for i in ans:
        c= i.replace("People (y/e):","")
        d = c.replace(" ","")
        e = d.replace(",", "")
        anj.append(int(e))
    return anj
def Pass(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
    txt = soup.find_all('p')
    new_list = [str(x) for x in txt]
    fin_list = [i for i in new_list if "Passengers:" in i]
    clean = []
    for i in fin_list:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', str(i))
        clean.append(cleantext)
    ans = [int(i.replace("m",",000,000").replace("Passengers:","").replace(" ","").replace(",", "")) for i in clean]
    ans[23]= ans[23]*10
    return ans 
    
    


# In[3]:


a = "https://corporate.ryanair.com/about-us/history-of-ryanair/"
df = pd.DataFrame()
df['Year']= year(a)
df['People (y/e)']= People(a)
df['Passengers']=Pass(a)


# In[4]:


print(df)


# ### Calculate The Growth Rate

# In[5]:


# To Calculate the Growth Rate the general formula would be (passenger this year - passenger last year) / passenger last year


# In[6]:


Pass_list = list(df['Passengers'])
Pass_list.reverse()
Growth_rate = []
for i in range(len(Pass_list)):
    if i == 0:
        Growth_rate.append(int("1"))
    else:
        temp = Pass_list[i] - Pass_list[i-1]
        Growth_rate.append(temp/Pass_list[i-1])
Growth_rate.reverse()
df['Growth_rate'] = Growth_rate


# In[7]:


print(df)


# In[8]:


print(f"The Total Number of Passengers of Ryan Air is {df['Passengers'].sum()}")


# ### Sum of all Passengers over time

# In[9]:


sum_pass = []
pass_ = list(df['Passengers'])
pass_.reverse()
a = 0
for i in pass_:
    a += i
    sum_pass.append(a)
sum_pass.reverse()
df['Sum of Passengers'] = sum_pass


# In[10]:


print(df)


# In[11]:


directory = r"C:\Users\rakee\OneDrive\Desktop\DS\Computer practicals rug"
file = "Ryanair2.xlsx"

if not os.path.exists(directory):
    os.makedirs(directory)

df.to_excel(os.path.join(directory, file))


# In[ ]:




