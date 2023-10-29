#!/usr/bin/env python

import collections
import flask
from pill_pal.db import Database

app = flask.Flask(__name__)

def get_db() -> Database:
	if "db" not in flask.g:
		flask.g.db = Database()

	return flask.g.db

@app.route("/")
def index():
  return flask.redirect(flask.url_for("all_medication"))

@app.route("/medication")
def all_medication():
	return flask.render_template("all_medication.html")

@app.route("/medication/<medication_id>")
def single_medication(medication_id):
  return flask.render_template("single_medication.html")

@app.route("/prescription/create")
def create_prescription():
	pass

@app.route("/api/medication")
def api_all_medication():
    return flask.jsonify(
		[medication.to_dict(get_db()) for medication in get_db().medication().medication_all()]
    )

@app.route("/api/medication/<medication_id>")
def api_medication_single(medication_id: str):
    medication = get_db().medication().medication_single(medication_id)

    if medication is None:
        return flask.Response(status=404)

    return flask.jsonify(medication.to_dict(get_db()))

@app.route("/api/medication/<medication_id>/image")
def api_medication_image(medication_id: str):
    medication = get_db().medication().medication_single(medication_id)

    if medication is None:
        return flask.Response(status=404)

    return medication.image, 200, {
        "Content-Type": medication.image_mimetype
    }

@app.route("/api/medication/<medication_id>/prescriptions")
def api_medication_prescriptions(medication_id: str):
    prescriptions = get_db().prescriptions().prescriptions_for_medication(medication_id)

    if prescriptions is None:
        return flask.Response(status=404)

    return flask.jsonify([perscription.to_dict() for perscription in prescriptions])

@app.route("/api/medication/<medication_id>/quantity")
def api_medication_quantity(medication_id: str):
    db = get_db()
    inventory_list = db.inventory().inventory_for_medication(medication_id)
    if inventory_list is None:
        flask.abort(404)
    quantity = sum(item.quantity for item in inventory_list)
    return flask.jsonify(quantity)

@app.route("/api/search/<name>")
def get_medication_by_meds(name):
	name = name.lower()
	all_substances = get_db().substances().substances()
	all_medications = get_db().medication().medication_all()
	result = []

	substance_medications = collections.defaultdict(list)

	for medication in all_medications:
		substance_medications[medication.substance_id].append(medication)

	for substance in all_substances:
		if name in substance.name.lower():
			result.extend(substance_medications[substance.id])

	return flask.jsonify(result)
