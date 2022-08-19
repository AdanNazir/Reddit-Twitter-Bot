#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tweepy
import requests
import urllib.request
import praw
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time
import os
import random
from selenium.webdriver.chrome.options import Options


# In[ ]:



def Scrape_Reddit(visited_list):
    reddit = praw.Reddit(
        client_id="", #Your developer account client id should be pasted here
        client_secret="", #Your developer secret key should be pasted here
        user_agent="script by u/username", #Optional to tweak anything here
        username="", #Your reddit account username needs to be pasted here
        password="", #Your reddit account password needs to be pasted here
    )
    
    reddit.read_only = True
    
    subreddit = reddit.subreddit('').new(limit=2) #Subreddit name in the input string
    temp_link=""
    urls_list=[] #Urls list, which you need to download the videos from a specific subreddit, its URL's should be added here as a string in the list
    post_title=""
    search_urls=[]#Let it be as it is
    search_titles=[] #Same as above
    flag=False
    for post in subreddit:
        for i in range(len(urls_list)):
            if urls_list[i] in post.url:
                search_urls.append(post.url)
                search_titles.append(post.title)
                flag=True
                break
    
    if flag==True:
        for i in range(len(search_urls)):
            if search_urls[i] not in visited_list:
                visited_list.append(search_urls[i])
                temp_link=search_urls[i]
                post_title=search_titles[i]
                break
        
            else:
                continue
    
    else:
        return (None,None,visited_list)
    
    if temp_link=="":
        return (None,None,visited_list)
    
    return (post_title,temp_link,visited_list)
            


# In[ ]:


def Download_Video(target_url,post_title,nums): #Function for downloading a video from the target url
    r=requests.get(target_url)
    fetched_url=""
    new_url=""
    temp=str(r.content)
    counter=0
    count_1=0
    for i in temp.split(" "):
        if "<source" in i:
            break
        counter+=1

    counter+=1

    for i in temp.split(" "):
        if count_1==counter:
            fetched_url=i.strip("src=")
            new_url=fetched_url[1:len(fetched_url)-1]
            break
        else:
            count_1+=1
    
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(new_url,str(nums)+'.mp4') 
    
    except:
        print("Video Under Processing by the website...")
        time.sleep(2)
        flag=False
        while flag==False:
            try:
                time.sleep(3)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(new_url,str(nums)+'.mp4')
                flag=True
                print("Video Processed by the website...")
            
            except:
                print("Video under processing by the website")
                time.sleep(3)
                pass   


# In[ ]:


def Check_Url(temp_link,post_title,nums): #To check the target URL here
    Download_Video(temp_link,post_title,nums)


# In[ ]:


def Twitter_Function(post_title,sharable_url):
    
    c_k=[""]#Client key
    c_s=[""]#Client secret id
    a_t=[""]#account token
    a_t_s=[""]#account token secret
    
    for i in range(2):
        client = tweepy.Client(consumer_key=c_k[i],
                    consumer_secret=c_s[i],
                    access_token=a_t[i],
                    access_token_secret=a_t_s[i])
# Replace the text with whatever you want to Tweet about
        text1=post_title +sharable_url
        response = client.create_tweet(text=text1)


# In[ ]:


my_list=[]
visited_list=[]
while(1):
    nums=random.randint(1,10000)
    if nums not in my_list:
        my_list.append(my_list)
    
    else:
        while num in my_list:
            nums=random.randint(1,10000)
    print("Scrapping Reddit...\n")
    post_title,temp_link,visited_list=Scrape_Reddit(visited_list)
    flag=True
    if temp_link!=None:
        print("Reddit Scrapped successfully!\n")
        print("Downloading Video: ",post_title,"\n")
        time.sleep(2)
        Check_Url(temp_link,post_title,nums)
        print("Video Downloaded Successfully!\n")
        time.sleep(2)
        print("Posting Tweet on Twitter...\n")
        Twitter_Function(post_title,sharable_url)
        print("Tweet Posted Successfully!\n")
        time.sleep(2)


    else:
        flag=False
        while flag!=True:
            post_title,temp_link,visited_list=Scrape_Reddit(visited_list)
            if temp_link!=None:
                flag=True
            else:
                print("No new video found!\n")
                time.sleep(3)
                pass

        print("Reddit Scrapped successfully!\n")
        time.sleep(2)
        print("Downloading Video: ",post_title,"\n")
        time.sleep(4)
        Check_Url(temp_link,post_title,nums)
        time.sleep(2)
        print("Video Downloaded Successfully!\n")
        time.sleep(2)
        print("Posting Tweet on Twitter...\n")
        time.sleep(2)
        Twitter_Function(post_title,sharable_url)
        print("Tweet Posted Successfully!\n")
        time.sleep(3)

