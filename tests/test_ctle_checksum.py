from ssogenerator.utils.ctle_checksum import tleline_checksum, tleline_checksum_valid

LINE1 = "1 08820C 76039A   25327.00000000  .00000000  00000+0  00000+0 0  3275"
LINE2 = "2 08820 109.8379 108.7292 0044676 346.4299  11.8724  6.38664905    11"

def test_line1_valid():
    assert tleline_checksum_valid(LINE1)

def test_line2_valid():
    assert tleline_checksum_valid(LINE2)

def test_line1_value():
    assert tleline_checksum(LINE1) == int(LINE1[-1])

def test_line2_value():
    assert tleline_checksum(LINE2) == int(LINE2[-1])
