class HaulError(Exception):
    def __init__(self, haul: float):
        self.haul = haul
        self.message = "Flight length: " + str(self.haul) + "km is invalid." + ("The flight length must be greater "
                                                                                "than zero")

    def __repr__(self):
        return "Haul: " + str(self.haul) + " invalid." + " Haul value must be greater than zero"


# Distance (length) expressed in km
# ATTENTION: definition of haul varies by carrier, organization and country
# also very short haul exists for flights shorter than 500km
# but, it will be considered as short haul,
# HAUL DEFINITION based on flight length according to Eurocontrol is used
def get_haul(flight_length: float) -> str:
    if 0 < flight_length <= 1500:
        return "ShortHaul"
    elif flight_length <= 3500:
        return "MediumHaul"
    elif flight_length > 3500:
        return "LongHaul"
    else:
        raise HaulError(flight_length)
