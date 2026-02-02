#ifndef CCHECKSUM_H
#define CCHECKSUM_H

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Compute the checksum of a TLE/GP line.
 *
 * Rules:
 *  - Sum digits (0–9) as their numeric value
 *  - Add 1 for each '-' character
 *  - Ignore all other characters
 *  - Compute sum % 10
 *
 * The checksum is computed over columns 1–68 (0–67 in C indexing).
 *
 * @param line  A null-terminated string containing a TLE/GP line.
 * @return      The computed checksum (0–9), or -1 on error.
 */
int tle_compute_checksum(const char *line);

/**
 * Validate the checksum of a TLE/GP line.
 *
 * @param line  A null-terminated string containing a TLE/GP line.
 * @return      true if checksum matches the last character, false otherwise.
 */
bool tle_checksum_valid(const char *line);

#ifdef __cplusplus
}
#endif

#endif // CCHECKSUM_H
