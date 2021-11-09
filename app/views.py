""" This module will manages the app interface """

from flask import render_template, jsonify, request
from . import app
from app.parser import Parser
from app.requester import Request
from app.config import config as c

api_key = c.API_KEY


@app.route("/")
def home():
    """ This method will diplau the app main interface """

    return render_template("index.html", key=api_key)


@app.route("/ajax", methods=["POST"])
def send_answer():
    """
    This method will catch the message of the user and send it to the
    python Parser class to clean the message and will send the result to the
    wikipedia API using the Request class. Finally, the result will be send
    on the front end.
    """

    user_text = request.form["userText"]
    parser = Parser(user_text)
    result = Request(parser.cleaned)
    answer = result.wiki_result
    lat = result.lat
    lng = result.lng
    return jsonify({"answer": answer, "lat": lat, "lng": lng})
