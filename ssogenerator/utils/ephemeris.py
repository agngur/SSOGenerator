import numpy as np
import pandas as pd
from datetime import datetime
from utils.cchecksum import tle_line_checksum
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
        #if isinstance(self.tle1, str):
        #    print("Object's name: %s" % name)
        # todo: estimate and print the epoch of TLEs
        # todo: validate TLE's format
        # *todo: validate TLE's checksums ?

    def __str__(self):
        """
        Print information about provided TLE set.
        """
        if self.tle0 is not None:
            print("TLE 0 line and object name is: %s" % self.tle0)
        if self.tle1 is not None:
            print("TLE 1st line is: %s" % self.tle1)
        if self.tle2 is not None:
            print("TLE 2nd line is: %s" % self.tle2)

        if self.validate_string():
            print("Provided TLE has valid format.")

            # Reading NORAD ID
            norad_id = self.get_noradid()
            print("NORAD ID of provided object is %s" % norad_id)

            # Reading TLE epoch
            tle_epoch = self.get_tle_epoch()
            tle_age = (datetime.today() - tle_age).total_seconds() / (3600*24) # in days
            txt = "TLE reference epoch is %s" % tle_epoch.isoformat()
            txt += "and it is currently %.2f days old" % tle_age
            print(txt)

            # Validate checksums
            if self.validate_checksum():
                # DO
                pass
        else:
            print("Provided TLE has invalid format.")

    def validate_string(self):
        """
        Function validating provided by user TLEs (simple)
        """
        if not isinstance(self.tle1, str) or not isinstance(self.tle2, str):
            raise ValueError(f"Invalid TLE - at least 1st and 2nd line should be provided, 0 line is optional.\n \
                Provided TLE:{self.tle0}\n{self.tle1}\n{self.tle2}")
            return False
        else:
            if len(self.tle1) == 69 and len(self.tle2) == 69:
                return True
            else:
                raise ValueError(f"Invalid TLE - lengths of provided TLE lines are wrong: {len(self.tle1)} and {len(self.tle2)}")
                return False
                

    def validate_checksum(self):
        """
        Function validating provided by user TLEs (by checksum)
        """
        # TLE line should have 69 characters, and the last one is checksum.
        # validate line1, line2 separately
        
        #checksum1 = tle_line_checksum(self.tle1)
        #checksum2 = tle_line_checksum(self.tle2)
        validator = 0
        
        for tleline_i in [self.tle1, self.tle2]:
            checksum_i = tle_line_checksum(tleline_i)
            checksum_exp = int(tleline_i[-1])
            if checksum_i == checksum_exp:
                print(f"Calculated checksum matches: {checksum_i} (expected: {checksum_exp})")
                validator += 1
            else:
                print(f"Calculated checksum does not match: {checksum_i} (expected: {checksum_exp})")

        # TLE are valid only if both checksums are valid
        if validator == 2:
            return True
        else:
            return False

    
    def get_noradid(self):
        """
        Function reading NORAD ID from provided TLE
        """
        return str(int(self.tle1.split()[1]))

    def get_cosparid(self):
        """
        Function reading COSPAR ID from provided TLE
        """
        _year = self.tle1.split()[2][:2]
        launch_no = self.tle1.split()[2][2:]
        
        # first object in space was deployed in 1957 (1957-001A)
        year = "19"+_year if int(_year) >= 57 else "20"+_year 
        cospar_id = f"{year}-{launch_no}"
        #print("COSPAR ID is %s" % cospar_id)
        return cospar_id

    
    def get_tle_epoch(self):
        """
        Function reading reference epoch from provided TLE
        """
        # first object in space was deployed in 1957 (1957-001A)
        # there will be no TLEs older than that (for sure)
        _year = self.tle1.split()[3][:2]
        doy = self.tle1.split()[3][2:]
        year = "19"+_year if int(_year) >= 57 else "20"+_year 
    
        # so we get 1st of January of a given year and then add DOYs-1
        tle_date = datetime(int(year), 1, 1) + timedelta(float(doy) - 1)
        #tle_age = (datetime.today() - tle_date).total_seconds() / (3600*24) # days
        
        return tle_date

    
    def propagate(self, epochs):
        """
        Function propagating Two Line Elements set for given list of UTC epochs.
        It returns pandas DataFrame with pairs: epoch, X_pos, Y_pos, Z_pos
        in Earth Centered Earth Fixed reference system.
        """
        pass


def get_latest_tle(norad_id):
    # do: download latest TLE from Celestrak/SpaceTrack/whatever
    pass


