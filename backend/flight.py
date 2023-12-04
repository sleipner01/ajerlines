# https://github.com/JeanExtreme002/FlightRadarAPI

import datetime
from pandas import pandas, DataFrame
from flask import Flask
from FlightRadar24 import FlightRadar24API, Flight

app = Flask(__name__)
api = FlightRadar24API()

defaultAirlineICAO = "SAS"
filePath = './data/exampleRoster.csv'

# Developmentvariables
devFlightNumber = "SK864"



def getTodaysDate() -> str:
    """
    It returns todays date as DDMMMYYYY.

    Example: 04DEC2023
    """
    return datetime.datetime.now().strftime("%d%b%Y").upper()



def loadRoster() -> DataFrame:
    """
    It returns a DataFrame with the roster data.
    It loads the data from a csv file.
    The csv file must be in the 'data' folder and be named 'roster.csv'.


    It should be im the format: Day,Date,Activity,From,To
    """
    data: DataFrame = pandas.read_csv(filePath)
    # Keep only the columns we need
    data = data['Day,Date,Activity,From,To'.split(',')]
    # Remove nonflying days
    data = data.dropna()
    return data



def getTodaysFlightplan() -> list:
    roster = loadRoster()
    print(getTodaysDate())
    # roster = roster.loc[roster['Date'] == getTodaysDate()]
    roster = roster.loc[roster['Date'] == '04DEC2023']
    print(roster)
    return []

getTodaysFlightplan()



def getFlightsByAirline(airlineICAO: str, registration: str = None) -> list:
    """
    It returns a list of flight instances.
    """
    if(airlineICAO == None):
        print("No airlineICAO was provided.")
        return None
    
    flights = api.get_flights(airline=airlineICAO, registration=registration)
    print(f"Retrieved {len(flights)} flights.")
    return flights



def searchLiveFlightByFlightNumber(flightNumber: str) -> dict:
    """
    It returns a dictionary with the flight details.

    flightNumber: str - Example: "SK2301"
    """

    # Get id from flight-search
    # api.search("SK2301").get('live')[0].get('id')

    if(flightNumber == None):
        print("No flightNumber was provided.")
        return None

    flight = api.search(flightNumber).get('live')
    print(f"Retrieved {len(flight)} flights.")
    if(len(flight) == 0):
        return None
    return flight



def getFlightDetails(flight: Flight | str) -> dict:
    """
    It returns a dictionary with the flight details.

    You can send a Flight object, I.E object returned from api.get_flights().

    flight: Flight | str - Example: "SK2301"
    """

    if(flight == None):
        print("No flight og flightId was provided.")
        return None

    flightDetails = api.get_flight_details(flight=flight)
    print(f"Retrieved flight details for {flight}.")
    return flightDetails



########## API ##########


# @app.route('/data')
# def get_data():
#     return "Hello World"



########## Server ##########

# if __name__ == '__main__':
#     app.run(port=5000)