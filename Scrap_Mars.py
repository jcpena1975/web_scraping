#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from splinter import Browser
import time
from bs4 import BeautifulSoup as bs
import requests

# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     return Browser("chrome", **executable_path, headless=False)
# In[2]:
def webScarpping():
        

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    urlnews ="https://mars.nasa.gov/news/8770/nasas-perseverance-rover-will-peer-beneath-mars-surface/"
    browser.visit(urlnews)


    # In[4]:


    html = browser.html
    newsSoup= bs(html, 'html.parser')




    for news in newsSoup:
    #finding title
        title = newsSoup.find_all("div", class_="content_title")[1].text
        #finding paragraph
        paragraph = newsSoup.find_all("div", class_="rollover_description")[1].text
        if (title and paragraph):
            #print (title)
           # print (paragraph)


    # In[8]:

    jplUrl="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


    # In[9]:


    browser.visit(jplUrl)


    # In[10]:


    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")
    html = browser.html
    jplSoup= bs(html, 'html.parser')


    # In[11]:


    #display(jplSoup)


    # In[12]:


    image = jplSoup.find_all("figure", class_= "lede") 
    image_results= image[0].a["href"]
    imageurl="https://www.jpl.nasa.gov/"+ image_results
    #print (imageurl)


    # In[13]:


    image1 = jplSoup.select_one('figure.lede a img').get("src")
    image1


    # In[15]:


    factsurl ="https://space-facts.com/mars/"
    table = pd.read_html(factsurl)


    # In[18]:


    df = table[0]
    df.columns=["Facts","Values"]
    df.set_index(["Facts"])
   #df


    # In[19]:


    factshtml =df.to_html(index = False)
    # factshtml.replace("\n","")

    USGSUrl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    # In[24]:


    response =requests.get(USGSUrl)


    # In[25]:


    hemisoup = bs(response.text, "html.parser")

    hem_item= hemisoup.find_all(class_="itemLink product-item")
    #hem_item


    # In[28]:


    hemilist = []

    for image in hem_item:
        url= "https://astrogeology.usgs.gov" + image.get("href")
        hemilist.append(url)
    # display(hemilist)


    # In[29]:


    hemiurl = []
    for images in hemilist:
        response = requests.get(images)
        imageSoup = bs(response.text, "html.parser")
        imagesurl = imageSoup.find("a",href = True, text="Sample")
        finalimage = imagesurl["href"]
        title =imageSoup.find(class_="title").text.strip().replace(" Enhanced", "")
        hemiurl.append({"img_url": finalimage, "title": title})
    #hemiurl
    marsData = {
       "NewsTitle": title, "newsparagraph": paragraph, "imageurl": imageurl, "marsFacts": factshtml, "hemiimage" : hemiurl
    }     
    return marsData







