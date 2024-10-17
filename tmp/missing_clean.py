# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os

path ="C:/DATA_SCIENCE_HAIZEA/SYNTHETIC_DATA_EVALUATOR\src/tmp_folder"

diabetes = pd.read_parquet(os.path.join(path,"preprocessed_file.parquet"),engine ="pyarrow")
synth = pd.read_parquet(os.path.join(path,"synthetic_data.parquet"),engine ="pyarrow")

num_cols = diabetes.select_dtypes(include='int64').columns.to_list()

'''# Check data distribution to determine if synthetizer numerical distribution need to be set or not
import matplotlib.pyplot as plt
import numpy as np

# Assuming 'diabetes' is your dataset
# Compare values per column
num_cols = diabetes.select_dtypes(include='int64').columns.to_list()
num_cols

diabetes[num_cols[3]].value_counts()

# Loop through continuous columns
for col in num_cols:
    # Plot histogram
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Get unique values count for binning (useful for integer columns)
    unique_values = diabetes[col].nunique()
    
    # Set the number of bins based on unique values or a minimum threshold for better visualization
    if unique_values < 30:
        bins = unique_values  # Use number of unique values if less than 30
    else:
        bins = 30  # Default to 30 bins if more than 30 unique values
    
    
    ax.hist(diabetes[col], bins= bins)
    
    # Set xticks based on min and max values in the column
    col_min, col_max = diabetes[col].min(), diabetes[col].max()
    
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
    input()'''




for col in num_cols:
    print(f"\n\nColumn: {col}")

    # Combine proportions into a DataFrame for easy comparison of real data
    real_data_info = pd.DataFrame({
        'Proportions': diabetes[col].value_counts(normalize=True, dropna=False)
    }).fillna(0)

    # For synthetic data
    synthetic_data_info = pd.DataFrame({
        'Proportions': synth[col].value_counts(normalize=True, dropna=False)
    }).fillna(0)  # Ensure NaNs are filled with 0 in synthetic data as well

    # Reset index to have a common column for merging
    real_data_info.reset_index(inplace=True)
    real_data_info.rename(columns={'index': 'Value'}, inplace=True)

    synthetic_data_info.reset_index(inplace=True)
    synthetic_data_info.rename(columns={'index': 'Value'}, inplace=True)

    # Merge the two DataFrames on 'Value' to compare proportions
    comparison = pd.merge(real_data_info, synthetic_data_info, on=col, how='outer', suffixes=('_real', '_synthetic'))

    # Print comparison table
    print("Comparison of Real and Synthetic Data:")
    print(comparison)