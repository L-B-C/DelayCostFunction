import os
import pandas as pd

df_airlines = pd.read_csv(os.path.join(os.path.dirname(__file__), "airline_static.csv"))


class AirlineCodeError(Exception):
    def __init__(self, airline_icao: str):
        self.airline_icao = airline_icao
        self.message = "Airline " + self.airline_icao + " not found"

    def __repr__(self):
        return "Airline " + self.airline_icao + " not found"


def is_valid_airline_icao(airline_icao: str):
    if airline_icao in df_airlines['ICAO'].values:
        return True
    else:
        raise AirlineCodeError


def is_LCC_airline_icao(airline_icao: str):
    if is_valid_airline_icao(airline_icao) and df_airlines[df_airlines.ICAO == airline_icao].iloc[0].AO_type == 'LCC':
        return True
    else:
        return False
