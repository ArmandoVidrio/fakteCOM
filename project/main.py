import requests
from bs4 import BeautifulSoup
import time
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

    # Methods

    # Setter
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

def crawl_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup)
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la pagina {e}")

def can_crawl(url:str) -> bool:
    print("en la funcion")
    robots_url = url + '/robots.txt'
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            # Get the text of the robot
            robot_txt = response.text
            des_ruts = []
            for linea in robot_txt.split("\n"):
                if "Disallow" in linea:
                    ruta = linea.split(":")[1].strip()
                    if ruta:
                        des_ruts.append(ruta)
            # print routes
            if len(des_ruts) == 0:
                print("There are no fucking routes")
            else:
                print(f"las fakins rutas +18 son: {des_ruts}")

    except requests.exceptions.RequestException as e:
        print(f"Problemas de acceder a al robot {robots_url}")
        return True
            

#crawl_page("https://www.linkedin.com/feed/")
#can_crawl("https://www.netflix.com/")

url = "https://www.netflix.com/"

robot_manager = RobotManager(url)

hot_routes = robot_manager.get_disallowed_routes()
print(hot_routes)