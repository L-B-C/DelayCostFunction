import os
import pandas as pd

from CostPackage.Aircraft.aircraft import is_wide_body
from CostPackage.Aircraft.aircraft_cluster import get_aircraft_cluster
from CostPackage.Scenario.scenario import get_scenario

df_seats = pd.read_csv(os.path.join(os.path.dirname(__file__), "../Aircraft/AircraftSeats_2019.csv"))


def get_passengers(aircraft_type: str, scenario: str = None, load_factor: float = None) -> int:
    entry_scenario = get_scenario(scenario)
    aircraft_cluster = get_aircraft_cluster(aircraft_type)
    seats = df_seats[(df_seats.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
    if load_factor is not None:
        if 0 <= load_factor <= 1:
            return round(seats * load_factor)
        else:
            raise PassengersLoadFactorError(load_factor)
    elif is_wide_body(aircraft_cluster):
        return round(seats * .85)
    elif entry_scenario == "LowScenario":
        return round(seats * .65)
    elif entry_scenario == "HighScenario":
        return round(seats * .95)
    else:  # BaseScenario
        return round(seats * .80)


class PassengersLoadFactorError(Exception):
    def __init__(self, load_factor: float):
        self.load_factor = load_factor
        self.message = "Passengers load factor " + str(self.load_factor) + " invalid. USE (0<=value<=1)"

    def __repr__(self):
        return "Passengers load factor " + str(self.load_factor) + " invalid. USE (0<=value<=1)"
