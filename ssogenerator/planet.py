class Planet:
    def __init__(self, name=None, mass=None, radius=None, semi_major_axis=None, inclination=None, eccentricity=None, argument_periapsis=None, ascnode_longitude=None):
        """
        Instantiates the planet class.
        Let's assume we have perfectly Keplerian orbit.

        :param name:
            The planet's name.
        :param mass:
            The mass of the planet in kg (or Solar Masses).
        :param radius:
            The radius of the planet in AU.
        :param semi_major_axis:
            The planet's orbit semi major axis in AU.
        :param inclination:
            The planet's orbit inclination (relative to Solar System orbital plane) in deg (only matter in 3D). 
        :param eccentricity:
            The planet's orbit eccentricity (0-1); 0-circular, 1(and above)-hyperbolic.
        :param argument_periapsis:
            The planet's orbit argument of periapsis (OMEGA).
        :param ascnode_longitude:
            The planet's orbit longitude of the ascending node (omega) (only matter in 3D).
        """

        self.name = name
        self.mass = mass
        self.radius = radius
        self.semi_major_axis = semi_major_axis
        self.inclination = inclination
        self.eccentricity = eccentricity
        self.argument_periapsis = argument_periapsis
        self.ascnode_longitude = ascnode_longitude

    def __str__(self):
        """
        Print information about a Planet object.
        """
        text = ""
        if self.name is not None:
            text += "Planet's name: %s\n" % self.name
        if self.mass is not None:
            text += "Planet's mass: %.2f Mo\n" % self.mass
        if self.radius is not None:
            text += "Planet's radius: %.2f AU\n" % self.radius
        if self.semi_major_axis is not None:
            text += "Planet's orbit semi major axis (a): %.2f \n" % self.semi_major_axis
        if self.inclination is not None:
            text += "Planet's orbit inclination (a): %.2f \n" % self.inclination
        if self.eccentricity is not None:
            text += "Planet's orbit eccentricity (e): %.4f \n" % self.eccentricity
        if self.argument_periapsis is not None:
            text += "Planet's orbit argument of periapsis (OMEGA): %.2f \n" % self.argument_periapsis
        if self.ascnode_longitude is not None:
            text += "Planet's orbit longitude of ascending node (omega): %.2f \n" % self.ascnode_longitude
            
        self.mass = mass
        self.radius = radius
        self.semi_major_axis = semi_major_axis
        self.inclination = inclination
        self.eccentricity = eccentricity
        self.argument_periapsis = argument_periapsis
        self.ascnode_longitude = ascnode_longitude
        
        return text