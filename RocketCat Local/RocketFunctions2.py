
#%%import modules
import numpy as np
import matplotlib.pyplot as plt
import math
import time 

#%% FREESTREAM PRESSURE FUNCTIONS

def Pressure_infinite(Altitude):

    Pressure_inf = np.zeros(len(Altitude))
    
    Temperature_SL = 288 #[K]
    Pressure_SL = 101000 #[Pa]
    M = 0.02869 #kg/mol - molar mass of dry air
    g = 9.81 #[m/s^2]
    R = 8.314 #J/mol - universal gas constant
    
    #Calculating the pressure at every altitude iterating over the altitude
    for i in range(len(Altitude)):
        
        if Altitude[i] < 11000: #Troposphere
            
            Pressure_inf[i] = Pressure_SL*(1-((0.0062*(Altitude[i]))/Temperature_SL))**5.2561
            
        elif Altitude[i] < 50000: #Stratosphere
            
            Pressure_inf[i] = 28244 * np.exp((-g*M*(Altitude[i]-11000))/(R*220))
            
        elif Altitude[i] < 85000: #Mesosphere
            
            Pressure_inf[i] = 81.56 * (np.exp((-g*M*(Altitude[i]-50000))/(R*220)))
            
        else:
        
            Pressure_inf[i] = 0 #approximately a vaccuum at this point.. :D
            
    return Pressure_inf

#Rate of change of the freestream pressure within earths atmosphere
def ROC_Pressure_infinite(Pressure_inf,Altitude,Altitude_Step): #CENTRAL FINITE DIFFERENCE
  
    dx = 1
    x = Altitude
    fun = Pressure_inf
    
    df_cen = np.zeros(len(x))    # initialize f' vector as zeros
    for i in range(len(x)-1):    # step through INDICES of x
        df_cen[i] = (fun[i+dx]-fun[i-dx])/(2*dx)
    return df_cen

#%% NOZZLE GEOMETRY ALGORITHM

#Nozzle Geometry - Radius
def nozzle_geometry(x,xthroat,xexit,Din,Dexit,Dthroat):
    
    nozzle_rad = np.zeros(len(x))
    
    for i in range(len(x)): #iterating over the length of the nozzle
    
        if x[i] < xthroat: #converging section
            
            rad_slope = (Din/2 - Dthroat/2)/(0-xthroat)
            
            nozzle_rad[i] =  rad_slope*x[i] + ((Din/2))
            
        elif x[i] == xthroat:
            
            nozzle_rad[i] = Dthroat/2
        
        else:
        
            rad_slope = (Dthroat/2 - Dexit/2)/(xthroat-xexit) 
            
            nozzle_rad[i] = rad_slope*(x[i]-xthroat) + Dthroat/2
            
    return nozzle_rad #returns the nozzle radius vector

#%% MACH NUMBER FINDING ALGORITHMS

#Root finding algorithm to estimate mach number at every point along the nozzle
def bisection_root_finder(the_function,xL,xU,ea,rad,gamma,Mass_Flux,P_inlet,T_inlet,R):
    #Mach_Equation,xL,xU,ea,nozzle_rad[i],gamma,Mass_Flux,P_inlet,T_inlet,R


    error = 100                # initialize error as something large
    iteration = 1              # initialize iteration counter (optional)

    while error > ea: 
        func_xL = the_function(xL,rad,gamma,R,Mass_Flux,P_inlet,T_inlet)              # eval function @ xL
        func_xU = the_function(xU,rad,gamma,R,Mass_Flux,P_inlet,T_inlet)              # eval function @ xU
        
        # estimate "old" root based on technique
        xr_old = ((xL+xU)/2)                       # bisection
        
        func_xr_old = the_function(xr_old,rad,gamma,R,Mass_Flux,P_inlet,T_inlet)      # eval function @ "old" root
        test_sign = (func_xL * func_xr_old)            # find product to determine the sign
   
        # check sign and decide what to do
        if test_sign < 0:
            xU = xr_old
        elif test_sign > 0:
            xL = xr_old
        else:
            xr_new = xr_old
            break
    
        # estimate "new" root based on technique
        xr_new = (xL+xU)/2                               # bisection

        # compare difference betwee "new" and "old" roots
        error = abs((xr_new - xr_old)/(xr_new)) * 100
        
        # increment iteration counter
        iteration = iteration + 1

    root = xr_new
    #print("iterations =",iteration-1)
    return root

def Mach_Equation(M,rad,gamma,R,Mass_Flux,P_inlet,T_inlet): #Area to Throat Area relationship to the mach number
    
    #current area
    A = (rad)**2 * math.pi
    
    #Area mach function equation with area ratio subtracted to other side
    Mach_Function = ((A*P_inlet)/math.sqrt(T_inlet))*math.sqrt(gamma/R)*M*(1+(((gamma-1)/2)*(M**2)))**(-(gamma+1)/(2*(gamma-1))) - Mass_Flux
    
    return Mach_Function

def Mach_Vector(Mach_Equation,gamma,nozzle_rad,x,xthroat,Mass_Flux,P_inlet,T_inlet,R): #calculates the mach number at every point along the rocket nozzle
    
    Mach_Vec = np.zeros(len(nozzle_rad))
    
    for i in range(len(nozzle_rad)):
        
        if x[i] < xthroat:
            
            xL = 0.001
            xU = 0.99999 #bounds for subsonic region
            ea = 0.0001
    
            Mach_Vec[i] = bisection_root_finder(Mach_Equation,xL,xU,ea,nozzle_rad[i],gamma,Mass_Flux,P_inlet,T_inlet,R)
            
        elif x[i] == xthroat:
            
            Mach_Vec[i] = 1
            
        elif x[i] > xthroat:
            
            xL = 1.01
            xU = 10 #bounds for supersonic region
            ea = 0.0001
            
            Mach_Vec[i] = bisection_root_finder(Mach_Equation,xL,xU,ea,nozzle_rad[i],gamma,Mass_Flux,P_inlet,T_inlet,R)
        
    return Mach_Vec

#%% TEMPERATURE, PRESSURE, and DENSITY FINING ALGORITHMS

#flow property calculations
def TPRhoV(Mach_Vec,T_inlet,P_inlet,Rho_inlet,gamma,R,rad,Mass_Flux):
    
    Flow_Properties = np.zeros((5,len(Mach_Vec)))
    
    a = np.zeros(len(Mach_Vec))
    
    #All fow properties contained within single matrix
    Mach_Num = Flow_Properties[0,:]
    Temperature = Flow_Properties[1,:]
    Pressure = Flow_Properties[2,:]
    Density = Flow_Properties[3,:]
    Velocity = Flow_Properties[4,:]
    
    #Mach Number
    for i in range(len(Mach_Vec)):
        
        Mach_Num[i] = Mach_Vec[i] #inputs the mach number for every point into the mach number row
    
    #Temperature, pressure, density and velocity
    for i in range(len(Mach_Vec)):
        
        if i ==0:
            
            #inlet conditions
            Temperature[0] = T_inlet
            Pressure[0] = P_inlet
            Density[0] = Rho_inlet
            Velocity[0] = 0 #stagnation
            
        else:
            
            Temperature[i] = T_inlet*(1+(0.5*(gamma-1)*(Mach_Num[i])**2))**(-1)
            Pressure[i] = P_inlet*(1+(0.5*(gamma-1)*(Mach_Num[i])**2))**(-gamma/(gamma-1))            
            Density[i] = Pressure[i]/(R*Temperature[i])
            Velocity[i] = Mass_Flux/(Density[i]*(math.pi*rad[i]**2)) #continuity
        
    return Flow_Properties

#%% THRUST FUNCTION

#thrust calculations
def Thrust_Function(Velocity,Pressure,D_exit,Pressure_inf,Altitude,Mass_Flux):
    
    Thrust = np.zeros(len(Altitude)) #initializing thrust vector

    #Exhaust conditions
    Exhaust_Velocity = Velocity[-1]
    Exhaust_Pressure = Pressure[-1]
    Exhaust_Area = ((D_exit/2)**2) * math.pi
            
    for i in range(len(Altitude)):
        
        #iterating over every ith freestream pressure value
        Thrust[i] = (Mass_Flux*(Exhaust_Velocity))+((Exhaust_Pressure-Pressure_inf[i])*Exhaust_Area)
        
    return Thrust