import numpy as np
import matplotlib.pyplot as plt

A = np.arange(0, 1)
B = np.arange(-1, 0)

plt.plot(A, np.sqrt(1-(A**2)))
plt.plot(A, -np.sqrt(1-(A**2)))
plt.plot(B, np.sqrt(1-B**2))
plt.plot(B, -np.sqrt(1-B**2))

plt.show()