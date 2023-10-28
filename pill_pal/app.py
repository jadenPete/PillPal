#!/usr/bin/env python

import flask
from pill_pal.db import Database

app = flask.Flask(__name__)

def get_db():
	if "db" not in flask.g:
		flask.g.db = Database()

	return flask.g.db

@app.route("/")
def index():
	get_db()

	return flask.render_template("index.html")


@app.route("/medication/<id>")
def item(id):
	return flask.render_template("itemviewer.html")

# @app.route("/medication/<id>/prescriptions")
# def view_med_prescriptions():
# 	return flask.render_template()

