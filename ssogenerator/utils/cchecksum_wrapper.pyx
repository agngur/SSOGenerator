# distutils: language = c++

from libcpp.string cimport string
cdef extern from "cchecksum.h":
    #double trapezoid(const vector[double]& x, const vector[double]& y)
    int tle_line_checksum(const std::string &line)

# Python wrapper
def tle_line_checksum(str line):
    cdef string cline
    cline = line
    return tle_line_checksum(cline)

# Example from classes
#def ctrapezoid(list x, list y):
#    cdef vector[double] cx
#    cdef vector[double] cy
#    for val in x:
#        cx.push_back(val)
#    for val in y:
#        cy.push_back(val)
#    return trapezoid(cx, cy)