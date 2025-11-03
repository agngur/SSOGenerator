class Sun:
    def __init__(self, name=None, mass=None, radius=None, luminosity=None):
        """
        Instantiates the Sun class.

        :param mass:
            The mass of the Sun in kg (or Solar Masses).
        :param radius:
            The radius of the Sun in AU.
        :param luminosity:
            The Sun's luminosity in ??.
        """

        self. mass = mass
        self.radius = radius
        self.luminosity = luminosity

    def __str__(self):
        """
        Print information about a Sun object.
        """
        if self.name is not None:
            print("Star's name: %s" % name)
        if self.mass is not None:
            print("Star's mass: %.2f Mo" % mass)
        if self.radius is not None:
            print("Star's radius: %.2f AU" % radius)
        if self.name is not None:
            print("Star's luminosity: %.2f" % luminosity)