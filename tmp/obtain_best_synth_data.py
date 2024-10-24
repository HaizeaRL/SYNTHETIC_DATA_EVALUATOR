# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:38:49 2024

@author: jonma
"""

import os
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# load synthetizers

path = "C:/DATA_SCIENCE_HAIZEA/SYNTHETIC_DATA_EVALUATOR/results"
synth_gcopula_kde
synth_gcopula_rest
ctgan

# load preprocessed original data
diabetes = pd.read_csv(os.path.join(path,"preprocessed_file.parquet"), engine ="pyarrow")

def evaluate_best_synth_data(df, synth_type, synthesizers, num_synth_data):
    overall_qa = 0.0
    col_shape_qa = 0.0
    col_pairs_qa = 0.0
    best_synth_data = None
    
    # obtain metadata
    
    # create n synth data
    for i in range(0,num_synth_data):
        if synth_type == "GaussianCopula" and len(synthesizers) == 2:
            # Generate synthetic data 
            synth_data = generate_synthetic_data_by_2_synths(synthesizers[1], 
                                                             synthesizers[0],
                                                             df.shape[0]) # GaussianCopula
                    
            
            # evaluate     
            quality = evaluate_quality(df, synth_data, metadata)  
            
            # get 3 indicators and compare to saved ones
            
            # best_synth_data

        elif ynth_type == "CTGAN" and len(synthesizers) == 1:
            
            # generate synth data
            synth_data = create_synth_data(df, synthesizers[0]) # CTGAN
            
            # obtain metada
            
            # evaluate     
            quality = evaluate_quality(df, synth_data, metadata)  
            
            # get 3 indicators and compare to saved ones
            
            # best_synth_data

    return best_synth_data




# EVALUATE SYNTH DATA QUALITY
