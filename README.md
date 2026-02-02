# SSOGenerator

:::{admonition} Overview
:class: tip
**Satellite System Objects (SSO) Generator** is a Python package for modeling, propagating, and visualizing Earth-orbiting satellite systems using Two-Line Element (TLE) or ELSET data. It provides tools for orbit propagation, closest approach detection, and 3D visualization.
:::

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

> *"Code is read much more often than it is written."* - Guido van Rossum --> great citation from course slides.

## ✨ Features

- 🌍 **Earth Model**: WGS84-compatible Earth representation
- 🛰️ **TLE Support**: Full Two-Line Element and ELSET parsing and validation
- 📡 **Orbit Propagation**: Skyfield-based SGP4/SDP4 propagation engine
- 🎯 **Closest Approaches**: Detect satellite conjunctions and closest approaches
- 📊 **3D Visualization**: Animated PyShine-style visualization with VPython
- 🔄 **Multiple Reference Frames**:  Both ECI (Earth-Centered Inertial) and ECEF (Earth-Centered Earth-Fixed) support (ECI is GCRF-aligned)
- 🧪 **Tested**: Covered with tests

## 🚀 Quick Start

### Installation

We recommend that you install the satellite system objects (SSO) generator in a conda environment.

If you don't have conda already, you can find it here: [Miniconda](https://www.anaconda.com/download/success) 
following the [instructions](https://www.anaconda.com/docs/getting-started/miniconda/install) for your operating system. 
Once you have miniconda, you can create a new conda environment i.e. sso-python3 with python 3.10 or use directly TOML file for installation and dependencies.
In a terminal (or Anaconda Powershell Prompt for Windows), run:

```bash
conda create --name sso-python3 python=3.10
```

Then, activate the conda environment:

```bash
conda activate sso-python3
```

Clone the repository and pip install:

```bash
git clone https://github.com/yourusername/SSOGenerator.git
cd SSOGenerator
pip install -e .
```

If you have any issues with installation (or when using it in jupyter-lab) please remember to try uninstall it and install it again:

```bash
pip uninstall SSOGenerator
pip install -no-build-isolation -e .
```

After work you can deactivate your conda environent simply by:


```bash
conda deactivate
```


### Basic Usage

```python
from datetime import datetime
from ssogenerator import Earth, SatelliteSystem
from ssogenerator.utils.ephemeris import TLE

# Create system
earth = Earth(name="Earth", radius=6378.137)
system = SatelliteSystem(earth)

# Add or validate TLE
lageos_tle = [
    "LAGEOS1 [DGF]",
    "1 08820C 76039A   25327.00000000  .00000000  00000+0  00000+0 0  3275",
    "2 08820 109.8379 108.7292 0044676 346.4299  11.8724  6.38664905    11"
]
tle_set = TLE(tle0=lageos_tle[0], tle1=lageos_tle[1], tle2=lageos_tle[2])
print(tle_set)

# Add satellites
system.add_satellite_by_norad_id("25544")  # ISS
system.add_satellite_by_norad_id("20580")  # Hubble

# Propagate orbits
start = datetime(2026, 2, 1, 0, 0, 0)
system.propagate_all(start_time=start, duration_hours=24, step_minutes=5)

# Find close approaches
approaches = system.find_closest_approaches(threshold_km=500)

# Visualize in 3D
system.visualize(mode='animate', fps=30)
```

## 📖 Documentation

Full documentation is available in the [docs/](docs/) directory.

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## Project Structure

```
SSOGenerator/
├── ssogenerator/           # Main package
│   ├── __init__.py
│   ├── earth.py           # Earth class
│   ├── satellite.py       # Satellite class
│   ├── system.py          # SatelliteSystem class
│   ├── visualization.py   # VPython visualization
│   └── utils/            # Utility modules
│       ├── ephemeris.py   # TLE handling
│       └── ctle_checksum/ # C++ checksum validation
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/             # Example scripts
└── pyproject.toml        # Project configuration
```

## Citation

If you use SSOGenerator in your research, please cite:

```{code-block} bibtex
@software{ssogenerator2026,
  author = {Gurgul, Agnieszka},
  title = {SSOGenerator: Satellite System Objects Generator},
  year = {2026},
  url = {https://github.com/yourusername/SSOGenerator}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) for details.

## 🙏 Acknowledgments

- Built with [Skyfield](https://rhodesmill.org/skyfield/) for orbit propagation
- Visualization inspired by [PyShine's GPS satellite tutorial](https://www.pyshine.com)
- TLE data from [CelesTrak](https://celestrak.org)

## Adnotation
---
title: SSOGenerator Documentation
subtitle: Satellite System Objects Generator
description: Python package for modeling and visualizing Earth-orbiting satellites
authors:
  - name: Agnieszka Gurgul
    email: agn.gurgul@umk.pl
    affiliation: Nicolaus Copernicus University in Toruń
---
