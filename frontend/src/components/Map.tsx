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
import { useQuery } from "@tanstack/react-query";
import { GET_ACTIVE_FLIGHT } from "../queries/queries";

type Coordinates = [number, number];

const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

export default function MapChart() {
	const { isPending, error, data } = useQuery({
		queryKey: ["activeflight"],
		queryFn: GET_ACTIVE_FLIGHT,
		refetchInterval: 10000,
	});

	if (isPending) console.log("Loading...");

	if (error) console.error("An error has occurred: " + error.message);

	if (data) console.log(data);

	return (
		<div className="map-container">
			<ComposableMap
				stroke="#00FF00"
				strokeWidth={0.2}
				fill="#666"
				projection="geoMercator"
			>
				<ZoomableGroup
					zoom={5}
					center={data && ([data.detail.lon, data.detail.lat] as Coordinates)}
				>
					<Sphere stroke="#000" strokeWidth={0.3} id={""} fill="transparent" />
					<Graticule stroke="#000" strokeWidth={0.1} />
					<Geographies geography={geoUrl} fill="#335533">
						{({ geographies }) =>
							geographies.map((geo) => (
								<Geography key={geo.rsmKey} geography={geo} />
							))
						}
					</Geographies>
					{data && (
						<Marker
							key={data.id}
							coordinates={[data.detail.lon, data.detail.lat]}
						>
							<circle r={1} fill="#FFF" />
							<text
								r={0.5}
								strokeWidth={0.3}
								textAnchor="middle"
								stroke="#000"
								fill="#FFF"
							>
								{data.detail.flight}
							</text>
						</Marker>
					)}
				</ZoomableGroup>
			</ComposableMap>
		</div>
	);
}
