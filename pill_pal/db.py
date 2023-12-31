import datetime
import enum
import flask
import humanize
from pill_pal.config import get_config
import psycopg
import psycopg.rows
import typing
import os

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
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	name TEXT NOT NULL,
	vendor TEXT,
	prescribed BOOLEAN NOT NULL,
	notices TEXT NOT NULL
);"""
		)

		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS medication(
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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
	notices: str

	def to_dict(self) -> dict[str, typing.Any]:
		return {
			"id": self.id,
			"name": self.name,
			"vendor": self.vendor,
			"prescribed": self.prescribed,
			"notices": self.notices
		}

class SubstanceModel(Model):
	def create_substance(self, name: str, vendor: str, prescribed: bool, notices: str )-> str:
		self.database.cursor.execute(
			"""
INSERT INTO substances (name, vendor, prescribed, notices) VALUES (%s, %s, %s, %s) RETURNING id;""",
			(name, vendor, prescribed, notices)
		)

		return self.database.cursor.fetchone()[0]

	def substance(self, substance_id: str) -> typing.Optional[Substance]:
		self.database.cursor.execute(
			"SELECT id, name, vendor, prescribed, notices FROM substances WHERE id = %s;",
			(substance_id,)
		)

		row = self.database.cursor.fetchone()

		if row is not None:
			return Substance(*row)

	def substances(self) -> list[Substance]:
		self.database.cursor.execute("SELECT id, name, vendor, prescribed, notices FROM substances;")

		return [Substance(*row) for row in self.database.cursor.fetchall()]

class DosageForm(enum.IntEnum):
	TABLET = 1
	CAPSULE = 2
	SYRUP = 3
	SUSPENSION = 4
	INJECTION = 5
	TOPICAL = 6

	@property
	def name(self) -> str:
		return {
			self.__class__.TABLET: "tablet",
			self.__class__.CAPSULE: "capsule",
			self.__class__.SYRUP: "syrup",
			self.__class__.SUSPENSION: "suspension",
			self.__class__.INJECTION: "injection",
			self.__class__.TOPICAL: "topical"
		}[self]

	@classmethod
	def from_name(cls, name: str) -> 'DosageForm':
		return {
			"tablet": cls.TABLET,
			"capsule": cls.CAPSULE,
			"syrup": cls.SYRUP,
			"suspension": cls.SUSPENSION,
			"injection": cls.INJECTION,
			"topical": cls.TOPICAL
		}[name]

class Medication(typing.NamedTuple):
	id: str
	substance_id: str
	dosage_form: DosageForm
	unit_mg: int
	cents_per_unit: int
	shelf_life: datetime.timedelta
	image: bytes
	image_mimetype: str

	def to_dict(self, database: Database) -> dict[str, typing.Any]:
		return {
			"id": self.id,
			"substance": database.substances().substance(self.substance_id).to_dict(),
			"dosageForm": self.dosage_form.name,
			"unitMg": self.unit_mg,
			"centsPerUnit": self.cents_per_unit,
			"shelfLife": humanize.naturaldelta(self.shelf_life),
			"imageURL": flask.url_for('api_medication_image', medication_id=self.id)
		}

class MedicationModel(Model):
	def read_image_file(self, filename: str) -> bytes:
		with open(os.path.join('static', 'img', filename), 'rb') as f:
			return f.read()

	def create_medication(
		self,
		substance_id: str,
		dosage_form: DosageForm,
		unit_mg: int,
		cents_per_unit: int,
		shelf_life: datetime.timedelta,
		image: str,
		image_mimetype: str,
	) -> str:
		self.database.cursor.execute(
			"""
INSERT INTO medication
	(substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES (%s, %s, %s, %s, %s, %s, %s)
	RETURNING id;""",
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

		return self.database.cursor.fetchone()[0]

	def medication_all(self) -> list[Medication]:
		self.database.cursor.execute(
			"""
SELECT id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype
	FROM medication;"""
		)

		return [
			Medication(*row[:2], DosageForm(row[2]), *row[3:])
			for row in self.database.cursor.fetchall()
		]

	def medication_single(self, medication_id: str) -> typing.Optional[Medication]:
		self.database.cursor.execute(
			"""
SELECT id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype
	FROM medication
 	WHERE id = %s;""",
	 		(medication_id,)
		)

		row = self.database.cursor.fetchone()

		if row is not None:
			return Medication(*row[:2], DosageForm(row[2]), *row[3:])

class Prescription(typing.NamedTuple):
	id: str
	medication_id: str
	quantity: int
	doctor_name: str
	patient_name: str
	instructions: str

	def to_dict(self) -> dict[str, typing.Any]:
		return {
			"id": self.id,
			"medicationID": self.medication_id,
			"quantity": self.quantity,
			"doctorName": self.doctor_name,
			"patientName": self.patient_name,
			"instructions": self.instructions
		}

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
INSERT INTO prescriptions
	(medication_id, quantity, doctor_name, patient_name, instructions)
	VALUES (%s, %s, %s, %s, %s);""",
			(medication_id, quantity, doctor_name, patient_name, instructions)
		)

	def prescriptions_for_medication(self, medication_id: str) -> list[Prescription]:
		self.database.cursor.execute(
			"""
SELECT id, medication_id, quantity, doctor_name, patient_name, instructions
	FROM prescriptions
	WHERE medication_id = %s;""",
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
			"INSERT INTO inventory (medication_id, quantity) VALUES (%s, %s);",
			(medication_id, quantity)
		)

	def inventory_for_medication(self, medication_id: str) -> list[Inventory]:
		self.database.cursor.execute(
			"SELECT id, medication_id, quantity, timestamp FROM inventory WHERE medication_id = %s;",
			(medication_id,)
		)

		return [Inventory(*row) for row in self.database.cursor.fetchall()]
