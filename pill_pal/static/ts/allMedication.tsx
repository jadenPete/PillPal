import React, { useEffect, useState } from "react"
import * as ReactDOMClient from "react-dom/client"

enum DosageForm {
	Tablet = "tablet",
	Capsule = "capsule",
	Syrup = "syrup",
	Suspension = "suspension",
	Injection = "injection",
	Topical = "topical"
}

type Medication = {
	id: string
	substance: Substance
	dosageForm: DosageForm
	unitMg: number
	centsPerUnit: number
	shelfLife: string
	imageURL: string
};

type Substance = {
	id: string
	name: string
	vendor: string
	prescribed: boolean
};

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

	return <a className="medication-card card bg-body-secondary border-0 shadow-2 text-decoration-none" href="#">
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

	// const medications = Array<Medication>(10).fill({
	// 	id: "7de68f37-4103-486b-baa8-cbd802634771",
	// 	substance: {
	// 		id: "id",
	// 		name: "Marijuana",
	// 		vendor: "Raven's dealer",
	// 		prescribed: true
	// 	},

	// 	dosageForm: DosageForm.Capsule,
	// 	unitMg: 1,
	// 	centsPerUnit: 1,
	// 	shelfLife: "1 month",
	// 	imageURL: "https://leafly-cms-production.imgix.net/wp-content/uploads/2020/06/22172933/cannabis-capsule.jpg?auto=compress"
	// });

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
