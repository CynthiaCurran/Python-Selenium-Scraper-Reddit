from scraper import RedditScraper
from settings import REDDIT_USER, REDDIT_PASS, FEED_URL, NUM_IMGS

if __name__ == "__main__":

    if not REDDIT_USER or not REDDIT_PASS:
        raise Exception("Username or password is incorrect or missing.")
    else:
        print("Credentials valid")

    scraper = RedditScraper()
    
    scraper.login(REDDIT_USER, REDDIT_PASS)
    imageNames = scraper.scrapeImageURLs(FEED_URL, int(NUM_IMGS))   #grab the names of the images from the feed

    scraper.close_browser()

    scraper.downloadImages(imageNames)
