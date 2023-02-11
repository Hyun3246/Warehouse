import numpy as np
import matplotlib.pyplot as plt

A = np.arange(0, 10)

plt.plot(A, A**2)
plt.plot(A, A**3)
plt.plot(A, np.log2(A))

plt.show()
