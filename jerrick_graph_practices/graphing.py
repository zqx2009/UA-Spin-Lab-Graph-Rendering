import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#reads a csv file and returns a list of dictionaries, where each dictionary represents a row in the csv file
def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep="\t", keep_default_na=False) #skips 1 row of header
    return df.to_dict(orient="records")

#graphs the resistance vs field data from a csv file and saves the graph to a specified output path
def graph_Res(data_path, output_path,color="black"): #choose color of line, default is black
    data = read_csv_to_json(data_path)
    data_low_temp = data[1:-1]
    H = np.array([d["Field (T)"] for d in data_low_temp])
    M = np.array([d["Resistance (Ohms)"] for d in data_low_temp])
    plt.clf()
    plt.plot(H, M, color=color, marker='s', markersize=3)
    plt.xlabel('Field (T)')
    plt.ylabel('Resistance (Ohms)')
    plt.legend()
    plt.grid()
    plt.savefig(output_path, dpi=300, transparent=False, bbox_inches='tight')
    plt.show()

def plot_inset_heff_num_loop(axis):
    num_loops = [1,2,3,4,5,6]
    heff_2 = [16.5, 16, 14.9, 13.75, 16.5, 13.5]
    heff_1 = [66, 56, 56, 56, 56, 56]
    axis.plot(num_loops, heff_1, marker = 'o', markersize = 3, color="black")
    axis.plot(num_loops, heff_2, marker = 's', markersize = 3, color="red")
    axis.grid(linewidth=0.2, alpha=0.8)
    axis.set_xlabel('Number of Loops', fontsize=8)
    axis.set_ylabel(r'$H_{\mathrm{eff}}$ (Oe)', fontsize=8)
    axis.set_xticks(np.arange(1, 7, 1))
    axis.set_xlim(0, 6.5)
    axis.tick_params(axis='both', which='major', labelsize=8)


graph_Res('./jerrick_graph_practices/300K_TMR.txt', './jerrick_graph_practices/300K_TMR.png')
graph_Res('./jerrick_graph_practices/2K_TMR.txt', './jerrick_graph_practices/2K_TMR.png', color="red")

data = read_csv_to_json('./jerrick_graph_practices/300K_TMR.txt')
data = data[1061:-1]  # Adjust the slice as needed
data_low_temp = [d for d in data if d["Field (T)"] > -400 and d["Field (T)"] < 400]
H = np.array([d["Field (T)"] for d in data_low_temp])
M = np.array([d["Resistance (Ohms)"] for d in data_low_temp])
plt.clf()
plt.plot(H, M, color='black', marker='s', markersize=3, label = '300K')
plt.legend()
data = read_csv_to_json('./jerrick_graph_practices/2K_TMR.txt')
data = data[1061:-1]  # Adjust the slice as needed
data_low_temp = [d for d in data if d["Field (T)"] > -400 and d["Field (T)"] < 400]
H = np.array([d["Field (T)"] for d in data_low_temp])
M = np.array([d["Resistance (Ohms)"] for d in data_low_temp])
plt.plot(H, M, color='red', marker='s', markersize=3, label = '2K')
plt.legend()

plt.xlabel('Field (T)')
plt.ylabel('Resistance (Ohms)')
plt.grid()
plt.savefig('jerrick_graph_practices/combined_graph.png', dpi=300, transparent=False, bbox_inches='tight')
plt.show()



#plotting the Heff vs temperature data
plt.clf()
# Dataset 1
temp1 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
heff1 = [25, 22, 16, 13, 10, 10, 10, 5, 0]

# Dataset 2
temp2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
heff2 = [61, 31, 21, 13, 2, 2, 2, 2, 0, 2]
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(temp1, heff1, 'o-', label='Dataset 1', color = 'black')
ax.plot(temp2, heff2, 's-', label='Dataset 2', color = 'red')

ax.set_xlabel('Temperature (K)')
ax.set_ylabel(r'$H_{\mathrm{eff}}$ (Oe)')
#plt.title(r'Effective Field vs. Temperature')
ax.legend(loc='lower left')
ax.grid(True)

#inset axis
inset_ax = fig.add_axes([0.45, 0.55, 0.4, 0.3]) # x, y, width, height
plot_inset_heff_num_loop(inset_ax)
fig.savefig('jerrick_graph_practices/heff_vs_temperature.png', dpi=300, transparent=False, bbox_inches='tight')
plt.show()
print("plotted successfully")

