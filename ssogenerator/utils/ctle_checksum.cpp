#include "ctle_checksum.h"
#include <ctype.h>
#include <string.h>

int tle_compute_checksum(const char *line) {
    if (!line) return -1;

    int sum = 0;

    // TLE checksum is computed over columns 1–68 (0–67 in C)
    for (int i = 0; i < 68 && line[i] != '\0'; ++i) {
        char c = line[i];

        if (c >= '0' && c <= '9') {
            sum += c - '0';
        } else if (c == '-') {
            sum += 1;
        }
        // all other characters ignored
    }

    return sum % 10;
}

bool tle_checksum_valid(const char *line) {
    if (!line) return false;

    int expected = tle_compute_checksum(line);
    if (expected < 0) return false;

    // The checksum digit is always at column 69 (index 68)
    char chk_char = line[68];
    if (!isdigit((unsigned char)chk_char))
        return false;

    int provided = chk_char - '0';

    return expected == provided;
}
