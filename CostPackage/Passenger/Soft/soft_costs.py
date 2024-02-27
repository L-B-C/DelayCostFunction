import os
from typing import Callable
import pandas as pd
from CostPackage.Scenario.scenario import get_scenario

# ATTENTION: as mentioned in the following document
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
# SOFT COSTS are considered in the calculation of the tactical cost of delay but there is
# very little information available and further research on the topic is needed to fully
# understand its actual cost and impact on the total cost of tactical delay

# Costs are expressed in EUR per passenger and are provided for three different scenarios low, base and high
# soft costs are taken from table 18 at page 38/110 from the document dated 2014
# https://www.eurocontrol.int/sites/default/files/publication/files/european-airline-delay-cost-reference-values-final-report-4-1.pdf
# and adjusted to 2019 with compound inflation rate of 5.5% as mentioned in page 23/39 of
# https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf
df_soft = pd.read_csv(os.path.join(os.path.dirname(__file__), "PassengerTacticalCosts_SOFT_2019.csv"))


def get_interpolated_value(delay, costs, delays):
    if delay < delays[0]:
        return delay * (costs[0]) / (delays[0])
    for i in range(delays.shape[0] - 1):
        if delays[i] <= delay < delays[i + 1]:
            return (delay - delays[i]) * (costs[i + 1] - costs[i]) / (delays[i + 1] - delays[i]) + costs[i]
    return costs[-1]


def get_soft_costs(passengers: int, scenario: str) -> Callable:
    entry_scenario = get_scenario(scenario)
    costs = df_soft[entry_scenario].to_numpy()
    delays = df_soft.Delay.to_numpy()
    # To calculate the overall soft costs only a 10% of provided soft costs are used
    # this is why the discount_factor is used see page 39/110 of following document
    # https://www.eurocontrol.int/sites/default/files/publication/files/european-airline-delay-cost-reference-values-final-report-4-1.pdf
    # see also page 64/110 of Annex D of the same document mentioned above where the use
    # of only 10% of total soft costs is mentioned
    discount_factor = 0.1
    return lambda delay: get_interpolated_value(delay, costs, delays) * passengers * delay * discount_factor
