import numpy as np
import math

def Mach_Equation(M, rad, gamma, R, Mass_Flux, P_inlet, T_inlet):
    A = (rad)**2 * math.pi
    term = (1 + ((gamma - 1)/2) * M**2)
    return A * P_inlet * np.sqrt(gamma / (R * T_inlet)) * M * term ** (-(gamma + 1) / (2 * (gamma - 1))) - Mass_Flux

def bisection_root_finder(func, xL, xU, tol, rad, gamma, Mass_Flux, P_inlet, T_inlet, R):
    error = 100
    while error > tol:
        f_xL = func(xL, rad, gamma, R, Mass_Flux, P_inlet, T_inlet)
        f_xU = func(xU, rad, gamma, R, Mass_Flux, P_inlet, T_inlet)
        xr_old = (xL + xU) / 2
        f_xr_old = func(xr_old, rad, gamma, R, Mass_Flux, P_inlet, T_inlet)
        if f_xL * f_xr_old < 0:
            xU = xr_old
        elif f_xL * f_xr_old > 0:
            xL = xr_old
        else:
            return xr_old
        xr_new = (xL + xU) / 2
        error = abs((xr_new - xr_old) / xr_new) * 100
    return xr_new

def find_all_roots(rad, Mass_Flux, gamma=1.2, R=300, P_inlet=7e6, T_inlet=3500, M_min=0.01, M_max=10, num_points=1000, tol=1e-6):
    def func(M, r, g, Rv, mf, P, T):
        return Mach_Equation(M, r, g, Rv, mf, P, T)
    M_vals = np.linspace(M_min, M_max, num_points)
    f_vals = [func(M, rad, gamma, R, Mass_Flux, P_inlet, T_inlet) for M in M_vals]

    roots = []
    for i in range(len(M_vals) - 1):
        if f_vals[i] * f_vals[i+1] < 0:
            root = bisection_root_finder(func, M_vals[i], M_vals[i+1], tol, rad, gamma, Mass_Flux, P_inlet, T_inlet, R)
            roots.append(root)
        elif abs(f_vals[i]) < tol:
            roots.append(M_vals[i])

    # Remove duplicates
    roots_unique = []
    roots.sort()
    for r in roots:
        if all(abs(r - ru) > tol for ru in roots_unique):
            roots_unique.append(r)

    return roots_unique

# Example usage:
if __name__ == "__main__":
    nozzle_radius = 0.15  # input your nozzle radius here [m]
    mass_flow_rate = 2000  # input mass flow rate [kg/s]

    mach_roots = find_all_roots(nozzle_radius, mass_flow_rate)
    print(f"Mach roots for radius = {nozzle_radius} m and mass flow = {mass_flow_rate} kg/s:")
    for m in mach_roots:
        print(f"{m:.6f}")
