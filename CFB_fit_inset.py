import numpy as np
import matplotlib.pyplot as plt

# 1. Experimental Data (Extracted from the image)
n_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
heb_data = np.array([67.4, 61.3, 58.2, 56.5, 55.4, 54.6, 54.0, 53.5, 53.1, 52.8])

# 2. Parameters from Fit
gamma = 4.01e-04
h_inf = 42.44

# 3. Generate Recursive Fit Curve
# The Binek model: H_eb(n+1) = H_eb(n) - gamma * (H_eb(n) - H_inf)^3
fit_n = np.arange(1, 11)
fit_heb = [heb_data[0]]  # Start the recursion at the first data point

for i in range(len(fit_n) - 1):
    h_next = fit_heb[-1] - gamma * (fit_heb[-1] - h_inf)**3
    fit_heb.append(h_next)

# 4. Plotting
plt.scatter(n_data, heb_data, color='black', s=80, label='Experimental Data', zorder=5)
plt.plot(fit_n, fit_heb, color='red', linestyle='--', linewidth=2.5,
         label=f'Binek Recursive Fit ($\\gamma$ = {gamma:.2e})')

# Formatting labels and grid
plt.xlabel('Cycle number ($n$)', fontsize=12)
plt.ylabel('Exchange Bias Field $H_{EB}$ (Oe)', fontsize=12)
plt.title('Exchange Bias Training Effect: NiO/FM Interface', fontsize=14)
plt.legend(frameon=True, shadow=True)
plt.grid(True, linestyle=':', alpha=0.6)

# Save the figure
plt.show()