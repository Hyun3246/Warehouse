from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

ua = np.linspace(0, 2 * np.pi, 100)
va = np.linspace(0, np.pi, 100)
X = 10 * np.outer(np.cos(ua), np.sin(va))
Y = 10 * np.outer(np.sin(ua), np.sin(va))
Z = 10 * np.outer(np.ones(np.size(ua)), np.cos(va))

ax.plot_surface(X, Y, Z, color = 'w')
plt.show()
