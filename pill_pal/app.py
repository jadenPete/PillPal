#!/usr/bin/env python

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

@app.route("/medication/<id>")
def single_medication(medication_id):
	pass

@app.route("/prescription/create")
def create_prescription():
	pass


@app.route("/api/medication/<id>")
def item(id):
    db = get_db()
    medication = db.medication().medication_single(id)
    if medication is None:
        flask.abort(404)
    return flask.jsonify({
        "id": medication.id,
		"substance_id": medication.substance_id,
		"dosage_form": medication.dosage_form,
		"unit_mg": medication.unit_mg,
		"cents_per_unit": medication.cents_per_unit,
		"shelf_life": medication.shelf_life.days,
		"image": medication.image.hex(),
		"image_mimetype": medication.image_mimetype,
	})

@app.route("/api/medication/<id>/prescriptions")
def view_med_prescriptions(id):
    db = get_db()
    prescriptions = db.prescriptions().prescriptions_for_medication(id)
    if prescriptions is None:
        flask.abort(404)
    return flask.jsonify(prescriptions)

@app.route("/api/medication/<id>/quantity")
def get_med_quantity(id):
    db = get_db()
    inventory_list = db.inventory().inventory_for_medication(id)
    if inventory_list is None:
        flask.abort(404)
    quantity = sum(item.quantity for item in inventory_list)
    return flask.jsonify(quantity)
