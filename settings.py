import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#Login credentials
REDDIT_USER = os.getenv("REDDIT_USER")
REDDIT_PASS = os.getenv("REDDIT_PASS")
FEED_URL = os.getenv("FEED_URL")    #The reddit page we are downloading images from

OPTIONS = webdriver.ChromeOptions()
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
OPTIONS.add_argument('--user-agent={}'.format(userAgent))
OPTIONS.add_argument("--blink-settings=imagesEnabled=false")    #saves processing by not loading images
OPTIONS.add_argument("--disable-notifications")
# OPTIONS.add_argument("headless")  #For debugging
# OPTIONS.add_argument("--log-level=3")  #For debugging

