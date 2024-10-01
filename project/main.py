import crawling

if __name__ == 'main':
    # We create a bot to search in the webpage
    crawler_bot = crawling.simpleCrawler(10);

    # We execute our robot
    crawler_bot.start_crawl()
    
    