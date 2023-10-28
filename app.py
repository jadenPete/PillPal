#!/usr/bin/env python

import flask

app = flask.Flask(__name__)

@app.route("/")
def index():
	return flask.render_template("index.html")


@app.route("/medication/<id>")
def item(id):
	return flask.render_template("itemviewer.html")

# @app.route("/medication/<id>/prescriptions")
# def view_med_prescriptions():
# 	return flask.render_template()

