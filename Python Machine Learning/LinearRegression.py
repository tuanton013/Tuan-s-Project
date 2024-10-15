import numpy as np
import math
import random

import matplotlib.pyplot as plt

# Generate random data
X = [4, 5, 10, 12, 13, 14, 24, 25, 30, 31, 32, 33,
     34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
y = [1, 2, 3, 6, 7, 8, 9, 11, 15, 16, 17, 18,
     19, 20, 21, 22, 23, 26, 27, 28, 29, 46, 47, 48]
X_quare = [x**2 for x in X]

plt.scatter(X, y)

# Transform data to numpy arrays and transpose
X = np.array([X]).T
X_quare = np.array([X_quare]).T

# create a column of ones
ones = np.ones((len(X), 1), dtype=int)

# Combine the ones with the X values
X = np.hstack((X_quare, X))
X = np.hstack((X, ones))

x = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.T, X)), X.T), y)
print(x)
# x = [[a],
#      [b],
#      [c]] where y = aX^2 + bX + c


x_buffer = np.linspace(1, 50, 10000)
y_buffer = x[0]*x_buffer**2 + x[1]*x_buffer + x[2]

plt.plot(x_buffer, y_buffer, color='red')
plt.show()
