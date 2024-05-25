# import required modules
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from dotenv import load_dotenv
import selenium.common.exceptions
import time
import os
import pandas as pd

load_dotenv()

USERNAME = os.getenv('USERNAME_VAR')
PASSWORD = os.getenv('PASSWORD_VAR')
TARGET = os.getenv('TARGET_VAR')
 
# get instagram account credentials
username = USERNAME
password = PASSWORD
target_profile = TARGET
 
url = 'https://instagram.com/'

user_names = []
user_comments = []
posts = []

 
def path():
    global chrome
    global wait
    chrome = webdriver.Chrome()
    wait = WebDriverWait(chrome, 15)
     
def url_name(url):
    chrome.get(url)
     
def login(username, your_password):
    wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(your_password)
    chrome.find_element("xpath","//button[contains(.,'Log in')]").click()

    time.sleep(5.5)
 
    notNowButton = chrome.find_element("xpath","//div[text()='Not now']")
    notNowButton.click()
    time.sleep(3)
    notif = chrome.find_element("xpath","//button[text()='Not Now']")
    notif.click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Search']"))).click()
    time.sleep(3)
    chrome.find_element(By.CSS_SELECTOR, "[aria-label='Search input']").send_keys(target_profile)
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href,"{}/")]'.format(target_profile)))).click()
    time.sleep(3)


def first_post():
    chrome.find_element(By.CLASS_NAME, value="_aagu").click()
    time.sleep(2)
     
# Function to get next post
def next_post():
    try:
        nex = chrome.find_element(By.CLASS_NAME, value="_abl-")
        return nex
    except selenium.common.exceptions.NoSuchElementException:
        return 0
       
def download_allposts():
 
    # open First Post
    first_post()
    post_num=1
    save_content(post_num)

    is_next = next_post()
    c=5
    while(c>1):
        if is_next != False:
            post_num = post_num +1
            is_next.click()
            time.sleep(5)
            try:
                save_content(post_num)
                c = c-1
            except selenium.common.exceptions.NoSuchElementException:
                    print("finished")
            
                    return
        else:
            write_comments()
            break
    
    write_comments()
 
def save_content(number):
    time.sleep(5)
     
    try:
        load_more_comment = chrome.find_element(By.CSS_SELECTOR, "[aria-label='Load more comments']")
        # print("more comments button", load_more_comment)
        print('more comments')
        i = 0
        while load_more_comment:
            load_more_comment.click()
            time.sleep(7)
            load_more_comment = chrome.find_element(By.CSS_SELECTOR, "[aria-label='Load more comments']")
            print(i)
            print("Found {}".format(str(load_more_comment)))
            i += 1
    except Exception as e:
        print("No more comments")
        print(e)
        pass

    comment = chrome.find_elements(By.CLASS_NAME,'_a9ym')
    for c in comment:
        container = c.find_element(By.CLASS_NAME,'_a9zr')
        content = container.find_element(By.TAG_NAME,'span').text
        comment_name = content.replace('\n', ' ').strip().rstrip()
        comment_con = c.find_element(By.CLASS_NAME,'_a9zs')
        comment = comment_con.find_element(By.TAG_NAME,'span').text
        comment_content = comment.replace('\n', ' ').strip().rstrip()

        # print("these COMMENTS", content)
        posts.append(number)
        user_names.append(comment_name)
        user_comments.append(comment_content)

    print('found: ',user_names)
    print("comments", user_comments)


def write_comments():
    temp = {}
    # print(len(posts), len(user_names), len(user_comments))
    temp.update({'post':posts, 'name':user_names, "comment": user_comments})
    print('ALL COMMENTS: ',temp)
    print("Writing to file")
    fname = '{}.xlsx'.format(target_profile)

    df = pd.DataFrame(temp)
    df.to_excel(fname)


 
# Driver Code
path()
time.sleep(1)
 
url_name(url)
login(username, password)
download_allposts()
chrome.close()