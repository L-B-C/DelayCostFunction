import pandas as pd
import os
from typing import Callable, List, Tuple, Union

from CostPackage.Aircraft.aircraft_cluster import get_aircraft_cluster, AircraftClusterError
from CostPackage.Airport.airport import is_valid_airport_icao, AirportCodeError
from CostPackage.Crew.crew_costs import get_crew_costs_from_exact_value, get_crew_costs, InvalidCrewCostsValueError
from CostPackage.FlightPhase.flight_phase import get_flight_phase, FlightPhaseError
from CostPackage.Fuel.fuel_costs import get_fuel_costs_from_exact_value, InvalidFuelCostsValueError
from CostPackage.Haul.haul import get_haul, HaulError
from CostPackage.Maintenance.maintenance_costs import get_maintenance_costs_from_exact_value, get_maintenance_costs, \
    InvalidMaintenanceCostsValueError
from CostPackage.Passenger.Hard.hard_costs import get_hard_costs
from CostPackage.Passenger.Soft.soft_costs import get_soft_costs
from CostPackage.Scenario.scenario import get_fixed_cost_scenario


def get_tactical_delay_costs(aircraft_type: str, flight_phase_input: str,  # NECESSARY PARAMETERS
                             passengers_number: int = None, passenger_scenario: str = None,
                             is_low_cost_airline: bool = None, flight_length: float = None,
                             origin_airport: str = None, destination_airport: str = None,
                             curfew_violated: bool = False, curfew_costs_exact_value: float = None,
                             crew_costs_exact_value: float = None, crew_costs_scenario: str = None,
                             maintenance_costs_exact_value: float = None, maintenance_costs_scenario: str = None,
                             fuel_costs_exact_value: float = None, fuel_costs_scenario: str = None,
                             passenger_hard_costs: float = None, passenger_soft_costs: float = None,
                             missed_connection_passengers: List[Tuple] = None
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
            boolean value set to true if flight is considered low-cost
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
        passenger_hard_costs: float = None
            passenger hard costs in EUR passed directly if known
        passenger_soft_costs: float = None
            passenger soft costs in EUR passed directly if known
        missed_connection_passengers: List[Tuple] = None
             list of tuples. Each tuple represents one passenger,
             its composition is (delay threshold, delay perceived).
             The delay threshold is the time at which the passenger misses the connection.
             The delay perceived is the delay at the passenger final destination,
             generally computed considering the next available flight of the same airline which carries
             the passenger to its final destination

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

        if flight_length is not None:
            haul = get_haul(flight_length)

        if (origin_airport is not None) and (is_valid_airport_icao(airport_icao=origin_airport.strip().upper())):
            origin_airport = origin_airport

        if (destination_airport is not None) and (
                is_valid_airport_icao(airport_icao=destination_airport.strip().upper())):
            destination_airport = destination_airport

        if is_low_cost_airline is not None or destination_airport is not None:
            scenario = get_fixed_cost_scenario(is_low_cost_airline, destination_airport)
            crew_costs_scenario = scenario
            maintenance_costs_scenario = scenario
            fuel_costs_scenario = scenario
            passenger_scenario = scenario



        # CREW COSTS
        # NO crew costs input
        if crew_costs_exact_value is None and crew_costs_scenario is None:
            crew_costs = zero_costs()
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
        # NO maintenance costs input
        if maintenance_costs_exact_value is None and maintenance_costs_scenario is None:
            maintenance_costs = zero_costs()
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
        # No fuel costs input
        if fuel_costs_exact_value is None and fuel_costs_scenario is None:
            fuel_costs = zero_costs()
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
        # elif curfew_costs_exact_value is not None and curfew_violated is True:
        #    curfew_costs = get_curfew_costs_from_exact_value()
        # elif curfew_violated is True and curfew_costs_exact_value is None:
        #   curfew_costs = get_curfew_costs()

        # PASSENGER COSTS
        if passengers_number is not None and passenger_scenario is not None:
            if missed_connection_passengers is None:
                number_missed_connection_passengers = 0
            else:
                number_missed_connection_passengers = len(missed_connection_passengers)
            passengers_number = passengers_number - number_missed_connection_passengers

            # Soft and Hard costs of passengers who didn't lose the connection
            passengers_hard_costs = get_hard_costs(passengers=passengers_number, scenario=passenger_scenario, haul=haul)
            passengers_soft_costs = get_soft_costs(passengers=passengers_number, scenario=passenger_scenario)

            # Soft and Hard costs of passengers with missed connection
            if number_missed_connection_passengers > 0:
                # Hard and soft costs for a single passenger
                missed_connection_passengers_hard_costs = get_hard_costs(passengers=1,
                                                                         scenario=passenger_scenario, haul=haul)
                missed_connection_passengers_soft_costs = get_soft_costs(passengers=1, scenario=passenger_scenario)

                # Set only care if delay is less than passenger connection threshold
                def hard_costs_considered_passenger(delay, passenger):
                    if delay < passenger[0]:
                        return missed_connection_passengers_hard_costs(delay)
                    else:
                        return missed_connection_passengers_hard_costs(passenger[1])

                # Set 0 if delay < passenger connection threshold
                def soft_costs_considered_passenger(delay, passenger):
                    if delay < passenger[0]:
                        return missed_connection_passengers_soft_costs(delay)
                    else:
                        return missed_connection_passengers_hard_costs(passenger[1])

                def passengers_costs(delay):
                    return (passengers_hard_costs(delay) + passengers_soft_costs(delay) +
                            sum(hard_costs_considered_passenger(delay, passenger) for passenger in
                                missed_connection_passengers) +
                            sum(soft_costs_considered_passenger(delay, passenger) for passenger in
                                missed_connection_passengers))
            else:
                def passengers_costs(delay):
                    return passengers_hard_costs(delay) + passengers_soft_costs(delay)

    except AircraftClusterError as aircraft_cluster_error:
        print(aircraft_cluster_error.message)

    except FlightPhaseError as flight_phase_error:
        print(flight_phase_error.message)

    except AirportCodeError as airport_code_error:
        print(airport_code_error.message)

    except HaulError as haul_error:
        print(haul_error.message)

    except InvalidCrewCostsValueError as invalid_crew_costs_value_error:
        print(invalid_crew_costs_value_error.message)

    except InvalidMaintenanceCostsValueError as invalid_maintenance_costs_value_error:
        print(invalid_maintenance_costs_value_error.message)

    except InvalidFuelCostsValueError as invalid_fuel_costs_value_error:
        print(invalid_fuel_costs_value_error.message)

    except FunctionInputParametersConflictError as function_input_parameters_conflict_error:
        print(function_input_parameters_conflict_error.message)

    except Exception as e:
        print(print(f"An unexpected exception occurred: {e}"))

    finally:
        return lambda delay: maintenance_costs(delay) + crew_costs(delay) + passengers_costs(delay)
