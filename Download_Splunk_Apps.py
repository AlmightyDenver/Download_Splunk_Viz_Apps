from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
import re
import codecs
import getpass
import sys

# # Splunk ID, PW
# spkid = 'yjlee'
# spkpw = ''
# # file, chromedriver directory
# html_file = '/Users/denver/Downloads/Splunkbase_viz.html'
# chromedriver = '/Users/denver/Downloads/chromedriver'

def initPage():
    name = """            
 ____                _           _   
|    \ ___ _ _ _ ___| |___ ___ _| |  
|  |  | . | | | |   | | . | .'| . |  
|____/|___|_____|_|_|_|___|__,|___|  
                                
 _____     _         _               
|   __|___| |_ _ ___| |_             
|__   | . | | | |   | '_|            
|_____|  _|_|___|_|_|_,_|            
      |_|                                              
     _                               
 _ _|_|___    ___ ___ ___ ___        
| | | |- _|  | .'| . | . |_ -|       
 \_/|_|___|  |__,|  _|  _|___|       
                 |_| |_|             
"""
    print(name)
    
def main():
    spkid = input('Enter Splunk ID : ')
    spkpw = getpass.getpass('Enter Splunk Password : ')
    html_file = input('Enter HTML File Location </my/dir/splunkbase.html> : ')
    chromedriver = input('Enter ChromeDriver Location <my/dir/chromedriver> : ') 
    
    # open html file
    f = codecs.open(html_file, "r", "utf-8")
    r = f.read()
    # extract app links using regex
    link_list = re.findall(r"https\:\/\/splunkbase\.splunk\.com\/app\/\d+", r)
    link_list=sorted(list(set(link_list)))

    # open chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(3)

    # reset flag
    flag = 0
    dl = 0
    # start download
    for i in range(0, len(link_list)):
        link=link_list[i]
        total_length = len(link_list)-1
        if link == 'https://splunkbase.splunk.com/app/4537':
            continue
        
        driver.get(link)
        # login at first time
        if flag == 0:
            flag = 1
            #accept cookie
            driver.find_element_by_xpath('//*[@id="agree"]/div[3]/div').click()
            # click "login to download" button
            driver.find_element_by_xpath('//*[@id="login-to-download"]').click()
            # login
            driver.find_element_by_xpath('//*[@id="username"]').send_keys(spkid)
            driver.find_element_by_xpath('//*[@id="login-form"]/div[2]/div[4]/button').click()
            driver.find_element_by_xpath('//*[@id="password"]').send_keys(spkpw)
            driver.find_element_by_xpath('//*[@id="login-form"]/div[2]/div[5]/button').click()
        #click download button
        element = driver.find_element_by_xpath('//*[@id="details-download"]').click()
        dl += 1
        # accept license agreement
        driver.find_element_by_xpath('//*[@id="download-agree"]').click()
        driver.find_element_by_xpath('//*[@id="download-lead"]').click()
        driver.find_element_by_xpath('//*[@id="agree"]/div[3]/input').click()
        # print downloading percent
        done = int(50 * dl / total_length)
        sys.stdout.write("\r downloading [%s%s]" % ('=' * done, ' ' * (50-done)) )    
        sys.stdout.flush()

if __name__=='__main__':
    initPage()
    main()
