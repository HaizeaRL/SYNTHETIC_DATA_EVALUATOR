# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:10:42 2024

@author: jonma
"""

import os
import pandas as pd
import patoolib

# Extract best synth data
path = "C:/DATA_SCIENCE_HAIZEA/SYNTHETIC_DATA_EVALUATOR/results"
path1 = "C:/DATA_SCIENCE_HAIZEA/SYNTHETIC_DATA_EVALUATOR"
patoolib.extract_archive(os.path.join(path,"best_synth_data.rar"), outdir=path1)

# Load best synth data
file1 = os.path.join(path,"GaussianCopula_best_synth_data.parquet")
file2 = os.path.join(path,"CTGAN_best_synth_data.parquet")

copula = pd.read_parquet(file1,engine="pyarrow")
ctgan = pd.read_parquet(file2,engine="pyarrow")


# Load original data
orig = os.path.join(path,"preprocessed_file.parquet")
diabetes =  pd.read_parquet(orig,engine="pyarrow")

# COMPARAR DIMENSIONES 

print(f"Real dimension: {diabetes.shape}")
print(f"Copula Synth dimension: {copula.shape}")
print(f"CTGAN Synth dimension: {ctgan.shape}")

pd.set_option("display.max_column",None)

# VALORES NO NULOS

# Get information from 3 datasets
real_data_info = pd.DataFrame({
    'Column': diabetes.columns,
    'Real Count':diabetes.notnull().sum()
    })

copula_synth_info = pd.DataFrame({
    'Column': copula.columns,
    'GaussianCopula Count':copula.notnull().sum()
})

ctgan_synth_info = pd.DataFrame({
    'Column': ctgan.columns,
    'CTGAN Count':ctgan.notnull().sum()
})


# Merge the  DataFrames on the 'Column' name
comparison = pd.merge(real_data_info, copula_synth_info, on='Column', how='outer')
comparison = pd.merge(comparison, ctgan_synth_info, on='Column', how='outer')

# Print comparison table
print("Comparison of Real and Synthetic Data:")
print(comparison)


# VALORES CATEGORICOS
orig_cat_cols = diabetes.select_dtypes('object').columns.tolist()
copula_cat_cols = copula.select_dtypes('object').columns.tolist()
ctgan_cat_cols = ctgan.select_dtypes('object').columns.tolist()

print(f"Same categorical columns: {orig_cat_cols == copula_cat_cols == ctgan_cat_cols}")


# DISTRIBUCION DE VALORES CATEGORICOS 
for col in orig_cat_cols:
    # Get information from 3 datasets
    real_data_info = diabetes[col].value_counts(dropna=True).reset_index()
    real_data_info.columns = ['Category', 'Real']

    copula_synth_info = copula[col].value_counts(dropna=True).reset_index()
    copula_synth_info.columns = ['Category', 'GaussianCopula']

    ctgan_synth_info = ctgan[col].value_counts(dropna=True).reset_index()
    ctgan_synth_info.columns = ['Category', 'CTGAN']

    # Merge the DataFrames on the 'Value' name
    comparison = pd.merge(real_data_info, copula_synth_info, on='Category', how='outer')
    comparison = pd.merge(comparison, ctgan_synth_info, on='Category', how='outer')

    # Print comparison table
    print(f"\nComparison of Real and Synthetic Data for column '{col}':")
    print(comparison)


diabetes["discharge_disposition_id"].value_counts(dropna = False)
copula["discharge_disposition_id"].value_counts(dropna = False)

# VALORES NUMERICOS
orig_cols = diabetes.select_dtypes('int64').columns.tolist()
copula_cols = copula.select_dtypes('int64').columns.tolist()
ctgan_cols = ctgan.select_dtypes('int64').columns.tolist()
print(f"Same numerical columns: {len(orig_cols) == len(copula_cols) == len(ctgan_cols)}")

# Visualizar distribución valores numericos
import matplotlib.pyplot as plt
import numpy as np

# plot their distribution
for col in orig_cols:
    # Plot histogram
    fig, ax = plt.subplots(1,2,figsize=(10, 5))
    
    # Get unique values count for binning (useful for integer columns)
    unique_values = diabetes[col].nunique()
    
    # Set the number of bins based on unique values or a minimum threshold for better visualization
    if unique_values < 30:
        bins = unique_values  # Use number of unique values if less than 30
    else:
        bins = 30  # Default to 30 bins if more than 30 unique values
    
    # Set xticks based on min and max values in the column
    col_min, col_max = diabetes[col].min(), diabetes[col].max()
    
    # Adjust step size for xticks dynamically (if range is small, step=1, else larger step)
    if col_max - col_min < 30:
        step_size = 1
    else:
        step_size = (col_max - col_min) // 10  # Step size as a fraction of the range
    
    
    # orig vs copula
    ax[0].hist(diabetes[col], bins= bins, alpha = 0.2, label = "orig")
    ax[0].hist(copula[col], bins= bins, alpha = 0.2, label = "copula")
    ax[0].set_xticks(np.arange(col_min, col_max + step_size, step_size))
    
    # Adjust & show the plot
    ax[0].set_title(f'Distribution of {col}')
    ax[0].set_xlabel(col)
    ax[0].set_ylabel('Frequency')
    ax[0].legend()
    
    # orig vs ctgan
    ax[1].set_xticks(np.arange(col_min, col_max + step_size, step_size))    
    ax[1].hist(diabetes[col], bins= bins, alpha = 0.2, label = "orig")
    ax[1].hist(ctgan[col], bins= bins, alpha = 0.2, label = "ctgan")
    
    # Adjust & show the plot
    ax[1].set_title(f'Distribution of {col}')
    ax[1].set_xlabel(col)
    ax[1].set_ylabel('Frequency')
    ax[1].legend()
    
    plt.tight_layout()
    plt.show()
