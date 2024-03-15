import pandas as pd
import os
from typing import Callable, List, Tuple, Union

from CostPackage.Aircraft.aircraft_cluster import get_aircraft_cluster, AircraftClusterError
from CostPackage.Airport.airport import is_valid_airport_icao, AirportCodeError
from CostPackage.Crew.crew_costs import get_crew_costs_from_exact_value, get_crew_costs, InvalidCrewCostsValueError
from CostPackage.Curfew.curfew_costs import get_curfew_costs_from_exact_value, get_curfew_costs, \
    InvalidCurfewCostsValueError
from CostPackage.FlightPhase.flight_phase import get_flight_phase, FlightPhaseError
from CostPackage.Fuel.fuel_costs import get_fuel_costs_from_exact_value, InvalidFuelCostsValueError
from CostPackage.Haul.haul import get_haul, HaulError
from CostPackage.Maintenance.maintenance_costs import get_maintenance_costs_from_exact_value, get_maintenance_costs, \
    InvalidMaintenanceCostsValueError
from CostPackage.Passenger.Hard.hard_costs import get_hard_costs
from CostPackage.Passenger.Soft.soft_costs import get_soft_costs
from CostPackage.Passenger.passenger import get_passengers, PassengersLoadFactorError
from CostPackage.Scenario.scenario import get_fixed_cost_scenario, ScenarioError