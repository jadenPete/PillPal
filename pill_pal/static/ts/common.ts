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
