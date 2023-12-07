import "./FlightPlan.css";
import { GET_FLIGHTPLAN } from "../queries/queries";
import { useQuery } from "@tanstack/react-query";

type FlightDetails = {
	Activity: string;
	STD: string;
	STA: string;
	From: string;
	To: string;
};

const FlightPlan = () => {
	const { isPending, error, data } = useQuery({
		queryKey: ["flightplan"],
		queryFn: GET_FLIGHTPLAN,
	});

	if (isPending) return "Loading...";

	if (error) return "An error has occurred: " + error.message;

	if (!data) return "Captain Olsen is not flying today...";

	return (
		<div className="schedule-container">
			{
				<div className="schedule">
					{data.map((flight: FlightDetails) => (
						<div className="flight" key={flight.Activity}>
							<div className="flight__activity">{flight.Activity}</div>
							<div className="flight__time">
								{flight.STD} - {flight.STA}
							</div>
							<div className="flight__route">
								{flight.From} - {flight.To}
							</div>
						</div>
					))}
				</div>
			}
		</div>
	);
};

export default FlightPlan;
