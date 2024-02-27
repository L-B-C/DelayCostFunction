import os
import pandas as pd


class AircraftTypeError(Exception):
    def __init__(self, aircraft_type: str):
        self.aircraft_type = aircraft_type
        self.message = "Aircraft " + self.aircraft_type + " not found"

    def __repr__(self):
        return "Aircraft " + self.aircraft_type + " not found"


# Returns True if aircraft type (ICAO code) is in 2019  csv of aircraft selection and clustering
# based on square root of MTOW
# see
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
def is_valid_aircraft(aircraft_type: str):
    df_aircraft_type = pd.read_csv(os.path.join(os.path.dirname(__file__), "AircraftClustering.csv"))
    aircraft_type_list = df_aircraft_type['AircraftType'].values.tolist()
    if aircraft_type in aircraft_type_list:
        return True
    else:
        raise AircraftTypeError(aircraft_type)


# Returns True if aircraft type (ICAO code) is in 2019 csv of AircraftWideBody
def is_wide_body(aircraft_type: str):
    df_wide_body_aircraft = pd.read_csv(os.path.join(os.path.dirname(__file__), "AircraftWideBody_2019.csv"))
    wide_body_aircraft = df_wide_body_aircraft['AircraftType'].values.tolist()
    return is_valid_aircraft(aircraft_type) and aircraft_type in wide_body_aircraft
