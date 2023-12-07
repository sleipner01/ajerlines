import { useQuery } from "@tanstack/react-query";
import { GET_DATE } from "../queries/queries";

const DateElement = () => {
	const backupDate = new Date().toLocaleDateString();

	const { isPending, error, data } = useQuery({
		queryKey: ["date"],
		queryFn: GET_DATE,
	});

	if (isPending) return <p className="date">...</p>;
	if (error) return <p className="date">{backupDate}</p>;

	return <p className="date">{data}</p>;
};

export default DateElement;
