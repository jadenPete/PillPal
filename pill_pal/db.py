import psycopg
import psycopg.rows

class Database:
	connection: psycopg.Connection[psycopg.rows.TupleRow]
	cursor: psycopg.Cursor[psycopg.rows.TupleRow]

	def __init__(self):
		self.connection = psycopg.connect("dbname=pill_pal")
		self.connection.autocommit = True
		self.cursor = self.connection.cursor()
		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS substance(
	id UUID PRIMARY KEY,
	name TEXT NOT NULL,
	vendor TEXT,
	perscribed BOOLEAN NOT NULL
);""")

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS medication(
	id UUID PRIMARY KEY,
	substance_id UUID NOT NULL REFERENCES substance(id),
	dosage_form SMALLINT NOT NULL,
	unit_mg INTEGER NOT NULL,
	cents_per_unit INTEGER NOT NULL,
	shelf_life INTERVAL NOT NULL,
	image BYTEA NOT NULL,
	image_mimetype TEXT NOT NULL,
	UNIQUE (substance_id, dosage_form)
);""")

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS prescriptions(
	id UUID PRIMARY KEY,
	medication_id UUID NOT NULL REFERENCES medication(id),
	quantity INTEGER NOT NULL,
	doctor_name TEXT NOT NULL,
	patient_name TEXT NOT NULL,
	instructions TEXT NOT NULL
);""")

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS inventory(
	id UUID PRIMARY KEY,
	medication_id UUID NOT NULL REFERENCES medication(id),
	quantity INTEGER NOT NULL,
	timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);""")
