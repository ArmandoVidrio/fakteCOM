import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

class RobotManager:
    """
    Class in charge of manage the robots.txt:
    Attributes:
    -----------
    url: str
        Base URL of the website where the 'robots.txt' file will be fetched

    Methods:
    --------
    get_robot_txt(url: str) -> str:
        Set the content of the 'robots.txt' file from the specified URL in the attribute robots_info_txt
    """
    # Constructor
    def __init__(self, url) -> None:
        self.url = url
        self.robots_info_txt = ""
        self.disallowed_routes = []
        
        # We set the attribute robots_info_txt with the info of the robots.txt file
        self.set_robots_info_txt()
        self.set_disallowed_routes()

    # Setters
    def fetch_robots_info_txt(self) -> None:
        # Url where the robot info is stored
        robot_url = self.url + 'robots.txt'

        # Get the response of the webpage
        response = requests.get(robot_url)
        
        # Set the info in the class attribute
        self.robots_info_txt = response.text

        return None
    
    def set_disallowed_routes(self) -> None:
        robots_info = self.robots_info_txt

        # We filter the text to find the disallowed routes
        for line in robots_info.split("\n"):
            if "Disallow" in line:
                route = line.split(":")[1].strip()
                self.disallowed_routes.append(route)

        return self.disallowed_routes

    #  Getters
    def get_robots_info_txt(self) -> str:
        return self.robots_info_txt
    
    def get_disallowed_routes(self) -> list:
        return self.disallowed_routes     

class simpleCrawler:
    def __init__(self, base_url, max_pages) -> None:
        self.base_url = base_url
        self.visited_urls = set()
        self.max_pages = max_pages

    def crawl(self, url):
        # We check if we already didn't visit the page
        if url in self.visited_urls:
            return
        
        # We validate that we havent reache the max num of pages
        if len(self.visited_urls) >= self.max_pages:
            return
        
        # We try to visit the page
        try:
            page_request = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"error requesting a url {url}: {e}")

        # Mark the url as visited
        print(f"Visiting: {url}")
        self.visited_urls.add(url)

        # We search all the links in the webpage
        soup = BeautifulSoup(page_request.text, 'html.parser')

        # We extract the title page and clean it
        page_title = soup.find("title").text.strip()

        # We update the path to save the file
        results_path = self._updateResultPath(page_title)

        # We save our .txt on the results dir
        with open(results_path, "w", encoding='utf-8') as document:
            document.write(soup.prettify())

        # We find all the links from the webpage
        links_in_page = soup.find_all("a", href=True)

        for link in links_in_page:
            next_url = urljoin(url, link['href'])
            self.crawl(next_url)

    def _updateResultPath(self, title) -> str:
        # We eliminate the simbols and spaces from the title
        clean_title = re.sub(r'[\\/*?:"<>| ]', "", title)

        # Create a path for save the results
        results_path = os.path.join("./project/search-results", f"{clean_title}.txt")

        return results_path

    def start_crawl(self):
        self.crawl(self.base_url)

url = "https://www.linkedin.com"

crawler = simpleCrawler(url, 100)

crawler.start_crawl()