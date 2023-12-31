import React, { useEffect, useState } from "react";
import * as ReactDOMClient from "react-dom/client";
import { Medication, MedicationInformation, Prescription } from "./common";

function App() {
	const medicationID = window.location.pathname.split("/")[2];

	return (
		<div className="row" id="shift">
			<div className="col-4">
				<MedicationPanel medicationID={medicationID}/>
			</div>
			<div className="col-8">
				<PrescriptionList medicationID={medicationID}/>
			</div>
		</div>
	);
}

function MedicationPanel(props: {
	medicationID: string
}) {
	const [medication, setMedication] = useState<Medication | undefined>(undefined);
	const [medicationQuantity, setMedicationQuantity] = useState<number | undefined>(undefined);

	useEffect(() => {
		fetch(`/api/medication/${props.medicationID}`)
			.then(response => response.json())
			.then(medication => setMedication(medication));

		fetch(`/api/medication/${props.medicationID}/quantity`)
			.then(response => response.json())
			.then(quantity => setMedicationQuantity(quantity));
	}, []);

	if (medication == undefined) {
		return <></>;
	}

	return <div>
		<h2 className="sub-header">{medication.substance.name}</h2>
		<div className="fs-5">
			<img id="pic" className="mb-3" src={medication.imageURL}/>
			<MedicationInformation medication={medication}/>
		</div>
	</div>;
}

function PrescriptionList(props: {
	medicationID: string
}) {
	const [prescriptions, setPrescriptions] = useState<Prescription[]>([]);

	useEffect(() => {
		fetch(`/api/medication/${props.medicationID}/prescriptions`)
			.then(response => response.json())
			.then(prescriptions => setPrescriptions(prescriptions));
	}, []);

	return <div>
		<h2 className="sub-header">Prescriptions</h2>
		<div id="scroller" className="table-responsive">
			<table className="table table-striped">
				<thead>
					<tr>
						<th className="col-md-1">ID</th>
						<th className="col-md-2">Doctor name</th>
						<th className="col-md-2">Patient name</th>
						<th className="col-md-3">Quantity</th>
						<th className="col-md-6">Instructions</th>
					</tr>
				</thead>

				<tbody>
					{prescriptions.map(prescription =>
						<tr key={prescription.id}>
							<td>{prescription.id}</td>
							<td>{prescription.doctorName}</td>
							<td>{prescription.patientName}</td>
							<td>{prescription.quantity}</td>
							<td>{prescription.instructions}</td>
						</tr>
					)}
				</tbody>
			</table>
		</div>
	</div>;
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>);
