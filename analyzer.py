import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Antoine Equation parameters: log10(P) = A - (B / (T + C))
# P in mmHg, T in Celsius
ANTOINE_CONSTANTS = {
    "Water": {"A": 8.07131, "B": 1730.63, "C": 233.426, "T_range": [1, 100]},
    "Ethanol": {"A": 8.20417, "B": 1642.89, "C": 230.300, "T_range": [-57, 80]},
    "Acetone": {"A": 7.02447, "B": 1161.0, "C": 224.0, "T_range": [-13, 55]}
}

def calculate_vapor_pressure(compound, temp_celsius_array):
    if compound not in ANTOINE_CONSTANTS:
        raise ValueError(f"Compound '{compound}' not in database.")
    params = ANTOINE_CONSTANTS[compound]
    # Vectorized NumPy calculation
    log_p = params["A"] - (params["B"] / (temp_celsius_array + params["C"]))
    return 10 ** log_p

def analyze_and_plot():
    # Array of temperatures from 10 to 100 deg C
    temperatures = np.linspace(10, 100, 200)
    data = {"Temperature_C": temperatures}

    plt.figure(figsize=(8, 5))
    for compound in ANTOINE_CONSTANTS.keys():
        pressures = calculate_vapor_pressure(compound, temperatures)
        data[f"{compound}_Pressure_mmHg"] = pressures
        plt.plot(temperatures, pressures, label=compound, linewidth=2)

    # 1 atm line (760 mmHg) for normal boiling point reference
    plt.axhline(y=760, color='r', linestyle='--', label="Atmospheric Pressure (760 mmHg)")
    plt.title("Vapor Pressure vs. Temperature (Antoine Formulation)")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Vapor Pressure (mmHg)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("vapor_pressure_curves.png")
    print("[*] Saved equilibrium plot as vapor_pressure_curves.png")

    # Export summary table with Pandas
    df = pd.DataFrame(data)
    sample_summary = df.iloc[::20]  # Every 20th point for clean summary
    sample_summary.to_csv("equilibrium_summary.csv", index=False)
    print("[*] Exported tabular summary to equilibrium_summary.csv")

if __name__ == "__main__":
    analyze_and_plot()
