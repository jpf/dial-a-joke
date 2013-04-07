#!/usr/bin/env python
import os
import random
import json


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
joke = random.choice(jokes)

laughs = load_laughs()
laugh = random.choice(laughs)


def make_joke_response(joke, joke_via, laughtrack, laughtrack_via, redirect):
    rv = ('<Response>' + "\n"
          '  <Say>%s</Say>' + "\n"
          '  <!-- joke via: %s -->' + "\n"
          '  <Play>%s</Play>' + "\n"
          '  <!-- audio via: %s -->' + "\n"
          '  <Redirect method="POST">%s</Redirect>' + "\n"
          '</Response>') % (joke, joke_via,
                            laughtrack, laughtrack_via,
                            redirect)
    return rv

print make_joke_response(joke['joke'], joke['via'],
                         laugh['file'], laugh['via'],
                         'http://example.com')
