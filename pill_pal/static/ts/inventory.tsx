import React, { ChangeEvent, useState } from "react"
import * as ReactDOMClient from "react-dom/client"
import { Medication, Substance } from "./common"

function App() {
    const [medications, setMedications] = useState<Medication[]>([]);
    const [substances, setSubstances] = useState<Substance[]>([]);

    const fetchData = async (event: ChangeEvent<HTMLInputElement>) => {
        const name = event.target.value;
        const response = await fetch(`/api/medication/search`);
        const newMedications = await response.json();
        const newSubstances = newMedications.map((medication: Medication) => medication.substance)
       
        setMedications(newMedications);
        setSubstances(newSubstances);
    };

    return (
        <form method="POST" action="/temporary_placeholder">
            <label htmlFor="substance" className="form-label">Select Substance</label>
            <input className="form-control" list="substance" id="substance" 
            placeholder="Substance name" onChange={fetchData}/>
            <datalist id="substance">
                {substances.map(substance => (
                    <option value={substance.name} />
                ))}
            </datalist>
                
            <label htmlFor="id">ID</label>
            <input id="id" type="number" className="form-control"
            //value={medication_data[0].id || ''}
            // readOnly={medication_data[0].id}
            />
            <button type="submit">Submit</button>

            {/* substance_id, dosage_form.value, unit_mg, cents_per_unit, shelf_life, image, image_mimetype */}
        </form>
    );
}

ReactDOMClient
.createRoot(document.querySelector(".root"))
.render(<App/>)