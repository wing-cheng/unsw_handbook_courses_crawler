#!/usr/bin/env python
# coding: utf-8

# In[6]:


import re


# In[7]:


import requests


# In[3]:


base = 'https://www.handbook.unsw.edu.au'


# In[8]:


resp = requests.get(base, timeout=10)
try:
    resp.encoding = resp.apparent.encoding
    resp.raise_for_status()
except:
    pass


# In[9]:


resp.text[:100]


# In[10]:


from bs4 import BeautifulSoup


# In[11]:


demo = resp.text
soup = BeautifulSoup(demo, 'html.parser')


# In[12]:


divs = soup.find_all('a', {'class': ['a-lettuce level-two', '']})
divs[:10]
divs[0].contents


# In[13]:


subject_areas = []
for item in divs:
    name = item.contents[1].string
    link = item.get('href')
    subject_areas.append([name, link])
subject_areas[:5]


# In[14]:


# but subject_areas contains 'by area of interest',
# 'by faculty' and by 'subject area'
# filer out 'by area of interest' nad 'by faculty'
subjects = []
for item in subject_areas:
    if re.search(r'[A-Z]{4}:[\s\w.]+', item[0]):
        subjects.append(item)
subjects[:20]


# In[ ]:


# now we have subject areas and href
# write them into a csv file
import csv
def write_csv(lst: list, filename: str, headers: list):
    with open('{:}.csv'.format(filename), 'w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in lst:
            writer.writerow(i)
# headers = ['Subject Area', 'href']
# write_csv(subjects, 'subject_areas', headers)


# In[17]:


from selenium import webdriver
driver = webdriver.Edge('msedgedriver.exe')
driver.implicitly_wait(60)


# In[18]:


driver.get(base)


# In[20]:


# crawl for the course codes given the subject area
# do big subject first
from time import sleep

total_code = []

for s in subjects:
    url = base + str(s[1])
    driver.get(url)
    button_exist = False
    # try find the button once
    try:
        button = driver.find_element_by_class_name('a-browse-more-controls-btn')
        button_exist = True
    except:
        button_exist = False
    # if button exists, courses are in 'section' tags
    if button_exist:
        # click expand button until there is no more to browse
        while True:
            try:
                button = driver.find_element_by_class_name('a-browse-more-controls-btn')
                if 'No more' in button.text:
                    break
                button.click()
                sleep(5)
            except:
                break
        courses = driver.find_elements_by_class_name('section')
        small_cs = []
    else:
        small_cs = driver.find_elements_by_class_name('align-left')
        courses = []
    
    codes = []
    for i in range(0, len(courses), 3):
        if courses[i].text:
            codes.append(courses[i].text)
    for l in small_cs:
        codes.append(l.text)
    
    total_code.append(codes)


# In[21]:


total_code[:100]


# In[24]:


total_code[-5:]


# In[25]:


# write the codes into a csv
write_csv(total_code, 'codes', ['Course Codes Grouped by Subject Area'])


# In[114]:


# start to crawl for each subject
driver.implicitly_wait(60)
total_info = []
base = 'https://www.handbook.unsw.edu.au'
path_u = '/undergraduate/courses/2020/'
path_p = '/postgraduate/courses/2020/'
path_r = '/research/courses/2020/'
path = [path_u, path_p, path_r]
for area in total_code:
    for code in area:
        if code == '':
            continue
        for p in path:
            try:
                url = base + p + code + '/'
                r = requests.get(url, timeout=30)
                r.raise_for_status()
            except:
                pass
            soup = BeautifulSoup(r.text, 'html.parser')
            if 'Error' in soup.title.string:
                continue
            else:
                break
                
        # code, name, course url, offering, enrolment condition, outline url, overview
        try:
            name = soup.title.string.split(' - ')[2]
        except:
            print(url)
        condi = soup.find_all('div', {'data-hbui': 'readmore__toggle-text'})
        try:
            pre = condi[1].div.string
        except:
            pre = ' '
        # find(name, attrs, recursive, text, **kwargs)
        ovs = soup.find('div', {'class': 'readmore__wrapper'})
        if ovs.p is None:
            ov = ovs.string
        else:
            ov = ovs.p.string
        offering = ' '
        offerings = soup.find_all('div', {'class': 'o-attributes-table-item'})
        for o in offerings:
            if not o.p is None and 'Term' in o.p.string:
                offering = o.p.string
                break
            
        outline = soup.find('a', {'class': 'a-btn-secondary a-btn-secondary--with-icon'}).get('href')
        info_lst = [code, name, url, offering, pre, outline, ov]
        total_info.append(info_lst)


# In[115]:


# write them into a csv file
headers = ['Course Code', 'Course Name', 'Course URL', 'Offering Terms', 'Enrolment Conditions', 'Outline URL', 'Overview']
with open('courses.csv', 'w+', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for t in total_info:
        try:
            writer.writerow(t)
        except:
            traceback.print_exc()


# In[108]:





# In[ ]:





# In[110]:





# In[112]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




