import matplotlib.pyplot as plt
import numpy as np

save_graph_file_path = "Hc_Temp_double_lines.png"
separator = "\t"

# Data points

def read_data(data_file_path):
    with open(data_file_path, "r") as data_file:
        data_str = data_file.read()

    xpoints = []
    ypoints = []

    for data_row_str in data_str.split("\n")[1:]:
        data_row = data_row_str.split(separator)
        xpoints.append(float(data_row[2][:-1]))     # [:-1] to remove 'K'
        ypoints.append((float(data_row[0]) + float(data_row[1])) / 2)    # take the absolute value of the exchange bias

    return np.array(xpoints), np.array(ypoints)


if __name__ == "__main__":
    xpoints, ypoints = read_data("Hc_Temp_1.txt")
    plt.plot(xpoints, ypoints, color = "red", marker='s')

    xpoints, ypoints = read_data("Hc_Temp_2.txt")
    plt.plot(xpoints, ypoints, color = "blue", marker='s')
    # plt.legend()      # Show legend
    plt.xlabel("Temperature (K)")
    plt.ylabel("Exchange bias (Oe)")
    plt.ylim(-400, 400)
    plt.grid(True)
    plt.savefig(save_graph_file_path, dpi=300, transparent=False, bbox_inches='tight')
    plt.show()
