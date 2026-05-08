import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy.optimize import curve_fit

CFB_hysteresis_data_path = "CFB_hysteresis.txt"
Hexc_vs_cicle_data_path = "CFB_Hexc_vs_cicle.txt"
output_path = "CFB_hysteresis.png"

sample_volume = 1.334e-7
gamma_guess = 1.2e-05

def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep='\t', keep_default_na=False)      # keep_default_na = True: return NaN if empty; keep_default_na = False: return '' if empty
    return df.to_dict(orient='records')

def hexc_n_model(cycle, k, C1, h_inf):
    return 1 / np.sqrt(2 * k * cycle + C1) + h_inf

def find_best_fit(cycle_list, hexc):
    # Set initial guesses for [gamma, C1, h_inf]
    # A good h_inf guess is the minimum value of your y data if it levels off
    h_inf_guess = np.min(hexc)
    p0 = [gamma_guess, 1/(hexc[0] - h_inf_guess)**2 - 2 * gamma_guess, h_inf_guess]
    try:
        popt, pcov = curve_fit(hexc_n_model, cycle_list, hexc, p0=p0)
        k, C1_fit, h_inf = popt

        print(f"Best fit values:\nk = {k}\nC1 = {C1_fit}\nh_inf = {h_inf}")
    except RuntimeError:
        print("Fit could not be found. Try adjusting the initial guesses (p0).")
        quit()

    """ Approximate gamma """
    h1 = hexc_n_model(1, k, C1_fit, h_inf)
    h2 = hexc_n_model(2, k, C1_fit, h_inf)

    gamma = (h1 - h2) / (h1 - h_inf) ** 3
    print(f"gamma = {gamma}")

    return gamma, h_inf

def draw_CFB_hysteresis(axis: plt.Axes):
    CFB_hysteresis_data = read_csv_to_json(CFB_hysteresis_data_path)

    H = np.array([d["Magnetic Field (Oe)"] for d in CFB_hysteresis_data])
    Moment = np.array([d["Moment (emu)"] for d in CFB_hysteresis_data])

    Magnetization = Moment / sample_volume

    axis.plot(H, Magnetization, color="black", marker='s')
    axis.set_xlabel('Magnetic Field (Oe)')
    axis.set_ylabel('Magnetization (emu/cm$^3$)')
    axis.grid(linewidth = 0.3)

def draw_Hexc_vs_cicle(axis: plt.Axes):
    Hexc_vs_cicle_data = read_csv_to_json(Hexc_vs_cicle_data_path)

    cycle = np.array([d["Number of Cycles"] for d in Hexc_vs_cicle_data])
    Hc_minus = np.array([d["Hc -"] for d in Hexc_vs_cicle_data])
    Hc_plus = np.array([d["Hc +"] for d in Hexc_vs_cicle_data])

    Hexc = abs(Hc_minus + Hc_plus) / 2

    axis.plot(cycle, Hexc, color = "red", marker='s', markersize=3, linewidth = 1, label="Data")
    axis.set_xlabel("Cycle number ($n$)")
    axis.set_ylabel("$H_{EB}$ (Oe)")
    axis.set_ylim(150, 400)
    axis.grid(linewidth = 0.2)

    return Hexc, cycle

def draw_Binek_model(axis: plt.Axes, Hexc, cycle_list):
    gamma, h_inf = find_best_fit(cycle_list[:-1], Hexc[:-1])
    # 2. Parameters from Fit
    gamma = 7.03e-06
    h_inf = 124

    # 3. Generate Recursive Fit Curve
    # The Binek model: H_eb(n+1) = H_eb(n) - gamma * (H_eb(n) - H_inf)^3
    fit_n = np.arange(1, np.max(cycle_list))
    fit_heb = [Hexc[0]]  # Start the recursion at the first data point

    for i in range(len(fit_n) - 1):
        h_next = fit_heb[-1] - gamma * (fit_heb[-1] - h_inf)**3
        fit_heb.append(h_next)

    axis.plot(fit_n, fit_heb, color = "blue", marker='s', markersize=3, linewidth = 1, label=f"Fit $\\gamma={gamma:.2e}$")
    axis.legend()

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(6, 4))

    # CFB Hysteresis
    draw_CFB_hysteresis(ax)

    # Exchange bias vs cicle
    ax_inset = ax.inset_axes([0.73, 0.15, 0.25, 0.3])
    Hexc, cycle_list = draw_Hexc_vs_cicle(ax_inset)

    draw_Binek_model(ax_inset, Hexc, cycle_list)

    plt.savefig(output_path, dpi=300, transparent=False, bbox_inches='tight')
    plt.show()
