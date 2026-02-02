# distutils: language = c++

from libcpp.string cimport string
cdef extern from "cchecksum.h":
    int tle_line_checksum(const string& line)

# Python wrapper
def tle_line_checksum(str line):

    # Convert Python str --> bytes as TLE lines are ASCII
    #if isinstance(line, str):
    #    line = line.encode("ascii")
    
    cdef string cline = line
    return tle_line_checksum(cline)

# AI Claude suggestion:
#def compute_checksum(str line):
#    return tle_line_checksum(line.encode('utf-8'))

# Example from classes
#def ctrapezoid(list x, list y):
#    cdef vector[double] cx
#    cdef vector[double] cy
#    for val in x:
#        cx.push_back(val)
#    for val in y:
#        cy.push_back(val)
#    return trapezoid(cx, cy)