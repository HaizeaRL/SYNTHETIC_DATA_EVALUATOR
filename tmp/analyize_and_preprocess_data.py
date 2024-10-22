# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:09:13 2024
Data pre-process and analysis
@author: hrumayor
"""

import pandas as pd
import os

pd.set_option('display.max_columns', None)


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
 Columns diag_1 The primary diagnosis (coded as first three digits of ICD9); 848 distinct values 
 diag_2 Secondary diagnosis (coded as first three digits of ICD9); 923 distinct values and 
 diag_3 Additional secondary diagnosis (coded as first three digits of ICD9); 954 distinct values
'''