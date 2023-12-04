# https://github.com/JeanExtreme002/FlightRadarAPI

import datetime
from pandas import pandas, DataFrame
from flask import Flask
from FlightRadar24 import FlightRadar24API, Flight

app = Flask(__name__)
api = FlightRadar24API()

defaultAirlineICAO = "SAS"
# filePath = './data/roster.csv'

# Developmentvariables
devFlightNumber = "SK864"
filePath = './data/exampleRoster.csv'



def getTodaysDate() -> str:
    """
    It returns todays date as DDBBBYYYY.

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



def checkValidRoster(roster: DataFrame) -> bool:
    """
    It returns True if the roster is valid.
    It returns False if the roster is invalid and/or contains old data.
    """

    # Check if roster is empty
    if(roster.empty):
        print("Roster is empty.")
        return False
    
    # Check if roster contains old data
    if(datetime.datetime.strptime(roster['Date'].iloc[-1], "%d%b%Y").date() < datetime.datetime.now().date()):
        print("Roster contains old data.")
        return False

    return True



def getTodaysFlightplan() -> DataFrame:
    roster = loadRoster()
    roster = roster.loc[roster['Date'] == getTodaysDate()]
    return roster



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



def searchForActiveFlightFromFlightplan(flightplan: DataFrame) -> dict:
    """
    It returns a dictionary with the flight details.

    flightplan: DataFrame - Example: getTodaysFlightplan()
    """

    if(flightplan.empty):
        print("No flightplan was provided.")
        return None

    for index, row in flightplan.iterrows():
        flight = searchLiveFlightByFlightNumber(row['Activity'])
        if(flight != None):
            return flight
    return None



########## API ##########

"""
It returns a list of flights for Captain Olsen at the current date, if any.
"""
@app.route('/todaysFlightplan')
def get_todays_flightplan():
    flightplan = getTodaysFlightplan()
    if(flightplan.empty):
        return None
    return flightplan.to_json(orient='records')



@app.route('/getActiveFlight')
def get_active_flight():
    flightplan = getTodaysFlightplan()
    flight = searchForActiveFlightFromFlightplan(flightplan)
    if(flight == None):
        return "No active flight found."
    return flight





########## Server ##########

if __name__ == '__main__':
    app.run(port=5000)