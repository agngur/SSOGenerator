"""
Example: Satellite Constellation Analysis
-----------------------------------------
This example demonstrates:
- Managing multiple satellites
- Different orbital regimes (LEO, MEO, GEO)
- Closest approach detection
- Constellation visualization
"""

from ssogenerator import Earth, SatelliteSystem
from datetime import datetime
import numpy as np

def main():
    print("=" * 70)
    print("SSOGenerator Example: Constellation Analysis")
    print("=" * 70)
    
    # Create system
    earth = Earth(name="Earth", radius=6378.137)
    system = SatelliteSystem(earth)
    
    # Add satellites from different orbital regimes
    print("\n1. Adding Satellites from Different Orbital Regimes...")
    
    satellites_config = [
        {
            'name': 'ISS',
            'norad_id': '25544',
            'regime': 'LEO',
            'description': 'International Space Station'
        },
        {
            'name': 'HST',
            'norad_id': '20580',
            'regime': 'LEO',
            'description': 'Hubble Space Telescope'
        },
        {
            'name': 'Starlink',
            'norad_id': '44941',
            'regime': 'LEO',
            'description': 'Starlink-1094'
        },
        {
            'name': 'Galileo-6',
            'norad_id': '40129',
            'regime': 'MEO',
            'description': 'Galileo Navigation Satellite'
        }
    ]
    
    # Add satellites
    added_satellites = []
    for sat_config in satellites_config:
        print(f"\n   Adding {sat_config['name']} ({sat_config['regime']})...")
        try:
            sat = system.add_satellite_by_norad_id(
                sat_config['norad_id'],
                sat_type=sat_config['regime']
            )
            if sat:
                added_satellites.append(sat_config)
                print(f"   ✓ {sat_config['description']}")
                print(f"     Altitude: {sat.semi_major_axis - 6378.137:.2f} km")
                print(f"     Period: {sat.get_orbital_period():.2f} minutes")
            else:
                print(f"   ✗ Failed to add {sat_config['name']}")
        except Exception as e:
            print(f"   ✗ Error adding {sat_config['name']}: {e}")
    
    if len(system.satellites) == 0:
        print("\nNo satellites were added. Using manual TLE data...")
        # Fallback to manual TLE data
        manual_tles = [
            {
                'name': 'ISS',
                'tles': [
                    'ISS (ZARYA)',
                    '1 25544U 98067A   26032.43601913  .00006280  00000+0  12479-3 0  9991',
                    '2 25544  51.6317 251.5712 0011128  53.0689 307.1316 15.48319189550710'
                ],
                'regime': 'LEO'
            },
            {
                'name': 'HST',
                'tles': [
                    'HST',
                    '1 20580U 90037B   26032.51426829  .00001234  00000+0  12345-3 0  9998',
                    '2 20580  28.4690 123.4567 0002813  45.6789  12.3456 15.09876543123456'
                ],
                'regime': 'LEO'
            }
        ]
        
        for sat_data in manual_tles:
            system.add_satellite_from_tle(sat_data['name'], sat_data['tles'])
            added_satellites.append({'name': sat_data['name'], 'regime': sat_data['regime']})
    
    print(f"\n   Total satellites in system: {len(system.satellites)}")
    
    # Display constellation summary
    print("\n2. Constellation Summary:")
    print(f"   {'Satellite':<15} {'Regime':<8} {'Altitude (km)':<15} {'Inclination (°)':<18} {'Period (min)'}")
    print(f"   {'-'*85}")
    
    for i, sat in enumerate(system.satellites):
        altitude = sat.semi_major_axis - 6378.137
        period = sat.get_orbital_period()
        regime = added_satellites[i].get('regime', 'N/A') if i < len(added_satellites) else 'N/A'
        
        print(f"   {sat.name:<15} {regime:<8} {altitude:>14.2f} {sat.inclination:>17.2f} {period:>13.2f}")
    
    # Propagate all satellites
    print("\n3. Propagating All Satellites...")
    start_time = datetime(2026, 2, 1, 0, 0, 0)
    duration_hours = 12
    step_minutes = 5
    
    system.propagate_all(
        start_time=start_time,
        duration_hours=duration_hours,
        step_minutes=step_minutes,
        frame='eci'
    )
    
    print(f"   ✓ Propagated {len(system.satellites)} satellites")
    print(f"   ✓ Time steps: {len(system.satellites[0].times)}")
    
    # Find closest approaches
    print("\n4. Finding Closest Approaches...")
    
    thresholds = [5000, 1000, 500, 100]  # km
    
    for threshold in thresholds:
        approaches = system.find_closest_approaches(threshold_km=threshold)
        
        print(f"\n   Within {threshold} km:")
        if len(approaches) > 0:
            print(f"   Found {len(approaches)} approach(es)")
            
            # Show top 5
            for i, app in enumerate(approaches[:5], 1):
                print(f"     {i}. {app['satellite1']} <-> {app['satellite2']}")
                print(f"        Distance: {app['distance_km']:.2f} km")
                print(f"        Time: {app['time'].strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"   No approaches found")
    
    # Analyze orbital coverage
    print("\n5. Orbital Coverage Analysis:")
    
    for sat in system.satellites:
        lats = [sp[0].degrees for sp in sat.subpoints]
        lons = [sp[1].degrees for sp in sat.subpoints]
        
        print(f"\n   {sat.name}:")
        print(f"     Latitude coverage: {min(lats):.2f}° to {max(lats):.2f}°")
        print(f"     Longitude coverage: {min(lons):.2f}° to {max(lons):.2f}°")
        print(f"     Number of orbits: ~{duration_hours * 60 / sat.get_orbital_period():.1f}")
    
    # Visualize constellation
    print("\n6. Visualization Options:")
    print("   • Static orbits: system.visualize(mode='static')")
    print("   • Animation: system.visualize(mode='animate', fps=30)")
    print("   • Snapshot: system.visualize(mode='snapshot', time_index=0)")
    
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        
        print("\n   Generating matplotlib 3D plot...")
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot Earth
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x = 6378.137 * np.outer(np.cos(u), np.sin(v))
        y = 6378.137 * np.outer(np.sin(u), np.sin(v))
        z = 6378.137 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='lightblue', alpha=0.3)
        
        # Plot satellite orbits
        colors = ['red', 'green', 'blue', 'orange', 'purple']
        for i, sat in enumerate(system.satellites):
            color = colors[i % len(colors)]
            pos = sat.positions_eci
            ax.plot(pos[:, 0], pos[:, 1], pos[:, 2],
                   color=color, label=sat.name, linewidth=2, alpha=0.7)
            
            # Mark starting position
            ax.scatter(pos[0, 0], pos[0, 1], pos[0, 2],
                      color=color, s=100, marker='o')
        
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')
        ax.set_title('Satellite Constellation - 3D View')
        ax.legend()
        
        max_range = max([sat.semi_major_axis for sat in system.satellites]) * 1.2
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        plt.savefig('constellation_3d.png', dpi=150, bbox_inches='tight')
        print("   ✓ Saved plot to constellation_3d.png")
        
        # Ground track plot
        fig2, ax2 = plt.subplots(figsize=(15, 8))
        
        for i, sat in enumerate(system.satellites):
            color = colors[i % len(colors)]
            lats = [sp[0].degrees for sp in sat.subpoints]
            lons = [sp[1].degrees for sp in sat.subpoints]
            
            ax2.plot(lons, lats, color=color, label=sat.name,
                    linewidth=2, alpha=0.7)
            ax2.scatter(lons[0], lats[0], color=color,
                       s=100, marker='o', edgecolors='black')
        
        ax2.set_xlabel('Longitude (°)')
        ax2.set_ylabel('Latitude (°)')
        ax2.set_title('Satellite Ground Tracks')
        ax2.set_xlim(-180, 180)
        ax2.set_ylim(-90, 90)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.savefig('constellation_ground_track.png', dpi=150, bbox_inches='tight')
        print("   ✓ Saved plot to constellation_ground_track.png")
        
    except ImportError:
        print("   Matplotlib not available for plotting")
    
    print("\n" + "=" * 70)
    print("Constellation Analysis Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
