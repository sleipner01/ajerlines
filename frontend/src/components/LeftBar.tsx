import Schedule from "./Schedule";
import "./LeftBar.css";

const LeftBar = () => {
	return (
		<div className="leftbar-container">
			<h1>Ajerlines &#128745;</h1>
			<h2>Where is Captain Olsen today?</h2>
			<Schedule />
		</div>
	);
};

export default LeftBar;
