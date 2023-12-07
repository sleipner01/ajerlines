const baseURL = "http://127.0.0.1:6969";

export const GET_DATE = () =>
	fetch(baseURL + "/getTodaysDate").then((res) => res.json());

export const GET_FLIGHTPLAN = () =>
	fetch(baseURL + "/getTodaysFlightplan").then((res) => res.json());
