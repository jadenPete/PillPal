import React from "react"
import * as ReactDOMClient from "react-dom/client"

function App() {
	return <div className="container-fluid justify-content-center gx-5 mb-5">
		<div className="row justify-content-center">
			<div className="col-lg-6 py-3">
				<SearchBar/>
			</div>
		</div>

		<MedicationTiles/>
	</div>
}

function MedicationTiles() {
	return <div className="d-flex flex-wrap gap-3">
		{Array(10).fill(
			<a className="medication-card card bg-body-secondary border-0 shadow-2 text-decoration-none" href="#">
				<img
					className="card-img-top"
					src="https://leafly-cms-production.imgix.net/wp-content/uploads/2020/06/22172933/cannabis-capsule.jpg?auto=compress"/>

				<div className="card-body">
					<h5 className="card-title">Marijuana</h5>
					<p className="card-text">
						Some quick example text to build on the card title and make up the bulk of the card's content.
					</p>
				</div>
			</a>
		)}
	</div>
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
	</div>
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>)
