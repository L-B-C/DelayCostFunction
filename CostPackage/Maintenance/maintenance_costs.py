import os
from typing import Callable
import pandas as pd

from CostPackage.FlightPhase.flight_phase import get_flight_phase, FlightPhaseError
from CostPackage.Scenario.scenario import get_scenario, ScenarioError

# Costs are expressed in EUR/min for three different scenarios low,base and high
# see Table 6 at page 14/39 of following document
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
df_maintenance_at_gate = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "MaintenanceTacticalCosts_AT_GATE_2019.csv"))

# Costs are expressed in EUR/min for three different scenarios low,base and high
# see Table 21 of Appendix C at page 38/39 of following document
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
df_maintenance_taxi = pd.read_csv(os.path.join(os.path.dirname(__file__), "MaintenanceTacticalCosts_TAXI_2019.csv"))

# Costs are expressed in EUR/min for three different scenarios low,base and high
# see Table 22 of Appendix C at page 39/39 of following document
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
df_maintenance_en_route = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "MaintenanceTacticalCosts_EN_ROUTE_2019.csv"))


def get_maintenance_costs(aircraft_cluster: str, scenario: str, flight_phase: str) -> Callable:
    try:
        entry_scenario = get_scenario(scenario)
        entry_flight_phase = get_flight_phase(flight_phase)
        if entry_flight_phase == "AT_GATE":
            maintenance_cost = \
                df_maintenance_at_gate[(df_maintenance_at_gate.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
        elif entry_flight_phase == "TAXI":
            maintenance_cost = \
                df_maintenance_taxi[(df_maintenance_taxi.Aircraft == aircraft_cluster)][entry_scenario].iloc[
                    0]
        else:  # EN_ROUTE
            maintenance_cost = \
                df_maintenance_en_route[(df_maintenance_en_route.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]

        return lambda delay: maintenance_cost * delay

    except ScenarioError as scenario_error:
        print(scenario_error.message)
    except FlightPhaseError as flight_phase_error:
        print(flight_phase_error.message)


# Maintenance costs in EUR/min provided directly by user without scenario
def get_maintenance_costs_from_exact_value(maintenance_costs_exact_value: float) -> Callable:
    if maintenance_costs_exact_value < 0:
        raise InvalidMaintenanceCostsValueError(maintenance_costs_exact_value)
    return lambda delay: maintenance_costs_exact_value * delay


class InvalidMaintenanceCostsValueError(Exception):
    def __init__(self, maintenance_costs_exact_value: float):
        self.maintenance_costs_exact_value = maintenance_costs_exact_value
        self.message = ("Exact maintenance costs value " + format(self.maintenance_costs_exact_value, '.2f')
                        + " invalid. Value should be >=0")

    def __repr__(self):
        return ("Exact maintenance costs value " + format(self.maintenance_costs_exact_value, '.2f')
                + " invalid. Value should be >=0")
