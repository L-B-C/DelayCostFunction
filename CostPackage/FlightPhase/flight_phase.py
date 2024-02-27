# Flight phases considered to calculate the cost of delay are
# AT_GATE, TAXI, EN_ROUTE
class FlightPhaseError(Exception):
    def __init__(self, flight_phase: str):
        self.flight_phase = flight_phase
        self.message = "Invalid flight phase" + self.flight_phase + "USE: AT_GATE, EN_ROUTE, TAXI"

    def __repr__(self):
        return "Invalid flight phase" + self.flight_phase + "USE: AT_GATE, EN_ROUTE, TAXI"


def get_flight_phase(flight_phase: str):
    match flight_phase.upper():
        case "AT_GATE":
            return "AT_GATE"
        case "TAXI":
            return "TAXI"
        case "EN_ROUTE":
            return "EN_ROUTE"
        case _:
            return FlightPhaseError(flight_phase)

