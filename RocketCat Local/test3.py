import numpy as np
from scipy.optimize import fsolve

# === CONSTANTS (Set Here) ===
gamma = 1.2               # Specific heat ratio
R = 300                   # Specific gas constant [J/kg-K]
P0 = 7_000_000.0          # Stagnation pressure [Pa]
T0 = 3500.0               # Stagnation temperature [K]
mdot = 2400            # 🔒 Fixed mass flow rate [kg/s]
Dthroat = 0.800           # Throat diameter [m]

# === FUNCTIONS ===

# Isentropic mass flow function
def mass_flow(M, A):
    if M <= 0:
        return 0
    term = M * (1 + (gamma - 1) / 2 * M**2) ** (-(gamma + 1) / (2 * (gamma - 1)))
    return A * P0 * np.sqrt(gamma / (R * T0)) * term

# Solver for Mach number given area and mdot
def solve_mach(A, mdot):
    def residual(M): return mass_flow(M, A) - mdot

    M_sub, M_sup = None, None

    try:
        M_sub = fsolve(residual, 0.2)[0]
        if M_sub <= 0 or np.isnan(M_sub):
            M_sub = None
    except:
        M_sub = None

    try:
        M_sup = fsolve(residual, 2.5)[0]
        if M_sup <= 1.0 or np.isnan(M_sup):
            M_sup = None
    except:
        M_sup = None

    return M_sub, M_sup

# === MAIN ===
if __name__ == "__main__":
    D = float(input("Enter diameter (m): "))
    A = np.pi * (D / 2)**2

    print(f"\nUsing fixed mass flow rate: {mdot:.2f} kg/s")
    print(f"Input Area: {A:.6f} m²")

    M_sub, M_sup = solve_mach(A, mdot)

    if M_sub:
        print(f"Subsonic Mach:    {M_sub:.4f}")
    else:
        print("Subsonic Mach:    ❌ No valid root")

    if M_sup:
        print(f"Supersonic Mach:  {M_sup:.4f}")
    else:
        print("Supersonic Mach:  ❌ No valid root")
