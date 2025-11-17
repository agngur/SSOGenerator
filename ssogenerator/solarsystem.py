from sun import Sun
from planet import Planet

class SolarSystem:
    def __init__(self, sun=None, planets=None):
        """
        Instantiates a SolarSystem

        :param sun:
            the Sun object.
        :param planets:
            a list of planets.
        """

        self.sun = sun
        if len(self.sun) != 1:
            print
        self.planets = planets

    def __str__(self):
        """
        Print information about a SolarSystem object.
        """
        text = ""
        if self.star is not None:
            text += "Star's name: %s\n" % self.name
        if self.planets is not None:
            text += "Planet's list: %.2f Mo\n" % self.mass
            
        self.mass = mass
        self.planets = radius
        
        return text
        
    def plot_2d(self):
        """
        Plot 2D model of Solar System.
        """
        pass
        