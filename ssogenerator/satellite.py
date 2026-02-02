import numpy as np
from datetime import datetime, timedelta
from skyfield.api import load, EarthSatellite, wgs84
from skyfield.toposlib import GeographicPosition
from typing import Optional
from ssogenerator.utils.ephemeris import TLE


class Satellite:
    """
    Satellite class with physical and orbital parameters from TLE
    """
    
    def __init__(self, name: str, tle_data: TLE, 
                 norad_id: Optional[str] = None,
                 sat_type: Optional[str] = None,
                 status: Optional[str] = None,
                 mass: Optional[float] = None,
                 rcs: Optional[float] = None):
        """
        Initialize the Satellite with TLE data
        
        :param name: 
            Satellite name
        :param tle: 
            TLE object
        :param norad_id: 
            NORAD catalog ID
        :param sat_type: 
            Type of satellite (i.e. from DISCOS)
        :param status: 
            Operational status (i.e. "operational","debris" - from DISCOS)
        :param mass: 
            Mass in kg (optional: not used currently)
        :param rcs: 
            Radar cross-section in m^2 (optional: not used currently)
        """
        
        self.name = name # or tle_data.tle0
        self.tle_line1 = tle_data.tle1
        self.tle_line2 = tle_data.tle2
        self.norad_id = norad_id or tle_data.norad_id
        self.sat_type = sat_type
        self.status = status
        self.mass = mass
        self.rcs = rcs
        
        # Create Skyfield satellite object
        ts = load.timescale()
        self.satellite = EarthSatellite(self.tle_line1, self.tle_line2, name, ts)
        
        # Orbital parameters extracted from TLE (as much as I can extract...)
        self.mean_motion = float(self.tle_line2[52:63])  # revolutions per day
        self.eccentricity = float('0.' + self.tle_line2[26:33])
        self.inclination = float(self.tle_line2[8:16])  # degrees
        self.raan = float(self.tle_line2[17:25])  # Right Ascension of Ascending Node (degrees)
        self.arg_perigee = float(self.tle_line2[34:42])  # Argument of perigee (degrees)
        self.mean_anomaly = float(self.tle_line2[43:51])  # degrees
        
        # Calculate semi-major axis
        n = self.mean_motion * 2 * np.pi / 86400  # Convertion to rad/s
        earth_mu = 398600.4418  # km^3/s^2 # constant
        self.semi_major_axis = (earth_mu / n**2)**(1/3)
        
        # Storage for propagated positions from Skyfield...
        self.positions_eci = []  # Earth-Centered Inertial frame
        self.positions_ecef = []  # Earth-Centered Earth-Fixed frame
        self.times = []
        self.velocities = []
        self.subpoints = []

    def __str__(self):
        """
        Print information about Satellite set.
        """
        txt = f"  - {self.name}"
        txt = f"\n    NORAD ID: {self.norad_id}"
        if self.status:
            txt += f"\n    Operational status: {self.status}"
        if self.sat_type:
            txt += f"\n    Satellite type: {self.sat_type}"
        if self.mass:
            txt += f"\n    Satellite mass: {self.mass}"
        if self.rcs:
            txt += f"\n    Satellite Radar Cross Section (RCS): {self.rcs}"
        txt += f"\n    Orbital altitude: {self.semi_major_axis - 6378.137:.2f} km"
        txt += f"\n    Inclination: {self.inclination:.2f}°"
        txt += f"\n    Orbital period: {self.get_orbital_period():.2f} minutes"
        txt += f"\n    Semi-major axis: {self.semi_major_axis:.2f} km"
        return txt

    def get_orbital_period(self) -> float:
        """Get orbital period in minutes"""
        return 1440.0 / self.mean_motion  # minutes

    def propagate(self, start_time: datetime, duration_hours=24.0, 
                  step_minutes=5.0, frame='eci'):
        """
        Propagate Satellite' Two Line Elements set for given UTC epochs since 
        start_time. It returns pandas DataFrame with pairs: 
        epoch, X_pos, Y_pos, Z_pos in ECI (GCRF-aligned) reference system.
        
        :params start_time: 
            Start time for propagation (datetime object)
        :param duration_hours: 
            Duration to propagate (hours)
        :param step_minutes: 
            Time step (minutes)
        :param frame: 
            Reference frame ('ecef' or 'eci', default 'eci')
        """
        ts = load.timescale()
        
        # Generate time array
        num_steps = int(duration_hours * 60 / step_minutes) + 1
        time_offsets = [timedelta(minutes=i*step_minutes) for i in range(num_steps)]
        
        self.times = []
        self.positions_eci = []
        self.positions_ecef = []
        self.velocities = []

        # UTC epochs for propagation...
        for offset in time_offsets:
            current_time = start_time + offset
            t = ts.utc(current_time.year, current_time.month, current_time.day,
                       current_time.hour, current_time.minute, current_time.second)
            
            # Get geocentric position (GCRF, aligned with ECI)
            geocentric = self.satellite.at(t)
            pos = geocentric.position.km
            vel = geocentric.velocity.km_per_s

            # Subpoints on Earth
            subpoint = wgs84.latlon_of(geocentric) # lat, lon 
            
            self.times.append(current_time)
            self.positions_eci.append(pos)
            self.velocities.append(vel)
            self.subpoints.append(subpoint)
            
            # Convert to ECEF if requested
            if frame == 'ecef':
                # Simple rotation
                gmst = self._greenwich_mean_sidereal_time(current_time)
                rotation_matrix = self._rotation_matrix_z(-gmst)
                pos_ecef = rotation_matrix @ pos
                self.positions_ecef.append(pos_ecef)
        
        self.positions_eci = np.array(self.positions_eci)
        if frame == 'ecef':
            self.positions_ecef = np.array(self.positions_ecef)
        self.velocities = np.array(self.velocities)
        self.subpoints = np.array(self.subpoints)
    
    def _greenwich_mean_sidereal_time(self, dt: datetime) -> float:
        """Calculate GMST in radians"""
        # Simplified GMST calculation
        j2000 = datetime(2000, 1, 1, 12, 0, 0)
        d = (dt - j2000).total_seconds() / 86400.0
        gmst = 280.46061837 + 360.98564736629 * d
        return np.radians(gmst % 360)
    
    def _rotation_matrix_z(self, angle: float) -> np.ndarray:
        """Rotation matrix around Z-axis"""
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
