# import required modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import selenium.common.exceptions
import time
from bs4 import BeautifulSoup as bs
import requests
import os

load_dotenv()

USERNAME = os.getenv('USERNAME_VAR')
PASSWORD = os.getenv('PASSWORD_VAR')
# TARGET_PROFILE ='tradisplaid'
 
 
# get instagram account credentials
username = input(USERNAME)
password = input(PASSWORD)
 
url = 'https://instagram.com/' + \
    input('tradisplaid')
 
def path():
    global chrome
    chrome = webdriver.Chrome()
     
def url_name(url):
    chrome.get(url)
    time.sleep(4)
     
def login(username, your_password):
    log_but = chrome.find_element(By.CLASS_NAME, value="ab1y")
    time.sleep(2)
    log_but.click()
    time.sleep(4)
    usern = chrome.find_element(By.CLASS_NAME, value="username")
    usern.send_keys(username)
    passw = chrome.find_element(By.CLASS_NAME, value="password")
    passw.send_keys(your_password)
    passw.send_keys(Keys.RETURN)
    time.sleep(5.5)
 
    notn = chrome.find_element(By.CLASS_NAME, value="yWX7d")
 
    notn.click()
    time.sleep(3)

def first_post():
    pic = chrome.find_element(By.CLASS_NAME, value="kIKUG").click()
    time.sleep(2)
     
# Function to get next post
def next_post():
    try:
        nex = chrome.find_element(By.CLASS_NAME, value="coreSpriteRightPaginationArrow")
        return nex
    except selenium.common.exceptions.NoSuchElementException:
        return 0
       
def download_allposts():
 
    # open First Post
    first_post()
 
    user_name = url.split('/')[-1]
 
    # check if folder corresponding to user name exist or not
    if(os.path.isdir(user_name) == False):
 
        # Create folder
        os.mkdir(user_name)
 
    multiple_images = nested_check()
 
    if multiple_images:
        nescheck = multiple_images
        count_img = 0
         
        while nescheck:
            elem_img = chrome.find_element(By.CLASS_NAME, value='rQDP3')
 
            # Function to save nested images
            save_multiple(user_name+'/'+'content1.'+str(count_img), elem_img)
            count_img += 1
            nescheck.click()
            nescheck = nested_check()
 
        # pass last_img_flag True
        save_multiple(user_name+'/'+'content1.' +
                      str(count_img), elem_img, last_img_flag=1)
    else:
        save_content('_97aPb', user_name+'/'+'content1')
    c = 2
     
    while(True):
        next_el = next_post()
         
        if next_el != False:
            next_el.click()
            time.sleep(1.3)
             
            try:
                multiple_images = nested_check()
                 
                if multiple_images:
                    nescheck = multiple_images
                    count_img = 0
                     
                    while nescheck:
                        elem_img = chrome.find_element(By.CLASS_NAME, value='rQDP3')
                        save_multiple(user_name+'/'+'content' +
                                      str(c)+'.'+str(count_img), elem_img)
                        count_img += 1
                        nescheck.click()
                        nescheck = nested_check()
                    save_multiple(user_name+'/'+'content'+str(c) +
                                  '.'+str(count_img), elem_img, 1)
                else:
                    save_content('_97aPb', user_name+'/'+'content'+str(c))
             
            except selenium.common.exceptions.NoSuchElementException:
                print("finished")
                return
         
        else:
            break
         
        c += 1
 
def save_content(class_name, img_name):
    time.sleep(0.5)
     
    try:
        pic = chrome.find_element(class_name)
     
    except selenium.common.exceptions.NoSuchElementException:
        print("Either This user has no images or you haven't followed this user or something went wrong")
        return
     
    html = pic.get_attribute('innerHTML')
    soup = bs(html, 'html.parser')
    link = soup.find('video')
     
    if link:
        link = link['src']
     
    else:
        link = soup.find('img')['src']
    response = requests.get(link)
     
    with open(img_name, 'wb') as f:
        f.write(response.content)
    time.sleep(0.9)
     
def save_multiple(img_name, elem, last_img_flag=False):
    time.sleep(1)
    l = elem.get_attribute('innerHTML')
    html = bs(l, 'html.parser')
    biglist = html.find_all('ul')
    biglist = biglist[0]
    list_images = biglist.find_all('li')
     
    if last_img_flag:
        user_image = list_images[-1]
     
    else:
        user_image = list_images[(len(list_images)//2)]
    video = user_image.find('video')
     
    if video:
        link = video['src']
     
    else:
        link = user_image.find('img')['src']
    response = requests.get(link)
     
    with open(img_name, 'wb') as f:
        f.write(response.content)
 
# Function to check if the post is nested
def nested_check():
    try:
        time.sleep(1)
        nes_nex = chrome.find_element('coreSpriteRightChevron  ')
        return nes_nex
     
    except selenium.common.exceptions.NoSuchElementException:
        return 0
 
# Driver Code
path()
time.sleep(1)
 
url_name(url)
login(username, password)
download_allposts()
chrome.close()