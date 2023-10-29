#!/usr/bin/env python

import os
import pill_pal.config
import psycopg

connection = psycopg.connect(pill_pal.config.get_config()["connectionInfo"])
connection.autocommit = True
cursor = connection.cursor()

def execute_with_filenames(query: str, filenames: tuple[str, ...] = ()) -> None:
	arguments = []

	for filename in filenames:
		with open(
			os.path.join(os.path.dirname(__file__), "pill_pal", "static", "img", filename),
			"rb"
		) as file:
			arguments.append(file.read())

	cursor.execute(query, tuple(arguments))

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('123e4567-e89b-12d3-a456-426614174000', 'Sildenafil', 'Viagra', FALSE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('b9dd4c4e-a1ce-400c-92cf-8cf1f28dc978', '123e4567-e89b-12d3-a456-426614174000', 1, 50, 8800, '2 years', %s, 'image/jpeg');""",
	("sildenafil-tablet.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO inventory
	(medication_id, quantity)
	VALUES ('b9dd4c4e-a1ce-400c-92cf-8cf1f28dc978', 900);"""
)

execute_with_filenames(
	"""
INSERT INTO prescriptions
	(medication_id, quantity, doctor_name, patient_name, instructions)
	VALUES ('b9dd4c4e-a1ce-400c-92cf-8cf1f28dc978', 30, 'Javier A. Weisson', 'Jaden Peterson', 'Take 1 tablet, as needed, 30 min to 4 hours before sexual activity');"""
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('c542c666-7628-11ee-b962-0242ac120002', 'Atorvastatin', 'Lipitor', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('ab2c6aba-2141-4f85-8bdd-f9b6f9bfc9f0','c542c666-7628-11ee-b962-0242ac120002', 1, 40, 1800, '5 years', %s, 'image/jpeg');""",
	("atorvastatin-tablet.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('544385d1-2d18-478f-a3eb-9c9c243663f7', 'Amoxicillin', 'Amoxil', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('8c3fcc50-ef81-4cb2-827c-b0bd27df7ccb','544385d1-2d18-478f-a3eb-9c9c243663f7', 2, 500, 3100, '3 years', %s, 'image/jpeg');""",
	("amoxicillin-capsule.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('eb17c62c-6220-4da6-ba11-334ce5d98781', 'Lisinopril', 'Prinivil, Zestril', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('20490fad-2f79-4db9-a181-aa143b625ff3','eb17c62c-6220-4da6-ba11-334ce5d98781', 1, 20, 1100, '1 year', %s, 'image/jpeg');""",
	("lisinopril-tablet.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('429d597c-9658-47df-b108-f7cd72ea254f', 'Ibuprofen', 'Advil', FALSE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('6f08d576-7bea-4576-bcf3-467fa7d39c63','429d597c-9658-47df-b108-f7cd72ea254f', 1, 200, 1339, '3 years', %s, 'image/jpeg');""",
	("ibuprofen-tablet.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('076978fe-773a-465d-86a6-b0ea45668e2b', 'Insulin', 'Lantus', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('fdc10f02-bf98-43e5-898e-5b455c625c6d','076978fe-773a-465d-86a6-b0ea45668e2b', 5, 100, 30800, '28 days', %s, 'image/jpeg');""",
	("lantus-injection.jpeg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('e77672c3-457b-413b-bef0-030663da7638', 'Omeprazole', 'Prilosec, Losec', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('9ead9d45-1fdb-46f4-925f-16b3441b1a1e','e77672c3-457b-413b-bef0-030663da7638', 2, 20, 280, '4 years', %s, 'image/jpeg');""",
	("omeprazole-capsule.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('15f1459a-e3ad-4a48-9ac3-4afd5880aa7c', 'Alprazolam', 'Xanax', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('db9684f1-103e-4a93-8765-9dc2208d7c01','15f1459a-e3ad-4a48-9ac3-4afd5880aa7c', 1, 1, 183, '2 years', %s, 'image/jpeg');""",
	("alprazolam-tablet.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('3a27037b-82e2-49f5-bf51-1add43ec0966', 'Lidocaine', 'Lidamantle, Xylocaine, Topicaine', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('65d80c6a-1d35-476c-96a0-5853f9a4f493','3a27037b-82e2-49f5-bf51-1add43ec0966', 6, 20, 97, '45 days', %s, 'image/jpeg');""",
	("lidocaine-topical.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('7b9227cf-d290-42b3-aa07-7635a3a784be', 'Carbamazepine', 'Tegretol', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('77f96c3c-3bca-4e7e-9028-e859148ee718','7b9227cf-d290-42b3-aa07-7635a3a784be', 4, 500, 57, '2 years', %s, 'image/jpeg');""",
	("carbamazepine-suspension.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('9fac1da4-b30d-4872-9939-02e759ca6319', 'Metformin', 'Glucophage', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('ccc2e64f-2fd5-45e4-8849-2a7903643e2a','9fac1da4-b30d-4872-9939-02e759ca6319', 1, 500, 75, '2 years', %s, 'image/jpeg');""",
	("metformin-tablet.jpg",)
)

execute_with_filenames(
	"""
INSERT INTO substances
	(id, name, vendor, prescribed, notices)
	VALUES('c7a783ab-4825-4e7a-8705-a4563b634b97', 'Oxycontin', 'Oxycodone', TRUE, 'Please be careful!');"""
)

execute_with_filenames(
	"""
INSERT INTO medication
	(id, substance_id, dosage_form, unit_mg, cents_per_unit, shelf_life, image, image_mimetype)
	VALUES ('e2d35b7c-0eb9-4a5a-8ee2-2c6f4db2c362','c7a783ab-4825-4e7a-8705-a4563b634b97', 1, 10, 43, '3 years', %s, 'image/jpeg');""",
	("oxycontin-tablet.jpg",)
)
