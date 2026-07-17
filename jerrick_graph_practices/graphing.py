import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_path = "300K_TMR.txt"
output_path = "300K_TMR.png"

def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep="\t", keep_default_na=False)
    return df.to_dict(orient="records")


data = read_csv_to_json(data_path)

data_low_temp = data[1:2819]  # Skip the first row (header)


H = np.array([d["Magnetic Field (Oe)"] for d in data_low_temp])
M = np.array([d["Resistance (Ohms)"] for d in data_low_temp])

plt.scatter(H, M)
plt.xlabel('Magnetic Field (Oe)')
plt.ylabel('Resistance (Ohms)')
plt.grid()
plt.savefig(output_path, dpi=300, transparent=False, bbox_inches='tight')
plt.show()
