/* 
Definition: "TLE Checksum equation computes the checksum value by performing these steps:

- The checksum sums the numeric value of all the numeric characters in - the string that is the TLE card (so 123 would sum to 6)
- The checksum ignores non-numeric characters except the minus sign ("-")
- The checksum assigns the value 0 to the alpha characters (so basically ignores the alpha characters)
- The checksum assigns the value 0 to periods and blanks (so basically ignores the periods and blanks)
- The checksum assigns the value 0 to '+' signs (so basically ignores plus signs)
- The checksum assigns the value 1 to  '-' signs and sums their assigned value (so each minus sign has a value 1)
- The TLE Checksum equation then takes modulo 10 of the total of numeric values and the 1's for the minus signs."

Prepared with help of AI
*/

// #include <iostream>
// #include <cctype>
// #include <string>
#include "cchecksum.h"

// Function to compute TLE checksum
int tle_line_checksum(const std::string &line) {
    int sum = 0;

    // TLE lines are typically 69 characters, last char is checksum
    // We sum only the first 68 characters
    for (size_t i = 0; i < line.size() && i < 68; ++i) {
        char c = line[i];
        if (std::isdigit(static_cast<unsigned char>(c))) {
            sum += c - '0'; // numeric value
        } else if (c == '-') {
            sum += 1; // minus sign counts as 1
        }
        // all other characters count as 0
    }

    return sum % 10; // checksum is modulo 10
}


