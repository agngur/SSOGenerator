"""
VPython-based 3D Visualization for Satellite System
PyShine-style animated visualization with Earth sphere and satellite orbits
"""

try:
    from vpython import sphere, curve, vector, rate, canvas, textures, color, label
    VPYTHON_AVAILABLE = True
except ImportError:
    VPYTHON_AVAILABLE = False
    print("Warning: VPython not installed. 3D visualization will not be available.")
    print("Install with: pip install vpython")

import time
import numpy as np
#from datetime import datetime
# from typing import Optional, List


class VPythonVisualizer:
    """
    VPython-based visualizer for satellite orbits around Earth
    Creates animated 3D view similar to PyShine GPS example
    """
    
    def __init__(self, system, title: str = "Earth Orbiting Satellites"):
        """
        Initialize VPython visualizer
        
        :param system:
            SatelliteSystem object with propagated satellites
        :param title:
            Window title for the visualization
        """
        if not VPYTHON_AVAILABLE:
            raise ImportError("VPython is required for 3D visualization. "
                            "Install with: pip install vpython")
        
        self.system = system
        self.title = title
        
        # Display parameters
        self.DISP_R = 6378.137  # Earth radius in km for display
        self.scale_factor = 1.0  # Scale factor for visualization
        
        # VPython objects
        self.scene = None
        self.earth = None
        self.satellite_objects = {}
        self.orbit_curves = {}
        self.satellite_labels = {}
        
    def setup_scene(self, width: int = 1024, height: int = 768, 
                   background_color=None):
        """
        Setup VPython scene/canvas
        
        :param width:
            Canvas width in pixels
        :param height:
            Canvas height in pixels
        :param background_color:
            Background color (default: black)
        """
        # Create scene
        self.scene = canvas(title=self.title, 
                          width=width, 
                          height=height,
                          background=background_color or color.black)
        
        # Set camera
        max_altitude = max([sat.semi_major_axis for sat in self.system.satellites])
        self.scene.range = max_altitude * 1.5
        self.scene.forward = vector(0, 0, -1)
        
        # Create Earth sphere with texture
        self.earth = sphere(radius=self.DISP_R,
                          texture=textures.earth,
                          shininess=0.1)
        
        print("VPython scene created successfully")
        
    def create_satellite_objects(self, trail_length: int = 50):
        """
        Create VPython objects for each satellite
        
        :param trail_length:
            Number of points to show in orbit trail
        """
        # Color palette for satellites
        colors = [
            color.red, color.green, color.blue, color.yellow,
            color.orange, color.cyan, color.magenta, color.white
        ]
        
        for i, sat in enumerate(self.system.satellites):
            sat_color = colors[i % len(colors)]
            
            # Initial position
            if len(sat.positions_eci) > 0:
                pos = sat.positions_eci[0]
                
                # Create satellite sphere
                sat_obj = sphere(pos=vector(pos[0], pos[1], pos[2]),
                               radius=self.DISP_R * 0.05,  # Small sphere
                               color=sat_color,
                               make_trail=False)
                
                # Create orbit curve (trail)
                orbit = curve(color=sat_color, radius=self.DISP_R * 0.01)
                
                # Create label
                sat_label = label(pos=vector(pos[0], pos[1], pos[2]),
                                text=sat.name,
                                xoffset=20,
                                yoffset=20,
                                space=30,
                                height=10,
                                border=4,
                                font='sans',
                                color=sat_color)
                
                self.satellite_objects[sat.name] = sat_obj
                self.orbit_curves[sat.name] = orbit
                self.satellite_labels[sat.name] = sat_label
        
        print(f"Created {len(self.satellite_objects)} satellite objects")
    
    def animate(self, fps: int = 30, speed_multiplier: float = 1.0,
               show_trails: bool = True, trail_length: int = 100):
        """
        Animate satellite orbits in real-time
        
        :param fps:
            Frames per second for animation
        :param speed_multiplier:
            Speed multiplier for animation (1.0 = real-time)
        :param show_trails:
            Whether to show orbit trails
        :param trail_length:
            Maximum number of trail points to display
        """
        if not self.scene:
            self.setup_scene()
        
        if not self.satellite_objects:
            self.create_satellite_objects(trail_length)
        
        print("\nStarting animation...")
        print(f"FPS: {fps}, Speed: {speed_multiplier}x")
        print(f"Time range: {self.system.satellites[0].times[0]} to "
              f"{self.system.satellites[0].times[-1]}")
        print("\nPress Ctrl+C to stop animation")
        
        # Animation loop
        num_steps = len(self.system.satellites[0].times)
        
        try:
            for step in range(num_steps):
                rate(fps)  # Control frame rate
                
                # Update each satellite
                for sat in self.system.satellites:
                    if step >= len(sat.positions_eci):
                        continue
                    
                    pos = sat.positions_eci[step]
                    sat_obj = self.satellite_objects[sat.name]
                    orbit = self.orbit_curves[sat.name]
                    sat_label = self.satellite_labels[sat.name]
                    
                    # Update satellite position
                    sat_obj.pos = vector(pos[0], pos[1], pos[2])
                    
                    # Update label position
                    sat_label.pos = vector(pos[0], pos[1], pos[2])
                    
                    # Add point to orbit trail
                    if show_trails:
                        orbit.append(vector(pos[0], pos[1], pos[2]))
                        
                        # Limit trail length
                        if orbit.npoints > trail_length:
                            orbit.points.pop(0)
                
                # Optional: rotate camera slowly
                # self.scene.forward = rotate(self.scene.forward, 
                #                            angle=0.001, axis=vector(0,1,0))
                
        except KeyboardInterrupt:
            print("\nAnimation stopped by user")
    
    def plot_static_orbits(self):
        """
        Plot complete static orbits (not animated)
        Shows full orbital paths for all satellites
        """
        if not self.scene:
            self.setup_scene()
        
        print("\nPlotting static orbits...")
        
        # Color palette
        colors_list = [
            color.red, color.green, color.blue, color.yellow,
            color.orange, color.cyan, color.magenta, color.white
        ]
        
        for i, sat in enumerate(self.system.satellites):
            sat_color = colors_list[i % len(colors_list)]
            
            # Create complete orbit curve
            orbit = curve(color=sat_color, radius=self.DISP_R * 0.01)
            
            # Add all points
            for pos in sat.positions_eci:
                orbit.append(vector(pos[0], pos[1], pos[2]))
            
            # Mark starting position
            start_pos = sat.positions_eci[0]
            sphere(pos=vector(start_pos[0], start_pos[1], start_pos[2]),
                  radius=self.DISP_R * 0.08,
                  color=sat_color)
            
            # Add label at starting position
            label(pos=vector(start_pos[0], start_pos[1], start_pos[2]),
                 text=sat.name,
                 xoffset=20,
                 yoffset=20,
                 height=12,
                 color=sat_color)
        
        print(f"Plotted {len(self.system.satellites)} complete orbits")
    
    def plot_time_step(self, time_index: int = 0, show_labels: bool = True):
        """
        Plot satellite positions at a specific time step
        
        :param time_index:
            Index of time step to visualize
        :param show_labels:
            Whether to show satellite labels
        """
        if not self.scene:
            self.setup_scene()
        
        # Color palette
        colors_list = [
            color.red, color.green, color.blue, color.yellow,
            color.orange, color.cyan, color.magenta, color.white
        ]
        
        for i, sat in enumerate(self.system.satellites):
            if time_index >= len(sat.positions_eci):
                continue
            
            sat_color = colors_list[i % len(colors_list)]
            pos = sat.positions_eci[time_index]
            
            # Create satellite
            sphere(pos=vector(pos[0], pos[1], pos[2]),
                  radius=self.DISP_R * 0.05,
                  color=sat_color)
            
            # Add label
            if show_labels:
                label(pos=vector(pos[0], pos[1], pos[2]),
                     text=f"{sat.name}\nTime: {sat.times[time_index]}",
                     xoffset=20,
                     yoffset=20,
                     height=10,
                     color=sat_color)
        
        print(f"Plotted satellites at time step {time_index}")


# Convenience function for quick visualization
def visualize_system(system, mode: str = 'animate', **kwargs):
    """
    Quick visualization of satellite system
    
    :param system:
        SatelliteSystem object with propagated satellites
    :param mode:
        Visualization mode: 'animate', 'static', or 'snapshot'
    :param kwargs:
        Additional arguments passed to visualization method
    
    Example:
        >>> visualize_system(system, mode='animate', fps=30, speed_multiplier=2.0)
        >>> visualize_system(system, mode='static')
        >>> visualize_system(system, mode='snapshot', time_index=0)
    """
    if not VPYTHON_AVAILABLE:
        print("VPython not available. Please install with: pip install vpython")
        return None
    
    viz = VPythonVisualizer(system)
    
    if mode == 'animate':
        viz.setup_scene()
        viz.create_satellite_objects()
        viz.animate(**kwargs)
    elif mode == 'static':
        viz.plot_static_orbits()
    elif mode == 'snapshot':
        time_index = kwargs.get('time_index', 0)
        viz.plot_time_step(time_index)
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'animate', 'static', or 'snapshot'")
    
    return viz


# Example usage
if __name__ == "__main__":
    # This is an example - requires a working SatelliteSystem
    print("VPython Visualizer for Satellite Systems")
    print("=" * 50)
    print("\nTo use this visualizer:")
    print("1. Create and propagate a SatelliteSystem")
    print("2. Import this module: from ssogenerator.visualization import visualize_system")
    print("3. Call: visualize_system(system, mode='animate')")
    print("\nModes available:")
    print("  - 'animate': Real-time animation of orbits")
    print("  - 'static': Show complete orbital paths")
    print("  - 'snapshot': Show satellites at specific time")
