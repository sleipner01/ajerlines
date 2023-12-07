# https://github.com/JeanExtreme002/FlightRadarAPI

import datetime
from pandas import pandas, DataFrame
from flask import Flask
from FlightRadar24 import FlightRadar24API, Flight
from flask import Flask, jsonify
from flask_cors import CORS



########## Variables ##########

defaultAirlineICAO = "SAS"
filePath = './data/roster.csv'

# Developmentvariables
# devFlightNumber = "SK864"
devFilePath = './data/exampleRoster.csv'



########## Setup ##########



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes
api = FlightRadar24API()



########## Helper Functions ##########



def getTodaysDate() -> str:
    """
    It returns todays date as DDBBBYYYY.

    Example: 04DEC2023
    """
    return datetime.datetime.now().strftime("%d%b%Y").upper()



########## API Functions ##########



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



########## Classes ##########



class Roster:
    def __init__(self, filePath: str = filePath):
        print(filePath)
        self.roster: DataFrame = self.loadRoster(filePath=filePath)

    def loadRoster(self, filePath: str) -> DataFrame:
        """
        It returns a DataFrame with the roster data.
        It loads the data from a csv file.
        The csv file must be in the 'data' folder and be named 'roster.csv'.

        It should be im the format: Day,Date,Activity,From,To
        """
        data: DataFrame = pandas.read_csv(filePath)
        # Keep only the columns we need
        data = data['Day,Date,Activity,From,To,STD,STA'.split(',')]
        # Remove nonflying days
        data = data.dropna()
        return data
    
    def refreshRoster(self):
        self.roster = self.loadRoster()

    def checkValidRoster(self) -> bool:
        """
        It returns True if the roster is valid.
        It returns False if the roster is invalid and/or contains old data.
        """

        # Check if roster is empty
        if(self.roster.empty):
            print("Roster is empty.")
            return False
        
        # Check if roster contains old data
        if(datetime.datetime.strptime(self.roster['Date'].iloc[-1], "%d%b%Y").date() < datetime.datetime.now().date()):
            print("Roster contains old data.")
            return False

        return True
    
    def getRoster(self) -> DataFrame:
        """
        It returns a DataFrame with the roster data.
        """

        # Check if roster is valid
        if(not self.checkValidRoster()):
            self.refreshRoster()
            if(not self.checkValidRoster()):
                print("Roster is invalid.")
                return None

        return self.roster



class Flightplan:
    def __init__(self, roster: Roster):
        self.roster = roster.getRoster()

    def updateRoster(self, roster: Roster):
        self.roster = roster.getRoster()

    def getTodaysFlightplan(self) -> DataFrame:
        """
        It returns a DataFrame with the flightplan for today.
        """
        if(self.roster.empty):
            print("No roster was provided.")
            return None
        
        todaysFlightplan = self.roster.loc[self.roster['Date'] == getTodaysDate()]
        return todaysFlightplan



class FlightSeeker: 
    def __init__(self, flightplan: Flightplan):
        self.flightplan = flightplan
        self.activeFlight = pandas.DataFrame()
        


    def searchForActiveFlightFromFlightplan(self) -> dict:
        """
        It returns a dictionary with the flight details.

        flightplan: DataFrame - Example: getTodaysFlightplan()
        """
        if(self.flightplan.empty):
            print("No flightplan was provided.")
            return None
        
        # Check if active flight is already found
        if(self.activeFlight.empty == False):
            flight = searchLiveFlightByFlightNumber(self.activeFlight['Activity'])
            
            # Check if flight is still active
            if(flight != None):
                return flight

            self.activeFlight = pandas.DataFrame()

        for index, row in self.flightplan.iterrows():
            flight = searchLiveFlightByFlightNumber(row['Activity'])
            if(flight != None):
                self.activeFlight = row
                return flight
        return None



########## Endpoints ##########



@app.route('/getTodaysDate')
def get_todays_date():
    """
    It returns todays date as DDBBBYYYY.

    Example: 04DEC2023
    """
    return jsonify(getTodaysDate())



@app.route('/hasValidRoster')
def has_valid_roster():
    """
    It returns True if the roster is valid.
    It returns False if the roster is invalid and/or contains old data.
    """
    return jsonify("True") if roster.checkValidRoster() else jsonify("False")



@app.route('/getTodaysFlightplan')
def get_todays_flightplan():
    """
    It returns a list of flights for Captain Olsen at the current date, if any.
    """
    return flightplan.getTodaysFlightplan().to_json(orient='records')



@app.route('/getActiveFlight')
def get_active_flight():
    """
    It returns the active flight for Captain Olsen at the current date, if any.
    """
    flight = flightSeeker.searchForActiveFlightFromFlightplan()
    if(flight == None):
        return jsonify("")
    return jsonify(flight[0])



@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response



########## Server ##########

if __name__ == '__main__':
    roster = Roster(devFilePath)
    flightplan = Flightplan(roster=roster)
    flightSeeker = FlightSeeker(flightplan=flightplan.getTodaysFlightplan())

    app.run(port=6969, debug=True)