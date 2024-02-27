class ScenarioError(Exception):
    def __init__(self, scenario: str):
        self.scenario = scenario
        self.message = "Scenario " + self.scenario + " not found"

    def __repr__(self):
        return "Scenario " + self.scenario + " not found"


def get_scenario(scenario: str):
    match scenario.lower():
        case 'low':
            entry_scenario = 'LowScenario'
        case 'base':
            entry_scenario = 'BaseScenario'
        case 'high':
            entry_scenario = 'HighScenario'
        case _:
            raise ScenarioError(scenario)
    return entry_scenario
