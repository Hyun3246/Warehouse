import numpy as np
import matplotlib.pyplot as plt
import numpy_financial as npf

rate = 0.05 / 12
nper = 10 * 12
pv = 155000

payment = -npf.pmt(rate, nper, pv)

A = np.linspace(0, nper)
B = -1 * npf.ppmt(rate, A, nper, pv) / payment


plt.plot(A, B)

plt.show()
