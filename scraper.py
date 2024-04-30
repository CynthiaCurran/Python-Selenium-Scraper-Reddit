from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.relative_locator import locate_with
from settings import OPTIONS
import os
import time
import requests
import re


class RedditScraper():
    """
    Scrapes a predetermined number of images from a specified Reddit feed.
    This can be the home page, a certain user's posts, or your saved posts.
    This may violate Reddit's Terms of Service and should not be run depending on what is being scraped. 
    FOR EDUCATIONAL PURPOSES ONLY
    """

    def __init__(self):
        self.browser = webdriver.Chrome(OPTIONS)
        self.logged_in = False
        print("Browser Opened Successfully")

    def close_browser(self):
        self.browser.close()

    def open_browser(self):
        self.browser = webdriver.Chrome(OPTIONS) #Original instance and info is lost. Reinitialize    


    #TBD: Add feedElement selection logic for different feed types and finish img grabbing logic
    def scrapeImageURLs(self, FEED_URL, NUM_IMGS):
        """
        From the selected Reddit feed, scrape the file names of images from posts.
        This is to prep them for download later. 
        Reddit grabs images by submitting a URL query with a specific file name.
        Unaltered images can be grabbed from Reddit with this file name in a specific query.
        """

        print("Scraping images...")

        #load reddit feed
        self.browser.get(FEED_URL)
        time.sleep(5)

        feedElement = ""

        if "/user/" in FEED_URL:  #for any user section
            feedElement = self.browser.find_element(By.XPATH, "/html/body/shreddit-app/report-flow-provider/div/div[1]/div/main/div[3]")
        elif "/r/popular/" in FEED_URL:
            feedElement = self.browser.find_element(By.XPATH, "/html/body/shreddit-app/div/div[1]/div[2]/main/dsa-transparency-modal-provider/report-flow-provider/shreddit-feed")
        elif "https://www.reddit.com/?feed=home" == FEED_URL or "https://www.reddit.com" == FEED_URL or "https://www.reddit.com/" == FEED_URL or "/r/all/" in FEED_URL:
            feedElement = self.browser.find_element(By.XPATH, "/html/body/shreddit-app/div/div[1]/div/main/dsa-transparency-modal-provider/report-flow-provider/shreddit-feed")
        elif "/r/" in FEED_URL: #any subreddit
            feedElement = self.browser.find_element(By.XPATH, "/html/body/shreddit-app/dsa-transparency-modal-provider/report-flow-provider/div/div[1]/div[2]/main/div[2]")

        if feedElement == "" or feedElement is None:
            raise Exception("Feed not found")

        imageNames = {}

        scrollHeight = 0
        newScrollHeight = 0

        #loop to grab image file names from the URLs. 
        #These can be used to grab unaltered images with different URLs later
        while True:
            imageElements = feedElement.find_elements(By.TAG_NAME, 'img')   #grab image elements
            for i in imageElements:
                url = i.get_attribute("src")
                alt = i.get_attribute("alt")

                if url is None or alt is None:
                    continue

                if "external-preview.redd.it" in url:   #ignore advertisements
                    continue

                #isolate the image file name from the URL
                if "?" in url or "-" in url:
                    url = url.split("?")[0].split("-")[-1]
                else:   #url is formatted as https://i.redd.it/filename.jpeg
                    url = url.split("/")[-1]
                url = url.split("/")[-1]

                imageNames[url] = alt  #store the URL


            #Start scrolling down. Does it incrementally to allow images to load without skipping
            self.browser.execute_script("window.scroll(0, window.scrollY + 2000);")
            newScrollHeight = self.browser.execute_script("return window.scrollY;")

            if scrollHeight == newScrollHeight:
                break
            else:
                scrollHeight = newScrollHeight

            if len(imageNames) >= NUM_IMGS:
                break

            time.sleep(10)

        print("Image Scraping Successful")
        return imageNames


    def downloadImages(self, imageNames):

        print("Downloading images...")

        #create output dir if it does not exist
        dir = "outputs"

        if not os.path.exists(dir):
            os.makedirs(dir)

        #navigate to the outputs dir
        os.chdir("./outputs")


        #download images
        for key, value in imageNames.items():
            url = "https://i.redd.it/{}".format(key)
            filename = re.sub(r'[^A-Za-z0-9\s]', '', value) + " - " + key
            img_data = requests.get(url).content

            if "ADVERTISING" in filename:   #ignore advertising
                continue

            with open(filename, 'wb') as handler:
                handler.write(img_data)

            time.sleep(1) #add a delay to avoid bot detection


        #navigate back to the main folder
        os.chdir("..")

        print("Downloading Complete")