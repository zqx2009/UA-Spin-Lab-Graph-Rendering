import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#reads a csv file and returns a list of dictionaries, where each dictionary represents a row in the csv file
def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep="\t", keep_default_na=False) 
    return df.to_dict(orient="records")

def graph_RA(data_path,color="black", temp=None): #choose color of line, default is black
    data = read_csv_to_json(data_path)
    data_temp = [d for d in data if d["Temp (C)"] == temp]
    Row_num = np.array([d["Row number"] for d in data_temp])
    RA = np.array([d["RA"] for d in data_temp])
    # transform row numbers using f(x) = 1.9 + (x/200)*2.8
    if Row_num.size > 0:
        x_trans = 1.9 + (Row_num / 200.0) * 2.8
    else:
        x_trans = Row_num.astype(float)
    plt.scatter(x_trans, RA, color=color, s=12, label=f"{temp}°C")
    # add average horizontal line for this temperature's RA values
    if RA.size > 0:
        avg = np.mean(RA)
        plt.axhline(avg, color=color, linestyle='--', linewidth=1)
        # annotate the average value near the right edge of transformed x
        x_pos = x_trans.max() if x_trans.size > 0 else 0
        plt.text(x_pos, avg, f"  avg={avg:.2g}", va='center', ha='left', color=color)

    plt.xlabel('NiO Thickness (nm)')
    plt.yscale('log')
    plt.ylabel('RA (MΩ μm$^2$)')  
    
    plt.grid()
    plt.show()

graph_RA('./jerrick_graph_practices/A829P_RA.txt', color="black", temp=350)

plt.legend()
plt.savefig('./jerrick_graph_practices/A829P_RA.png', dpi=300, transparent=False, bbox_inches='tight')

