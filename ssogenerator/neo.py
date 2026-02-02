class Neo:
    def __init__(self, name=None, radius=None):
        """
        Instantiates the Near Eeart Object (NEO) class - to be dev in future!

        :param mpc_ephem:
            The MPC ephemeris.
        :param name:
            The NEO name to display.
        """

        self.name = name
        self.mpc_ephem = radius

    def __str__(self):
        """
        Print information about a NEO object.
        """
        if self.name is not None:
            print("NEO object's name: %s" % name)
        if self.mpc_ephem is not None:
            print("MPC ephemeris is as follows" % mpc_ephem)
