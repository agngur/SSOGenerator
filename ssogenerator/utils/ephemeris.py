import numpy as np
import pandas as pd
# from skyfield import ??


class TLE:

    def __init__(self, tle0=None, tle1=None, tle2=None):
        """
        Instantiates the TLE class.

        :param tle0:
            The TLE's 0 line.
        :param tle0:
            The TLE's 0 line.
        :param tle0:
            The TLE's 0 line.
        """

    self.tle0 = tle0
    self.tle1 = tle1
    self.tle2 = tle2

    # todo: print NORAD IDs from TLE
    # todo: estimate and print the epoch of TLEs
    # todo: validate TLE's format
    # *todo: validate TLE's checksums ?

    def __str__(self):
        # print
        pass

    def validate(self):
        """
        Function validating provided by user TLEs
        """
        pass

    def propagate(self, epochs):
        """
        Function propagating Two Line Elements set for given list of UTC epochs.
        It returns pandas DataFrame with pairs: epoch, X_pos, Y_pos, Z_pos
        in Earth Centered Earth Fixed reference system.
        """
        pass


def get_latest_tle(norad_id):
    # do: download latest TLE from Celestrak
    pass
