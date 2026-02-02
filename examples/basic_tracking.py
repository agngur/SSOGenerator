"""
Example: Basic Satellite Tracking
----------------------------------
This example demonstrates basic usage of SSOGenerator:
- Creating a satellite system
- Adding satellites
- Propagating orbits
- Accessing position data
"""

from ssogenerator import Earth, SatelliteSystem
from datetime import datetime
import numpy as np

def main():
    print("=" * 70)
    print("SSOGenerator Example: Basic Satellite Tracking")
    print("=" * 70)
    
    # Step 1: Create Earth and System
    print("\n1. Creating Earth and Satellite System...")
    earth = Earth(name="Earth", radius=6378.137)
    system = SatelliteSystem(earth)
    print(f"   ✓ Created system with {earth}")
    
    # Step 2: Add ISS
    print("\n2. Adding ISS (International Space Station)...")
    iss_tle = [
        'ISS (ZARYA)',
        '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
        '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
    ]
    
    system.add_satellite_from_tle(
        name="ISS",
        tles=iss_tle,
        sat_type="Space Station",
        status="operational",
        mass=419700,  # kg
        rcs=481.801   # m²
    )
    print(f"   ✓ Added ISS to system")
    
    # Step 3: Display satellite info
    iss = system.satellites[0]
    print("\n3. ISS Orbital Parameters:")
    print(f"   NORAD ID: {iss.norad_id}")
    print(f"   Altitude: {iss.semi_major_axis - 6378.137:.2f} km")
    print(f"   Inclination: {iss.inclination:.2f}°")
    print(f"   Eccentricity: {iss.eccentricity:.6f}")
    print(f"   Orbital Period: {iss.get_orbital_period():.2f} minutes")
    print(f"   Mean Motion: {iss.mean_motion:.8f} rev/day")
    
    # Step 4: Propagate orbit
    print("\n4. Propagating orbit for 24 hours...")
    start_time = datetime(2026, 2, 1, 0, 0, 0)
    duration_hours = 24
    step_minutes = 5
    
    system.propagate_all(
        start_time=start_time,
        duration_hours=duration_hours,
        step_minutes=step_minutes,
        frame='eci'
    )
    print(f"   ✓ Propagated {len(iss.positions_eci)} positions")
    
    # Step 5: Analyze results
    print("\n5. Analyzing Propagation Results:")
    print(f"   Time range: {iss.times[0]} to {iss.times[-1]}")
    print(f"   Number of time steps: {len(iss.times)}")
    
    # Calculate statistics
    altitudes = np.linalg.norm(iss.positions_eci, axis=1) - 6378.137
    speeds = np.linalg.norm(iss.velocities, axis=1)
    
    print(f"\n   Altitude Statistics:")
    print(f"     Mean: {np.mean(altitudes):.2f} km")
    print(f"     Min: {np.min(altitudes):.2f} km")
    print(f"     Max: {np.max(altitudes):.2f} km")
    print(f"     Std Dev: {np.std(altitudes):.2f} km")
    
    print(f"\n   Velocity Statistics:")
    print(f"     Mean: {np.mean(speeds):.3f} km/s")
    print(f"     Min: {np.min(speeds):.3f} km/s")
    print(f"     Max: {np.max(speeds):.3f} km/s")
    
    # Step 6: Sample some positions
    print("\n6. Sample Positions (first 5 time steps):")
    print(f"   {'Time':<20} {'X (km)':<12} {'Y (km)':<12} {'Z (km)':<12} {'Alt (km)':<10}")
    print(f"   {'-'*76}")
    
    for i in range(min(5, len(iss.times))):
        time = iss.times[i]
        pos = iss.positions_eci[i]
        alt = np.linalg.norm(pos) - 6378.137
        
        print(f"   {time.strftime('%Y-%m-%d %H:%M'):<20} "
              f"{pos[0]:>11.2f} {pos[1]:>11.2f} {pos[2]:>11.2f} {alt:>9.2f}")
    
    # Step 7: Ground track information
    print("\n7. Ground Track Information:")
    
    # Find maximum and minimum latitudes
    lats = [sp[0].degrees for sp in iss.subpoints]
    lons = [sp[1].degrees for sp in iss.subpoints]
    
    print(f"   Latitude range: {min(lats):.2f}° to {max(lats):.2f}°")
    print(f"   Longitude range: {min(lons):.2f}° to {max(lons):.2f}°")
    print(f"   Number of orbits: ~{duration_hours * 60 / iss.get_orbital_period():.1f}")
    
    # Step 8: Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  • Successfully tracked ISS for {duration_hours} hours")
    print(f"  • Computed {len(iss.positions_eci)} position vectors")
    print(f"  • Average altitude: {np.mean(altitudes):.2f} km")
    print(f"  • Average speed: {np.mean(speeds):.3f} km/s")
    print("=" * 70)
    
    # Optional: Visualize
    try:
        print("\n8. Starting 3D Visualization...")
        print("   (Press Ctrl+C to stop animation)")
        system.visualize(mode='animate', fps=30, speed_multiplier=10.0)
    except (ImportError, KeyboardInterrupt):
        print("   Visualization skipped or stopped by user")
    except Exception as e:
        print(f"   Visualization not available: {e}")

if __name__ == "__main__":
    main()
