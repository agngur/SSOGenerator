"""
Unit tests for SatelliteSystem class
"""

import pytest
import numpy as np
from datetime import datetime
from ssogenerator.system import SatelliteSystem
from ssogenerator.earth import Earth
from ssogenerator.satellite import Satellite
from ssogenerator.utils.ephemeris import TLE


class TestSatelliteSystem:
    """Test suite for SatelliteSystem class"""
    
    @pytest.fixture
    def earth(self):
        """Earth fixture"""
        return Earth(name="Earth", radius=6378.137)
    
    @pytest.fixture
    def system(self, earth):
        """Empty SatelliteSystem fixture"""
        return SatelliteSystem(earth)
    
    @pytest.fixture
    def iss_tle_list(self):
        """ISS TLE as list"""
        return [
            'ISS (ZARYA)',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        ]
    
    @pytest.fixture
    def populated_system(self, system, iss_tle_list):
        """System with satellites"""
        system.add_satellite_from_tle("ISS", iss_tle_list)
        
        # Add more satellites
        hst_tle = [
            'HST',
            '1 20580U 90037B   26032.51426829  .00001234  00000+0  12345-3 0  9998',
            '2 20580  28.4690 123.4567 0002813  45.6789  12.3456 15.09876543123456'
        ]
        system.add_satellite_from_tle("HST", hst_tle)
        
        return system
    
    def test_system_initialization(self, earth):
        """Test system initialization"""
        system = SatelliteSystem(earth)
        
        assert system.earth is not None
        assert len(system.satellites) == 0
        assert isinstance(system.satellites, list)
    
    def test_invalid_earth_type(self):
        """Test that invalid Earth type raises error"""
        with pytest.raises(TypeError):
            system = SatelliteSystem("not an Earth object")
    
    def test_add_satellite_from_object(self, system):
        """Test adding satellite from Satellite object"""
        tle = TLE(
            'TEST',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        )
        sat = Satellite("TEST", tle)
        
        result = system.add_satellite(sat)
        
        assert len(system.satellites) == 1
        assert system.satellites[0] is sat
        assert result is sat
    
    def test_add_satellite_from_tle(self, system, iss_tle_list):
        """Test adding satellite from TLE lines"""
        result = system.add_satellite_from_tle("ISS", iss_tle_list,
                                              status="operational",
                                              rcs=481.801)
        
        assert len(system.satellites) == 1
        assert system.satellites[0].name == "ISS"
        assert system.satellites[0].status == "operational"
        assert system.satellites[0].rcs == 481.801
        assert result is not None
    
    def test_add_multiple_satellites(self, populated_system):
        """Test adding multiple satellites"""
        assert len(populated_system.satellites) == 2
        
        names = [sat.name for sat in populated_system.satellites]
        assert "ISS" in names
        assert "HST" in names
    
    def test_propagate_all(self, populated_system):
        """Test propagating all satellites"""
        start = datetime(2026, 2, 1, 0, 0, 0)
        duration = 6
        step = 10
        
        populated_system.propagate_all(
            start_time=start,
            duration_hours=duration,
            step_minutes=step,
            frame='eci'
        )
        
        # Check all satellites were propagated
        for sat in populated_system.satellites:
            assert len(sat.positions_eci) > 0
            assert len(sat.velocities) > 0
            assert len(sat.times) > 0
            
            # Check number of time steps
            expected_steps = int(duration * 60 / step) + 1
            assert len(sat.positions_eci) == expected_steps
    
    def test_propagate_all_ecef(self, populated_system):
        """Test propagation in ECEF frame"""
        start = datetime(2026, 2, 1, 0, 0, 0)
        
        populated_system.propagate_all(
            start_time=start,
            duration_hours=3,
            step_minutes=15,
            frame='ecef'
        )
        
        # Check ECEF positions were calculated
        for sat in populated_system.satellites:
            assert len(sat.positions_ecef) > 0
    
    def test_propagate_all_duration_limit(self, populated_system, capsys):
        """Test that duration is limited to 72 hours"""
        start = datetime(2026, 2, 1, 0, 0, 0)
        
        populated_system.propagate_all(
            start_time=start,
            duration_hours=100,  # Exceeds limit
            step_minutes=60
        )
        
        # Check warning was printed
        captured = capsys.readouterr()
        assert "WARNING" in captured.out or "limited" in captured.out.lower()
        
        # Check duration was actually limited
        assert populated_system.duration_hours == 72
    
    def test_find_closest_approaches_no_satellites(self, system):
        """Test closest approaches with no satellites"""
        approaches = system.find_closest_approaches(threshold_km=100)
        assert len(approaches) == 0
    
    def test_find_closest_approaches_one_satellite(self, system, iss_tle_list):
        """Test closest approaches with only one satellite"""
        system.add_satellite_from_tle("ISS", iss_tle_list)
        approaches = system.find_closest_approaches(threshold_km=100)
        assert len(approaches) == 0
    
    def test_find_closest_approaches_unpropagated(self, populated_system, capsys):
        """Test closest approaches without propagation"""
        # Don't propagate
        approaches = populated_system.find_closest_approaches(threshold_km=100)
        
        # Should return empty and print warning
        assert len(approaches) == 0
        captured = capsys.readouterr()
        assert "propagated" in captured.out.lower()
    
    def test_find_closest_approaches(self, populated_system):
        """Test finding closest approaches"""
        start = datetime(2026, 2, 1, 0, 0, 0)
        populated_system.propagate_all(start, duration_hours=12, step_minutes=10)
        
        # Use large threshold to ensure we find something
        approaches = populated_system.find_closest_approaches(threshold_km=10000)
        
        # Should find approaches between ISS and HST
        if len(approaches) > 0:
            approach = approaches[0]
            
            # Check structure
            assert 'satellite1' in approach
            assert 'satellite2' in approach
            assert 'distance_km' in approach
            assert 'time' in approach
            assert 'position1' in approach
            assert 'position2' in approach
            
            # Check types
            assert isinstance(approach['distance_km'], float)
            assert isinstance(approach['time'], datetime)
            assert approach['position1'].shape == (3,)
            assert approach['position2'].shape == (3,)
    
    def test_closest_approaches_sorted(self, populated_system):
        """Test that closest approaches are sorted by distance"""
        start = datetime(2026, 2, 1, 0, 0, 0)
        populated_system.propagate_all(start, duration_hours=12, step_minutes=10)
        
        approaches = populated_system.find_closest_approaches(threshold_km=10000)
        
        if len(approaches) > 1:
            # Check sorting
            distances = [app['distance_km'] for app in approaches]
            assert distances == sorted(distances)
    
    def test_system_str(self, populated_system):
        """Test __str__ method"""
        string_repr = str(populated_system)
        
        # Should contain information about satellites
        assert "2 satellites" in string_repr or "2" in string_repr
        assert "Earth" in string_repr
    
    def test_empty_system_str(self, system):
        """Test __str__ for empty system"""
        string_repr = str(system)
        assert "0 satellites" in string_repr or "0" in string_repr
    
    def test_system_attributes_after_propagation(self, populated_system):
        """Test that system stores propagation parameters"""
        start = datetime(2026, 2, 1, 0, 0, 0)
        duration = 12
        step = 5
        frame = 'eci'
        
        populated_system.propagate_all(start, duration, step, frame)
        
        assert populated_system.start_time == start
        assert populated_system.duration_hours == duration
        assert populated_system.step_minutes == step
        assert populated_system.reference_frame == frame
    
    def test_add_satellite_with_kwargs(self, system, iss_tle_list):
        """Test adding satellite with additional keyword arguments"""
        system.add_satellite_from_tle(
            "ISS",
            iss_tle_list,
            sat_type="Space Station",
            mass=419700,
            rcs=481.801,
            status="operational"
        )
        
        sat = system.satellites[0]
        assert sat.sat_type == "Space Station"
        assert sat.mass == 419700
        assert sat.rcs == 481.801
        assert sat.status == "operational"


class TestSatelliteSystemIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_workflow(self):
        """Test complete workflow from creation to analysis"""
        # Create system
        earth = Earth(name="Earth", radius=6378.137)
        system = SatelliteSystem(earth)
        
        # Add satellites
        iss_tle = [
            'ISS (ZARYA)',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        ]
        system.add_satellite_from_tle("ISS", iss_tle)
        
        hst_tle = [
            'HST',
            '1 20580U 90037B   26032.51426829  .00001234  00000+0  12345-3 0  9998',
            '2 20580  28.4690 123.4567 0002813  45.6789  12.3456 15.09876543123456'
        ]
        system.add_satellite_from_tle("HST", hst_tle)
        
        # Propagate
        start = datetime(2026, 2, 1, 0, 0, 0)
        system.propagate_all(start, duration_hours=6, step_minutes=10)
        
        # Analyze
        approaches = system.find_closest_approaches(threshold_km=5000)
        
        # Verify results
        assert len(system.satellites) == 2
        for sat in system.satellites:
            assert len(sat.positions_eci) == 37  # 6 hours / 10 min + 1
            assert sat.positions_eci.shape == (37, 3)
    
    def test_different_orbital_regimes(self):
        """Test satellites in different orbital regimes"""
        earth = Earth(name="Earth", radius=6378.137)
        system = SatelliteSystem(earth)
        
        # LEO satellite (ISS)
        leo_tle = [
            'ISS',
            '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
            '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
        ]
        system.add_satellite_from_tle("LEO", leo_tle)
        
        # MEO satellite (GPS)
        meo_tle = [
            'GPS',
            '1 24876U 97035A   26032.51426829 -.00000023  00000+0  00000+0 0  9999',
            '2 24876  55.4567 234.5678 0123456  12.3456  45.6789  2.00561234567890'
        ]
        system.add_satellite_from_tle("MEO", meo_tle)
        
        # GEO satellite
        geo_tle = [
            'GEO',
            '1 12545U 81057B   26032.13894835 -.00000250  00000+0  00000+0 0  9998',
            '2 12545   7.3448 297.9013 0022532 231.2845 340.6936  1.00050650121029'
        ]
        system.add_satellite_from_tle("GEO", geo_tle)
        
        # Propagate all
        start = datetime(2026, 2, 1, 0, 0, 0)
        system.propagate_all(start, duration_hours=12, step_minutes=30)
        
        # Verify different altitudes
        leo_sat = system.satellites[0]
        meo_sat = system.satellites[1]
        geo_sat = system.satellites[2]
        
        leo_alt = leo_sat.semi_major_axis - 6378.137
        meo_alt = meo_sat.semi_major_axis - 6378.137
        geo_alt = geo_sat.semi_major_axis - 6378.137
        
        assert leo_alt < meo_alt < geo_alt
        assert leo_alt < 2000  # km
        assert 10000 < meo_alt < 30000
        assert geo_alt > 30000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
