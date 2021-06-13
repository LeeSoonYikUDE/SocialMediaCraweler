"""
Developed on 2021-06-09

"""

#imports section
import os
from sys import platform
from PySimpleGUI.PySimpleGUI import Combo, Input
from selenium.webdriver.common import utils
import wget
import time
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import urllib.request as utr


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

#function to initialize webdriver
def driverini():
 chrome_option = webdriver.ChromeOptions()
 prefs = {"profile.default_content_setting_values.notifications" : 2}
 chrome_option.add_experimental_option("prefs",prefs)
 driver = webdriver.Chrome('C:/Users/chromedriver.exe',chrome_options=chrome_option)
 return driver


#Function of FacebookImageCrawling
def fbdatacrawl(URL_link,DIR_link,DC_ID,DC_Pass,DC_Plat):

 #notification handling (Referred pythonjar from Stackoverflow)
 

 #Chrome Driver Path
 driver = driverini()

 #Web page to login
 driver.get("http://www.facebook.com")


 button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='cookie-policy-dialog-accept-button']"))).click()
 username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
 password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

 #enter username and password
 time.sleep(2)
 username.clear()
 username.send_keys(DC_ID)
 password.clear()
 password.send_keys(DC_Pass)

 #target the login button and click it
 button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


 #wait 5 seconds to allow your new page to load
 time.sleep(5)
 images = []

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
   # print("printing anchors")
   # print(anchors)
    anchors = [a for a in anchors if str(a).startswith(URL_link + "photos/")]

    #extract the [1]st image element in each link
    for a in anchors:
        driver.get(a) #navigate to link
        time.sleep(5) #wait a bit
        img = driver.find_elements_by_tag_name("img")
        images.append(img[1].get_attribute("src"))
 
 if DIR_link=="" :
  path = os.getcwd()
  path = os.path.join(path, "OutputFolder")
  if os.path.isdir(path +"OutputFolder") :
      os.mkdir(path)
  
 else:
     path= DIR_link 

 counter = 0
 for image in images:
     save_as = os.path.join(path, str(counter) + '.jpg')
     wget.download(image, save_as)
     counter += 1
 

#function to InstagramImageCrawling
def instadatacrawl(URL_link,DIR_link,DC_ID,DC_Pass,DC_Plat):
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
 alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
 driver.get(URL_link)
 autoscroll(driver)

 
 if URL_link[-1] == '/':
  URL_link= URL_link[:-1]
 if DIR_link [-1] != '/':
  DIR_link = DIR_link +"\\"

 base = BeautifulSoup(driver.page_source,'html.parser')
 post_number = int(base.find('span',class_ = 'g47SY').get_text())
 print(f'Number of Post {post_number}')
 post_li_link = []
 for i in range(int(post_number/10)): 
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        soup = BeautifulSoup(driver.page_source,'html.parser')
        posts = soup.findAll('a')
        for post in posts:
            if '/p/' in post['href']:
                post_li_link.append(post['href'])
        time.sleep(1.5)
        vi_counter = 0
        photo_counter = 0
        for lk in post_li_link:
         link = URL_link + lk
         driver.get(link)
         time.sleep(1)
         soup = BeautifulSoup(driver.page_source,'html.parser')
         images = soup.findAll('img')
         for image in images:
            if image.has_key('srcset'):
                if image['srcset'].find('1080w') == -1 :
                    pass
                else:
                    x = image['srcset'].split(',')
                    for y in x:
                        if y.find('1080w') == -1 :
                            pass
                        else:
                            photo_counter += 1
                            download_image(DIR_link,y,photo_counter)
                          


def download_image(DIR_link,image_link,counter):
    file_name =  DIR_link  +  (str(counter)) + '.jpg'
    print(file_name)
    img_li = image_link.replace(' 1080w','')
    r = utr.urlopen(img_li)
    with open(file_name, "wb" ) as f:
        f.write(r.read())


 
 
 




 


#Function for main window UI
def mainUI():
 sg.theme('LightBrown1')   

 
 layout = [  [sg.Text('Input the site you want to crawl'),sg.Input("https://www.instagram.com/deutsch._.meme/", key='dclink')],
            [sg.Text('Select Folder that you want to save image'),sg.Input('D:\PythonProject\whar',key='dcfile'), sg.FolderBrowse()],
            [sg.Text('Input the Account'),sg.Input("",key='dcmail')],
            [sg.Text('Input the Password'), sg.Input('', key='Password', password_char='*')],
            [sg.Button('Run'), sg.Button('Cancel'), sg.Text("Platform"), sg.Combo(["Facebook","Instagram"], default_value="Instagram", key='Plat')] 
            ]

 # Create the Window
 window = sg.Window('Social Media Image Crawler v1.1', layout)

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
             fbdatacrawl(URL_link,DIR_link,DC_ID,DC_Pass,DC_Plat)
             sg.popup("Operation completed", title='Success')
         elif DC_Plat =="Instagram":
             instadatacrawl(URL_link,DIR_link,DC_ID,DC_Pass,DC_Plat)
             sg.popup("Operation completed", title='Success')
         
         


#Main Function
#instadatacrawl()
#fbdatacrawl()
mainUI()
    




















 










