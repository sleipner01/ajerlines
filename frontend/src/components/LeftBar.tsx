import "./LeftBar.css";
import DateElement from "./DateElement";
import FlightPlan from "./FlightPlan";

const LeftBar = () => {
	return (
		<div className="leftbar-container">
			<DateElement />
			<h1>Ajerlines &#128745;</h1>
			<h2>Where is Captain Olsen today?</h2>
			<FlightPlan />
		</div>
	);
};

export default LeftBar;
