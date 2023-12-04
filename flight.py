# https://github.com/JeanExtreme002/FlightRadarAPI

from flask import Flask
from FlightRadar24 import FlightRadar24API

app = Flask(__name__)
api = FlightRadar24API()

def getFlightsByAirline(airlineICAO: str) -> list:
    """
    It returns a list of flight instances.
    """
    flights = api.get_flights(airline=airlineICAO)
    print(f"Retrieved {len(flights)} flights.")
    return flights

flights = getFlightsByAirline("SAS")

"""
# Get the flight details from a flight instance
# The returned object is a dictionary
"""
flight = flights[0]
flightdata = api.get_flight_details(flight=flight)
print(flightdata)



########## Server ##########

# @app.route('/data')
# def get_data():
#     return "Hello World"

# if __name__ == '__main__':
#     app.run(port=5000)