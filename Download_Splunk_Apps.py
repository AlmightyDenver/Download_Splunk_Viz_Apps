#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Python = 3.7
# Selenium = 4.5.0
# Created By  : DenverAlmighty
# Created Date: 2022-10-24
# Updated Date : 2022-10-24
# version = '2.0.0'
# ---------------------------------------------------------------------------

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import re
import codecs
import getpass
import sys

# # Splunk ID, PW
# spkid = 'yjlee'
# spkpw = ''
# # file, chromedriver directory
# html_file = '/Users/denver/Downloads/Splunkbase_viz.html'
# # html_file = '/Users/denver/Downloads/Splunkbase_visualization.html'
# chromedriver = '/Users/denver/Documents/Tennis/chromedriver'

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
    # Splunk ID, PW
    spkid = input('Enter Splunk ID : ')
    spkpw = getpass.getpass('Enter Splunk Password : ')
    # file, chromedriver directory
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
    # reset download percent
    dl = 0
    
    # start download
    for i in range(0, len(link_list)):
        # downloading percent total length
        link=link_list[i]
        total_length = len(link_list)-1
        
        #except link 
        if link == 'https://splunkbase.splunk.com/app/4537' or link == 'https://splunkbase.splunk.com/app/3205': 
            continue
        
        driver.get(link)
                
        #if appname not match *viz* OR *visualization* -> continue(do not download)
        appname = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[1]/div/div/div[2]/h1').text
        appname_viz = re.findall(r"Viz|viz|visualization|Visualization", appname)
        if not len(appname_viz):
            continue
        else:
            # login at first time
            if flag == 0:
                flag = 1
                # click "login to download" button
                driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/button/span/span[2]').click()
                driver.implicitly_wait(5)
                # login
                # id input
                driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(spkid)
                # click next button
                driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/div[4]/button').click()
                # pw input
                driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(spkpw)
                #click login button
                driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/div[5]/button').click()
                
            # if button name != Download -> Do not click
            button_value = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/button/span/span[2]').text
            if button_value != 'Download':
                continue
            try:
                #click download button
                element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/button').click()
                
                # + download perc
                dl += 1
                # Warning confirm download
                if driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div/div').text == 'Warning':
                    driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[3]/button[2]/span/span').click()
                # accept license agreement
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div[2]').click()
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div[3]').click()
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[3]/a').click()
                # print downloading percent
                done = int(50 * dl / total_length)
                sys.stdout.write("\r downloading [%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
            except Exception as e:
                print(e)

if __name__=='__main__':
    initPage()
    main()