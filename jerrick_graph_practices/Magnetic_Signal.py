import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# reads a csv file and returns a list of dictionaries, where each dictionary represents a row in the csv file
def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep="\t", keep_default_na=False)
    df["thickness"] = pd.to_numeric(df["thickness"], errors="coerce")
    for col in ["250C", "350C", "375C"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["thickness", "250C", "350C", "375C"])
    return df.to_dict(orient="records")

#graph magnetically dead zones
def plot_magnetically_dead_zone(axis: plt.Axes):
    data = read_csv_to_json('./jerrick_graph_practices/Magnetic_Signal.txt')

    thickness = np.array([d["thickness"] for d in data])
    signal_250C = np.array([d["250C"] for d in data])
    signal_350C = np.array([d["350C"] for d in data])
    signal_375C = np.array([d["375C"] for d in data])
    datasets = [signal_250C, signal_350C, signal_375C]
    labels = ["250°C", "350°C", "375°C"]
    colors = ["black", "blue", "red"] #change to modify colors

    x_fit = np.linspace(min(thickness), max(thickness), 100)

    for y, label, color in zip(datasets, labels, colors):
        axis.scatter(thickness, y, color=color, s=12)
        fit = np.poly1d(np.polyfit(thickness, y, 1))
        x_fit = np.linspace(-2, 2, 300)   # or whatever range includes the intercept
        axis.plot(x_fit, fit(x_fit), label=label, color=color)
    axis.grid(linewidth=0.2, alpha=0.8)
    axis.set_ylim(bottom=0)
    axis.set_xlim(left=0, right=2)
    axis.set_xlabel('Thickness (nm)', fontsize=8)
    axis.set_ylabel('Areal Magnetization\n(emu/cm²)', fontsize=8)
    axis.tick_params(axis='both', which='major', labelsize=8)
    axis.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))
    axis.yaxis.get_offset_text().set_fontsize(8)
    axis.legend(fontsize=8)





#plotting the magnetically dead zone
temperatures = ["250°C", "350°C", "375°C"]
values = [0.74402, 0.399475361, 0.244046793]

fig, ax = plt.subplots(figsize=(6,4))
ax.bar(temperatures, values, width=0.6, color = "black")

ax.set_xlabel("Annealing Temperature (°C)")
ax.set_ylabel("Magnetically dead zone (nm)")


ax.set_ylim(0, 0.8)           # Start y-axis at 0
ax.grid(axis="y", alpha=0.3)
#inset axis
inset_ax = fig.add_axes([0.55, 0.59, 0.3, 0.24]) # x, y, width, height
plot_magnetically_dead_zone(inset_ax)
fig.savefig('jerrick_graph_practices/magnetically_dead_zone.png', dpi=300, transparent=False, bbox_inches='tight')
plt.show()
print("plotted successfully")

#plotting oxygen percentage vs RA
Oxygen_percentage = ["0", "1", "5", "15", "30"]
RA = [110000, 1.18E+05, 9.51E+05, 1.43E+06, 4.13E+06]

plt.figure(figsize=(6,4))
plt.bar(Oxygen_percentage, RA, width=0.4, color = "black")

plt.xlabel("O2%")
plt.ylabel("RA (MΩ μm²)")
plt.grid(axis = "y", alpha=0.3)
plt.savefig('jerrick_graph_practices/Oxygen_percentage_vs_RA.png', dpi=300, transparent=False, bbox_inches='tight')
plt.show()