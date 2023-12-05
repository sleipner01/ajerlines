import {
	ComposableMap,
	Geographies,
	Geography,
	Marker,
} from "react-simple-maps";

const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

export default function MapChart() {
	return (
		<ComposableMap>
			<Geographies geography={geoUrl}>
				{({ geographies }) =>
					geographies.map((geo) => (
						<Geography key={geo.rsmKey} geography={geo} />
					))
				}
			</Geographies>
			<Marker coordinates={[-15.57808, 27.8282]}>
				<circle r={2} fill="#F53" />
			</Marker>
		</ComposableMap>
	);
}
