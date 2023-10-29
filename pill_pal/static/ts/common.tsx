import React from "react";

export enum DosageForm {
	Tablet = "tablet",
	Capsule = "capsule",
	Syrup = "syrup",
	Suspension = "suspension",
	Injection = "injection",
	Topical = "topical"
}

export interface Medication {
	id: string
	substance: Substance
	dosageForm: DosageForm
	unitMg: number
	centsPerUnit: number
	shelfLife: string
	imageURL: string
}

export interface Prescription {
	id: string
	medicationID: string
	quantity: number
	doctorName: string
	patientName: string
	instructions: string
}

export interface Substance {
	id: string
	name: string
	vendor: string
	prescribed: boolean
}

export function MedicationInformation(props: {
	medication: Medication
}) {
	const dosageForm = props.medication.dosageForm;

	return <div>
		<div>
			<strong>Brand name(s)</strong>: {props.medication.substance.vendor}
		</div>

		<div>
			<strong>Dosage form</strong>: {`${dosageForm.charAt(0).toUpperCase()}${dosageForm.slice(1)}`}
		</div>

		<div>
			<strong>Unit mass</strong>: {props.medication.unitMg} mg
		</div>

		<div>
			<strong>Price/unit</strong>: {props.medication.centsPerUnit}¢
		</div>
	</div>;
}
