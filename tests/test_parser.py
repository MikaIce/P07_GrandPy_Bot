
"""
    this module will test all the Parser's functions with pytest. The Parser
    class contain 5 methods what are executing each after other one with the
    result of the previous one as paramater. So for each test, the next method
    in the chain will be mocked to break the chain that the test can't stay
    a unit test.
    """
from app import parser
import string


def test_unit_regex_method(monkeypatch):
    """ Will test the first method regex of the chain """

    def mock_init(self, message):
        self.message = message

    def mock_lower_letter(self, *args, **kwargs):
        pass

    monkeypatch.setattr("app.parser.Parser.__init__", mock_init)
    monkeypatch.setattr("app.parser.Parser.lower_letter", mock_lower_letter)

    test_parser1 = parser.Parser(string.punctuation)
    result1 = test_parser1.regex()
    for symbol in string.punctuation:
        assert symbol not in result1

    test_sample = {
        "Hey salut !!!": "Hey salut    ",
        "Ceci, bonhomme... est un test !": "Ceci  bonhomme    est un test  ",
        "Test_de_la tour de L'Europe?": "Test de la tour de L Europe ",
        "Hey, je compte 1,2,3,4,5 etc.": "Hey  je compte 1 2 3 4 5 etc "
    }
    for key, value in test_sample.items():
        test_parser2 = parser.Parser(key)
        result2 = test_parser2.regex()
        assert result2 == value


def test_unit_lower_letter_method(monkeypatch):
    """ Will test the second method lower_letter of the chain """

    def mock_remove_accent(self, *args, **kwargs):
        pass

    monkeypatch.setattr("app.parser.Parser.remove_accent", mock_remove_accent)

    test_parser = parser.Parser()
    result1 = test_parser.lower_letter(string.ascii_uppercase)
    for letter in string.ascii_uppercase:
        assert letter.lower() in result1
        assert letter not in result1

    test_sample = {
        "Hey salut !!!": "hey salut !!!",
        "Ceci, Bonhomme... est un TEst !": "ceci, bonhomme... est un test !",
        "Test_de_cayenne": "test_de_cayenne",
        "Hey, je compte 1,2,3,4,5 etc.": "hey, je compte 1,2,3,4,5 etc."}

    for key, value in test_sample.items():
        result2 = test_parser.lower_letter(key)
        assert result2 == value


def test_unit_remove_accent_method(monkeypatch):
    """ Will test the third method remove_accent of the chain """

    def mock_split_reworked_message(self, strascii):
        pass

    monkeypatch.setattr(
        "app.parser.Parser.split_reworked_message",
        mock_split_reworked_message)

    test_parser = parser.Parser()
    test_sample = {"ééé": "eee",
                   "Salut Pépé": "Salut Pepe",
                   "éàçûò": "eacuo"
                   }
    for key, value in test_sample.items():
        result = test_parser.remove_accent(key)
        assert result == value


def test_unit_split_reworked_message_method(monkeypatch):
    """ Will test the 4th method split_reworked_message of the chain """

    def mock_check_stopwords(self, strascii):
        pass

    monkeypatch.setattr(
        "app.parser.Parser.check_stopwords", mock_check_stopwords)

    test_parser = parser.Parser()
    test_sample = {
        "Hey salut !!!": ['Hey', 'salut', '!!!'],
        "Ceci, Bonhomme... est un TEst !":
        ['Ceci,', 'Bonhomme...', 'est', 'un', 'TEst', '!'],
        "Test_de_la tour de L'Europe?":
        ['Test_de_la', 'tour', 'de', "L'Europe?"],
        "Hey, je compte 1,2,3,4,5 etc.":
        ['Hey,', 'je', 'compte', '1,2,3,4,5', 'etc.']
    }
    for key, value in test_sample.items():
        result = test_parser.split_reworked_message(key)
        assert result == value


def test_unit_check_stopwords():
    """ Will test the last method check_stopwords of the chain """

    test_parser = parser.Parser()
    test_sample = [
        ["salut", "Michael"],
        ["je", "veux", "visiter", "Marseille"],
        ["je", "reve", "aller", "voir", "grande", "pyramide"]
    ]
    expect_results = [
        ["Michael"],
        ["Marseille"],
        ["grande", "pyramide"]
    ]
    for lists in test_sample:
        result = test_parser.check_stopwords(lists)
        assert result in expect_results
