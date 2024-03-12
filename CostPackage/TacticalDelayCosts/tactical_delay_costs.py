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


def get_tactical_delay_costs(aircraft_type: str, flight_phase_input: str,  # NECESSARY PARAMETERS
                             passengers_number: int = None, passenger_scenario: str = None,
                             is_low_cost_airline: bool = None, flight_length: float = None,
                             origin_airport: str = None, destination_airport: str = None,
                             curfew_violated: bool = False, curfew_costs_exact_value: float = None,
                             crew_costs_exact_value: float = None, crew_costs_scenario: str = None,
                             maintenance_costs_exact_value: float = None, maintenance_costs_scenario: str = None,
                             fuel_costs_exact_value: float = None, fuel_costs_scenario: str = None,
                             missed_connection_passengers: List[Tuple] = None,
                             curfew: Union[tuple[float, int], float] = None
                             ) -> Callable:
    """Generate cost function of delay of a given flight according to the specifics
    Parameters:
        aircraft_type: str
            aircraft(ICAO code)
        flight_phase_input: str
            can be AT_GATE, TAXI or EN_ROUTE
        passengers_number: int=None
            actual number of passengers boarded on the aircraft,
            when not provided a generic cost per passenger will be generated
        passenger_scenario: str =None
            "low" 65% of seats capacity: 
            "base" 80% of seats capacity is the normal scenario (most common)
            "high" 95% of seats capacity
            for wide-body aircraft the capacity is set to 85%
        is_low_cost_airline: bool=None
            boolean value set to true if airline is Low-Cost Carrier (LCC), if true
            sets all the cost scenarios to low
        flight_length: float=None
            Length of flight in kilometers to calculate the type of haul
            (actual fuel costs can be calculated only if provided)
        origin_airport: str=None
            ICAO code of airport of departure
        destination_airport: str=None
            ICAO code of airport of arrival
        curfew_violated: bool=None
            boolean value true if curfew has been violated
        curfew_costs_exact_value: float=None
            total cost of curfew violation in EUR
        crew_costs_exact_value: float=None
            costs of entire crew (pilots and cabin crew) in EUR/hour
            if provided will be used directly by the model
        crew_costs_scenario: str=None
            can be either "low", "base" or "high"
            "low" means zero EUR/hour costs for the entire crew
            "base" is the normal scenario (most common)
            "high" is the expensive scenario
        maintenance_costs_exact_value: float = None
            costs expressed in EUR/hour provided directly
            (CAREFUL tactical maintenance costs may be very different at the various flight phases)
        maintenance_costs_scenario: str = None
            can be either "low", "base" or "high" depending on
            aircraft age, maintenance status etc.
            "low" can be applied for example on newer aircraft or if ordinary maintenance was recently made
            "base"
            "base" is the normal scenario (most common)
            "high" is the expensive scenario (e.g. old aircraft or expensive tactical maintenance)
        fuel_costs_exact_value: float = None
            costs expressed in EUR/hour provided directly
            (ATTENTION: fuel_costs may be very different at the various flight phases and depending on fuel prices,
            and the way fuel has been bought e.g. hedging, on spot and other paying schemas)
        fuel_costs_scenario: str = None
            can be either "low", "base" or "high"
            FUEL COSTS CURRENTLY UNAVAILABLE FOR CALCULATION
        missed_connection_passengers: List[Tuple] = None
             list of tuples. Each tuple represents one passenger,
             its composition is (delay threshold, delay perceived).
             The delay threshold is the time at which the passenger misses the connection.
             The delay perceived is the delay at the passenger final destination,
             generally computed considering the next available flight of the same airline which carries
             the passenger to its final destination
        curfew: Tuple[curfew_time: float, n_passenger: int] or float, default None,
             react_curfew: Union[tuple[float, str], tuple[float, int]] = None

        """

    # Zero costs lambda if both scenario and exact value are None
    global haul

    def zero_costs():
        return lambda delay: 0

    class FunctionInputParametersConflictError(Exception):
        def __init__(self, conflict_type: str):
            self.conflict_type = conflict_type
            self.message = ("Conflict between exact value and scenario for: " + self.conflict_type
                            + " Cannot both be non None")

        def __repr__(self):
            return "Conflict between exact value and scenario for: " + self.conflict_type + " Cannot both be non None"

    try:
        aircraft_cluster = get_aircraft_cluster(aircraft_type)

        flight_phase = get_flight_phase(flight_phase_input.strip().upper())

        # to calculate passengers hard costs, haul determined according to flight length is needed
        # if flight_length is None a default value could be used to have a Medium Haul e.g. flight_length=2000
        # this could be valid only AT GATE, default flight_length value could disrupt fuel costs in EN ROUTE phase
        # if flight_length is None:
        #   haul = get_haul(fixed_flight_length)

        if flight_length is not None:
            haul = get_haul(flight_length)

        if (origin_airport is not None) and (is_valid_airport_icao(airport_icao=origin_airport.strip().upper())):
            origin_airport = origin_airport

        if (destination_airport is not None) and (
                is_valid_airport_icao(airport_icao=destination_airport.strip().upper())):
            destination_airport = destination_airport

            # If airline is LCC sets all costs scenario to low,
            # elif destination airport is in group 1 airports (more than 25 million passengers) set scenario to high
            # else scenario default is base
        if is_low_cost_airline is not None or destination_airport is not None:
            scenario = get_fixed_cost_scenario(is_LCC_airline=is_low_cost_airline,
                                               destination_airport_ICAO=destination_airport)
            crew_costs_scenario = scenario if crew_costs_scenario is None else crew_costs_scenario
            maintenance_costs_scenario = scenario if maintenance_costs_scenario is None else maintenance_costs_scenario
            fuel_costs_scenario = scenario if fuel_costs_scenario is None else fuel_costs_scenario
            passenger_scenario = scenario if passenger_scenario is None else passenger_scenario

        # without passengers number input inserted use passengers load factor based on scenario either inserted by user
        # or indirectly obtained by previous if statement
        if passengers_number is None:
            passengers_number = get_passengers(aircraft_type=aircraft_cluster, scenario=passenger_scenario)

        number_missed_connection_passengers = 0 if missed_connection_passengers is None else len(
            missed_connection_passengers)

        if passengers_number is not None:
            passengers_number = passengers_number - number_missed_connection_passengers

        # CREW COSTS
        # NO crew costs input, either manage as zero costs or choose a default scenario
        if crew_costs_exact_value is None and crew_costs_scenario is None:
            # crew_costs = zero_costs()
            crew_costs = get_crew_costs(aircraft_cluster=aircraft_cluster, scenario="BASE")
        # Crew costs based on exact value
        elif crew_costs_exact_value is not None and crew_costs_scenario is None:
            crew_costs = get_crew_costs_from_exact_value(crew_costs_exact_value)
        # Crew cost estimation based on scenario
        elif crew_costs_scenario is not None and crew_costs_exact_value is None:
            crew_costs = get_crew_costs(aircraft_cluster=aircraft_cluster, scenario=crew_costs_scenario)
        # Both parameters are not None, situation managed as a conflict
        else:
            raise FunctionInputParametersConflictError("CREW")

        # MAINTENANCE COSTS
        # NO maintenance costs input,  either manage as zero costs or choose a default scenario
        if maintenance_costs_exact_value is None and maintenance_costs_scenario is None:
            # maintenance_costs = zero_costs()
            maintenance_costs = get_maintenance_costs(aircraft_cluster=aircraft_cluster,
                                                      scenario="BASE", flight_phase=flight_phase)
        # Maintenance costs based on exact value
        elif maintenance_costs_exact_value is not None and maintenance_costs_scenario is None:
            maintenance_costs = get_maintenance_costs_from_exact_value(maintenance_costs_exact_value)
        # Maintenance costs based on scenario
        elif maintenance_costs_scenario is not None and maintenance_costs_exact_value is None:
            maintenance_costs = get_maintenance_costs(aircraft_cluster=aircraft_cluster,
                                                      scenario=maintenance_costs_scenario, flight_phase=flight_phase)
        else:  # Both parameters are not None, situation managed as a conflict
            raise FunctionInputParametersConflictError("MAINTENANCE")

        # FUEL COSTS
        # No fuel costs input,  either manage as zero costs or choose a default scenario
        if fuel_costs_exact_value is None and fuel_costs_scenario is None:
            fuel_costs = zero_costs()
            # fuel_costs = get_fuel_costs(aircraft_cluster=aircraft_cluster, scenario="base", flight_phase=flight_phase)
        # Fuel costs based on exact value
        elif fuel_costs_exact_value is not None and fuel_costs_scenario is None:
            fuel_costs = get_fuel_costs_from_exact_value(fuel_costs_exact_value)
        # Fuel costs based on scenario
        # elif fuel_costs_scenario is not None and fuel_costs_exact_value is None:
        #     fuel_costs = get_fuel_costs(aircraft_cluster=aircraft_cluster,
        #                                 scenario=fuel_costs_scenario, flight_phase=flight_phase)
        else:  # Both parameters are not None, situation managed as a conflict
            raise FunctionInputParametersConflictError("FUEL")

        # CURFEW COSTS
        # Curfew not violated and no curfew costs provided
        if curfew_violated is False and curfew_costs_exact_value is None:
            curfew_costs = zero_costs()
        # Curfew costs base on exact value
        elif curfew_costs_exact_value is not None and curfew_violated is True:
            curfew_costs = get_curfew_costs_from_exact_value(curfew_costs_exact_value)
        elif curfew_violated is True and curfew is None:
            curfew_costs = zero_costs()
        elif curfew_violated is True and curfew is not None:
            curfew_threshold = curfew[0] if curfew is tuple else curfew
            curfew_passengers = curfew[
                1] if curfew is tuple else passengers_number + number_missed_connection_passengers
            curfew_costs = get_curfew_costs(aircraft_cluster=aircraft_cluster, curfew_passengers=curfew_passengers)
        else:  # Both parameters are not None, situation managed as a conflict
            raise FunctionInputParametersConflictError("CURFEW")

        # PASSENGER COSTS
        # Soft and Hard costs of passengers who didn't lose the connection
        passengers_hard_costs = get_hard_costs(passengers=passengers_number, scenario=passenger_scenario, haul=haul)
        passengers_soft_costs = get_soft_costs(passengers=passengers_number, scenario=passenger_scenario)

        # Soft and Hard costs of passengers with missed connection
        if number_missed_connection_passengers > 0:
            # Hard and soft costs for a single passenger
            missed_connection_passengers_hard_costs = get_hard_costs(passengers=1, scenario=passenger_scenario,
                                                                     haul=haul)
            missed_connection_passengers_soft_costs = get_soft_costs(passengers=1, scenario=passenger_scenario)

            def considered_passenger_costs(delay, passenger, cost_type):
                # Set only care if delay is less than passenger connection threshold
                # Set 0 if delay < passenger connection threshold
                cost_function = missed_connection_passengers_hard_costs if cost_type == 'hard' else missed_connection_passengers_soft_costs
                return cost_function(delay if delay < passenger[0] else passenger[1])

            passengers_costs = lambda delay: passengers_hard_costs(delay) + passengers_soft_costs(delay) + sum(
                considered_passenger_costs(delay, passenger, 'hard') for passenger in
                missed_connection_passengers) + sum(
                considered_passenger_costs(delay, passenger, 'soft') for passenger in
                missed_connection_passengers)
        else:
            passengers_costs = lambda delay: passengers_hard_costs(delay) + passengers_soft_costs(delay)

    except AircraftClusterError as aircraft_cluster_error:
        print(aircraft_cluster_error.message)

    except FlightPhaseError as flight_phase_error:
        print(flight_phase_error.message)

    except AirportCodeError as airport_code_error:
        print(airport_code_error.message)

    except HaulError as haul_error:
        print(haul_error.message)

    except ScenarioError as scenario_error:
        print(scenario_error.message)

    except PassengersLoadFactorError as passengers_load_factor_error:
        print(passengers_load_factor_error.message)

    except InvalidCrewCostsValueError as invalid_crew_costs_value_error:
        print(invalid_crew_costs_value_error.message)

    except InvalidMaintenanceCostsValueError as invalid_maintenance_costs_value_error:
        print(invalid_maintenance_costs_value_error.message)

    except InvalidFuelCostsValueError as invalid_fuel_costs_value_error:
        print(invalid_fuel_costs_value_error.message)

    except InvalidCurfewCostsValueError as invalid_curfew_costs_value_error:
        print(invalid_curfew_costs_value_error.message)

    except FunctionInputParametersConflictError as function_input_parameters_conflict_error:
        print(function_input_parameters_conflict_error.message)

    except Exception as e:
        print(print(f"An unexpected exception occurred: {e}"))

    finally:
        return lambda delay: maintenance_costs(delay) + crew_costs(delay) + passengers_costs(delay) + curfew_costs(
            delay)
