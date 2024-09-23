# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:49:33 2024

@author: hrumayor
"""
import os
import pandas as pd

tmp_folder = "D:/HAIZEARL/Real_vs_synthetic_evaluation/SYNTHETIC_DATA_EVALUATOR/src/tmp_folder"


# CONVERT ONE-HOT

# One-hot function
def apply_one_hot(df, cols):
    # Apply: one-hot encode categorical variables    
    return pd.get_dummies(df, columns=cols, drop_first=True)

# LOAD data
diabetes = pd.read_parquet(os.path.join(tmp_folder,"generalized_file.parquet"),engine="pyarrow")

# Set target value
X = diabetes.drop(columns='readmitted')
y = diabetes['readmitted']

# get only categorical data
categorical_cols = X.select_dtypes(include=['object']).columns

# call to function
X_encoded = apply_one_hot(diabetes, categorical_cols)
X_encoded


# REVERSE ONE-HOT

categorical_cols
X_encoded.columns

diabetes.info()