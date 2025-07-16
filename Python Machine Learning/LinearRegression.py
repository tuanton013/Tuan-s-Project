import numpy as np
import math
import random
import matplotlib.pyplot as plt

# Generate random data
X = [4, 5, 10, 12, 13, 14, 24, 25, 30, 31, 32, 33,
     34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
y = [1, 2, 3, 6, 7, 8, 9, 11, 15, 16, 17, 18,
     19, 20, 21, 22, 23, 26, 27, 28, 29, 46, 47, 48]

# Convert to numpy arrays for efficient operations
X = np.array(X)
y = np.array(y)
X_square = X**2  # More efficient than list comprehension

plt.scatter(X, y)

# Create feature matrix using numpy operations
X_features = np.column_stack([X_square, X, np.ones(len(X))])

# Normal equation solution (more efficient)
coefficients = np.linalg.inv(X_features.T @ X_features) @ X_features.T @ y
print("Coefficients:", coefficients)

# Prediction
x_buffer = np.linspace(1, 50, 10000)
y_buffer = coefficients[0]*x_buffer**2 + coefficients[1]*x_buffer + coefficients[2]

plt.plot(x_buffer, y_buffer, color='red')
plt.title('Quadratic Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.show()

# Calculate R-squared
y_pred = X_features @ coefficients
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"R-squared: {r_squared:.4f}")
