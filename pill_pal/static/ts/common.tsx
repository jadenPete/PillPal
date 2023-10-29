import React, { useEffect, useState } from "react";

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

export function capitalizeDosageForm(dosageForm: DosageForm) {
	return `${dosageForm.charAt(0).toUpperCase()}${dosageForm.slice(1)}`;
}

export function MedicationInformation(props: {
	medication: Medication
}) {
	return <div>
		<div>
			<strong>Brand name(s)</strong>: {props.medication.substance.vendor}
		</div>

		<div>
			<strong>Dosage form</strong>: {`${capitalizeDosageForm(props.medication.dosageForm)}`}
		</div>

		<div>
			<strong>Unit mass</strong>: {props.medication.unitMg} mg
		</div>

		<div>
			<strong>Price/unit</strong>: {props.medication.centsPerUnit}¢
		</div>
	</div>;
}

export function useSearchedMedications(): [
	Medication[],
	Medication[],
	(searchQuery: string) => void
] {
	const [allMedications, setAllMedications] = useState<Medication[]>([]);
	const [currentMedications, setCurrentMedications] = useState<Medication[]>([]);

	function updateSearchQuery(query: string) {
		if (query == "") {
			setCurrentMedications(allMedications);
		} else {
			fetch(`/api/medication/search?query=${query}`)
				.then(response => response.json())
				.then(medications => {
					setCurrentMedications(medications)
				});
		}
	}

	useEffect(() => {
		fetch("/api/medication")
			.then(response => response.json())
			.then(medications => {
				setAllMedications(medications);
				setCurrentMedications(medications);
			});
	}, []);

	return [allMedications, currentMedications, updateSearchQuery];
}
