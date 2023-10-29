import React from "react"
import * as ReactDOMClient from "react-dom/client"

function App() {

  // Variable of the ID from the url 
  const MEDICATION_ID = window.location.pathname.split("/")[2];

  // Drug name var, get from fetch
  const DRUG_NAME =`Drug Name (current id: ${MEDICATION_ID})`;
  // Drug desc var, get from fetch
  const DRUG_DESC = "Drug Description.....";
  // Drug stock var, get from fetch
  const DRUG_STOCK = "Drug Stock";
  // Drug pic var, get from fetch
  const DRUG_PIC = "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iarrvNQy.B8w/v1/-1x-1.jpg";
  
  return (
    <div className="row" id="shift">
      <div className="col-8">
        <h2 className="sub-header">Prescriptions</h2>
        <div className="table-responsive" id="scroller">
          <table className="table table-striped">
            <thead>
              <tr>
                <th className="col-md-1">ID</th>
                <th className="col-md-2">Name</th>
                <th className="col-md-3">Quantity</th>
                <th className="col-md-4">Prescriber</th>
                <th className="col-md-5">Date</th>
                <th className="col-md-6">Filled</th>
              </tr>
            </thead>
            <tbody>
              {/** map each part of json to tr
               * 
               * FORMAT:
               * 
               * for each prescription:
               * <tr>
               *    <td className="col-md-1">*data*</td>
               *    <td className="col-md-2">*data2*</td>
               *    <td className="col-md-3">*data3*</td>
               *    etc
               * </tr>
               * 
              */}

            </tbody>
          </table>
        </div>
      </div>
      <div className="col-4">
        <h2 className="sub-header">{DRUG_NAME}</h2>
        <div className="table-responsive">
          <table className="table table-borderless">
            <tbody>
              <tr>
                <td className="col-lg-4"><img id="pic" src={DRUG_PIC}></img></td>
              </tr>
              <tr>
                <td className="col-md-1">{DRUG_DESC}</td>
              </tr>
              <tr>
                <td className="col-md-1">{DRUG_STOCK}</td>
              </tr>
              {/**
               * TO ADD MORE GENERAL DRUG DATA:
               * 
               * <tr>
               *  <td className="col-md-1">data</td>
               * </tr>
               * for each new paragraph
               */}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>)