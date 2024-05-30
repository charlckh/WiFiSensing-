import pickle
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np
from sklearn.linear_model import LinearRegression

# Split dataset into training set and test set


# Open the pickle file and load the data
with open('data_env1.pickle', 'rb') as f:
    data = pickle.load(f)

with open('data_env2.pickle', 'rb') as f:
    data2 = pickle.load(f)


rssi_values = data['rssi']
label = data['labels']
ap_locations = data['ap']

y1 = rssi_values.reshape(-1, 1)

x1 = []


rssi_values2 = data2['rssi']
label2 = data2['labels']
ap_locations2 = data2['ap']

y2 = rssi_values2.reshape(-1, 1)
x2 = []

errors = []
error2 = []

def plot(x,y):
    print("plotting")
    x_squared = []
    for i in range(len(x)):
        if x[i] is None:
            continue
        x_squared.append(x[i]**2)

    
    xy = x * y

    n = len(x)
    w = (n * np.sum(xy) - np.sum(x) * np.sum(y)) / (n * np.sum(x_squared) - np.sum(x) ** 2)
    b = (np.sum(y) - w * np.sum(x)) / n

    print(f"Slope (w): {w[0][0]:.6f}")
    print(f"Intercept (b): {b[0]:.6f}")

    # Create a linear regression model using scikit-learn
    linreg = LinearRegression().fit(x, y)
    print(f"Intercept from sklearn: {linreg.intercept_[0]:.6f}")
    print(f"Slope from sklearn: {linreg.coef_[0][0]:.6f}")

    # Visualize the data and regression line
    plt.scatter(x, y, color='blue', label='Data')
    plt.plot(x, linreg.predict(x), color='red', label='Regression Line')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Least Squares Linear Regression")
    plt.legend()
    plt.show()
    plt.savefig('regression.png')




# Algorithm for task 3
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


# Loop over all sets of RSSI measurements for data set 1
for i in range(len(rssi_values)):
    # Estimate the client's location

    estimated_location = task_3_localization(rssi_values[i], ap_locations)
    x1.append(estimated_location)
    if estimated_location is None:
        continue

    
    # Calculate the error
    error = np.linalg.norm(estimated_location - label[i])
    errors.append(error)

# plot(x1, y1)

# Calculate the mean error
mean_error = np.mean(errors)
median_error = np.median(errors)

print(f'Data Set 1 Mean error: {mean_error}')
print(f'Data Set 1 Median error: {median_error}')

plt.hist(errors, bins='auto', density=True, cumulative=True, label='CDF',
         histtype='step', alpha=0.8, color='k')
plt.title('CDF of Error for data set 1 ')
plt.xlabel('Error')
plt.ylabel('Likelihood of occurrence')
plt.savefig('error_cdf1.png')

plt.figure()

for i in range(len(rssi_values2)):
    # Estimate the client's location
    estimated_location = task_3_localization(rssi_values2[i], ap_locations2)
    x2.append(estimated_location)
    if estimated_location is None:
        continue

    
    # Calculate the error
    error = np.linalg.norm(estimated_location - label2[i])
    error2.append(error)

#plot(x2, y2)

# Calculate the mean error
mean_error2 = np.mean(error2)
median_error2 = np.median(error2)

print(f'Data Set 2 Mean error: {mean_error2}')
print(f'Data Set 2 Median error: {median_error2}')

plt.hist(error2, bins='auto', density=True, cumulative=True, label='CDF',
         histtype='step', alpha=0.8, color='k')
plt.title('CDF of Error for data set 2')
plt.xlabel('Error')
plt.ylabel('Likelihood of occurrence')
plt.savefig('error_cdf2.png')





