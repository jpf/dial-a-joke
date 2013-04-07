#!/usr/bin/env python
import os
import random
import json

from flask import Flask
from flask import Response
from twilio import twiml
app = Flask(__name__)


def non_blank_lines_in(filename):
    """
    Given a filename, returns all non-blank lines.
    """
    lines = open(filename).readlines()
    lines = map(lambda x: x.rstrip(), lines)
    lines = filter(lambda x: x is not '', lines)
    return lines


def load_jokes():
    jokes = []
    joke_path = 'jokes/'
    for dirpath, dirnames, filenames in os.walk(joke_path):
        if len(filenames) is 0:
            continue
        for name in filenames:
            filename = os.path.join(dirpath, name)
            via = filename.replace(joke_path, 'http://')
            for joke in non_blank_lines_in(filename):
                entry = {'joke': joke, 'via': via}
                jokes.append(entry)
    return jokes


def load_laughs():
    index_path = 'static/laughs/'
    index_file = 'index.json'
    filename = os.path.join(index_path, index_file)
    index_data = open(filename)
    rv = json.load(index_data)
    for obj in rv:
        obj['file'] = os.path.join(index_path, obj['file'])
    return rv

jokes = load_jokes()

laughs = load_laughs()


def make_joke_response(joke, joke_via,
                       laughtrack, laughtrack_via,
                       redirect="/"):
    r = twiml.Response()
    r.say(joke)
    with r.gather(timeout=60, numDigits=1) as g:
        g.play(laughtrack)
    r.redirect(redirect)
    via = "<!-- joke via: %s laughtrack via: %s -->" % (
        joke_via, laughtrack_via)
    return str(r) + via


@app.route("/")
def index():
    return "hi."


@app.route("/joke", methods=['GET', 'POST'])
def tell_joke():
    joke = random.choice(jokes)
    laugh = random.choice(laughs)

    rv = make_joke_response(joke['joke'], joke['via'],
                            laugh['file'], laugh['via'])
    return Response(rv, mimetype='text/xml')

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
