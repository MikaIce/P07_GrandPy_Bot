""" This module is request the Google Maps & Wikipedia API's with the
parsed message """

import requests
import random
from app.config import config as c


class Request:
    """ this class will send the request to the API's """

    def __init__(self, query=None):

        self.query = query
        self.wiki_result = None
        self.lat = ""
        self.lng = ""
        if query is not None:
            self.first_request_wiki()

    def first_request_wiki(self):
        """ Send a request to Wikipedia API with the user text """

        url = "https://fr.wikipedia.org/w/api.php"
        payload = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": "{}".format(self.query),
            "srlimit": "1"
        }
        if self.query == []:  # if no query reach Grandpy
            self.wiki_result = random.choice(c.GRANDPY_EMPTY)
            return self.wiki_result
        else:
            try:
                request = requests.get(url, params=payload)
                json = request.json()
                self.get_wiki_page_id(json)
                print(json)
                return json

            except ValueError:
                self.wiki_result = random.choice(c.GRANDPY_DONT_UNDERSTAND)
                return self.wiki_result

    def get_wiki_page_id(self, json):
        """ get the page_id of the first request """

        try:
            data = json
            pages = data['query']['search']
            for key, value in enumerate(pages):
                page_id = str(value['pageid'])
            self.second_request_wiki(page_id)
            return page_id

        except UnboundLocalError:
            # if no result :
            # UnboundLocalError: local variable 'page_id' referenced
            # before assignment in next method 'second_request_wiki'
            self.wiki_result = random.choice(c.GRANDPY_DONT_UNDERSTAND)
            return self.wiki_result

    def second_request_wiki(self, page_id):
        """ Send a second request with the page_id to extract datas """

        url = "https://fr.wikipedia.org/w/api.php"
        payload = {
            "action": "query",
            "format": "json",
            "prop": "extracts|coordinates",
            "exsentences": "7",
            "explaintext": "1",
            "exsectionformat": "plain",
            "pageids": page_id
        }
        request = requests.get(url, params=payload)
        json = request.json()
        self.get_wiki_text(json)
        self.get_wiki_coordinates(json)
        return json

    def get_wiki_text(self, json):
        """ get the text of extracted datas """

        data = json
        pages = data['query']['pages']
        for k, v in pages.items():
            self.wiki_result = [random.choice(c.GRANDPY_KNOWS) + str(
                v['extract']) + random.choice(c.GRANDPY_END)]
        return self.wiki_result

    def get_wiki_coordinates(self, json):
        """ get the coordinates of the wikipedia page if it is a place """
        try:
            data = json
            pages = data['query']['pages']
            for k, v in pages.items():
                coordinates = (
                    v['coordinates'][0]['lat'], v['coordinates'][0]['lon'])
            self.lat = str(coordinates[0])
            self.lng = str(coordinates[1])
            return self.lat, self.lng

        except KeyError:
            pass
