""" This module will parse the user message to Grandpy """

from app.config import config as c
import re
import unicodedata


class Parser:
    """ This class is parsing the message of the user """

    def __init__(self, message=None):

        self.stopwords = c.STOP_WORDS
        self.message = message
        self.cleaned = []
        if message is not None:
            self.regex()

    def regex(self):
        """ remove punctuation of message using regex """

        first_regexed = re.sub(r'[^\w\s]', ' ', self.message)
        final_regexed = re.sub(r'\_', ' ', first_regexed)
        self.lower_letter(final_regexed)
        return final_regexed

    def lower_letter(self, regexed):
        """
            remove capital letter of the above regexed message
            (from above method regex)
        """

        message_low = regexed.lower()
        self.remove_accent(message_low)
        return message_low

    def remove_accent(self, message_low):
        """
            remove accent of the regexed lower message
            (from both above methods regex + lower_letter)
        """

        nk = unicodedata.normalize('NFKD', message_low)
        ascii = nk.encode('ASCII', 'ignore')
        strascii = ascii.decode('utf-8')  # convert byte data to string
        self.split_reworked_message(strascii)
        return strascii

    def split_reworked_message(self, strascii):
        """ split each word of the message reworked """

        list_of_words = strascii.split()
        self.check_stopwords(list_of_words)
        return list_of_words

    def check_stopwords(self, list_of_words):
        """ remove words what are in the stop_words """

        self.cleaned = []
        for word in list_of_words:
            if word not in self.stopwords:
                print(word)
                self.cleaned.append(word)
        return self.cleaned
