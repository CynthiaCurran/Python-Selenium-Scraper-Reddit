from scraper import RedditScraper
from settings import REDDIT_USER, REDDIT_PASS, FEED_URL

if __name__ == "__main__":

    if not REDDIT_USER or not REDDIT_PASS:
        raise Exception("Username or password is incorrect or missing.")
    else:
        print("Credentials valid")

    scraper = RedditScraper()
    
    scraper.login(REDDIT_USER, REDDIT_PASS)
    scraper.scrapeImageURLs(FEED_URL)

    scraper.close_browser()