from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.relative_locator import locate_with
from settings import OPTIONS
import os
import time


class RedditScraper():
    """
    Scrapes a predetermined number of images from a specified Reddit feed.
    This can be the home page, a certain user's posts, or your saved posts.
    This may violate Reddit's Terms of Service and should not be run depending on what is being scraped. 
    FOR EDUCATIONAL PURPOSES ONLY
    """

    def __init__(self):
        self.browser = webdriver.Chrome(OPTIONS)
        print("Browser Opened Successfully")

    def close_browser(self):
        self.browser.close()

    def open_browser(self):
        self.browser = webdriver.Chrome(OPTIONS) #Original instance and info is lost. Reinitialize




    def login(self, username, password):
        """Log into an account."""

        self.browser.get("https://www.reddit.com/login/")
        time.sleep(2)

        #Click login button
        #self.browser.find_element(by=By.ID, value='login-button').click()
        time.sleep(2)

        #enter username
        self.browser.find_element(by=By.ID, value='login-username').send_keys(username)
        time.sleep(2)

        #enter password
        self.browser.find_element(by=By.ID, value='login-password').send_keys(password)
        time.sleep(2)

        #click login button
        #the login button is buried in a few nested shadow roots, so select down until it is visible
        root = self.browser.find_elements(By.TAG_NAME, "shreddit-overlay-display")
        root = self.expand_shadow_element_arr(root, 0)
        root = root.find_element(By.CSS_SELECTOR, "shreddit-signup-drawer")
        root = self.expand_shadow_element(root)
        root = root.find_element(By.CSS_SELECTOR, "shreddit-slotter")
        root = self.expand_shadow_element(root)
        root = root.find_element(By.CSS_SELECTOR, "button").click()
        time.sleep(10)  #give time to login

    def expand_shadow_element_arr(self, element, index):
        """
        Selenium needs to manually find shadow roots to select elements inside them.
        Returns the shadow element within a certain index of an element.
        """
        shadow_root = self.browser.execute_script('return arguments[0][{index}].shadowRoot'.format(index=index), element)
        return shadow_root
    
    def expand_shadow_element(self, element):
        """
        Selenium needs to manually find shadow roots to select elements inside them.
        Returns the shadow element within an element.
        """
        shadow_root = self.browser.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root
    



    def scrapeImageURLs(self, FEED_URL):
        """
        From the selected Reddit feed, scrape the URLs of the posts with images.
        This is to prep them for image scraping later.
        """
        print(FEED_URL)


    def folder_write_test(self):
        os.chdir("./output")
        with open('test.txt', 'w') as test:
            test.write("Hello test")