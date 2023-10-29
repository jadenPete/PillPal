import * as bootstrap from "bootstrap";
import React, { ChangeEvent, FormEvent, forwardRef, useRef, useState } from "react";
import * as ReactDOMClient from "react-dom/client";
import { capitalizeDosageForm, DosageForm, Medication, useSearchedMedications } from "./common";

enum Page {
	CreateMedication,
	CreatePrescription
}

enum FulfillmentMode {
	AddInventory,
	AddMedication,
	AddSubstance
}

const page = window.location.pathname == "/prescription/create" ?
	Page.CreatePrescription :
	Page.CreateMedication;

const NoticeModal = forwardRef<HTMLDivElement, {notices: string}>((props, ref) => {
	return <div className="modal" tabIndex={-1} ref={ref}>
		<div className="modal-dialog">
			<div className="modal-content">
				<div className="modal-header">
					<h5 className="modal-title">Fulfillment Notice Acknowledgement Required</h5>
				</div>

				<div className="modal-body">
					{props.notices}
				</div>

				<div className="modal-footer">
					<button type="button" className="btn btn-primary" data-bs-dismiss="modal">
						Ok
					</button>
				</div>
			</div>
		</div>
	</div>
});

function App() {
	const [name, setName] = useState("");
	const [dosageForm, setDosageForm] = useState("");
	const [allMedications, currentMedications, updateSearchQuery] = useSearchedMedications();
	const [matchingName, setMatchingName] = useState<Medication | undefined>(undefined);
	const [matchingNameAndForm, setMatchingNameAndForm] =
		useState<Medication | undefined>(undefined);

	const noticeModalRef = useRef<HTMLDivElement>();

	let mode: FulfillmentMode

	if (name == "" || dosageForm == "" || matchingNameAndForm != undefined) {
		mode = FulfillmentMode.AddInventory
	} else if (matchingName != undefined) {
		mode = FulfillmentMode.AddMedication
	} else {
		mode = FulfillmentMode.AddSubstance
	}

	function handleNameChange(event: ChangeEvent<HTMLInputElement>) {
		const name = event.currentTarget.value;

		setName(name);
		updateSearchQuery(name);

		const nowMatchingName =
			allMedications.find(medication => medication.substance.name == name);

		setMatchingName(nowMatchingName);
		setMatchingNameAndForm(
			nowMatchingName != undefined &&
				nowMatchingName.dosageForm == dosageForm ?
				nowMatchingName :
				undefined
		);
	}

	function handleDosageFormChange(event: ChangeEvent<HTMLSelectElement>) {
		setDosageForm(event.currentTarget.value);
		setMatchingNameAndForm(
			matchingName != undefined &&
				matchingName.dosageForm == event.currentTarget.value ?
				matchingName :
				undefined
		);
	}

	async function handleFormSubmit(event: FormEvent<HTMLFormElement>) {
		event.preventDefault();

		const formData = new FormData(event.currentTarget);

		if (!await possibleInterruptSubmission()) {
			return;
		}

		let substanceID: string;
		let medicationID: string;

		if (mode == FulfillmentMode.AddSubstance) {
			substanceID = await (
				await fetch("/api/substance", {
					method: "POST",
					body: formData
				})
			).json();
		} else {
			substanceID = matchingName.substance.id;
		}

		formData.set("substanceID", substanceID);

		if (mode == FulfillmentMode.AddInventory) {
			medicationID = matchingNameAndForm.id;
		} else {
			medicationID = await (
				await fetch("/api/medication", {
					method: "POST",
					body: formData
				})
			).json();
		}

		formData.set("medicationID", medicationID);

		await fetch("/api/prescription", {
			method: "POST",
			body: formData
		});

		window.location.href = "/";
	}

	async function possibleInterruptSubmission(): Promise<boolean> {
		if (page == Page.CreatePrescription) {
			if (mode != FulfillmentMode.AddInventory) {
				alert(
					"Unfortunately, you're unable to register new substances or medications. Please ask a pharmacist to, or fulfill an existing substance or medication."
				);

				return false;
			}

			let closeModal: () => void;

			const modalClosed = new Promise(resolve => {
				closeModal = () => resolve(undefined);
			})

			noticeModalRef.current.addEventListener("hide.bs.modal", () => {
				closeModal();
			});

			new bootstrap.Modal(noticeModalRef.current).show();

			await modalClosed;
		}

		return true;
	}

	return <div className="container">
		<form encType="multipart/form-data" onSubmit={handleFormSubmit}>
			<NoticeModal notices={matchingName?.substance?.notices ?? ""} ref={noticeModalRef}/>

			<div className="form-floating">
				<input
					type="text"
					id="substance-name-input"
					className="form-control mb-2"
					autoComplete="off"
					list="substance-name-datalist"
					name="name"
					placeholder="Substance name"
					required
					onChange={handleNameChange}/>

				<label htmlFor="substance-name-input">Substance name</label>
			</div>

			<datalist id="substance-name-datalist">
				{currentMedications.map(medication =>
					<option
						key={medication.id}
						value={medication.substance.name}>{medication.substance.name}</option>
				)}
			</datalist>

			<div className="form-floating">
				<select
					id="dosage-form"
					className="form-select mb-2"
					defaultValue=""
					disabled={name == ""}
					name="dosageForm"
					onChange={handleDosageFormChange}>
					<option value="" disabled>Choose a dosage form</option>

					{[
						DosageForm.Capsule,
						DosageForm.Injection,
						DosageForm.Suspension,
						DosageForm.Syrup,
						DosageForm.Tablet,
						DosageForm.Topical
					].map(dosageForm =>
						<option value={dosageForm}>{capitalizeDosageForm(dosageForm)}</option>
					)}
				</select>

				<label htmlFor="dosage-form">Dosage form</label>
			</div>

			<div className="form-floating">
				<input
					type="text"
					id="substance-vendor-input"
					className="form-control mb-2"
					autoComplete="off"
					disabled={mode != FulfillmentMode.AddSubstance}
					name="vendor"
					placeholder="Brand name(s)"
					required
					{...matchingName == undefined ? {} : {
						value: matchingName.substance.vendor
					}}/>

				<label htmlFor="substance-vendor-input">Brand name(s)</label>
			</div>

			<div className="form-check my-3">
				<input
					type="checkbox"
					id="substance-prescribed-input"
					className="form-check-input"
					autoComplete="off"
					disabled={mode != FulfillmentMode.AddSubstance}
					name="prescribed"
					{...matchingName == undefined ? {} : {
						checked: matchingName.substance.prescribed
					}}/>

				<label className="form-check-label" htmlFor="substance-prescribed-input">
					Must be prescribed
				</label>
			</div>

			<div className="form-floating">
				<textarea
					id="substance-notices-textarea"
					className="form-control mb-2"
					autoComplete="off"
					disabled={mode != FulfillmentMode.AddSubstance}
					name="notices"
					required
					{...matchingName == undefined ? {} : {
						value: matchingName.substance.notices
					}}>
				</textarea>

				<label htmlFor="substance-notices-textarea">
					Fulfillment notices (separate each notice with a newline)
				</label>
			</div>

			<div className="form-floating">
				<input
					type="number"
					id="medication-unit-mg-input"
					className="form-control mb-2"
					autoComplete="off"
					disabled={mode == FulfillmentMode.AddInventory}
					name="unitMg"
					required
					{...matchingNameAndForm == undefined ? {} : {
						value: matchingNameAndForm.unitMg
					}}/>

				<label htmlFor="medication-unit-mg-input">mg/unit</label>
			</div>

			<div className="form-floating">
				<input
					type="number"
					id="medication-cents-per-unit-input"
					className="form-control mb-2"
					autoComplete="off"
					disabled={mode == FulfillmentMode.AddInventory}
					name="centsPerUnit"
					required
					{...matchingNameAndForm == undefined ? {} : {
						value: matchingNameAndForm.centsPerUnit
					}}/>

				<label htmlFor="medication-cents-per-unit-input">¢/unit</label>
			</div>

			<div className="form-floating">
				<input
					type="datetime-local"
					id="medication-expiration-input"
					className="form-control mb-2"
					autoComplete="off"
					disabled={mode == FulfillmentMode.AddInventory}
					name="expiration"
					required/>

				<label htmlFor="medication-expiration-input">Expiration</label>
			</div>

			<div className="form-floating">
				<input
					type="number"
					id="prescription-quantity-input"
					className="form-control mb-2"
					autoComplete="off"
					name="quantity"
					required/>

				<label htmlFor="prescription-quantity-input">Prescription quantity</label>
			</div>

			<div className="form-floating">
				<input
					type="text"
					id="prescription-doctor-name"
					className="form-control mb-2"
					autoComplete="off"
					name="doctorName"
					required/>

				<label htmlFor="prescription-doctor-name">Prescription doctor name</label>
			</div>

			<div className="form-floating">
				<input
					type="text"
					id="prescription-patient-name"
					className="form-control mb-2"
					autoComplete="off"
					name="patientName"
					required/>

				<label htmlFor="prescription-patient-name">Prescription patient name</label>
			</div>

			<div className="form-floating">
				<textarea
					id="prescription-instructions-textarea"
					className="form-control mb-2"
					autoComplete="off"
					name="instructions"
					required/>

				<label htmlFor="prescription-instructions-textarea">Prescription instructions</label>
			</div>

			<div className="mb-3">
				<label htmlFor="medication-image-input" className="form-label">
					Medication image
				</label>

				<input
					type="file"
					id="edication-image-input"
					className="form-control"
					name="image"
					required/>
			</div>

			<button type="submit" className="btn btn-primary">Submit</button>
		</form>
	</div>;
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>);
