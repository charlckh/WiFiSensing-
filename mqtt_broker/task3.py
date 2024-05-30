## the algorithm used in task4 is exported in here 
# Algorithm for task 3

import pickle
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np




def task_3_localization(rssi_values, ap_locations, n=7, A =50):
    #n is the environment exponenet, referenced from websites and founded by plotting regression graph
    distances = A * ((- rssi_values) / (10 * n))  # convert RSSI to distance 

    if np.any(np.isnan(distances)) or np.any(np.isinf(distances)):
        #print(f'Warning: Invalid distances calculated from RSSI values: {rssi_values}')
        return None
    return estimate_position(distances, ap_locations)

def estimate_position(distances, ap_locations):
    def error(x, c, r):
        return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

    x0 = np.array([0.0, 0.0])  # Initial guess for the client's location'

    return minimize(error, x0, args=(ap_locations, distances), method='Nelder-Mead').x