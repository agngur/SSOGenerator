# distutils: language = c++

cdef extern from "ctle_checksum.h":
    int tle_compute_checksum(const char *line)
    bint tle_checksum_valid(const char *line)

def tleline_checksum(line: str) -> int:
    if len(line) < 69:
        raise ValueError("TLE line must be at least 69 characters long")
    return tle_compute_checksum(line.encode("ascii"))

def tleline_checksum_valid(line: str) -> bool:
    if len(line) < 69:
        return False
    return bool(tle_checksum_valid(line.encode("ascii")))
