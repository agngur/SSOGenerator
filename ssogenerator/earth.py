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
        if self.name is not None:
            print("Central object's name: %s" % name)
        if self.radius is not None:
            print("Central object's radius: %.2f km" % radius)