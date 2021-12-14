"""
Started coding on 2021-06-09
**********
ChangeLog
**********

2021-06-12
- Added UI for the crawler

2021-06-14
- Fixed known bug for facebook crawling

2021-06-15
- Added Instagram image crawling functionality

2021-06-20
- Improved crawling algorithm to increase efficiency

2021-06-24
- Added insta link crawling and image download based on link in csv

2021-12-10
- Fixed known bug

"""



#imports section
import os #to access file directory
import re
from tkinter import image_names #for replacing 
import wget #to download image from FB
import time #to set time to let page load
import PySimpleGUI as sg #UI API
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup #for HTML parsing
import urllib.request as utr #to download image from IG
import pandas as pd  #output link to csv


#Function to scroll pages to the end of responding page
def autoscroll(driver):
 last_height = driver.execute_script("return document.body.scrollHeight")
 while True :
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(2)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
        break
      last_height = new_height
 return driver


#function to initialize webdriver
def driverini():
 chrome_option = webdriver.ChromeOptions()
 prefs = {"profile.default_content_setting_values.notifications" : 2}
 chrome_option.add_experimental_option("prefs",prefs)
 #chrome_option.add_argument('--disable-gpu')
 #pathing of webdriver
 driver = webdriver.Chrome('C:/Users/chromedriver.exe',chrome_options=chrome_option) 
 return driver


#Function of FacebookImageCrawling
def fbdatacrawl(URL_link,DIR_link,DC_ID,DC_Pass):

 driver = driverini()
 #Web page to login
 driver.get("http://www.facebook.com")

 #Cookie Accept Handling
 WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='cookie-policy-dialog-accept-button']"))).click()
 username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
 password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

 time.sleep(2)
 username.clear()
 username.send_keys(DC_ID)
 password.clear()
 password.send_keys(DC_Pass)

 WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


 #wait 5 seconds to allow your new page to load
 time.sleep(5)
 images = []
 
 #
 if URL_link[-1] != '/':
  URL_link= URL_link + "/"

 #itterate over both uploaded and tagged images respectively
 for i in ["photos"]:

    driver.get(URL_link + i + "/")
    time.sleep(2)
    
    autoscroll(driver)
          
    #target all the link elements on the page
    anchors = driver.find_elements_by_tag_name('a')
    anchors = [a.get_attribute('href') for a in anchors]
    #narrow down all links to image links only
    anchors = [a for a in anchors if str(a).startswith(URL_link + "photos/")]

    #extract the [1]st image element in each link
    for a in anchors:
        driver.get(a) #navigate to link
        time.sleep(2) #wait a bit
        img = driver.find_elements_by_tag_name("img")
        images.append(img[0].get_attribute("src"))
 
 if DIR_link[-1] != '/':
  DIR_link= DIR_link + "/"
 
 if os.path.isfile(DIR_link +'out.csv')  :
     df1 = pd.read_csv(DIR_link +'out.csv')
     counter = df1.shape[0] +1
 else:
     counter = 0

 df3 = pd.DataFrame(images) 
 df3.to_csv(DIR_link +'out.csv', mode='a', header=False, index=False) 
 for image in images:
     save_as = os.path.join(DIR_link, str(counter) + '.jpg')
     wget.download(image, save_as)
     counter += 1
 



#function to InstagramImageCrawling
def instadatacrawl(URL_link,DIR_link,DC_ID,DC_Pass):
 driver = driverini()
 driver.get("http://www.instagram.com")

 button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='aOOlW  bIiDR  ']"))).click()
 username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
 password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
 
 time.sleep(3)
 #enter username and password
 username.clear()
 username.send_keys(DC_ID)
 password.clear()
 password.send_keys(DC_Pass)
 time.sleep(3)


 #target the login button and click it
 button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']"))).click()
 time.sleep(3)
 #alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
 if URL_link[-1] == '/':
  URL_link= URL_link[:-1]
 if DIR_link [-1] != '/':
  DIR_link = DIR_link +"\\"
 print(URL_link)
 time.sleep(5)
 driver.get(URL_link)
 time.sleep(3)
  
 base = BeautifulSoup(driver.page_source,'html.parser')
 post_number = base.find('span',class_ = 'g47SY').get_text()
 post_number = int(re.sub('[!@#$,]', '', post_number))
 #post_number = int(base.find('span',class_ = 'g47SY').get_text())
 print(f'Number of Post {post_number}')
 post_li_link = []
 photo_counter = 0
 for i in range(int(post_number/10)): 
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        soup = BeautifulSoup(driver.page_source,'html.parser')
        posts = soup.findAll('a')
        for post in posts:
            if '/p/' in post['href']:
                post_li_link.append(post['href'])
        time.sleep(1.5)
 post_li_link = list(set(post_li_link))
 print(post_li_link)
 
 if os.path.isfile(DIR_link +'out.csv')  :
     df1 = pd.read_csv(DIR_link +'out.csv')
     counter = df1.shape[0] +1
 else:
     counter = 0

 df3 = pd.DataFrame(post_li_link) 
 df3.to_csv(DIR_link +'out.csv', mode='a', header=False, index=False) 
 

 for lk in post_li_link:
         link = URL_link + lk
         link = link.replace('/explore/tags','')
         driver.get(link)
         time.sleep(1)
         soup = BeautifulSoup(driver.page_source,'html.parser')
         images = soup.findAll('img')
         for image in images:
            if image.has_attr('srcset'):
                if image['srcset'].find('1080w') == -1 :
                    pass
                else:
                    x = image['srcset'].split(',')
                    for y in x:
                        if y.find('1080w') == -1 :
                            pass
                        else:
                            photo_counter += 1
                            print(link)
                            download_image(DIR_link,y,photo_counter,counter)
                          

def download_image(DIR_link,image_link,counter,count):
    file_name =  DIR_link  +  (str(count)) + '.jpg'
    print(file_name)
    img_li = image_link.replace(' 1080w','')
    r = utr.urlopen(img_li)
    with open(file_name, "wb" ) as f:
        f.write(r.read())

def instalinkcrawl(URL_link,DIR_link,DC_ID,DC_Pass):
 driver = driverini()
 driver.get("http://www.instagram.com")

 button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='aOOlW  bIiDR  ']"))).click()
 username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
 password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
 
 time.sleep(3)
 #enter username and password
 username.clear()
 username.send_keys(DC_ID)
 password.clear()
 password.send_keys(DC_Pass)
 time.sleep(3)


 #target the login button and click it
 button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']"))).click()
 time.sleep(3)
 if URL_link[-1] == '/':
  URL_link= URL_link[:-1]
 if DIR_link [-1] != '/':
  DIR_link = DIR_link +"\\"
 driver.get(URL_link)

 base = BeautifulSoup(driver.page_source,'html.parser')
 post_number = base.find('span',class_ = 'g47SY').get_text()
 post_number = int(re.sub('[!@#$,]', '', post_number))
 #post_number = int(base.find('span',class_ = 'g47SY').get_text())
 print(f'Number of Post {post_number}')
 post_li_link = []
 photo_counter = 0
 for i in range(int(post_number/10)): 
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        soup = BeautifulSoup(driver.page_source,'html.parser')
        posts = soup.findAll('a')
        for post in posts:
            if '/p/' in post['href']:
                post_li_link.append(post['href'])
        time.sleep(1.5)
 post_li_link = list(set(post_li_link))
 print(post_li_link)
 df = pd.DataFrame(post_li_link)    
 df.to_csv(DIR_link +'out.csv') 

def instaimgdown(URL_link,DIR_link,DC_ID,DC_Pass):
 driver = driverini()
 driver.get("http://www.instagram.com")

 button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='aOOlW  bIiDR  ']"))).click()
 username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
 password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
 
 time.sleep(3)
 #enter username and password
 username.clear()
 username.send_keys(DC_ID)
 password.clear()
 password.send_keys(DC_Pass)
 time.sleep(3)


 #target the login button and click it
 button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']"))).click()
 time.sleep(3)
 if URL_link[-1] == '/':
  URL_link= URL_link[:-1]
 if DIR_link [-1] != '/':
  DIR_link = DIR_link +"\\"

 column_names = ["Number", "Letter"]
 myL= pd.read_csv(DIR_link +'out.csv',names=column_names)
 myL = myL.Letter.to_list()
 myL.pop(0)
 print(myL)
 photo_counter= 0
 for lk in myL:
         link = URL_link + lk
         link = link.replace('/explore/tags','')
         driver.get(link)
         time.sleep(1)
         soup = BeautifulSoup(driver.page_source,'html.parser')
         images = soup.findAll('img')
         for image in images:
            if image.has_attr('srcset'):
                if image['srcset'].find('1080w') == -1 :
                    pass
                else:
                    x = image['srcset'].split(',')
                    for y in x:
                        if y.find('1080w') == -1 :
                            pass
                        else:
                            photo_counter += 1
                            print(link)
                            download_image(DIR_link,y,photo_counter)
 


 


#Function for main window UI
def mainUI():
 sg.theme('LightBrown1')   

 
 layout = [  [sg.Text('Input the site you want to crawl'),sg.Input("https://www.instagram.com/deutsch._.meme/", key='dclink')],
            [sg.Text('Select the output Folder'),sg.Input('D:\InstaImageCrawlDemo',key='dcfile'), sg.FolderBrowse()],
            [sg.Text('Input the Account'),sg.Input("soon.lee@stud.uni-due.de",key='dcmail')],
            [sg.Text('Input the Password'), sg.Input('Ude123!', key='Password', password_char='*')],
            [sg.Button('Run'), sg.Button('Cancel'), sg.Text("Platform"), sg.Combo(["Facebook","Instagram","Instagram_link","Instagram_download"], default_value="Facebook", key='Plat')] 
            ]

 # Create the Window
 window = sg.Window('Social Media Image Crawler v1.3', layout)

 # Event Loop to process "events" and get the "values" of the inputs
 while True:
     event, values = window.read()
     if event == sg.WIN_CLOSED or event == 'Cancel':
         #driver.quit() 
         break
     if event == 'Run':
         URL_link = values['dclink']
         DIR_link = values['dcfile']
         DC_ID = values['dcmail']
         DC_Pass = values['Password']
         DC_Plat = values['Plat']
         if DIR_link == "" :
             sg.popup("Please Input the File Directory", title='Error')
         elif URL_link == "" :
             sg.popup("Please Input Link you want to crawl", title='Error')
         elif DIR_link == "" :
             sg.popup("Please Input File Directory", title='Error')
         elif DC_ID == "" :
             sg.popup("Please Input the Facebook ID", title='Error')
         elif DC_Pass == "" :
             sg.popup("Please Input the Password", title='Error')
         elif DC_Plat =="Facebook":
             fbdatacrawl(URL_link,DIR_link,DC_ID,DC_Pass)
             sg.popup("Operation completed", title='Success')
         elif DC_Plat =="Instagram":
             instadatacrawl(URL_link,DIR_link,DC_ID,DC_Pass)
             sg.popup("Operation completed", title='Success')
         elif DC_Plat =="Instagram_link":
             instalinkcrawl(URL_link,DIR_link,DC_ID,DC_Pass)
             sg.popup("Operation completed", title='Success')
         elif DC_Plat =="Instagram_download":
             instaimgdown(URL_link,DIR_link,DC_ID,DC_Pass)
             sg.popup("Operation completed", title='Success')
         
         


#Main Function
#instadatacrawl()
#fbdatacrawl()
mainUI()
    
"""
test website and demo account

https://www.facebook.com/Deutsch-Spa%C3%9F-104211548118278/
soon.lee@stud.uni-due.de
Ude123!

https://www.instagram.com/deutsch._.meme/
https://www.instagram.com/explore/tags/germanmeme/
udetestsoonyik
Ude123!


"""
