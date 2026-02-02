---
title: Getting Started
---

# Getting Started with SSOGenerator

This guide will help you get up and running with SSOGenerator.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Install from source

```{code-block} bash
git clone https://github.com/yourusername/SSOGenerator.git
cd SSOGenerator
pip install -e .
```

If it will not work please try uninstall and install again with additional flag:

```bash
pip uninstall SSOGenerator
pip install --no-build-isolation -e .
```

This will install SSOGenerator along with all required dependencies:
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `astropy` - Astronomical calculations
- `skyfield` - Satellite orbit propagation
- `vpython` - 3D visualization (optional)

## Basic Concepts

### Core Classes

SSOGenerator is built around three main classes:

1. **Earth**: Represents the central body (Earth)
2. **Satellite**: Represents individual satellites with TLE data
3. **SatelliteSystem**: Manages collections of satellites orbiting Earth

### TLE (Two-Line Elements)

TLE (or ELSET) is a standardized format for representing satellite orbital elements:

```{code-block} text
ISS (ZARYA)
1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991
2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710
```

- **Line 0**: Satellite name (optional)
- **Line 1**: Epoch, drag terms, and orbital data
- **Line 2**: Orbital elements (inclination, RAAN, eccentricity, ...)

## Your First Satellite System

### Step 1: Import the package

```{code-block} python
from ssogenerator import Earth, Satellite, SatelliteSystem
from ssogenerator.utils.ephemeris import TLE
from datetime import datetime
```

### Step 2: Create Earth and System

```{code-block} python
# Create Earth with WGS84 equatorial radius
earth = Earth(name="Earth", radius=6378.137)

# Initialize satellite system
system = SatelliteSystem(earth)
```

### Step 3: Add Satellites

There are three ways to add satellites:

#### Method 1: From TLE lines

```{code-block} python
iss_tle = ['ISS (ZARYA)',
           '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
           '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710']

system.add_satellite_from_tle(
    name="ISS",
    tles=iss_tle,
    status="operational",
    rcs=481.801  # Radar Cross Section in m²
)
```

#### Method 2: From NORAD ID (fetches TLE from CelesTrak)

```{code-block} python
# Hubble Space Telescope
system.add_satellite_by_norad_id("20580")

# Starlink satellite
system.add_satellite_by_norad_id("44941")
```

#### Method 3: Create Satellite object directly

```{code-block} python
apple_tle = TLE(
    'APPLE',
    '1 12545U 81057B   26032.13894835 -.00000250  00000+0  00000+0 0  9998',
    '2 12545   7.3448 297.9013 0022532 231.2845 340.6936  1.00050650121029'
)

apple_sat = Satellite(
    name="Apple",
    tle_data=apple_tle,
    norad_id="12545",
    sat_type="GEO",
    rcs=2.0
)

system.add_satellite(apple_sat)
```

### Step 4: Propagate Orbits

```{code-block} python
# Define time parameters
start_time = datetime(2026, 2, 1, 0, 0, 0)
duration_hours = 24  # Propagate for 24 hours
step_minutes = 5     # 5-minute time steps

# Propagate all satellites
system.propagate_all(
    start_time=start_time,
    duration_hours=duration_hours,
    step_minutes=step_minutes,
    frame='eci'  # or 'ecef'
)
```

:::{note}
Maximum propagation duration is 72 hours (3 days) to maintain accuracy.
:::

### Step 5: Analyze Results

#### Find Closest Approaches

```{code-block} python
# Find when satellites come within 500 km
approaches = system.find_closest_approaches(threshold_km=500)

for approach in approaches:
    print(f"{approach['satellite1']} <-> {approach['satellite2']}")
    print(f"Distance: {approach['distance_km']:.2f} km")
    print(f"Time: {approach['time']}")
```

#### Access Satellite Data

```{code-block} python
# Get first satellite
sat = system.satellites[0]

# Orbital parameters
print(f"Name: {sat.name}")
print(f"Altitude: {sat.semi_major_axis - 6378.137:.2f} km")
print(f"Inclination: {sat.inclination:.2f}°")
print(f"Period: {sat.get_orbital_period():.2f} minutes")

# Propagated positions (numpy arrays)
print(f"Positions shape: {sat.positions_eci.shape}")
print(f"Velocities shape: {sat.velocities.shape}")
print(f"Number of time steps: {len(sat.times)}")
```

### Step 6: Visualize (Optional)

If VPython is installed:

```{code-block} python
# Animated visualization
system.visualize(mode='animate', fps=30, speed_multiplier=2.0)

# Static orbit plot
system.visualize(mode='static')

# Snapshot at specific time
system.visualize(mode='snapshot', time_index=0)
```

---
title: Example
---

## Complete Example

Here's a complete working example:

```{code-block} python
:caption: complete_example.py
:linenos:

from ssogenerator import Earth, SatelliteSystem
from datetime import datetime

# Create system
earth = Earth(name="Earth", radius=6378.137)
system = SatelliteSystem(earth)

# Add satellites
system.add_satellite_by_norad_id("25544")  # ISS
system.add_satellite_by_norad_id("20580")  # Hubble
system.add_satellite_by_norad_id("44941")  # Starlink

# Propagate
start = datetime(2026, 2, 1, 0, 0, 0)
system.propagate_all(
    start_time=start,
    duration_hours=12,
    step_minutes=5,
    frame='eci'
)

# Analyze
approaches = system.find_closest_approaches(threshold_km=1000)
print(f"Found {len(approaches)} close approaches")

# Visualize
system.visualize(mode='animate', fps=30)
```

For more - Learn about [PLOTTING](api/visualization) options


## Common NORAD IDs

Here are some commonly tracked objects:

| Name | NORAD ID | Type | Altitude |
|------|----------|------|----------|
| ISS (Zarya) | 25544 | Space Station | ~400 km |
| Hubble Space Telescope | 20580 | Observatory | ~540 km |
| Starlink-1094 | 44941 | Communications | ~550 km |
| GPS BIIR-2 | 24876 | Navigation | ~20,200 km |
| APPLE | 12545 | Communications | ~35,786 km (GEO) |
| Galileo 6 | 40129 | Navigation | ~23,222 km |

## TLE Data Sources

### CelesTrak
- URL: https://celestrak.org
- Free, no registration required
- Updated regularly
- Used by `add_satellite_by_norad_id()`

### Space-Track
- URL: https://www.space-track.org
- Free registration required
- Most comprehensive database
- Higher update frequency

### N2YO
- URL: https://www.n2yo.com
- Real-time satellite tracking
- Visual tools
- API available but used mostly for visual inspection
