import React, { ChangeEventHandler, useEffect, useState } from "react";
import * as ReactDOMClient from "react-dom/client";
import { Medication, MedicationInformation, useSearchedMedications } from "./common";

function App() {
	const [_, medications, updateSearchQuery] = useSearchedMedications();

	return <div className="container-fluid justify-content-center gx-5 mb-5">
		<div className="row justify-content-center">
			<div className="get_medication_by_medscol-lg-6 py-3">
				<SearchBar onChange={event => updateSearchQuery(event.target.value)}/>
			</div>
		</div>

		<MedicationCardContainer medications={medications}/>
	</div>;
}

function MedicationCard(props: {
	medication: Medication
}) {
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
				<MedicationInformation medication={props.medication}/>
			</div>
		</div>
	</a>;
}

function MedicationCardContainer(props: {
	medications: Medication[]
}) {
	return <div className="d-flex flex-wrap justify-content-center gap-3">
		{props.medications.map(medication =>
			<MedicationCard key={medication.id} medication={medication}/>
		)}
	</div>;
}

function SearchBar(props: {
	onChange: ChangeEventHandler<HTMLInputElement>
}) {
	return <div className="input-group shadow-2">
		<span id="search-icon" className="input-group-text">
			<i className="bi bi-search"/>
		</span>

		<input
			type="text"
			className="form-control bg-body-tertiary"
			placeholder="Search for a medication"
			aria-label="Search for medication"
			aria-describedby="search-icon"
			onChange={props.onChange}/>
	</div>;
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>);
