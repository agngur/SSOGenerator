import requests
from datetime import datetime, timedelta
from typing import Tuple

# from .cchecksum import tle_line_checksum
# This import works only with absolute path
from ssogenerator.utils.ctle_checksum import tleline_checksum


class TLE:
    """
    TLE class - orbital parameters (incl. validation of TLE format)
    """
    def __init__(self, tle0=None, tle1=None, tle2=None):
        """
        Instantiates the TLE class.

        :param tle0:
            The TLE's 0 line.
        :param tle1:
            The TLE's 1 line.
        :param tle2:
            The TLE's 2 line.
        :param verbose:
            The verbosity.
        """

        self.tle0 = tle0
        self.tle1 = tle1
        self.tle2 = tle2
        self.norad_id = self.get_noradid()
        self.cospar_id = self.get_cosparid()
        self.tle_epoch = self.get_tle_epoch()
        # TLE age in days
        self.tle_age = (datetime.today() - self.tle_epoch).total_seconds()/(3600*24)
        if self.validate_string() and self.validate_checksum():
            self.valid = True
        else:
            self.valid = False

    def __str__(self):
        """
        Print information about provided TLE set.
        """

        txt = ""
        if self.tle0 is not None:
            txt += "TLE 0 line and object name is: %s" % self.tle0
        if self.tle1 is not None:
            txt += "\nTLE 1st line is: %s" % self.tle1
        if self.tle2 is not None:
            txt += "\nTLE 2nd line is: %s" % self.tle2

        if self.validate_string():
            txt += "\nProvided TLE has valid format."

            # Reading NORAD ID
            norad_id = self.get_noradid()
            txt += "\nNORAD ID of provided object is %s" % norad_id
            
            # Reading COSPAR ID
            cospar_id = self.get_cosparid()
            txt += "\nCOSPAR ID of provided object is %s" % cospar_id

            # Reading TLE epoch
            tle_epoch = self.get_tle_epoch()
            tle_age = (datetime.today() - tle_epoch).total_seconds()/(3600*24)
            txt += "\nTLE reference epoch is %s" % tle_epoch.isoformat()
            txt += " and it is currently %.2f days old" % tle_age
            if tle_age > 3:
                txt += "\nWARNING (only): TLE is more than 3 days old. Use carefully!"

            # Validate checksums
            if self.validate_checksum():
                txt += "\nTLE checksums are correct."
        else:
            txt += "\nProvided TLE has invalid format."
        return txt

    def validate_string(self):
        """
        Function validating provided by user TLEs (simple)
        """
        if not isinstance(self.tle1, str) or not isinstance(self.tle2, str):
            raise ValueError(f"Invalid TLE - at least 1st and 2nd line \
                should be provided, 0 line is optional.\n \
                Provided TLE:{self.tle0}\n{self.tle1}\n{self.tle2}")
            return False
        else:
            if len(self.tle1) == 69 and len(self.tle2) == 69:
                return True
            else:
                raise ValueError(f"Invalid TLE - lengths of provided TLE lines are wrong: {len(self.tle1)} and {len(self.tle2)}")
                return False
                
    def validate_checksum(self, verbose=True):
        """
        Function validating provided by user TLEs (by checksum)
        """
        # TLE line should have 69 characters, and the last one is checksum.
        # validate line1, line2 separately
        # checksum1 = tle_line_checksum(self.tle1)
        # checksum2 = tle_line_checksum(self.tle2)
        validator = 0
        
        for tleline_i in [self.tle1, self.tle2]:
            # print(len(tleline_i), repr(tleline_i), tleline_i[-1])
            # print("LINE LEN:", len(tleline_i), "CONTENT:", repr(tleline_i))
            # print("ORDS:", [ord(c) for c in tleline_i])

            checksum_i = tleline_checksum(tleline_i)
            checksum_exp = int(tleline_i[-1])
            if checksum_i == checksum_exp:
                # Sorry, no idea how to divide these lines properly (f-string has its own issues) 
                if verbose:
                    print(f"[validate info] Calculated checksum matches: {checksum_i} (expected: {checksum_exp})")
                validator += 1
            else:
                if verbose:
                    print(f"[validate info] Calculated checksum does not match: {checksum_i} (expected: {checksum_exp})")

        # TLE are valid only if both checksums are valid
        if validator == 2:
            return True
        else:
            return False   
    
    def get_noradid(self):
        """
        Function reading NORAD ID from provided TLE
        """
        
        return str(int(self.tle2.split()[1]))

    def get_cosparid(self):
        """
        Function reading COSPAR ID from provided TLE
        """
        _year = self.tle1.split()[2][:2]
        launch_no = self.tle1.split()[2][2:]
        
        # first object in space was deployed in 1957 (1957-001A)
        year = "19"+_year if int(_year) >= 57 else "20"+_year 
        cospar_id = f"{year}-{launch_no}"
        # print("COSPAR ID is %s" % cospar_id)
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
        # tle_age = (datetime.today() - tle_date).total_seconds() / (3600*24) # days
        return tle_date

    
def get_latest_tle(norad_id: str) -> Tuple[str, str, str]:
    # do: download latest TLE from Celestrak/SpaceTrack/whatever and return in 3LE format
    """
    Get latest TLE from CelesTrak by NORAD ID

    :param norad_id:
        NORAD ID
    
    :return:
        Tuple of (name or tle_line0, tle_line1, tle_line2)
    """
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            if len(lines) >= 3:
                return lines[0].strip(), lines[1].strip(), lines[2].strip()
    except Exception as e:
        print(f"Error fetching TLE for {norad_id}: {e}")
    return None, None, None
