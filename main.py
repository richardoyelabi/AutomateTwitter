#FOR EACH OF CHROME, EDGE, AND FIREFOX BROWSERS,
#POST TWEETS FROM TWEETS.JSON EVERY 10-13 MINUTES
#ACCEPT NEW MESSAGE REQUESTS AND REPLY THEM WITH TEXT FROM DMREPLY.TXT

from selenium import webdriver
from selenium import common
from selenium.webdriver.common import keys

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import pyautogui

import time
import asyncio
import random
import json
import os

from threading import Thread, Lock

#lock to determine which thread is allowed to use screen gui
screen = Lock()


async def post_tweet(browser, driver, tweets):
    """ Post tweets"""
    
    def insert_tweet_text(tweet_text):
        driver.find_element(By.XPATH, "//div[@role='textbox']").send_keys(tweet_text)
        time.sleep(2)
        
    def insert_media(media_paths):
        element = driver.find_element(By.XPATH, "//div[@aria-label='Add photos or video']")
        screen.acquire()
        for media_path in media_paths:
            element.click()
            time.sleep(20)
            pyautogui.write(os.path.abspath(media_path))
            pyautogui.press("enter")
            time.sleep(30)
            driver.execute_script("arguments[0].scrollIntoView();", element)
        screen.release()
    
    err = 0
    
    while True:
        try:
            for tweet in tweets.values():
                driver.find_element(By.XPATH, "//a[@href='/home']").click()
                time.sleep(2)
                driver.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()
                time.sleep(4)
                for tweet_text, media_paths in tweet.items():
                    if (tweet_text and media_paths):
                        insert_tweet_text(tweet_text)
                        insert_media(media_paths)
                    elif (tweet_text):
                        insert_tweet_text(tweet_text)
                    elif (media_paths):
                        insert_media(media_paths)
                    else:
                        print('Nothing to tweet.')
                    driver.find_element(By.XPATH, "//div[@data-testid='tweetButton']").click()
                    time.sleep(7)
                
                    err = 0
                    await asyncio.sleep(60*random.choice([10,11,12,13]))
                    
        except:
            err += 1
            print(f"ATTENTION!!! An unexpected situation has come up while trying to post a tweet on {browser}. Please check and correct. Remove any pop ups or obstructions to the Twitter interface. Ideally, go back to 'https://twitter.com/home'. Also check if the last tweet was successfully sent.")
            print("Will try again after one minute.")
            if (err<10):
                print(f"Will refresh page after {10 - err} more tries.")
                time.sleep(60)
            else:
                driver.refresh()
                time.sleep(5)


async def message(browser, driver, dmreply):
    """ Check for message requests, accept, and reply """
    
    n = 0
    err = 0

    while True:
        try:
            driver.find_element(By.XPATH, "//a[@data-testid='AppTabBar_DirectMessage_Link']").click()
            try:
                driver.find_element(By.XPATH, "//a[@href='/messages/requests']").click()
                time.sleep(10)
                request = driver.find_elements(By.XPATH, "//div[@data-testid='conversation']")
            except:
                print(f"There are no more message requests to reply to on {browser}.")
                print("Will try again after five minutes.")
                await asyncio.sleep(60*5)
                continue
            if (len(request)>0):
                driver.find_element(By.XPATH, "//div[@data-testid='conversation']").click()
                driver.find_element(By.XPATH, "//span[text()='Accept']").click()
                driver.find_element(By.XPATH, "//div[@data-testid='dmComposerTextInput']").send_keys(dmreply)
                time.sleep(2)
                driver.find_element(By.XPATH, "//div[@data-testid='dmComposerTextInput']").send_keys(Keys.RETURN)
                time.sleep(1)
                n += 1
                err = 0
                if (n>=13):
                    n = 0
                    await asyncio.sleep(60*random.choice([17,18,19,20,21]))

        except:
            err += 1
            print(f"ATTENTION!!! An unexpected situation has come up while trying to reply a message request on {browser}. Please check and correct. Remove any pop ups or obstructions to the Twitter interface. Ideally, go back to 'https://twitter.com/home'. Also check if the last message request was successfully replied.")
            print("Will try again after one minute.")
            if (err<10):
                print(f"Will refresh page after {10 - err} more tries.")
                time.sleep(60)
            else:
                driver.refresh()
                time.sleep(5)


def launch_browser(browser, credentials, tweets, dmreply):
    """ Launches a specified web browser and logs in to Twitter"""
    
    async def execute(browser, driver, tweets, dmreply):
        await asyncio.gather(post_tweet(browser, driver, tweets), message(browser, driver, dmreply))
            
    
    #Login credentials
    username = credentials[0]
    password = credentials[1]
    
    #Initialize and go to twitter login page
    if (browser=="chrome"):
        driver = webdriver.Chrome()
    elif (browser=="firefox"):
        driver = webdriver.Firefox()
    elif (browser=="edge"):
        driver = webdriver.Edge()
    driver.implicitly_wait(20)
    driver.maximize_window()
    driver.get('https://twitter.com/i/flow/login')
    
    #Login
    driver.find_element(By.XPATH, "//input[@autocomplete='username']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@autocomplete='username']").send_keys(Keys.RETURN)
    driver.find_element(By.XPATH, "//input[@autocomplete='current-password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@autocomplete='current-password']").send_keys(Keys.RETURN)
    time.sleep(2)
    
    asyncio.run(execute(browser, driver, tweets, dmreply))


def main():
    """ Manages post_tweet() and message() and interfaces with the browsers """
    
    print("Initializing...")
    
    #Read tweets
    tweets_json = open("tweets.json")
    tweets = json.load(tweets_json)
    
    #Read dmreply
    dmreply_file = open("dmreply.txt")
    dmreply = dmreply_file.read()
    dmreply_file.close()
    
    #Read credentials
    credentials_json = open("credentials.json")
    credentials = json.load(credentials_json)
    
    t1 = Thread(target= launch_browser, args= ("chrome", credentials["chrome"], tweets, dmreply))
    t2 = Thread(target= launch_browser, args= ("firefox", credentials["firefox"], tweets, dmreply))
    t3 = Thread(target= launch_browser, args= ("edge", credentials["edge"], tweets, dmreply))

    t1.start()
    t2.start()
    t3.start()

    
if __name__ == "__main__":
    main()
