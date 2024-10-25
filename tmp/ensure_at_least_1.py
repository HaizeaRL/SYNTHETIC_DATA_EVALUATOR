# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 13:25:34 2024

@author: jonma
"""

import pandas as pd
from sdv.tabular import GaussianCopulaSynthesizer
from sdv import Metadata

# Sample data
data = {
    'age': [25, 30, 35, 40, 45],
    'gender': ['male', 'female', 'female', 'male', 'female'],
    'income': [50000, 60000, 70000, 80000, 90000]
}
df = pd.DataFrame(data)

# Define Metadata
metadata = Metadata()
metadata.add_table(
    name='people',
    data=df,
    index=None,  # No index column
    categorical_columns=['gender']  # Specify categorical columns here
)

# Initialize the Synthesizer
synthesizer = GaussianCopulaSynthesizer(
    metadata,
    enforce_min_max_values=True,
    enforce_rounding=True,
)

# Fit the synthesizer
synthesizer.fit(df)

# Function to sample ensuring at least one per category
def sample_with_minimum_categories(synthesizer, num_rows, category_column, categories):
    # Create an empty DataFrame to hold results
    samples = pd.DataFrame()
    
    # Generate samples for each category
    for category in categories:
        # Sample enough data for the current category
        min_samples = 1  # Minimum samples for this category
        current_samples = synthesizer.sample(num_rows=(num_rows // len(categories) + min_samples), 
                                              conditions={category_column: category})
        
        # Add at least one sample of the current category to the samples DataFrame
        samples = pd.concat([samples, current_samples], ignore_index=True)
    
    # If total samples are less than num_rows, sample again
    if len(samples) < num_rows:
        additional_samples = synthesizer.sample(num_rows=num_rows - len(samples))
        samples = pd.concat([samples, additional_samples], ignore_index=True)

    return samples.sample(num_rows=num_rows, random_state=42)  # Shuffle the final samples

# Define categories
categories = df['gender'].unique()

# Generate synthetic data ensuring at least one record per category
synthetic_data = sample_with_minimum_categories(synthesizer, num_rows=10, category_column='gender', categories=categories)
print(synthetic_data)
