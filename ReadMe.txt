CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Setting Up
 * Use Guide
 * Troubleshooting
 * Change Log
 * Contact

-----------------------
Introduction
-----------------------
This Image Crawler Tools is to capture Image from Popular Social Media Pages such as Facebook and Instagram 

For version 1.0, it only support Facebook page image crawling.



-----------------------
Requirement
-----------------------
 > Stable Internet Connection
 > Google Chrome
 > Chrome Driver

-----------------------
Setting up
-----------------------
1) Before using the tool, please intall the chrome, and check the chrome version at chrome://version/
2) Based on the chrome version, download the right version of chrome driver at https://chromedriver.chromium.org/
3) Extract the ZIP file downloaded, and paste chromedriver.exe at  C:\Users directory
4) Once it is done, execute IMG_crawler.exe to run the tools.

For developer:
1)install following package(also with standard python library from https://www.python.org/ )
pip install selenium
pip install PySimpleGUI
pip install bs4
pip install pandas
pip install urllib3
pip install wget

2) Open the ImageCrawler.py file
3) Run and edit whenever necessary




-----------------------
Use Guide
-----------------------
1) Input the necessary Input
2) Click Run
3) Let it run automatically, and once its done, it will prompt a success window
4) If something is wrong, refer to the prompted CMD, and copy the error for bug solving


-----------------------
Troubleshooting
-----------------------
1) Accidentally closed Chrome and causing the application stuck.
 > close the application, and execute again

2) Filled wrong data and clicked run
 > close the application, and execute again

-----------------------
Change Log
-----------------------
 *1.3 (Released at 10 December 2021)
- Added csv file output
- Fixed known Instagram Crawler bug

 *1.2 (Released at 12 August 2021)
- Added Instagram Image Crawling
- Fixed known FB Crawler bug

 *1.1 (Released at 10 June 2021)
- Added error prompt when all field is not filled
- Added link auto complete feature when user fill "https://www.facebook.com/deutschlandfunk" withou / at the end.
- Added Test Account for testing purpose

 *1.0 (Released at 9 June 2021)
- Support Facebook Image crawling




-----------------------
Contact
-----------------------
- For bug issue, contact soon.lee@stud.uni-due.de

