import {
	ComposableMap,
	Geographies,
	Geography,
	Graticule,
	Marker,
	Sphere,
	ZoomableGroup,
} from "react-simple-maps";
import "./Map.css";

type Coordinates = [number, number];
const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

export default function MapChart() {
	const coordinates: Coordinates = [-15.57808, 27.8282];
	return (
		<div className="map-container">
			<ComposableMap
				stroke="#00FF00"
				strokeWidth={0.2}
				fill="#666"
				projection="geoMercator"
			>
				<ZoomableGroup zoom={5} center={coordinates}>
					<Sphere stroke="#000" strokeWidth={0.3} id={""} fill="transparent" />
					<Graticule stroke="#000" strokeWidth={0.1} />
					<Geographies geography={geoUrl} fill="#335533">
						{({ geographies }) =>
							geographies.map((geo) => (
								<Geography key={geo.rsmKey} geography={geo} />
							))
						}
					</Geographies>
					<Marker coordinates={coordinates}>
						<circle r={1} fill="#F53" />
					</Marker>
				</ZoomableGroup>
			</ComposableMap>
		</div>
	);
}
