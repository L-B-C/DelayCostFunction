class CostObject:
    def __init__(self, cost_function, aircraft_type, flight_phase_input,
                 is_low_cost_airline, flight_length, origin_airport, destination_airport, curfew_violated, curfew_costs_exact_value,
                 crew_costs, maintenance_costs, fuel_costs, missed_connection_passengers, curfew, aircraft_cluster, flight_phase, haul,
                 scenario, passenger_scenario, passengers_number, total_crew_costs, total_maintenance_costs, total_fuel_costs, curfew_costs,
                 passengers_hard_costs, passengers_soft_costs):
        """Object containg the result of the cost function computation

        cost_function: lambda
            the lambda function which take as input the delay and returns the cost

        params_dixt: dict
            the dictonary contanining all parameters of the cost object

        get_params() ->list(str):
            methods which return all parameters included in the cost object

        info():
            methods that prints all parameters of the cost object
        """

        self.cost_function = cost_function

        self.aircraft_type = aircraft_type
        self.flight_phase_input = flight_phase_input
        self.passengers_number = passengers_number
        self.passenger_scenario = passenger_scenario
        self.is_low_cost_airline = is_low_cost_airline
        self.flight_length = flight_length
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.curfew_violated = curfew_violated
        self.curfew_costs_exact_value = curfew_costs_exact_value
        self.crew_costs = crew_costs
        self.maintenance_costs = maintenance_costs
        self.fuel_costs = fuel_costs
        self.missed_connection_passengers = missed_connection_passengers
        self.curfew = curfew
        self.aircraft_cluster = aircraft_cluster
        self.flight_phase = flight_phase
        self.haul_type = haul
        self.final_cost_scenario = scenario
        self.final_passenger_scenario = passenger_scenario
        self.adjusted_passengers_number = passengers_number
        self.total_crew_costs_function = total_crew_costs
        self.total_maintenance_costs_function = total_maintenance_costs
        self.total_fuel_costs_function = total_fuel_costs
        self.curfew_costs_function = curfew_costs
        self.passengers_hard_costs_function = passengers_hard_costs
        self.passengers_soft_costs_function = passengers_soft_costs

        self.params_dict = self.make_params_dict()

    def make_params_dict(self):
        return {
            "cost_function": self.cost_function,
            "parameters": {
                "aircraft_type": self.aircraft_type,
                "flight_phase_input": self.flight_phase_input,
                "passengers_number": self.passengers_number,
                "passenger_scenario": self.passenger_scenario,
                "is_low_cost_airline": self.is_low_cost_airline,
                "flight_length": self.flight_length,
                "origin_airport": self.origin_airport,
                "destination_airport": self.destination_airport,
                "curfew_violated": self.curfew_violated,
                "curfew_costs_exact_value": self.curfew_costs_exact_value,
                "crew_costs": self.crew_costs,
                "maintenance_costs": self.maintenance_costs,
                "fuel_costs": self.fuel_costs,
                "missed_connection_passengers": self.missed_connection_passengers,
                "curfew": self.curfew
            },
            "derived_parameters": {
                "aircraft_cluster": self.aircraft_cluster,
                "flight_phase": self.flight_phase,
                "haul_type": self.haul_type,
                "final_cost_scenario": self.final_cost_scenario,
                "final_passenger_scenario": self.passenger_scenario,
                "adjusted_passengers_number": self.passengers_number,
                "total_crew_costs_function": self.total_crew_costs_function,
                "total_maintenance_costs_function": self.total_maintenance_costs_function,
                "total_fuel_costs_function": self.total_fuel_costs_function,
                "curfew_costs_function": self.curfew_costs_function,
                "passengers_hard_costs_function": self.passengers_hard_costs_function,
                "passengers_soft_costs_function": self.passengers_soft_costs_function
            }
        }

    def get_params(self):
        return (list(self.params_dict.keys())[0] + list(list(self.params_dict.keys())[1].keys())
                + list(list(self.params_dict.keys())[2].keys()))

    def info(self):

        print((list(self.params_dict.keys())[0]), "\n")

        print("Input parameters")
        l = list(list(self.params_dict.keys())[1].keys())
        for key in l:
            print(key)

        print("\nDerived parameters")

        l = list(list(self.params_dict.keys())[2].keys())
        for key in l:
            print(key)
