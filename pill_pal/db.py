import datetime
import enum
from pill_pal.config import get_config
import psycopg
import psycopg.rows
import typing

class Database:
	connection: psycopg.Connection[psycopg.rows.TupleRow]
	cursor: psycopg.Cursor[psycopg.rows.TupleRow]

	def __init__(self):
		self.connection = psycopg.connect(get_config()["connectionInfo"])
		self.connection.autocommit = True
		self.cursor = self.connection.cursor()
		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS substances(
	id UUID PRIMARY KEY,
	name TEXT NOT NULL,
	vendor TEXT,
	prescribed BOOLEAN NOT NULL
);"""
		)

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS medication(
	id UUID PRIMARY KEY,
	substance_id UUID NOT NULL REFERENCES substances(id),
	dosage_form SMALLINT NOT NULL,
	unit_mg INTEGER NOT NULL,
	cents_per_unit INTEGER NOT NULL,
	shelf_life INTERVAL NOT NULL,
	image BYTEA NOT NULL,
	image_mimetype TEXT NOT NULL,
	UNIQUE (substance_id, dosage_form)
);"""
		)

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS prescriptions(
	id UUID PRIMARY KEY,
	medication_id UUID NOT NULL REFERENCES medication(id),
	quantity INTEGER NOT NULL,
	doctor_name TEXT NOT NULL,
	patient_name TEXT NOT NULL,
	instructions TEXT NOT NULL
);"""
		)

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS inventory(
	id UUID PRIMARY KEY,
	medication_id UUID NOT NULL REFERENCES medication(id),
	quantity INTEGER NOT NULL,
	timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""
		)

	def substances(self) -> 'SubstanceModel':
		return SubstanceModel(self)

	def medication(self) -> 'MedicationModel':
		return MedicationModel(self)

	def prescriptions(self) -> 'PrescriptionModel':
		return PrescriptionModel(self)

	def inventory(self) -> 'InventoryModel':
		return InventoryModel(self)

class Model:
	database: Database

	def __init__(self, database: Database):
		self.database = database

class Substance(typing.NamedTuple):
	id: str
	name: str
	vendor: str
	prescribed: bool

class SubstanceModel(Model):
	def create_substance(self, name: str, vendor: str, prescribed: bool) -> None:
		self.database.cursor.execute(
			"INSERT INTO substances (name, vendor, prescribed) VALUES (?, ?, ?);",
			(name, vendor, prescribed)
		)

	def substances(self) -> list[Substance]:
		self.database.cursor.execute("SELECT id, name, vendor, prescribed FROM substances;")

		return [Substance(*row) for row in self.database.cursor.fetchall()]

class DosageForm(enum.IntEnum):
	TABLET = 1
	CAPSULE = 2
	SYRUP = 3
	SUSPENSION = 4
	INJECTION = 5
	TOPICAL = 6

class Medication(typing.NamedTuple):
	id: str
	substance_id: str
	dosage_form: DosageForm
	unit_mg: int
	cents_per_unit: int
	shelf_life: datetime.timedelta
	image: bytes
	image_mimetype: str

class MedicationModel(Model):
	def create_medication(
		self,
		substance_id: str,
		dosage_form: DosageForm,
		unit_mg: int,
		cents_per_unit: int,
		shelf_life: datetime.timedelta,
		image: bytes,
		image_mimetype: str,
	) -> None:
		self.database.cursor.execute(
			"""
INSERT INTO medication
	(substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES (?, ?, ?, ?, ?, ?, ?);""",
			(
				substance_id,
				dosage_form.value,
				unit_mg,
				cents_per_unit,
				shelf_life,
				image,
				image_mimetype
			)
		)

	def medication_all(self) -> list[Medication]:
		self.database.cursor.execute(
			"""
SELECT id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype
	FROM medication;"""
		)

		return [
			Substance(*row[:2], DosageForm(row[2]), *row[3:])
			for row in self.database.cursor.fetchall()
		]

	def medication_single(self) -> Medication:
		self.database.cursor.execute(
			"""
SELECT id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype
	FROM medication
 	WHERE id = ?;"""
		)

		return Medication(*self.database.cursor.fetchone())

class Prescription(typing.NamedTuple):
	id: str
	medication_id: str
	quantity: int
	doctor_name: str
	patient_name: str
	instructions: str

class PrescriptionModel(Model):
	def create_prescription(
		self,
		medication_id: str,
		quantity: int,
		doctor_name: str,
		patient_name: str,
		instructions: str
	) -> None:
		self.database.cursor.execute(
			"""
INSERT INTO prescription
	(medication_id, quantity, doctor_name, patient_name, instructions)
	VALUES (?, ?, ?, ?, ?);""",
			(medication_id, quantity, doctor_name, patient_name, instructions)
		)

	def prescriptions_for_medication(self, medication_id: str) -> list[Prescription]:
		self.database.cursor.execute(
			"""
SELECT (id, medication_id, quantity, doctor_name, patient_name, instructions)
	FROM prescriptions
	WHERE medication_id = ?;", (medication_id,);""",
			(medication_id,)
		)

		return [Prescription(*row) for row in self.database.cursor.fetchall()]

class Inventory(typing.NamedTuple):
	id: str
	medication_id: str
	quantity: int
	timestamp: datetime.datetime

class InventoryModel(Model):
	def add_inventory(self, medication_id: str, quantity: int) -> None:
		self.database.cursor.execute(
			"INSERT INTO inventory (medication_id, quantity) VALUES (?, ?);",
			(medication_id, quantity)
		)

	def inventory_for_medication(self, medication_id: str) -> list[Inventory]:
		self.database.cursor.execute(
			"SELECT id, medication_id, quantity, timestamp FROM inventory WHERE medication_id = ?;",
			(medication_id,)
		)

		return [Inventory(*row) for row in self.database.cursor.fetchall()]
