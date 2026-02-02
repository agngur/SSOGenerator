---
title: Visualization API
---

# Visualization API Reference

The visualization module provides VPython-based 3D visualization for satellite systems, inspired by PyShine's GPS satellite tutorial with custom satellites combination and orbits propagation. Created with help of AI.

## Classes

### VPythonVisualizer

```
.. autoclass:: ssogenerator.visualization.VPythonVisualizer
   :members:
   :undoc-members:
   :show-inheritance:
```

Main class for creating VPython-based 3D visualizations.

#### Constructor

```python
VPythonVisualizer(system, title="Earth Orbiting Satellites")
```

**Parameters:**
- `system` (SatelliteSystem): System with propagated satellites
- `title` (str): Window title

**Example:**
```python
from ssogenerator.visualization import VPythonVisualizer

viz = VPythonVisualizer(system, title="My Satellites")
```

#### Methods

##### setup_scene

```python
setup_scene(width=1024, height=768, background_color=None)
```

Initialize the VPython scene/canvas.

**Parameters:**
- `width` (int): Canvas width in pixels (default: 1024)
- `height` (int): Canvas height in pixels (default: 768)
- `background_color`: VPython color object (default: black)

**Example:**
```python
from vpython import color
viz.setup_scene(width=1920, height=1080, background_color=color.gray(0.2))
```

##### create_satellite_objects

```python
create_satellite_objects(trail_length=50)
```

Create VPython sphere objects for each satellite.

**Parameters:**
- `trail_length` (int): Number of trail points (default: 50)

##### animate

```python
animate(fps=30, speed_multiplier=1.0, show_trails=True, trail_length=100)
```

Animate satellite orbits in real-time.

**Parameters:**
- `fps` (int): Frames per second (default: 30)
- `speed_multiplier` (float): Animation speed factor (default: 1.0)
- `show_trails` (bool): Display orbital trails (default: True)
- `trail_length` (int): Maximum trail points (default: 100)

**Example:**
```python
# 2x speed animation at 60 FPS
viz.animate(fps=60, speed_multiplier=2.0)
```

**Notes:**
- Press Ctrl+C to stop animation
- Higher FPS requires more CPU
- Speed multiplier affects time progression

##### plot_static_orbits

```python
plot_static_orbits()
```

Plot complete static orbital paths for all satellites.

**Example:**
```python
viz.plot_static_orbits()
```

##### plot_time_step

```python
plot_time_step(time_index=0, show_labels=True)
```

Plot satellites at a specific time step.

**Parameters:**
- `time_index` (int): Index of time step (default: 0)
- `show_labels` (bool): Show satellite labels (default: True)

**Example:**
```python
# Plot at 100th time step
viz.plot_time_step(time_index=100)
```

## Functions

### visualize_system

```python
visualize_system(system, mode='animate', **kwargs)
```

Convenience function for quick visualization.

**Parameters:**
- `system` (SatelliteSystem): System to visualize
- `mode` (str): Visualization mode
  - `'animate'`: Real-time animation
  - `'static'`: Complete orbital paths
  - `'snapshot'`: Single time step
- `**kwargs`: Additional mode-specific arguments

**Returns:**
- `VPythonVisualizer`: Visualizer instance

**Examples:**

```python
from ssogenerator.visualization import visualize_system

# Animated view
visualize_system(system, mode='animate', fps=30, speed_multiplier=2.0)

# Static orbits
visualize_system(system, mode='static')

# Snapshot at specific time
visualize_system(system, mode='snapshot', time_index=50)
```

## Usage Examples

### Basic Animation

```python
from ssogenerator import Earth, SatelliteSystem
from ssogenerator.visualization import visualize_system
from datetime import datetime

# Create and propagate system
earth = Earth(name="Earth", radius=6378.137)
system = SatelliteSystem(earth)
system.add_satellite_by_norad_id("25544")  # ISS

start = datetime(2026, 2, 1, 0, 0, 0)
system.propagate_all(start, duration_hours=24, step_minutes=5)

# Visualize
visualize_system(system, mode='animate', fps=30)
```

### Custom Visualization

```python
from ssogenerator.visualization import VPythonVisualizer
from vpython import color

# Create custom visualizer
viz = VPythonVisualizer(system, title="My Custom View")
viz.setup_scene(width=1920, height=1080, background_color=color.gray(0.1))
viz.create_satellite_objects(trail_length=200)

# Animate with custom settings
viz.animate(fps=60, speed_multiplier=5.0, trail_length=150)
```

### Static Orbit Display

```python
viz = VPythonVisualizer(system)
viz.plot_static_orbits()
# Scene will remain open for inspection
```

### Time-Lapse Snapshots

```python
viz = VPythonVisualizer(system)

# Show snapshots at regular intervals
for i in range(0, len(system.satellites[0].times), 20):
    viz.plot_time_step(time_index=i)
    input("Press Enter for next snapshot...")
```

## VPython Elements

### Earth Visualization

The Earth is rendered as a textured sphere using VPython's built-in Earth texture:

```python
from vpython import sphere, textures

earth = sphere(radius=6378.137,  # km
              texture=textures.earth,
              shininess=0.1)
```

### Satellite Representation

Satellites are shown as small colored spheres:

```python
from vpython import sphere, vector, color

sat_sphere = sphere(pos=vector(x, y, z),
                   radius=300,  # km (scaled for visibility)
                   color=color.red)
```

### Orbit Trails

Trails are drawn using VPython curves:

```python
from vpython import curve, color

trail = curve(color=color.green, radius=50)
trail.append(vector(x, y, z))
```

### Labels

Satellite names are displayed using VPython labels:

```python
from vpython import label, vector

sat_label = label(pos=vector(x, y, z),
                 text="ISS",
                 xoffset=20,
                 yoffset=20,
                 color=color.white)
```

## Technical Notes

### Performance

- **Recommended:** 5-10 satellites for smooth animation
- **Maximum:** ~20 satellites with reduced FPS
- **Trail length:** Longer trails increase memory usage
- **FPS:** 30-60 FPS typical; higher requires more CPU

### Browser Requirement

VPython requires a web browser for rendering:
- Works on desktop (opens browser automatically)
- Requires GUI environment (not suitable for headless servers)
- Uses WebGL for 3D rendering

### Coordinate System

VPython uses the same coordinate system as your satellite data:
- **X**: Along Earth's equator (0° longitude)
- **Y**: Along Earth's equator (90° E)
- **Z**: Toward North Pole

### Camera Controls

VPython provides mouse controls:
- **Rotate**: Left-click and drag
- **Zoom**: Right-click and drag or scroll
- **Pan**: Shift + left-click and drag

## Troubleshooting

### VPython Not Available

If you see: `"VPython not installed"`

```bash
pip install vpython
```

### Browser Not Opening

VPython opens automatically. If it doesn't:
1. Check firewall settings
2. Try different browser
3. Check console for errors

### Slow Animation

If animation is laggy:
- Reduce FPS: `fps=15`
- Reduce trail length: `trail_length=30`
- Decrease satellites
- Close other browser tabs

### Headless Server

VPython requires GUI. For servers:
- Use matplotlib visualization instead
- Generate images/videos offline
- Use X11 forwarding (advanced)

## See Also

- [VPython Documentation](https://vpython.org) - Official VPython docs
- [PyShine Tutorial](https://www.pyshine.com) - Original inspiration
