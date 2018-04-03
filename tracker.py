# -*- coding: utf-8 -*-
# @Author: Theo
# @Date:   2018-04-01 00:43:57
# @Last Modified by:   TheoLong
# @Last Modified time: 2018-04-03 01:20:17
from personal_info import get_info
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import gmtime, strftime
from notifier import updateEmail
import argparse
import time
'''
=============       User Info       ============
'''
info = get_info()
DL = info['DL']
DOB = info['DOB']
oldStatus = info['oldStatus']
restartCounter = info['restartCounter']
refreshRate = info['refreshRate']
codeshareLogAddr = info['codeshareLogAddr']

def parse():
    parser = argparse.ArgumentParser(description='Web browser driver mode: chrome/phantomjs (default chrome)')
    parser.add_argument('-d', dest='driverMode',  help="web driver mode", type = str, action="store", default="chrome")
    args = parser.parse_args()
    return args.driverMode

def getCurrentTime():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def printLog(logs):
    global driverMode
    if driverMode == "chrome":
        driver = webdriver.Chrome()
    elif driverMode == "phantomjs":
        driver = webdriver.PhantomJS()
    elif driverMode == "firefox":
        driver = webdriver.Firefox()
    else:
        print ('>>>>>>>>>>>>>   Error: invalid webdriver')
    driver.get(codeshareLogAddr)
    time.sleep(1)
    actions = ActionChains(driver)
    print (logs)
    actions.send_keys(logs)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(0.5)
    driver.close()

def callUpdate(things2Update, changedTime):
    updateEmail(things2Update, changedTime)

def checkStatus(oldStatus, newStatus, counter):
    if oldStatus[0] != newStatus[0]:
        things2Update = 'Background Check status changed from ' + '[' + oldStatus[0] + ']' + ' to ' + '[' + newStatus[0] + ']'
        callUpdate(things2Update, getCurrentTime())
        printLog(getCurrentTime() + ': UPDATES SENT TO EMAIL!')
        oldStatus[0] = newStatus[0]

    elif oldStatus[1] != newStatus[1]:
        things2Update = 'LTC status changed from ' + '[' + oldStatus[1] + ']' + ' to ' + '[' + newStatus[1] + ']'
        callUpdate(things2Update, getCurrentTime())
        printLog(getCurrentTime() + ': UPDATES SENT TO EMAIL!')
        oldStatus[1] = newStatus[1]

    else:
        printLog(getCurrentTime() + ': ' + str(oldStatus) + ' Restart counter = ' + str (counter))

driverMode = parse()

while 1:
    printLog('>>>>>>>>>>>>> starting driver')
    if driverMode == "chrome":
        driver = webdriver.Chrome()
    elif driverMode == "phantomjs":
        driver = webdriver.PhantomJS()
    elif driverMode == "firefox":
        driver = webdriver.Firefox()
    else:
        print ('>>>>>>>>>>>>>   Error: invalid webdriver')


    driver.get("https://txapps.texas.gov/txapp/txdps/ltc/")
    driver.find_element_by_xpath('//*[@id="renew-trigger"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="DL"]').send_keys(DL)
    driver.find_element_by_xpath('//*[@id="dob"]').send_keys(DOB)
    driver.find_element_by_xpath('//*[@id="continue"]').click()
    printLog('>>>>>>>>>>>>> Login')

    counter = restartCounter
    while counter != 0:
        BGC_status=driver.find_element_by_xpath('//*[@id="statii"]/ul/li[11]').text.split(': ')
        LTC_status=driver.find_element_by_xpath('//*[@id="statii"]/ul/li[12]').text.split(': ')

        BGC_status=BGC_status[1]
        LTC_status=LTC_status[1]

        currentStatus = [BGC_status,LTC_status]
        checkStatus(oldStatus, currentStatus, counter)

        time.sleep(refreshRate)
        counter = counter - 1
        driver.refresh();
        
    driver.close()
    printLog('>>>>>>>>>>>>> Driver restarting')
    

