"""
Unit tests for Satellite class
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
from ssogenerator.satellite import Satellite
from ssogenerator.utils.ephemeris import TLE


class TestSatellite:
    """Test suite for Satellite class"""
    
    @pytest.fixture
    def iss_tle(self):
        """ISS TLE fixture"""
        return TLE(
            'ISS (ZARYA)',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        )
    
    @pytest.fixture
    def gps_tle(self):
        """GPS satellite TLE fixture"""
        return TLE(
            'GPS BIIR-2',
            '1 24876U 97035A   26032.51426829 -.00000023  00000+0  00000+0 0  9999',
            '2 24876  55.4567 234.5678 0123456  12.3456  45.6789  2.00561234567890'
        )
    
    @pytest.fixture
    def iss_satellite(self, iss_tle):
        """ISS Satellite object fixture"""
        return Satellite(
            name="ISS",
            tle_data=iss_tle,
            norad_id="25544",
            sat_type="Space Station",
            status="operational",
            mass=419700,
            rcs=481.801
        )
    
    def test_satellite_initialization(self, iss_satellite, iss_tle):
        """Test satellite initialization"""
        assert iss_satellite.name == "ISS"
        assert iss_satellite.norad_id == "25544"
        assert iss_satellite.sat_type == "Space Station"
        assert iss_satellite.status == "operational"
        assert iss_satellite.mass == 419700
        assert iss_satellite.rcs == 481.801
        assert iss_satellite.tle_line1 == iss_tle.tle1
        assert iss_satellite.tle_line2 == iss_tle.tle2
    
    def test_orbital_parameters_extraction(self, iss_satellite):
        """Test extraction of orbital parameters from TLE"""
        # ISS typical values
        assert 50 < iss_satellite.inclination < 53  # degrees
        assert 0 < iss_satellite.eccentricity < 0.01
        assert 15 < iss_satellite.mean_motion < 16  # rev/day
        assert 0 <= iss_satellite.raan < 360
        assert 0 <= iss_satellite.arg_perigee < 360
        assert 0 <= iss_satellite.mean_anomaly < 360
    
    def test_semi_major_axis_calculation(self, iss_satellite):
        """Test semi-major axis calculation from mean motion"""
        # ISS altitude should be around 400-450 km
        altitude = iss_satellite.semi_major_axis - 6378.137
        assert 390 < altitude < 470  # km
    
    def test_orbital_period(self, iss_satellite, gps_tle):
        """Test orbital period calculation"""
        # ISS period should be around 90 minutes
        iss_period = iss_satellite.get_orbital_period()
        assert 88 < iss_period < 95
        
        # GPS period should be around 12 hours (720 minutes)
        gps_sat = Satellite("GPS", gps_tle)
        gps_period = gps_sat.get_orbital_period()
        assert 700 < gps_period < 740
    
    def test_propagation_eci(self, iss_satellite):
        """Test orbit propagation in ECI frame"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        duration_hours = 2
        step_minutes = 10
        
        iss_satellite.propagate(start_time, duration_hours, step_minutes, frame='eci')
        
        # Check that positions were calculated
        assert len(iss_satellite.positions_eci) > 0
        assert len(iss_satellite.velocities) > 0
        assert len(iss_satellite.times) > 0
        
        # Check shapes
        num_steps = int(duration_hours * 60 / step_minutes) + 1
        assert len(iss_satellite.positions_eci) == num_steps
        assert iss_satellite.positions_eci.shape == (num_steps, 3)
        assert iss_satellite.velocities.shape == (num_steps, 3)
    
    def test_propagation_ecef(self, iss_satellite):
        """Test orbit propagation in ECEF frame"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        
        iss_satellite.propagate(start_time, duration_hours=1, 
                               step_minutes=10, frame='ecef')
        
        # Check ECEF positions were calculated
        assert len(iss_satellite.positions_ecef) > 0
        assert len(iss_satellite.positions_eci) > 0
    
    def test_position_magnitudes(self, iss_satellite):
        """Test that position magnitudes are reasonable"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        iss_satellite.propagate(start_time, duration_hours=1, step_minutes=10)
        
        # Calculate distances from Earth center
        distances = np.linalg.norm(iss_satellite.positions_eci, axis=1)
        
        # Should be around Earth radius + altitude (6378 + 420 km)
        assert np.all(distances > 6700)  # km
        assert np.all(distances < 6900)  # km
        
        # Check altitude consistency
        altitudes = distances - 6378.137
        assert np.all(altitudes > 390)
        assert np.all(altitudes < 470)
    
    def test_velocity_magnitudes(self, iss_satellite):
        """Test that velocity magnitudes are reasonable"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        iss_satellite.propagate(start_time, duration_hours=1, step_minutes=10)
        
        # Calculate velocity magnitudes
        speeds = np.linalg.norm(iss_satellite.velocities, axis=1)
        
        # ISS orbital velocity should be around 7.6-7.8 km/s
        assert np.all(speeds > 7.4)
        assert np.all(speeds < 8.0)
    
    def test_subpoints_calculation(self, iss_satellite):
        """Test ground track subpoint calculation"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        iss_satellite.propagate(start_time, duration_hours=1, step_minutes=10)
        
        # Check subpoints were calculated
        assert len(iss_satellite.subpoints) > 0
        
        # Check latitude and longitude bounds
        for subpoint in iss_satellite.subpoints:
            lat = subpoint[0].degrees
            lon = subpoint[1].degrees
            
            # Latitude should be within ISS inclination (±51.6°)
            assert -52 <= lat <= 52
            
            # Longitude should be -180 to 180
            assert -180 <= lon <= 180
    
    def test_time_progression(self, iss_satellite):
        """Test that times progress correctly"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        step_minutes = 5
        duration_hours = 1
        
        iss_satellite.propagate(start_time, duration_hours, step_minutes)
        
        # Check first and last times
        assert iss_satellite.times[0] == start_time
        expected_end = start_time + timedelta(hours=duration_hours)
        assert iss_satellite.times[-1] == expected_end
        
        # Check time step consistency
        for i in range(len(iss_satellite.times) - 1):
            dt = (iss_satellite.times[i+1] - iss_satellite.times[i]).total_seconds()
            assert abs(dt - step_minutes * 60) < 1  # Within 1 second
    
    def test_multiple_propagations(self, iss_satellite):
        """Test that multiple propagations overwrite previous data"""
        start_time = datetime(2026, 2, 1, 0, 0, 0)
        
        # First propagation
        iss_satellite.propagate(start_time, duration_hours=1, step_minutes=10)
        num_points_1 = len(iss_satellite.positions_eci)
        
        # Second propagation with different parameters
        iss_satellite.propagate(start_time, duration_hours=2, step_minutes=15)
        num_points_2 = len(iss_satellite.positions_eci)
        
        # Should have different number of points
        assert num_points_1 != num_points_2
    
    def test_greenwich_mean_sidereal_time(self, iss_satellite):
        """Test GMST calculation"""
        # Test at J2000 epoch
        j2000 = datetime(2000, 1, 1, 12, 0, 0)
        gmst = iss_satellite._greenwich_mean_sidereal_time(j2000)
        
        # GMST at J2000 should be around 280.46° (in radians)
        expected_gmst = np.radians(280.46061837)
        assert abs(gmst - expected_gmst) < 0.01  # radians
    
    def test_rotation_matrix_z(self, iss_satellite):
        """Test Z-axis rotation matrix"""
        angle = np.pi / 4  # 45 degrees
        R = iss_satellite._rotation_matrix_z(angle)
        
        # Check it's a valid rotation matrix
        # R^T * R should be identity
        identity = R.T @ R
        assert np.allclose(identity, np.eye(3))
        
        # Determinant should be 1
        assert np.isclose(np.linalg.det(R), 1.0)
        
        # Test rotation of unit vector
        v = np.array([1, 0, 0])
        v_rotated = R @ v
        expected = np.array([np.cos(angle), np.sin(angle), 0])
        assert np.allclose(v_rotated, expected)
    
    def test_string_representation(self, iss_satellite):
        """Test __str__ method"""
        string_repr = str(iss_satellite)
        
        # Should contain key information
        assert "25544" in string_repr  # NORAD ID
        assert "operational" in string_repr.lower()
        assert "space station" in string_repr.lower()
        assert "km" in string_repr  # Altitude units
        assert "°" in string_repr or "degrees" in string_repr  # Inclination
    
    def test_high_eccentricity_orbit(self):
        """Test satellite with high eccentricity (Molniya-type)"""
        molniya_tle = TLE(
            'MOLNIYA 1-93',
            '1 25485U 98051A   26032.12345678  .00000123  00000+0  12345-3 0  9998',
            '2 25485  63.1234 123.4567 0.7234567 123.4567 234.5678  2.00561234567890'
        )
        
        sat = Satellite("MOLNIYA", molniya_tle)
        
        # High eccentricity orbit
        assert sat.eccentricity > 0.7
        
        # Period should be around 12 hours
        assert 700 < sat.get_orbital_period() < 740
    
    def test_geostationary_orbit(self):
        """Test GEO satellite characteristics"""
        geo_tle = TLE(
            'APPLE',
            '1 12545U 81057B   26032.13894835 -.00000250  00000+0  00000+0 0  9998',
            '2 12545   7.3448 297.9013 0022532 231.2845 340.6936  1.00050650121029'
        )
        
        sat = Satellite("APPLE", geo_tle)
        
        # GEO altitude should be around 35,786 km
        altitude = sat.semi_major_axis - 6378.137
        assert 35000 < altitude < 36500
        
        # Period should be around 24 hours (1436 minutes)
        assert 1400 < sat.get_orbital_period() < 1470
        
        # Low inclination
        assert sat.inclination < 15


class TestSatelliteEdgeCases:
    """Test edge cases and error handling"""
    
    def test_short_propagation(self):
        """Test very short propagation duration"""
        tle = TLE(
            'TEST',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        )
        sat = Satellite("TEST", tle)
        
        # Propagate for just 1 minute
        start = datetime(2026, 2, 1, 0, 0, 0)
        sat.propagate(start, duration_hours=0.0167, step_minutes=1)
        
        # Should have at least 2 points
        assert len(sat.positions_eci) >= 2
    
    def test_large_time_step(self):
        """Test propagation with large time step"""
        tle = TLE(
            'TEST',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        )
        sat = Satellite("TEST", tle)
        
        # Large time step (1 hour)
        start = datetime(2026, 2, 1, 0, 0, 0)
        sat.propagate(start, duration_hours=24, step_minutes=60)
        
        # Should have 25 points (0, 1, 2, ..., 24 hours)
        assert len(sat.positions_eci) == 25


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
