from .satellite import Satellite
from .earth import Earth
from ssogenerator.utils.ephemeris import TLE, get_latest_tle
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta

class SatelliteSystem:
    """Implements a SatelliteSystem class which consists of one central body - an Earth - and a collection of - at least one - (artificial) satellites.

    :param earth:
        the Earth.
    :param satellites:
        collection of Satellites.

    Instance variables
        - earth: The Earth.
        - satellites: The list of Satellites.

    """

    def __init__(self, earth: Earth):
        """Initializes a satellite system."""
        
        self.earth = earth
        self.satellites: List[Satellite] = []
        
        # check if variable earth is a Earth-type object.
        if isinstance(earth, Earth):
            self.earth = Earth
        else:
            raise TypeError("SSOGenerator: no Earth provided.")

    def __str__(self):
        """Print information about the system with provided satellites."""
        txt = (
            "The satellite system consists of one central body (Earth) and %d satellites.\n\n"
            % len(self.satellites)
        )
        txt += self.earth.__str__() + "\n"
        for sat in self.satellites:
            if sat.name is not None:
                txt += sat.name
        return txt

    def add_satellite(self, sat: Satellite, **kwargs):
        """Add satellite from Satellite object"""
        self.satellites.append(sat)
        return sat
    
    def add_satellite_from_tle(self, name: str, tles: list, **kwargs):
        """Add satellite from TLE data"""
        tle_data = TLE(tles[0], tles[1], tles[2])
        sat = Satellite(name, tle_data, **kwargs)
        self.satellites.append(sat)
        return sat

    def add_satellite_by_norad_id(self, norad_id: str, **kwargs):
        """Add satellite by fetching TLE from CelesTrak"""
        name, tle1, tle2 = get_latest_tle(norad_id)
        # Check whether TLEs are not None
        if tle1 and tle2:
            tles = [name, tle1, tle2]
            return self.add_satellite_from_tle(name, tles, norad_id=norad_id, **kwargs)
        else:
            print(f"Failed to fetch TLE for NORAD ID: {norad_id}")
            return None

    def propagate_all(self, start_time: Optional[datetime] = None, 
                     duration_hours=24, step_minutes=5, frame='eci'):
        """
        Propagate all satellites in collection
        
        :params start_time: 
            Start time (default: current time)
        :params duration_hours: 
            Duration to propagate (max 72 hours)
        :params step_minutes: 
            Time step in minutes
        :params frame: 
            Reference frame ('eci' or 'ecef', default: 'eci')
        """
        if duration_hours > 72:
            print("\nWARNING: Propagation period limited to 72 hours (3 days)")
            duration_hours = 72
        
        self.start_time = start_time or datetime.utcnow()
        self.duration_hours = duration_hours
        self.step_minutes = step_minutes
        self.reference_frame = frame
        
        print(f"\nPropagating {len(self.satellites)} satellites...")
        print(f"Start: {self.start_time}")
        print(f"Duration: {duration_hours} hours, Step: {step_minutes} minutes")
        print(f"Reference frame: {frame.upper()}")
        
        for i, sat in enumerate(self.satellites):
            print(f"  [{i+1}/{len(self.satellites)}] {sat.name}...")
            sat.propagate(self.start_time, duration_hours, step_minutes, frame)
    
    def find_closest_approaches(self, threshold_km=100.0):
        """
        Find closest approaches between satellites
        
        :params threshold_km: 
            Distance threshold in km
            
        :return:
            List of dictionaries with approach information: List[Dict]
        """
        approaches = []

        # Nonsense to estimate for single satellite...
        if len(self.satellites) < 2:
            return approaches
        
        # Ensure all satellites have been propagated
        if not all(len(sat.positions_eci) > 0 for sat in self.satellites):
            print("Not all satellites have been propagated. Run propagate_all() first.")
            return approaches
        
        print(f"\nFinding closest approaches (threshold: {threshold_km} km)...")
        
        # Check each pair of satellites
        for i in range(len(self.satellites)):
            for j in range(i+1, len(self.satellites)):
                sat1 = self.satellites[i]
                sat2 = self.satellites[j]
                
                # Calculate distances at each time step
                distances = np.linalg.norm(sat1.positions_eci - sat2.positions_eci, axis=1)
                min_distance = np.min(distances)
                min_idx = np.argmin(distances)
                
                if min_distance < threshold_km:
                    approaches.append({
                        'satellite1': sat1.name,
                        'satellite2': sat2.name,
                        'distance_km': min_distance,
                        'time': sat1.times[min_idx],
                        'position1': sat1.positions_eci[min_idx],
                        'position2': sat2.positions_eci[min_idx]
                    })
        
        # Sort by distance
        approaches.sort(key=lambda x: x['distance_km'])
        
        print(f"Found {len(approaches)} close approaches:")
        for app in approaches[:10]:  # Show only first 10
            print(f"  {app['satellite1']} <-> {app['satellite2']}: "
                  f"{app['distance_km']:.2f} km at {app['time']}")
        
        return approaches

    

# ---- Example usage ---- #

if __name__ == "__main__":

    print("Initializing Satellite System (Object) Generator!")
    # Create/Initiate the system
    earth = Earth(name="Earth", radius=6378.137)  # Equatorial radius in km 
    system = SatelliteSystem(earth)
    
    # Add satellites
    print("Adding satellites...")
    
    ## Three options to add satellite:
    # (1) add satellite directly by Satellite object
    # (2) add satellite by Norad ID (and then get TLE and construct Satellite object)
    # (3) add satellite by TLEs (if valid! from there get "name" (or random) 
    #     and construct Satellite object)
    
    ## ISS Zarya ==> 25544
    ## Hubble Space Telescope (HST) ==> 20580
    ## LEO YAM-3 ==> 48915
    ## Starlink-1094 ==> 44941
    ## GEO APPLE ==> 12545
    ## Galileo 6 (GSAT0202) ==> 40129
    
    ## Adding directly from TLE as a Satellite object
    random_tle = ['APPLE',
                  '1 12545U 81057B   26032.13894835 -.00000250  00000+0  00000+0 0  9998',
                  '2 12545   7.3448 297.9013 0022532 231.2845 340.6936  1.00050650121029']
    apple_tle = TLE(random_tle[0], random_tle[1], random_tle[2])
    apple_sat = Satellite(name="Apple", tle_data=apple_tle, norad_id="12545",
                          sat_type="geo", rcs=2.0)
    system.add_satellite(apple_sat)
    
    ## Adding from TLE...
    iss_tle = ['ISS (ZARYA)',
               '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
               '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710']
    system.add_satellite_from_tle(name="ISS", tles=iss_tle, status="operational", rcs=481.801)
    
    ## Adding by norad -> then download TLE
    sats_to_add = ["20580","44941","40129"]
    for sat_noradid in sats_to_add:
        system.add_satellite_by_norad_id(sat_noradid)
    
    # Propagate orbits
    start = datetime(2026, 2, 1, 0, 0, 0)
    system.propagate_all(start_time=start, duration_hours=12, step_minutes=1, frame='eci')
    
    # Find close approaches
    approaches = system.find_closest_approaches(threshold_km=500)
    
    print("\nSimulator ready!")
    print(f"Total satellites: {len(system.satellites)}")
    for sat in system.satellites:
        print(f"  - {sat}")