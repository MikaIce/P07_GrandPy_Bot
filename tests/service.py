""" This module will test the return jsonify method of the views app """

from app.parser import Parser
from app.requester import Request


def manage_send_answer(user_text):
    """
    This method  imitate the ajax route method of views.py to test the
    globality of the app
    """

    parser = app.parser.Parser(user_text)
    result = Request(parser.cleaned)
    answer = result.wiki_result
    lat = result.lat
    lng = result.lng
    json = {"answer": answer, "lat": lat, "lng": lng}
    return json
