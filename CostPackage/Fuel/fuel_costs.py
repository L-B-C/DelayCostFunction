import os
from typing import Callable
import pandas as pd

from CostPackage.FlightPhase.flight_phase import get_flight_phase, FlightPhaseError
from CostPackage.Scenario.scenario import get_scenario, ScenarioError


# df_fuel_at_gate = pd.read_csv(os.path.join(os.path.dirname(__file__), "FuelTacticalCosts_AT_GATE_2019.csv"))

# df_fuel_taxi = pd.read_csv(os.path.join(os.path.dirname(__file__), "FuelTacticalCosts_TAXI_2019.csv"))

# df_fuel_en_route = pd.read_csv(os.path.join(os.path.dirname(__file__), "FuelTacticalCosts_EN_ROUTE_2019.csv"))


# Fuel costs should be generated using BADA3 average fuel consumption for different flight phases and
# an updated fuel costs table based on different scenarios LOW, BASE, HIGH.
# clustering should be reconsidered/verified for fuel costs calculation due to high variance aircraft/engine

# def get_fuel_costs(aircraft_cluster: str, scenario: str, flight_phase: str) -> Callable:
#     try:
#         entry_scenario = get_scenario(scenario)
#         entry_flight_phase = get_flight_phase(flight_phase)
#         # AT_GATE fuel costs should be zero (different from zero if APU usage is considered)
#         if entry_flight_phase == "AT_GATE":
#             fuel_cost = df_fuel_at_gate[(df_fuel_at_gate.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
#         elif entry_flight_phase == "TAXI":
#             fuel_cost = df_fuel_taxi[(df_fuel_taxi.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
#         else:  # EN_ROUTE
#             fuel_cost = df_fuel_en_route[(df_fuel_en_route.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
#
#         return lambda delay: fuel_cost * delay
#     except ScenarioError as scenario_error:
#         print(scenario_error.message)
#     except FlightPhaseError as flight_phase_error:
#         print(flight_phase_error.message)

# Fuel costs in EUR/min provided directly by user without scenario
def get_fuel_costs_from_exact_value(fuel_costs_exact_value: float) -> Callable:
    if fuel_costs_exact_value < 0:
        raise InvalidFuelCostsValueError(fuel_costs_exact_value)
    return lambda delay: fuel_costs_exact_value * delay


class InvalidFuelCostsValueError(Exception):
    def __init__(self, fuel_costs_exact_value: float):
        self.fuel_costs_exact_value = fuel_costs_exact_value
        self.message = ("Exact fuel costs value " + format(self.fuel_costs_exact_value, '.2f')
                        + " invalid. Value should be >=0")

    def __repr__(self):
        return "Exact fuel costs value " + format(self.fuel_costs_exact_value, '.2f') + " invalid. Value should be >=0"
