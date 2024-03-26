import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from CostPackage.TacticalDelayCosts.tactical_delay_costs import *

# help(get_tactical_delay_costs)

# Array of delays to analyze
delays = np.arange(0, 305, 5)


# print(delays)

# Function to extract cost function and calculate costs for given delays
def calculate_costs_for_delays(result, delays):
    cost_function = result['cost_function']  # Extracting the cost function
    return [cost_function(d) for d in delays]




cost_function = get_tactical_delay_costs(aircraft_type="A320", flight_length=800, flight_phase_input="AT_GATE",
                                         passenger_scenario="BASE", passengers_number=170)
cost_function_with_missed_connections = get_tactical_delay_costs(aircraft_type="A320", flight_length=800,
                                                                 flight_phase_input="AT_GATE",
                                                                 passenger_scenario="BASE", passengers_number=170,
                                                                 missed_connection_passengers=[(20, 300), (40, 200),
                                                                                               (25, 185)])
cost_function_with_missed_connections_20 = get_tactical_delay_costs(aircraft_type="A320", flight_length=800,
                                                                    flight_phase_input="AT_GATE",
                                                                    passenger_scenario="BASE",
                                                                    passengers_number=170,
                                                                    missed_connection_passengers=[(20, 300), (40, 200),
                                                                                                  (25, 185), ])

# Boeing 738, flight length (2000km - medium haul), flight phase "AT_GATE (no fuel costs), no curfew,
# passenger number as 80% of max capacity no passengers with missed connections

cost_function_B738 = get_tactical_delay_costs(aircraft_type="B738", flight_length=2000, flight_phase_input="AT_GATE",
                                              passenger_scenario="BASE", crew_costs="BASE",
                                              maintenance_costs="BASE", passengers_number=151)
# 10% of boarded passengers with connections
cost_function_B738_mc = get_tactical_delay_costs(aircraft_type="B738", flight_length=2000, flight_phase_input="AT_GATE",
                                                 passenger_scenario="BASE", crew_costs="BASE",
                                                 maintenance_costs="BASE", passengers_number=151,
                                                 missed_connection_passengers=[(33, 177), (38, 247), (45, 151),
                                                                               (107, 273),
                                                                               (18, 147), (35, 215), (44, 284),
                                                                               (148, 259),
                                                                               (192, 294), (70, 194)])

# Boeing 738, flight length (2000km - medium haul), flight phase "AT_GATE (no fuel costs), no curfew,
# passenger number as 80% of max capacity no passengers with missed connections,
cost_function_B744 = get_tactical_delay_costs(aircraft_type="B744", flight_length=2000, flight_phase_input="AT_GATE",
                                              passenger_scenario="BASE", crew_costs="BASE",
                                              maintenance_costs="BASE", passengers_number=364)

# 10% of boarded passengers with connections
# Boeing 738, flight length (2000km - medium haul), flight phase "AT_GATE (no fuel costs), no curfew,
# passenger number as 80% of max capacity no passengers with missed connections,
cost_function_B744_mc = get_tactical_delay_costs(aircraft_type="B744", flight_length=2000, flight_phase_input="AT_GATE",
                                                 passenger_scenario="BASE", crew_costs="BASE",
                                                 maintenance_costs="BASE", passengers_number=364,
                                                 missed_connection_passengers=[(33, 177), (38, 247), (45, 151),
                                                                               (18, 147), (35, 215), (44, 284),
                                                                               (148, 259), (192, 294), (70, 194),
                                                                               (18, 171), (73, 214), (171, 288),
                                                                               (145, 274), (194, 294), (11, 129),
                                                                               (133, 300), (56, 160), (133, 274),
                                                                               (172, 294), (175, 294), (191, 298),
                                                                               (66, 282), (81, 187), (89, 281),
                                                                               (180, 295), (123, 264), (141, 272),
                                                                               (46, 297), (49, 161), (34, 277),
                                                                               (122, 256), (71, 278), (62, 234),
                                                                               (187, 287), (133, 296), (107, 273)])

cost_values_738 = [cost_function_B738(d) for d in delays]
cost_values_738_mc = [cost_function_B738_mc(d) for d in delays]

cost_values_744 = [cost_function_B744(d) for d in delays]
cost_values_744_mc = [cost_function_B744_mc(d) for d in delays]

# Plotting
plt.plot(delays, cost_values_738, label="B738")
plt.plot(delays, cost_values_738_mc, label="B738 (10% passengers with connections)")
plt.plot(delays, cost_values_744, label="B744")
plt.plot(delays, cost_values_744_mc, label="B744 (10% passengers with connections)")
plt.xlabel('Delay (minutes)')
plt.ylabel('Cost (€)')
plt.title('Primary Tactical Delay Costs AT GATE for Aircraft B738 and B744')
plt.legend()  # Display the legend

plt.show()

seats_80_percent = np.array([119, 141, 80, 151, 188, 216, 364, 125, 150, 188, 38, 62, 64, 85, 262, 118, 101, 59])
aircraft = np.array(['B737', 'B734', 'CRJX', 'B738', 'B752', 'B763', 'B744', 'A319', 'A320', 'A321', 'AT43', 'AT76',
                     'DH8D', 'E190', 'A332', 'B733', 'B735', 'AT72'])

delays_thresholds = [(33, 177), (38, 247), (45, 151), (107, 273), (18, 147), (35, 215), (44, 284),
                     (148, 259), (192, 294), (70, 194), (18, 171), (73, 214), (171, 288), (145, 274),
                     (194, 294), (11, 129), (133, 300), (56, 160), (133, 274), (172, 294), (175, 294),
                     (191, 298), (66, 282), (81, 187), (89, 281), (180, 295), (123, 264), (141, 272),
                     (46, 297), (49, 161), (34, 277), (122, 256), (71, 278), (62, 234), (187, 287), (133, 296)]


def get_cost_values(sel_aircraft, num_passengers, missed_connections=False):
    delays_sel = np.array([5, 10, 15, 30, 45, 60, 90, 120, 240, 300])
    cost_function_sel = get_tactical_delay_costs(aircraft_type=sel_aircraft,
                                                 flight_length=2000,
                                                 flight_phase_input="AT_GATE",
                                                 passenger_scenario="BASE",
                                                 crew_costs="BASE",
                                                 maintenance_costs="BASE",
                                                 passengers_number=num_passengers,
                                                 missed_connection_passengers=None if not missed_connections
                                                 else delays_thresholds[:int(round(num_passengers * 0.1))])
    print(sel_aircraft, missed_connections, delays_thresholds[:int(round(num_passengers * 0.1))], "\n")
    return [int(round(cost_function_sel(d))) for d in delays_sel]


# Create an empty dictionary to hold the cost values for each aircraft
cost_values_dict = {}

# Loop through each aircraft and its corresponding 80% seats value
for ac_type, seats in zip(aircraft, seats_80_percent):
    # Apply the get_cost_values function to each aircraft and its seats
    cost_values_dict[ac_type] = get_cost_values(ac_type, seats)

# Now, transform this dictionary into a pandas DataFrame for a tabular view
# Each key (aircraft type) becomes a row, and the columns will be the delays
delays = [5, 10, 15, 30, 45, 60, 90, 120, 240, 300]  # Delays as column headers
costs_df = pd.DataFrame.from_dict(cost_values_dict, orient='index', columns=delays)

# Display the DataFrame (optional, depending on your use case)
print(costs_df)
costs_df.to_csv("aircraft_delay_costs.csv", index=True, header=True)

# ------------------MISSED CONNECTIONS---------------------------------------------

# Create an empty dictionary to hold the cost values for each aircraft
cost_values_mc_dict = {}

# Loop through each aircraft and its corresponding 80% seats value
for ac_type, seats in zip(aircraft, seats_80_percent):
    # Apply the get_cost_values function to each aircraft and its seats
    cost_values_mc_dict[ac_type] = get_cost_values(ac_type, seats, missed_connections=True)

# Now, transform this dictionary into a pandas DataFrame for a tabular view
# Each key (aircraft type) becomes a row, and the columns will be the delays
delays = [5, 10, 15, 30, 45, 60, 90, 120, 240, 300]  # Delays as column headers
costs_mc_df = pd.DataFrame.from_dict(cost_values_mc_dict, orient='index', columns=delays)

# Display the DataFrame (optional, depending on use case)
print(costs_mc_df)
costs_mc_df.to_csv("aircraft_delay_costs_mc.csv", index=True, header=True)
