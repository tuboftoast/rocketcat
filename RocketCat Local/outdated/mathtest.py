import numpy as np
import matplotlib.pyplot as plt
import math

# Nozzle Geometry Function
def nozzle_geometry(x, xthroat, xexit, Din, Dexit, Dthroat):
    nozzle_rad = np.zeros(len(x))
    for i in range(len(x)):
        if x[i] < xthroat:
            rad_slope = (Din/2 - Dthroat/2)/(0 - xthroat)
            nozzle_rad[i] = rad_slope * x[i] + (Din/2)
        elif x[i] == xthroat:
            nozzle_rad[i] = Dthroat/2
        else:
            rad_slope = (Dthroat/2 - Dexit/2)/(xthroat - xexit)
            nozzle_rad[i] = rad_slope * (x[i] - xthroat) + Dthroat/2
    return nozzle_rad

# Mach Equation for root finder
def Mach_Equation(M, rad, gamma, R, Mass_Flux, P_inlet, T_inlet):
    A = (rad)**2 * math.pi
    term = (1 + ((gamma - 1)/2) * M**2)
    func = A * P_inlet * np.sqrt(gamma / (R * T_inlet)) * M * term ** (-(gamma + 1) / (2 * (gamma - 1))) - Mass_Flux
    return func

# Bisection root finder
def bisection_root_finder(the_function, xL, xU, ea, rad, gamma, Mass_Flux, P_inlet, T_inlet, R):
    error = 100
    while error > ea:
        func_xL = the_function(xL, rad, gamma, R, Mass_Flux, P_inlet, T_inlet)
        func_xU = the_function(xU, rad, gamma, R, Mass_Flux, P_inlet, T_inlet)
        xr_old = (xL + xU) / 2
        func_xr_old = the_function(xr_old, rad, gamma, R, Mass_Flux, P_inlet, T_inlet)
        test_sign = func_xL * func_xr_old
        if test_sign < 0:
            xU = xr_old
        elif test_sign > 0:
            xL = xr_old
        else:
            return xr_old
        xr_new = (xL + xU) / 2
        error = abs((xr_new - xr_old) / xr_new) * 100
    return xr_new

# Calculate Mach Vector
def Mach_Vector(Mach_Equation, gamma, nozzle_rad, x, xthroat, Mass_Flux, P_inlet, T_inlet, R):
    Mach_Vec = np.zeros(len(nozzle_rad))
    for i in range(len(nozzle_rad)):
        if x[i] < xthroat:
            xL = 0.01
            xU = 1.0
            ea = 0.0001
            Mach_Vec[i] = bisection_root_finder(Mach_Equation, xL, xU, ea, nozzle_rad[i], gamma, Mass_Flux, P_inlet, T_inlet, R)
        elif x[i] == xthroat:
            Mach_Vec[i] = 1.0
        else:
            xL = 1.0
            xU = 10.0
            ea = 0.0001
            Mach_Vec[i] = bisection_root_finder(Mach_Equation, xL, xU, ea, nozzle_rad[i], gamma, Mass_Flux, P_inlet, T_inlet, R)
    return Mach_Vec

# Parameters
Gamma = 1.2
R = 300
P0 = 7e6
T0 = 3500
Mass_Flux = 2000  # Adjust this mass flow rate as needed (kg/s)
Din = 2.0
Dthroat = 0.357
Dexit = 2.4
xthroat = 0.55
xexit = 4.0

# Axial positions
x = np.linspace(0, xexit, 500)

# Calculate nozzle radius
nozzle_rad = nozzle_geometry(x, xthroat, xexit, Din, Dexit, Dthroat)

# Calculate Mach numbers
Mach = Mach_Vector(Mach_Equation, Gamma, nozzle_rad, x, xthroat, Mass_Flux, P0, T0, R)

# Plot Mach number vs radius
plt.figure(figsize=(10,6))
plt.plot(nozzle_rad, Mach, label='Mach Number')
plt.xlabel('Nozzle Radius (m)')
plt.ylabel('Mach Number')
plt.title('Mach Number vs Nozzle Radius')
plt.grid(True)
plt.legend()
plt.show()
