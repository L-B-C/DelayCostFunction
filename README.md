# DelayCostFunction
Primary tactical gate-to-gate flight delay cost software simulator

## Reference Documents

In the development of this project, which aims at estimating flight delay costs, three documents have been instrumental in ensuring the consistency, relevance, and comprehensiveness of the integrated cost values. These documents provide valuable insights and data on delay costs within the European aviation sector and have shaped the functionalities included in the project:

1. **Evaluating The True Cost To Airlines Of One Minute Of Airborne Or Ground Delay (2004)**: 
   Commissioned by the Performance Review Commission to the University of Westminster - Transport Studies Group, this report offers a foundational understanding of the diverse impacts of delays, including a range of cost components. It served as the initial step for in-depth analysis of delay costs.
   [View Document](https://www.eurocontrol.int/sites/default/files/field_tabs/content/documents/single-sky/pru/publications/other/cost-of-delay.pdf)

2. **European Airline Delay Cost Reference Values (2015)**: 
   Produced by the University of Westminster, this report examines specific airline delay costs, presenting reference values for the European aviation context. It is key to understanding the economic effects of delays on airlines operating in Europe, offering detailed insights into cost variations under different scenarios.
   [View Document](https://www.eurocontrol.int/sites/default/files/publication/files/european-airline-delay-cost-reference-values-final-report-4-1.pdf)

3. **BEACON SESAR's Industry Briefing on Updates to the European Cost of Delay (2021)**: 
   This document provides updates on the cost of delay with the latest reference values dated 2019, reflecting the state of the aviation industry just before the pandemic. It is especially significant as it offers the most recent values for delay costs, ensuring that the cost estimations in the software are based on the most current and applicable data.
   [View Document](https://www.beacon-sesar.eu/wp-content/uploads/2022/10/893100-BEACON-D3.2-Industry-briefing-on-updates-to-the-European-cost-of-delay-V.01.01.00-1.pdf)

## Input Parameters

The `get_tactical_delay_costs` function calculates the cost of delay for a specific flight based on various parameters. Below are the details of each parameter:

- `aircraft_type` (str, required): The aircraft's ICAO code.
  
- `flight_phase_input` (str, required): The phase of the flight. Can be `AT_GATE`, `TAXI`, or `EN_ROUTE`.

- `passengers` (int or str, optional): The actual number of passengers on board as integeger (if not provided, a generic cost per passenger is generated) or passenger load scenario as string, it can be `low` (65% capacity), `base` (80% capacity, most common), or `high` (95% capacity). For wide-body aircraft, capacity is set to 85%.

- `is_low_cost_airline` (bool, optional): Set to `true` if the flight is considered low-cost.

- `flight_length` (float, optional): Length of the flight in kilometers, used to calculate the type of haul.

- `origin_airport` (str, optional): ICAO code of the departure airport.

- `destination_airport` (str, optional): ICAO code of the arrival airport.

- `curfew_violated` (bool, optional): Set to `true` if a curfew has been violated.

- `curfew_costs_exact_value` (float, optional): Total cost of curfew violation in EUR.

- `crew_costs` (float or str, optional): Costs for the entire crew (pilots and cabin crew) in EUR/min as float or string for crew cost scenario, which can be `low`, `base`, or `high`.

- `maintenance_costs` (float or str, optional): Directly provided maintenance costs in EUR/min (float) or string representing maintenance cost scenario, which can be `low`, `base`, or `high`.

- `fuel_costs` (float or str, optional): Directly provided fuel costs in EUR/min (float) or string representing fuel cost scenario. NOTE: Fuel costs are currently unavailable for calculation.


- `missed_connection_passengers` (List[Tuple], optional): List of tuples representing passengers who may miss connections. Each tuple contains the delay threshold and the perceived delay at the final destination.
  
- `curfew` (Union[Tuple[float, int], float], optional): Information regarding the curfew. If a tuple, it includes the curfew time and the number of passengers affected. 


Note: Parameters marked as "required" must be provided for the function to execute correctly.
 
## Output
Python dictionary containing the main lambda function: total of considered costs expressed in EUR as a function of delay and all the parameters used to calculate this function either provided as input or derived

## Cost Scenarios

In alignment with the reference values provided in the included models from the reports: Evaluating The True Cost To Airlines Of One Minute Of Airborne Or Ground Delay (2004), European Airline Delay Cost Reference Values (2015), and BEACON SESAR's Industry Briefing on Updates to the European Cost of Delay (2021), we categorize costs into three scenarios: 'LOW', 'BASE', and 'HIGH'. These scenarios encapsulate the potential cost spectrum faced by European carriers. The 'BASE' scenario is designed to reflect the typical case as closely as possible, representing the average situation. Cost scenarios can be adapted to depict specific types of airlines, influenced by their operational model and network configuration. For example, an airline operating long-distance flights with a modern fleet may have 'LOW' scenario maintenance expenses and 'BASE' scenario costs related to fleet, crew, and passengers.

## Flight Phases

The operational cycle of an aircraft includes several distinct phases, each representing a specific part of the flight process. These phases are:

- **AT-GATE**: This phase refers to the time when the aircraft is parked at the airport with engines off. Activities include boarding of passengers, loading of cargo, aircraft servicing, and departure preparations.

- **TAXI**: The TAXI phase covers the aircraft's ground movement under its own power, including moving from the gate to the runway before takeoff and from the runway to the gate after landing. It includes both taxi-out for departure and taxi-in after arrival.

- **EN-ROUTE**: This phase includes the part of the flight from takeoff until landing at the destination. It includes various segments such as lift-off, cruise, descent, pattern holding, and approach. This is the main segment where the aircraft is airborne and travels from the departure to the arrival airport.


## Considered Costs

### Crew Costs
The latest updates in reference values for crew costs reflect the evolving landscape of pilot and flight attendant compensation, capturing salary adjustments across the aviation industry from 2014 to 2019. These changes are based on informal sources and grey literature, indicating shifts such as modest pay increases for pilots and larger raises for flight attendants at the lower end of the salary scale. The model includes low, base, and high cost scenarios, with the low scenario assuming no additional cost for delays. Adjustments in base and high scenarios reflect the salary increases to maintain relevance and accuracy in assessing the financial impact of flight delays.

### Maintenance Costs
Maintenance costs vary significantly across different flight phases: AT-GATE, TAXI, and EN-ROUTE. The complexity and availability of these costs have been detailed, utilizing the latest available reference values to estimate the total cost of delay. Maintenance cost estimations take into account the overall trend in expenses, changes in fleet composition, and operational specifics, excluding anomalies from exceptional costs.

### Passenger Costs

#### Hard Costs
Passenger hard costs refer to direct expenses incurred due to passenger delays, these costs are calculate according to Regulation EC 261/2004. They also cover the cost of providing care to delayed passengers, such as meals, refreshments, and accommodations. Hard costs are strictly regulated and quantifiable, with specific thresholds set for different delay intervals. These costs directly impact an airline's financials and are typically non-negotiable due to regulatory requirements.

#### Soft Costs
Passenger soft costs, on the other hand, represent indirect or intangible expenses associated with delays. These include potential loss of revenue from dissatisfied customers who may choose alternative airlines in the future or the lost value from passengers who cancel their trips altogether due to delays. Soft costs also include the negative impact on airline reputation and passenger loyalty, which can indirectly affect future revenue. Unlike hard costs, soft costs are more challenging to quantify and vary widely among airlines and specific incidents. They reflect broader, long-term financial impacts rather than immediate expenses.

### Fuel Costs
Incorporating accurate fuel costs presents challenges due to diverse aircraft operations, varied fuel purchasing strategies, and differences in fuel consumption across flight phases. The software allows users to input fuel costs directly, accommodating specific operational costs and ensuring the most accurate and current fuel expenses are reflected. Users with access to BADA3 license can use it to compute average fuel consumptions for different aircraft at different phases, use fuel cost value according to the airline fuel buying strategy considered and calculate the resulting fuel costs. \
In this project for the moment fuel costs at gate are not considered (APU and/or engine usage at gate not modelled)

### Curfew Costs
Curfew cost estimations are complicated by varying airport regulations and the dynamic nature of these rules. The software design allows users to input known curfew costs directly, accommodating the lack of a universal model for curfew cost estimation but ensuring flexibility and relevance in analyses of curfew breaches expenses.

## Reference Code

The design of the software has been significantly influenced by a thorough analysis of two main resources:

1. **Cost Models**: This source code  focuses on quantifying the costs of delays in aviation. The analysis of this model has been crucial in understanding different approaches to estimate delay costs within the aviation industry. [View the Cost Models code on GitHub](https://github.com/andygaspar/CostModels).

2. **Mercury**: An open-source platform developed by the University of Westminster - ATM Research Group serves as a tool for the evaluation of air transport mobility and has been instrumental in providing insights into aviation industry concepts and mechanisms. [View the Mercury project on GitHub](https://github.com/UoW-ATM/Mercury/).
[Read the Mercury article](https://westminsterresearch.westminster.ac.uk/item/w7012/mercury-an-open-source-platform-for-the-evaluation-of-air-transport-mobility).

These resources have been invaluable in shaping the methodologies and functionalities integrated into the developed software, offering a comprehensive understanding of delay costs and aviation dynamics.

## Reference Data
Data from the Mercury project was used \
[most up-to-date dataset Mercury](https://zenodo.org/records/10246302) \
[dataset Mercury V3](https://zenodo.org/records/10222526) 


