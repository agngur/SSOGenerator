class Earth:
    def __init__(self, name=None, radius=None):
        """
        Instantiates the Earth class.

        :param radius:
            The radius of the Earth in km.
        :param name:
            The Earth's name to display.
        """

        self.name = name
        self.radius = radius

    def __str__(self):
        """
        Print information about an Earth object.
        """
        txt = ""
        if self.name is not None:
            txt += "Central object's name: %s" % self.name
        if self.radius is not None:
            txt += " and radius: %.2f km" % self.radius
        return txt
