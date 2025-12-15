from .satellite import Satellite
from .earth import Earth


class SatelliteSystem:
    """Implements a SatelliteSystem class which consists of one central body - an Earth and a collection of - at least one - (artificial) satellites.

    :param earth:
        the Earth.
    :param satellites:
        collection of Satellites.

    Instance variables
        - sun: The sun.
        - satellites: The list of Satellites.

    """

    def __init__(self, earth, satellites):
        """Initializes a satellite system."""

        # check if variable earth is a Earth-type object.
        if isinstance(earth, Earth):
            self.earth = Earth
        else:
            raise TypeError("SSOGenerator: no Earth provided.")

        # check if variable satellites is a list of (Satellite-type) objects.
        if isinstance(satellites, list):
            self.satellites = satellites
        else:
            raise TypeError("SSOGenerator: no valid satellites provided.")


    def __str__(self):
        """Print information about the system with provided satellites."""
        text = (
            "The satellite system consists of one central body and %d satellites.\n\n"
            % len(self.satellites)
        )
        text += self.earth.__str__() + "\n"
        for sat in self.satellites:
            if sat.name is not None:
                text += sat.name
        return text