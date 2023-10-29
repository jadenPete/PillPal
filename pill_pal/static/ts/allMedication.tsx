import React, { useEffect, useState } from "react"
import * as ReactDOMClient from "react-dom/client"
import { Medication } from "./common";

function App() {
	return <div className="container-fluid justify-content-center gx-5 mb-5">
		<div className="row justify-content-center">
			<div className="col-lg-6 py-3">
				<SearchBar/>
			</div>
		</div>

		<MedicationCardContainer/>
	</div>;
}

function MedicationCard(props: {
	medication: Medication
}) {
	const dosageForm = props.medication.dosageForm;

	return <a
		className="medication-card card bg-body-secondary border-0 shadow-2 text-decoration-none"
		href={`/medication/${props.medication.id}`}>
		<img className="card-img-top" src={props.medication.imageURL}/>
		<div className="card-body">
			<h5 className="card-title">
				{props.medication.substance.name}
				<div className="medication-id mt-1">{props.medication.id}</div>
			</h5>

			<div className="card-text">
				<div>
					<strong>Vendor</strong>: {props.medication.substance.vendor}
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
			</div>
		</div>
	</a>;
}

function MedicationCardContainer() {
	const [medications, setMedications] = useState<Medication[]>([]);

	useEffect(() => {
		fetch("/api/medication")
			.then(response => response.json())
			.then(medications => setMedications(medications));
	}, []);

	return <div className="d-flex flex-wrap gap-3">
		{medications.map(medication =>
			<MedicationCard key={medication.id} medication={medication}/>
		)}
	</div>;
}

function SearchBar() {
	return <div className="input-group shadow-2">
		<span id="search-icon" className="input-group-text">
			<i className="bi bi-search"/>
		</span>

		<input
			type="text"
			className="form-control bg-body-tertiary"
			placeholder="Search for a medication"
			aria-label="Search for medication"
			aria-describedby="search-icon"/>
	</div>;
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>);
