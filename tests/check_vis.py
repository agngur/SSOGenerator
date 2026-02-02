from ssogenerator import Earth, SatelliteSystem
from datetime import datetime

earth = Earth(name="Earth", radius=6378.137)
system = SatelliteSystem(earth)
system.add_satellite_by_norad_id("25544")  # ISS

start = datetime(2026, 2, 1, 0, 0, 0)
system.propagate_all(start, duration_hours=24, step_minutes=5)

# PyShine-style 3D visualization!
system.visualize(mode='animate', fps=10)