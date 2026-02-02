### Troubleshooting

### VPython not working?

VPython visualization requires a browser. If you're on a headless server:

```{code-block} python
# Use matplotlib-based visualization instead
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Access positions directly
sat = system.satellites[0]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(sat.positions_eci[:, 0], 
        sat.positions_eci[:, 1],
        sat.positions_eci[:, 2])
plt.show()
```

### TLE fetch failing?

If `add_satellite_by_norad_id()` fails:
- Check internet connection
- Verify NORAD ID is correct
- Try manual TLE input
- Check CelesTrak website status

### Propagation errors?

- Ensure TLE is recent (< 7 days old)
- Keep duration < 72 hours
- Check TLE checksum validation
- Verify datetime format
