import cvxpy as cp
import numpy as np
import csv
from datetime import date as dt
from dateutil.relativedelta import relativedelta as rd

data = np.array(list(np.loadtxt(open("Factors.csv","rb"),delimiter = ",",usecols=range(1,21),skiprows=2)))
num_factors = 10
num_securities = 10
num_rollingmonths = 60 
num_rolling_windows = data.shape[0] - num_rollingmonths

csv_file = open('Optimal_Rolling_Weights.csv','w')
csv_writer = csv.writer(csv_file)

# Calculate optimal weights for each security
for i in range(num_securities):
    date = dt(2005,1,31)
    csv_writer.writerow(['Security {}  - Optimal Weights'.format(i+1)])
    csv_writer.writerow(['Date','Factor 1','Factor 2','Factor 3','Factor 4','Factor 5','Factor 6','Factor 7','Factor 8','Factor 9','Factor 10','Sum of Weights'])

    # Calculate optimal weights for each rolling window
    for j in range(num_rolling_windows):
        # X represents matrix of risk factor returns
        X = data[j:j+(num_rollingmonths),0:10]
        # Y represents security/index to be tested against
        y = data[j:j+(num_rollingmonths),(10+i,)].reshape(num_rollingmonths,)

        # b is optimal beta/ optimal weights to solve for
        b = cp.Variable(num_factors)
        print(b.value)
        cost = cp.sum_squares(X @ b - y)
        constraints = [cp.sum(b) == 1.0]
        prob = cp.Problem(cp.Minimize(cost),constraints)
        prob.solve()

        # Output to csv
        csv_writer.writerow([date,]+list(b.value)+[sum(b.value),])
        date = date + rd(months = 1) +rd(day = 31)

csv_file.close()
