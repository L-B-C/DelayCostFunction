import pandas as pd
import os


class AirportCodeError(Exception):
    def __init__(self, airport_icao: str):
        self.airport_icao = airport_icao
        self.message = "Airport " + self.airport_icao + " not found"

    def __repr__(self):
        return "Airport " + self.airport_icao + " not found"


df_airports = pd.read_csv(os.path.join(os.path.dirname(__file__), "Airports.csv"))
group_1_airports = pd.read_csv(os.path.join(os.path.dirname(__file__), "airportMore25M.csv"))


def is_valid_airport_icao(airport_icao: str):
    if airport_icao in df_airports['ICAO'].values:
        return True
    else:
        raise AirportCodeError


# airport is in group 1 if it has more than 25 million passengers
# groups according to Airport Council International (ACI) based on number of passengers per year per airport
# calculation done by RDC Aviation
# see following document at page 28/39
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
def is_group_1_airport(airport_icao: str):
    if is_valid_airport_icao(airport_icao):
        if airport_icao in group_1_airports.to_list():
            return True
        else:
            return False
