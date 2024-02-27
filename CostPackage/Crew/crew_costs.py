import os
from typing import Callable
import pandas as pd
from CostPackage.Scenario.scenario import get_scenario

# Costs are expressed in EUR/min for three different scenarios low,base and high
# low scenario costs are set to zero by default
# see Table 8 at page 16/39 of following document
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
df_crew = pd.read_csv(os.path.join(os.path.dirname(__file__), "CrewTacticalCosts_2019.csv"))


def get_crew_costs(aircraft_cluster: str, scenario: str) -> Callable:
    entry_scenario = get_scenario(scenario)
    crew_cost = df_crew[(df_crew.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
    return lambda delay: crew_cost * delay


# Crew costs in EUR/min provided directly by user without scenario
def get_crew_costs_from_exact_value(crew_costs_exact_value: float) -> Callable:
    if crew_costs_exact_value < 0:
        raise InvalidCrewCostsValueError(crew_costs_exact_value)
    return lambda delay: crew_costs_exact_value * delay


class InvalidCrewCostsValueError(Exception):
    def __init__(self, crew_costs_exact_value: float):
        self.crew_costs_exact_value = crew_costs_exact_value
        self.message = ("Exact crew costs value " + format(self.crew_costs_exact_value, '.2f')
                        + " invalid. Value should be >=0")

    def __repr__(self):
        return "Exact crew costs value " + format(self.crew_costs_exact_value, '.2f') + " invalid. Value should be >=0"
