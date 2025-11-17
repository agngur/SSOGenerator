class Sun:
    def __init__(self, name=None, mass=None, radius=None, luminosity=None):
        """
        Instantiates the Sun class.

        :param name:
            The star's (Sun) name.
        :param mass:
            The mass of the Sun in kg (or Solar Masses).
        :param radius:
            The radius of the Sun in AU.
        :param luminosity:
            The Sun's luminosity in ??.
        """

        self.name = name
        self.mass = mass
        self.radius = radius
        self.luminosity = luminosity

    def __str__(self):
        """
        Print information about a Sun object.
        """
        text = ""
        if self.name is not None:
            text += "Star's name: %s\n" % self.name
        if self.mass is not None:
            text += "Star's mass: %.2f Mo\n" % self.mass
        if self.radius is not None:
            text += "Star's radius: %.2f AU\n" % self.radius
        if self.name is not None:
            text += "Star's luminosity: %.2f \n" % self.luminosity
        return text