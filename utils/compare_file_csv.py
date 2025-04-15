import pandas as pd
import numpy as np
import os

def compare_csv_files(file1_path, file2_path, output_path=None):
    """
    Compare two CSV files and report differences.
    
    Args:
        file1_path (str): Path to the first CSV file
        file2_path (str): Path to the second CSV file
        output_path (str, optional): Path to save results. If None, prints to console.
    
    Returns:
        float: Normalized score representing similarity between files
    """
    # Read the two CSV files into pandas dataframes
    try:
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
    except Exception as e:
        print(f"Error reading files: {e}")
        return 0
    
    # Check dimensions
    print(f"File 1: {df1.shape[0]} rows, {df1.shape[1]} columns")
    print(f"File 2: {df2.shape[0]} rows, {df2.shape[1]} columns")
    
    # Check column names
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    
    if cols1 != cols2:
        print("\nColumns in the two files are different:")
        print(f"Columns only in file 1: {cols1 - cols2}")
        print(f"Columns only in file 2: {cols2 - cols1}")
    else:
        print("\nBoth files have the same columns.")
    
    # Initialize counter for matching entries
    counter = 0
    
    # Ensure both DataFrames have the expected column structure
    if 'node_id' in df1.columns and 'offset' in df1.columns and 'node_id' in df2.columns and 'offset' in df2.columns:
        # Iterate through the rows of the DataFrames to calculate similarity
        for i in range(min(len(df1), len(df2))):
            node_id1 = df1.iloc[i, 0]
            node_id2 = df2.iloc[i, 0]
            offset1 = df1.iloc[i, 1]
            offset2 = df2.iloc[i, 1]
            
            # Check if node_ids are the same
            if node_id1 == node_id2:
                # Check if the offset difference is within threshold
                if abs(offset1 - offset2) < 10:
                    counter += 1
        
        # Calculate normalized score
        normalized_counter = counter / max(len(df1), len(df2))
        print(f"\nSimilarity score: {normalized_counter:.4f} ({counter} matching entries out of {max(len(df1), len(df2))})")
        
        return normalized_counter
    else:
        print("Error: CSV files do not have the expected 'node_id' and 'offset' columns")
        return 0

# Example usage
if __name__ == "__main__":
    # Compare individual files
    file1 = "/home/users/ignazio.spaccavento/GGBS/results/position_csv_ga/d_100.csv"
    file2 = "/home/users/ignazio.spaccavento/GGBS/zip_reads_folder/dati_fa_ggbs/long_match/position_csv/f_1k.csv"
    compare_csv_files(file1, file2)
