import os
import pandas as pd


class AircraftClusterError(Exception):
    def __init__(self, flight: str):
        self.flight = flight
        self.message = "Aircraft " + self.flight + " not found"

    def __repr__(self):
        return "Aircraft " + self.flight + " not found"


aircraft_cluster = pd.read_csv(os.path.join(os.path.dirname(__file__), "AircraftClustering.csv"))
aircraft_cluster_dict = dict(zip(aircraft_cluster.AircraftType, aircraft_cluster.AssignedAircraftType))


# NOTE: Aircraft types are identified by their ICAO codes
def get_aircraft_cluster(aircraft_type: str):
    if aircraft_type in list(aircraft_cluster_dict.keys()):
        return aircraft_cluster_dict[aircraft_type]
    else:
        raise AircraftClusterError(aircraft_type)
