# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:09:13 2024
Data pre-process and analysis
@author: hrumayor
"""

import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Load data
from ucimlrepo import fetch_ucirepo 

'''# metadata 
print(diabetes_130_us_hospitals_for_years_1999_2008.metadata) 
  
# variable information 
print(diabetes_130_us_hospitals_for_years_1999_2008.variables) '''
  
# fetch dataset 
diabetes_130_us_hospitals_for_years_1999_2008 = fetch_ucirepo(id=296) 
  
# data (as pandas dataframes) 
X = diabetes_130_us_hospitals_for_years_1999_2008.data.features 
y = diabetes_130_us_hospitals_for_years_1999_2008.data.targets 

# create complete real_data
diabetes = pd.DataFrame(X)
diabetes["readmitted"] = y

# visualize data
diabetes.head()

# save data into file
diabetes.to_csv(os.path.join("C:/DATA_SCIENCE_HAIZEA/SYNTHETIC_DATA_EVALUATOR/resources","diabetes.csv"),
                index = False)

# load data again
diabetes = pd.read_csv(os.path.join("C:/DATA_SCIENCE_HAIZEA/SYNTHETIC_DATA_EVALUATOR/resources",
                                    "diabetes2.csv"))

diabetes.shape

# CHECK CATEGORICAL DATA
# optimize memory use changing object to string
categorical_cols = diabetes.select_dtypes('object').columns.tolist()

# Check column values, correspond to dtypes
for cat in categorical_cols:
    print(f"\nColumn: {cat} values: {diabetes[cat].unique()}")
    
    
# nulls per columns (percentage)
diabetes.isna().sum() * 100 / len(diabetes)

'''
ACTION FOR THIS COLUMNS!!
 Columns diag_1 (coded as first three digits of ICD9); 662 distinct values 
 diag_2 (coded as first three digits of ICD9); 701 distinct values and 
 diag_3 (coded as first three digits of ICD9); 740 distinct values
'''

len(diabetes["diag_3"].unique())

# Cambiar Nulls por ""
df1 = diabetes.copy()
df1 = df1.fillna("")

df1

# Juntar en una unica columna los tres diagnosticos
def new_diagnose_column(row):
    count = 0
    if row['diag_1'] != "":
        count +=1
    if row['diag_2'] != "":
        count +=1
    if row['diag_3'] != "":
        count +=1
    
    row["ICD9_Diag_count"] = count   
    row["ICD9_Diag"] = f"{row['diag_1']}_{row['diag_2']}_{row['diag_3']}".strip('_')
    return row

# crear nueva columna
df1 = df1.apply(new_diagnose_column, axis=1)

# check how many distinct values are
len(df1["ICD9_Diag"].unique())
len(df1["ICD9_Diag_count"].unique())


df1["ICD9_Diag"].value_counts()
df1["ICD9_Diag_count"].value_counts()
 
# Kolmogorov-Smirnov test
from scipy.stats import kstest, truncnorm, beta, expon, uniform, norm, gamma

distributions = ["norm","truncnorm","beta","expon", "uniform" ,"gamma"]
num_columns = ["time_in_hospital",'num_lab_procedures', 'num_procedures', 'num_medications',
'number_outpatient', 'number_emergency', 'number_inpatient']

for col in num_columns:
    print(f"\nColumn: {col}")
    for distr in distributions:
        print(f"Testing H0: Data follows '{distr}' distribution?")
       
        if distr == "norm":
           # Normal distribution doesn't need additional parameters
           ks_result = kstest(df1[col], 'norm', args=(df1[col].mean(), df1[col].std()))
       
        elif distr == "truncnorm":
           # Truncated normal needs lower and upper bounds, mean and std
           a, b = (df1[col].min() - df1[col].mean()) / df1[col].std(), (df1[col].max() - df1[col].mean()) / df1[col].std()
           ks_result = kstest(df1[col], 'truncnorm', args=(a, b, df1[col].mean(), df1[col].std()))
       
        elif distr == "beta":
           # Beta distribution needs 'a' and 'b' parameters (shape parameters)
           a, b = 2, 5  # These are example values, you'd need to estimate them or use fitting methods
           ks_result = kstest(df1[col], 'beta', args=(a, b, df1[col].min(), df1[col].max() - df1[col].min()))
       
        elif distr == "expon":
           # Exponential distribution requires 'loc' and 'scale' parameters (loc is usually the minimum of the data)
           ks_result = kstest(df1[col], 'expon', args=(df1[col].min(), df1[col].mean()))
       
        elif distr == "uniform":
           # Uniform distribution needs min and max values
           ks_result = kstest(df1[col], 'uniform', args=(df1[col].min(), df1[col].max() - df1[col].min()))
       
        elif distr == "gamma":
         # Fit the gamma distribution to get shape, loc, and scale parameters
         shape, loc, scale = gamma.fit(df1[col])
         # Perform KS test with the fitted parameters
         ks_result = kstest(df1[col], 'gamma', args=(shape, loc, scale))
         
       # Output the result
        print(ks_result)
        if ks_result[1] < 0.05: 
            print(f"H0 rejected. No '{distr}' distribution type.")
        else:
            print("Yes, is '{distr}' type.")
       
        input()
       

import matplotlib.pyplot as plt
import numpy as np

# plot their distribution
for col in num_columns:
    # Plot histogram
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Get unique values count for binning (useful for integer columns)
    unique_values = df1[col].nunique()
    
    # Set the number of bins based on unique values or a minimum threshold for better visualization
    if unique_values < 30:
        bins = unique_values  # Use number of unique values if less than 30
    else:
        bins = 30  # Default to 30 bins if more than 30 unique values
    
    
    ax.hist(df1[col], bins= bins)
    
    # Set xticks based on min and max values in the column
    col_min, col_max = df1[col].min(), df1[col].max()
    
    # Adjust step size for xticks dynamically (if range is small, step=1, else larger step)
    if col_max - col_min < 30:
        step_size = 1
    else:
        step_size = (col_max - col_min) // 10  # Step size as a fraction of the range

    # Set the xticks on the axis
    ax.set_xticks(np.arange(col_min, col_max + step_size, step_size))

    # Adjust & show the plot
    ax.set_title(f'Distribution of {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    
    input()
    
    
# time_in_hospital is skewed, left skewed.
# Fit and obtain 
from scipy.stats import gamma, skew

def create_numerical_colums_distribution(df):
    num_distribution = {}
    for col in num_columns:
        
        # Calculate the skewness 
        skewness = skew(df1[col])
        print(f"\nColumn: {col} skewness: {skewness}")

        # Fit a gamma distribution
        gamma_params = gamma.fit(df1[col])

        # get params to configure 
        shape, loc, scale = gamma_params
        print(f"Gamma distribution parameters:\nShape: {shape}, Loc: {loc}, Scale: {scale}")

        # Add the distribution details to the num_distribution dictionary
        num_distribution[col] = {
            'distribution': 'gamma',
            'parameters': {
                'shape': shape,
                'loc': loc,
                'scale': scale
            }
        }
    return num_distribution



num_distribution