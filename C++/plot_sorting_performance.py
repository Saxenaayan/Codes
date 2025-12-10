import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("sorting_results_int.csv")  # or sorting_results_int.csv

# Plot CPU vs OpenMP sorting time
plt.figure(figsize=(8, 5))
plt.plot(df["ArraySize"], df["CPUTime"], marker='o', label="CPU (Single Thread)")
plt.plot(df["ArraySize"], df["OpenMPTime"], marker='o', label="OpenMP (Parallel)")

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Array Size (log scale)")
plt.ylabel("Execution Time (s, log scale)")
plt.title("CPU vs OpenMP Sorting Performance")
plt.legend()
plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.show()

# Plot Speedup
plt.figure(figsize=(6, 4))
plt.plot(df["ArraySize"], df["Speedup"], marker='s', color='green')
plt.xscale('log')
plt.xlabel("Array Size (log scale)")
plt.ylabel("Speedup (CPU Time / OpenMP Time)")
plt.title("Speedup Achieved with OpenMP Parallel Sorting")
plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.show()
