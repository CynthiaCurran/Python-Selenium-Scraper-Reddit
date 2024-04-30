from scraper import RedditScraper
from settings import REDDIT_USER, REDDIT_PASS, FEED_URL, NUM_IMGS

if __name__ == "__main__":

    scraper = RedditScraper()
    
    imageNames = scraper.scrapeImageURLs(FEED_URL, int(NUM_IMGS))   #grab the names of the images from the feed

    scraper.close_browser()

    scraper.downloadImages(imageNames)
