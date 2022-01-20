import requests
from bs4 import BeautifulSoup


class FindLink:
    url = 'https://playisgame.com/halyava/epic-store/'  # website link that we want to parse

    def find_link(self):  # find game link
        pg = requests.get(self.url)  # get html code of website
        soup = BeautifulSoup(pg.text, "html.parser")  # initialise a tool for parsing
        link = soup.find('h2', class_="pp-post-title")  # looking for the parent tag of the link by class
        link = link.find("a").get("href")  # we are looking for the a tag in the received code, from which we get link
        return link