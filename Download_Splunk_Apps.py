#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Python = 3.7
# Selenium = 4.5.0
# Created By  : DenverAlmighty
# Created Date: 2022-10-24
# Updated Date : 2022-11-01
# version = '1.2.0'
# ---------------------------------------------------------------------------

import sys
import time
import json
import re
import requests
import argparse
import getpass
from selenium.webdriver.common.by import By
from selenium import webdriver


def init_page():
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
    sys.stdout.write(name)


def draw_pb(pb, total_len, title):
    perc = int(pb / total_len * 100)
    done = int(perc / 2)
    sys.stdout.write('\r %02d%% [%s%s] %s' % (perc, '=' * done, ' ' * (50-done), title))   
    sys.stdout.flush()


def input():
    pw = getpass.getpass('Enter Splunk Password : ')
    parser = argparse.ArgumentParser(description='Unzip .tgz file and edit apps.conf file', add_help=True)
    parser.add_argument('--id', '-i', dest='id', help='(required) Enter Splunk ID')
    parser.add_argument('--keyword', '-k', dest='keyword', help='(required) Enter Search Keyword')
    parser.add_argument('--driverlocation', '-driver', dest='driver', help='(required) Enter Driver Dir')
    args = parser.parse_args()
    
    id = args.id
    kw = args.keyword
    driver = args.driver
    
    return id, pw, kw, driver


def req_func(link, **kargs):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    try:
        res = requests.get(link, headers=header)
        if res.status_code != 200:
            raise Exception('ERROR status_code : {res.status_code}')
        else: 
            return res.text
    except Exception as e:
        sys.stderr.write(e)
        sys.exit()


def get_download_links(keyword):
    base_link = 'https://api.splunkbase.splunk.com/api/v2/apps?product=splunk&product_types=enterprise&'
    # get apps total count
    total = 0
    link = '%squery=%s&offset=0' % (base_link, keyword)
    res = req_func(link)
    # str to dict
    res_dict = json.loads(res)
    total = res_dict['total']
    # print(total)

    # init offset, res_txt
    offset = 0
    res_txt = ''
    res = {}
    while offset < total:
        link = '%sinclude=release&limit=100&query=%s&order=relevance&offset=%s' % (base_link, keyword, offset)
        res[offset] = json.loads(req_func(link))
        offset += 100
        
    return total, res


def login(id, pw, driver):
    # login
    driver.get('https://login.splunk.com/')
    # id input
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(id)
    # click next button
    driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/div[4]/button').click()
    # pw input
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pw)
    # click login button
    driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/div[5]/button').click()
    # wait
    driver.implicitly_wait(5)
    time.sleep(5)
    
    return driver


def main():
    # init error message to print at last
    ERR_MSG = ''

    #input
    id, pw, kw, driver = input()

    # get app download links
    total, res_dict = get_download_links(kw)

    # extract appname and download link from dict
    apps = []
    for k in res_dict.keys():
        tmp_lst = res_dict[k]['results']
        for dic in tmp_lst:
            apps.append({'app_name':dic['app_name'], 'link': dic['release']['path']})

    # create driver
    driver = webdriver.Chrome(driver)
    # login
    sys.stdout.write('Try to Login...')
    driver = login(id, pw, driver)


    # init count, progress bar, total length of links list
    cnt = 0
    pb = 0
    total_len = len(apps)
    
    # download
    for i in range(total_len):
        #draw progress bar
        pb += 1
        
        dic = apps[i]
        # check app_name matchs keyword or not
        if not re.compile(kw, re.I).search(dic['app_name']):
            ERR_MSG += 'ERROR App Name %s does not match %s\n' % (dic['app_name'], kw)
            continue
        # check link == None or not
        elif dic['link'] == None:
            ERR_MSG += 'ERORR invalid argument: "url" must be string   link : %s\n' %dic['link']
            continue
        
        # download
        link = dic['link']
        title = 'Started Download%s%s  %s' % ('.'*(pb%3), ' '*(3-pb%3), dic['app_name'] )
        draw_pb(pb, total_len, title)
        try:
            driver.get(link)
            cnt += 1
        except Exception as e:
            ERR_MSG += e
            continue

        time.sleep(1)

    # Complete Download
    sys.stdout.write('%s\n%s\nDownload %d Apps Completed Successfully.\n\
        %d Exception Occurred.\nProgramme would be terminated after 30 seconds\n%s'\
        % (ERR_MSG, '=' * 70, cnt, total-cnt, '=' * 70))
    time.sleep(30)
    driver.quit()



if __name__=='__main__':
    init_page()
    main()