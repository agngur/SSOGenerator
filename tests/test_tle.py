import numpy as np
from ssogenerator.utils.ephemeris import TLE

lageos_tle = [
    "LAGEOS1 [DGF]",
    "1 08820C 76039A   25327.00000000  .00000000  00000+0  00000+0 0  3275",
    "2 08820 109.8379 108.7292 0044676 346.4299  11.8724  6.38664905    11"
]

tle_test = TLE(tle0=lageos_tle[0], tle1=lageos_tle[1], tle2=lageos_tle[2])

def test_tle_valid():
    assert tle_test

def test_tle_norad():
    assert tle_test.norad_id == "8820"

def test_tle_cospar():
    assert tle_test.cospar_id == "1976-039A"

def test_tle_valid():
    assert tle_test.valid == True

#print(tle_test)