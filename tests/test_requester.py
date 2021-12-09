""" this module will test the requester.py module using pytest """

from app import requester
from app.config import config as c


class MockResponse:
    """
        this class will create a fake json for mocking the requests.get
        method
        """

    def __init__(self, json=None):

        if json is None:
            raise ValueError

        else:
            self.fake_json = {
                "batchcomplete": "",
                "query": {
                    "searchinfo": {
                        "totalhits": 1,
                        "suggestion": "face 200 valid queen",
                    },
                    "search": [
                        {
                            "ns": 0,
                            "title": "La La Land (film)",
                            "pageid": 10052634,
                            "size": 145412,
                            "wordcount": 16382,
                        }
                    ],
                    "pages": {
                        "10052634": {
                            "extract": "a nice short fake text for testing",
                            "coordinates": [{'lat': 4.93461, 'lon': -52.33033}]}
                    },
                },
            }

    def json(self):
        return self.fake_json


def test_unit_first_request_wiki_method_if_there_is_a_query(monkeypatch):
    """
       this method will test the first method of the chain with mocking the
       __init__ of the class, the requests.get and the next method considering
       a valid query
       """

    test = requester.Request("fake 200 valid query")

    def mock_init(self, query):
        self.query = query

    def mock_get(*args, **kwargs):
        return MockResponse("fake response")

    def mock_get_wiki_page_id(self, *args, **kwargs):
        pass

    monkeypatch.setattr("app.requester.Request.__init__", mock_init)
    monkeypatch.setattr("app.requester.requests.get", mock_get)
    monkeypatch.setattr(
        "app.requester.Request.get_wiki_page_id", mock_get_wiki_page_id)

    result = test.first_request_wiki()
    assert result['query']['search'][0]['title'] == "La La Land (film)"


def test_unit_first_request_wiki_method_if_there_is_no_query(monkeypatch):
    """
       this method will test the first method of the chain with mocking the
       __init__ of the class considering a empty query
       """

    test = requester.Request([])

    def mock_init(self, query):
        self.query = query

    monkeypatch.setattr("app.requester.Request.__init__", mock_init)

    result = test.first_request_wiki()
    assert result in c.GRANDPY_EMPTY


def test_unit_first_request_wiki_method_if_there_is_value_error(monkeypatch):
    """
        this method will test the first method of the chain with mocking the
        __init__ of the class,the requests.get and the next method considering
        a unvalid query
        """

    test = requester.Request("fake 404 failed query")

    def mock_init(self, query):
        self.query = query

    def mock_get(*args, **kwargs):
        return MockResponse()

    def mock_get_wiki_page_id(self, *args, **kwargs):
        pass

    monkeypatch.setattr("app.requester.Request.__init__", mock_init)
    monkeypatch.setattr("app.requester.requests.get", mock_get)
    monkeypatch.setattr(
        "app.requester.Request.get_wiki_page_id", mock_get_wiki_page_id)

    result = test.first_request_wiki()
    assert result in c.GRANDPY_DONT_UNDERSTAND


def test_unit_get_wiki_page_id_if_valid_json(monkeypatch):
    """
       this method will test the second method of the chain with mocking the
       requests.get and the next method considering a valid query
       """

    test = requester.Request("fake 200 valid query")

    def mock_get(*args, **kwargs):
        return MockResponse("fake response")

    def mock_second_request_wiki(self, *args, **kwargs):
        pass

    monkeypatch.setattr(
        "app.requester.Request.second_request_wiki", mock_second_request_wiki)
    monkeypatch.setattr("app.requester.requests.get", mock_get)

    mock_json = MockResponse("fake valid response").json()
    result = test.get_wiki_page_id(mock_json)
    assert result == "10052634"


def test_unit_second_request_wiki_method(monkeypatch):
    """
     this method will test the third method of the chain with mocking the
     requests.get and the two next method considering a valid query
     """
    test = requester.Request("fake 200 valid query")

    def mock_get(*args, **kwargs):
        return MockResponse("fake response")

    def mock_get_wiki_text(self, *args, **kwargs):
        pass

    def mock_get_wiki_coordinates(self, *args, **kwargs):
        pass

    monkeypatch.setattr(
        "app.requester.Request.get_wiki_coordinates",
        mock_get_wiki_coordinates)
    monkeypatch.setattr(
        "app.requester.Request.get_wiki_text", mock_get_wiki_text)
    monkeypatch.setattr("app.requester.requests.get", mock_get)

    result = test.second_request_wiki("10052634")
    assert result['query']['search'][0]['title'] == "La La Land (film)"


def test_unit_get_wiki_text(monkeypatch):
    """
    this method will test the fourth method of the chain with mocking the
    requests.get and the random.choice to provide a stable answer.
    """

    test = requester.Request("fake 200 valid query")

    def mock_get(*args, **kwargs):
        return MockResponse("fake response")

    def mock_random_choice(*args, **kwargs):
        return " fake random "

    monkeypatch.setattr("app.requester.random.choice", mock_random_choice)
    monkeypatch.setattr("app.requester.requests.get", mock_get)

    mock_json = MockResponse("fake valid response").json()
    result = test.get_wiki_text(mock_json)
    assert result == [
        ' fake random a nice short fake text for testing fake random ']


def test_unit_get_wiki_coordinates(monkeypatch):
    """
    this method will test the fifth method of the chain with mocking the
    requests.get to get the latitude and longitude
    """
    test = requester.Request("fake 200 valid query")

    def mock_get(*args, **kwargs):
        return MockResponse("fake response")

    monkeypatch.setattr("app.requester.requests.get", mock_get)

    mock_json = MockResponse("fake valid response").json()
    result = test.get_wiki_coordinates(mock_json)
    assert result == ('4.93461', '-52.33033')
