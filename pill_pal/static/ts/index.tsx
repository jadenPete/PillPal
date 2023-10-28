import React from "react"
import * as ReactDOMClient from "react-dom/client"

function App() {
	return <h1>Hello, world!</h1>
}

ReactDOMClient
	.createRoot(document.querySelector(".root"))
	.render(<App/>)
