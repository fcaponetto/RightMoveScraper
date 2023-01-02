import os
import sys
import json
import math
import time
import requests
import random
import argparse
import datetime
from bs4 import BeautifulSoup


class TelegramBotSender:
    def __init__(self, token=None, chatid=None):
        self.telegramApiFile = "telegram_credentials"
        self.apiCredentials = dict()
        if token is None or chatid is None:
            self.apiCredentials = self.load_api_credentials()
        else:
            self.apiCredentials["token"] = token
            self.apiCredentials["chatid"] = chatid
            self.__save_api_credentials()

    def __save_api_credentials(self):
        with open(self.telegramApiFile, 'w') as file:
            file.write(json.dumps(self.apiCredentials))

    def load_api_credentials(self):
        if os.path.isfile(self.telegramApiFile):
            with open(self.telegramApiFile) as file:
                return json.load(file)
        else:
            return []

    def send_telegram_message(self, msg: str):
        request_url = "https://api.telegram.org/bot" + self.apiCredentials["token"] + "/sendMessage?chat_id=" + \
                      self.apiCredentials["chatid"] + "&text=" + msg
        requests.get(request_url)

    def send_telegram_messages(self, msg: []):
        for m in msg:
            self.send_telegram_message(m)


class RightMoveScraper:
    class Property:
        def __init__(self, l, p, a):
            self.link = l
            self.price = p
            self.address = a

        def __str__(self):
            return self.address + "\t" + self.price + "\t" + self.link

    def __init__(self,
                 url: str):
        self.base = "http://www.rightmove.co.uk"
        self._url = url
        self._dbFile = "searches.json"
        self.queries = self.load_queries()

    # load from file
    def load_queries(self):
        if os.path.isfile(self._dbFile):
            with open(self._dbFile) as file:
                return json.load(file)
        else:
            return dict()

    def save_queries(self):
        with open(self._dbFile, 'w') as file:
            file.write(json.dumps(self.queries))

    def page_count(self, soup):
        results = soup.find(class_="searchHeader-resultCount")
        tot = results.text.strip()
        print()
        print("Found " + tot + " properties")
        print()
        return math.ceil(int(tot) / 24)

    def __get_in_page(self, propertiesHtml, properties):
        for prop in propertiesHtml:
            price = prop.find("span", class_="propertyCard-priceValue").text.strip()
            address = prop.find("address", class_="propertyCard-address").text.strip()
            link = prop.find("a", class_="propertyCard-link")["href"]
            link = f"{self.base}{link}"

            if not properties.get(link):
                properties[link] = RightMoveScraper.Property(link, price, address)

    def __get_all_pages(self):
        p_url = f"{str(self._url)}"
        page = requests.get(p_url)
        soup = BeautifulSoup(page.content, "html.parser")

        # For each page, RightMove returns duplicate ads (Featured Property)
        properties = dict()

        for p in range(0, self.page_count(soup)):
            # Create the URL of the specific results page
            p_url = f"{str(self._url)}&index={p * 24}"
            page = requests.get(p_url)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="l-searchResults")
            propertiesHtml = results.find_all("div", class_="l-searchResult is-list")
            self.__get_in_page(propertiesHtml, properties)

        return properties

    def get_all_properties(self):
        return self.__get_all_pages()

    def get_new_properties(self):
        allProperties = self.__get_all_pages()
        newProperties = dict()

        ret = True
        if len(self.queries) == 0:
            ret = False

        for p in allProperties:
            if not self.queries.get(p):
                tmpProperty = allProperties.get(p)
                self.queries[tmpProperty.link] = {'address': tmpProperty.address, 'price': tmpProperty.price}
                # self.save_queries()
                newProperties[p] = allProperties.get(p)
                self.save_queries()

        if ret:
            return newProperties
        else:
            return []


class RightMoveRobot:
    def __init__(self,
                 rmScraper: RightMoveScraper,
                 telegram: TelegramBotSender,
                 delayMin: int = 0,
                 delayMax: int = 0,
                 notify: bool = True):
        self.__delayMin = delayMin
        self.__delayMax = delayMax
        self.__rmScraper = rmScraper
        self.__telegram = telegram
        self.__notify = notify

    def daemonize(self):
        while True:
            properties = self.__rmScraper.get_new_properties()
            if self.__notify:
                for p in properties:
                    tmpProperty = properties.get(p)
                    msg = "New result: \n" + tmpProperty.address + " - " + tmpProperty.price + " - " + tmpProperty.link
                    self.__telegram.send_telegram_message(msg)
                    print(msg)

            sleep_seconds = random.randint(self.__delayMin, self.__delayMax)
            date_and_time_now = datetime.datetime.now()
            time_change = datetime.timedelta(seconds=sleep_seconds)
            new_time = date_and_time_now + time_change
            print("Next request " + str(new_time))
            time.sleep(sleep_seconds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url for your new tracking search query")
    parser.add_argument('--delayMin', help="delay min for the daemon option (in seconds)")
    parser.set_defaults(delayMin=1800)
    parser.add_argument('--delayMax', help="delay max for the daemon option (in seconds)")
    parser.set_defaults(delayMax=3600)
    parser.add_argument('--addtoken', dest='token', help="telegram setup: add bot API token")
    parser.add_argument('--addchatid', dest='chatid', help="telegram setup: add bot chat id")
    args = parser.parse_args()

    if args.url is not None:
        rmScraper = RightMoveScraper(args.url)

        telegramBot = TelegramBotSender()
        if args.token is not None and args.chatid is not None:
            telegramBot = TelegramBotSender(args.token, args.chatid)

        rmRobot = RightMoveRobot(rmScraper, telegramBot, args.delayMin, args.delayMax)

        try:
            rmRobot.daemonize()
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
    else:
        print("no argument provided")
