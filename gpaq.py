#!/bin/bash

import os
import pandas as pd
import argparse
import time
import subprocess
import sys

def print_warning(message):
    """Prints a warning message in yellow"""
    print(f"\033[93mWarning: {message}\033[0m")

def print_error(message):
    """Prints an error message in red"""
    print(f"\033[91mError: {message}\033[0m")

def install_requirements():
    """
    This functions checks if the necessary packages are installed, and install them. 
    They are present in "requirements.txt"
    """
    print("Checking for the presence of correct packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'])
    except subprocess.CalledProcessError as e:
        error_message = f"Error during package installation: {e}"
        print_error(error_message)

def import_csv_files(path):
    """
    This function imports all .csv files from a given directory, 
    checks that files and directory exist, and files are correctly structured,
    and returns a dictionary containing the DataFrames.

    Args:
        path (str): The path of the directory containing .csv files.

    Returns:
        dict: A dictionary with file names as keys and corresponding DataFrames as values.
    """
    print(f"Importing data from {path}...")

    # Check if the path exists
    if not os.path.exists(path):
        error_message = f"The path {path} does not exist."
        print_error(error_message)
        return {}

    # List of CSV files in the directory
    csv_files = [file_name for file_name in os.listdir(path) if file_name.endswith('.csv')]
    csv_file_count = len(csv_files)

    # Check if the directory contains any CSV files
    if csv_file_count == 0:
        error_message = f"The directory {path} is empty or contains no .csv files."
        print_error(error_message)
        return {}

    data_dict = {}
    expected_columns = [
        'ID', 'P1', 'P2', 'P3a', 'P3b', 'P4', 'P5', 'P6a', 'P6b',
        'P7', 'P8', 'P9a', 'P9b', 'P10', 'P11', 'P12a', 'P12b',
        'P13', 'P14', 'P15a', 'P15b', 'P16a', 'P16b'
    ]
    
    # Loop through the CSV files to import them
    for file_name in csv_files:
        file_path = os.path.join(path, file_name)

        df = pd.read_csv(file_path) 
        df.columns = expected_columns  

        # Reset index after dropping the first row
        df = df.reset_index(drop=True) 

        # Check for expected columns
        if not all(col in df.columns for col in expected_columns):
            print_error(f"Error: The following expected columns are missing in {file_name}: {set(expected_columns) - set(df.columns)}")
            return None 

        # Check that values in columns P1 through P16b are either empty or numeric
        for col in expected_columns[1:]:  # Skip 'ID'
            if col in df.columns:
                if not df[col].apply(lambda x: pd.isnull(x) or isinstance(x, (int, float))).all():
                    print_error(f"Error: Column '{col}' in {file_name} should contain only empty or numeric values.")
                    return None 
        
        data_dict[file_name] = df

    # Check if all CSV files were successfully imported
    if csv_file_count == len(data_dict):
        print(f"{csv_file_count} csv files imported.")
        return data_dict  
    else:
        warning_message = f"{csv_file_count} .csv files found but only {len(data_dict)} imported."
        print_warning(warning_message)
        return data_dict

def get_columns_to_check(col):
    """Return the list of columns to check based on the given column."""
    mapping = {
        'P1': ['P2', 'P3a', 'P3b'],
        'P4': ['P5', 'P6a', 'P6b'],
        'P7': ['P8', 'P9a', 'P9b'],
        'P10': ['P11', 'P12a', 'P12b'],
        'P13': ['P14', 'P15a', 'P15b']
    }
    return mapping.get(col, [])

def check_data_integrity(data_dict):
    """
    This function checks for duplicates, validates values in specific columns, 
    and prints the findings for data integrity in the imported DataFrames.

    Args:
        data_dict (dict): A dictionary containing DataFrames keyed by their file names.
    
    Returns:
        set: A set of DataFrame names that have integrity issues.
    """
    print("Check data integrity...")

    names_list = []

    # Duplicates in df
    for df_name in data_dict.keys():
        names_list.append(df_name)

    has_issues = False  # Track if any issues are found
    problematic_dfs = set()  # To keep track of DataFrames with issues

    if len(names_list) != len(set(names_list)):
        print_warning("Duplicates in provided dataframes")
        has_issues = True
        problematic_dfs.update(names_list)

    # Yes or No items filed and correctly filed (1 or 2 value)
    columns_to_check = ['P1', 'P4', 'P7', 'P10', 'P13'] 

    for key, df in data_dict.items():
        mask = (df[columns_to_check] != 1) & (df[columns_to_check] != 2)
        if mask.any().any():
            print_warning(f"Dataframe {key} has invalid values (value not 1 or 2)")
            problematic_dfs.add(key)
            has_issues = True

    # No PA behavior described if no PA mentioned before ('NO')
    for key, df in data_dict.items():
        for col in ['P1', 'P4', 'P7', 'P10', 'P13']:
            mask = df[col] == 2
            if mask.any():
                sub_df = df.loc[mask, [col] + get_columns_to_check(col)]
                error_mask = sub_df[get_columns_to_check(col)].notnull().any(axis=1)
                if error_mask.any():
                    print_warning(f"Error in {key} for columns {sub_df.loc[error_mask].index.tolist()}: no PA mentioned before, yet items filled")
                    print_warning("According to ONAPS, questionnaire must be deleted if PA described while NO mentioned")
                    problematic_dfs.add(key)
                    has_issues = True

    # PA behavior described if PA mentioned before ('YES')
    for key, df in data_dict.items():
        cols_to_check = ['P1', 'P4', 'P7', 'P10', 'P13']
        for col in cols_to_check:
            mask = df[col] == 1
            if mask.any():
                col_index = df.columns.get_loc(col)
                next_col = df.columns[col_index + 1]
                sub_df = df.loc[mask, [col, next_col]]
                error_mask = (sub_df[col].notnull()) & (sub_df[next_col].isna() | (sub_df[next_col] < 1))
                if error_mask.any():
                    print_warning(f"Error in {key} for columns {sub_df.loc[error_mask].index.tolist()}: PA mentioned before, yet no items filled")
                    problematic_dfs.add(key)
                    has_issues = True

    # At least 1 minute of PA behavior described if PA mentioned before ('YES')
    for key, df in data_dict.items():
        cols_to_check = ['P1', 'P4', 'P7', 'P10', 'P13']
        for col in cols_to_check:
            col_index = df.columns.get_loc(col)
            mask = df[col] == 1
            if mask.any():
                sub_df = df.loc[mask, [col, df.columns[col_index + 2], df.columns[col_index + 3]]]
                error_mask = sub_df[[df.columns[col_index + 2], df.columns[col_index + 3]]].isna().all(axis=1)
                if error_mask.any():
                    print_warning(f"Error in {key} for columns {col} at index {col_index + 2} and {col_index + 3}: 0 minute of PA described, yet PA mentioned before")
                    print_warning('According to ONAPS, subdomain must be deleted if no PA described while YES mentioned')
                    problematic_dfs.add(key)
                    has_issues = True
                else:
                    sub_df = sub_df.loc[~error_mask]
                    error_mask = (sub_df[df.columns[col_index + 2]].isna() | sub_df[df.columns[col_index + 2]] < 1) & (sub_df[df.columns[col_index + 3]].isna() | sub_df[df.columns[col_index + 3]] < 1)
                    if error_mask.any():
                        print_warning(f"Error in {key} for columns {col} at index {col_index + 2} and {col_index + 3}: 0 minute of PA described, yet PA mentioned before")
                        print_warning('According to ONAPS, subdomain must be deleted if no PA described while YES mentioned')
                        problematic_dfs.add(key)
                        has_issues = True

    # Correct time format: 7 days, 24 hours, 60 minutes
    columns_to_check = ['P2', 'P5', 'P8', 'P11', 'P14',
                        'P3a', 'P6a', 'P9a', 'P12a', 'P15a', 'P16a',
                        'P3b', 'P6b', 'P9b', 'P12b', 'P15b', 'P16b']

    acceptable_ranges = {
        'P2': (0, 7),
        'P5': (0, 7),
        'P8': (0, 7),
        'P11': (0, 7),
        'P14': (0, 7),     
        'P3a': (0, 16),
        'P6a': (0, 16),
        'P9a': (0, 16),
        'P12a': (0, 16),
        'P15a': (0, 16),
        'P16a': (0, 24),
        'P3b': (0, 60),
        'P6b': (0, 60),
        'P9b': (0, 60),
        'P12b': (0, 60),
        'P15b': (0, 60),
        'P16b': (0, 60)
    }

    aberrant_data = {}

    for key, df in data_dict.items():
        for index, row in df.iterrows():
            for col in columns_to_check:
                value = row[col]
                if value < acceptable_ranges[col][0] or value > acceptable_ranges[col][1]:
                    if key not in aberrant_data:
                        aberrant_data[key] = []
                    aberrant_data[key].append((index, col))
                    
    for key, values in aberrant_data.items():
        print_warning(f"Dataframe {key}:")
        for index, col in values:
            print_warning(f"Wrong value in {col} at {index}. Please check the correct time format: 7 days, 24 hours, 60 minutes")

    if has_issues:
        print("This has to be checked manually in raw data.")
    if not has_issues:
        print("No issues found in data integrity checks.")

    return problematic_dfs  # Return the DataFrames with integrity issues

def MET_min_calculation(data_dict, names_with_issues):
    """
    Calculate MET minutes for physical activities based on specified columns in the DataFrames.
    
    Args:
        data_dict (dict): A dictionary containing DataFrames keyed by their file names.
        names_with_issues (list): A list of DataFrame names that have integrity issues.
    """
    print("Calculating MET/minutes...")
    for key, df in data_dict.items():
        if key in names_with_issues:  # Skip this DataFrame if it has issues
            print(f"Skipping {key} due to integrity issues.")
            continue
        
        # Fill NaN values with 0
        df = df.infer_objects().fillna(0)
        
        # Calculate various MET values
        df['VPA_work'] = 8 * (df['P2'] * ((df['P3a'] * 60) + df['P3b']))
        df['MPA_work'] = 4 * (df['P5'] * ((df['P6a'] * 60) + df['P6b']))
        df['travel'] = 4 * (df['P8'] * ((df['P9a'] * 60) + df['P9b']))
        df['VPA_hobbies'] = 8 * (df['P11'] * ((df['P12a'] * 60) + df['P12b']))
        df['MPA_hobbies'] = 4 * (df['P14'] * ((df['P15a'] * 60) + df['P15b']))
        df['sed'] = 7 * ((df['P16a'] * 60) + df['P16b'])
        
        # Sum up the calculated values
        df['work'] = df['VPA_work'] + df['MPA_work']
        df['hobbies'] = df['VPA_hobbies'] + df['MPA_hobbies']
        df['VPA'] = df['VPA_work'] + df['VPA_hobbies']
        df['MPA'] = df['MPA_work'] + df['MPA_hobbies'] + df['travel']
        df['MVPA'] = df['VPA'] + df['MPA']
        
        # Update the dictionary with the modified DataFrame
        data_dict[key] = df

def save_data(data_dict, saving_path_ind, save_independent):
    """Saves data to CSV files."""
    print("Saving files...")
    if save_independent:
        # Save independent files
        for key, value in data_dict.items():
            filename = os.path.join(saving_path_ind, f"{key}")
            value.to_csv(filename,  index=False)
            print(f"Saved independent file: {filename}")
    
    # Save concatenated files (one unique DataFrame)
    if not save_independent:
        concatenated_df = pd.concat(data_dict.values(), axis=0)
        concatenated_df = concatenated_df.sort_values(by=['ID'])
        concatenated_filename = os.path.join(saving_path_ind, "concatenated_data.csv")
        concatenated_df.to_csv(concatenated_filename, index=False)
        print(f"Saved concatenated file: {concatenated_filename}")

def main():
    start_time = time.time()

    install_requirements()

    default_data_path = "./data"
    default_results_path = "./results"

    parser = argparse.ArgumentParser(description="Import CSV files from a directory.")

    # Precise input directory (default = ./data)
    parser.add_argument(
        "-d", "--directory", 
        type=str, 
        default=default_data_path, 
        help="Directory containing CSV files (default: './data')"
    )
    # Precise output directory (default = ./results)
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default=default_results_path, 
        help="Directory to save results (default: './results')"
    )
    # Precise if you want individual results (default = 1 concatenated file)
    parser.add_argument(
        "--ind", 
        action="store_true", 
        help="Save independent files"
    )

    args = parser.parse_args()

    # Use the provided directory or the default one
    path = args.directory
    saving_path_ind = args.output

    # Create output directory if it doesn't exist
    if not os.path.exists(saving_path_ind):
        os.makedirs(saving_path_ind)

    data_dict = import_csv_files(path)
    if data_dict:
        problematic_dfs = check_data_integrity(data_dict)  
        MET_min_calculation(data_dict, problematic_dfs)  
        save_data(data_dict, saving_path_ind, args.ind)

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Done in {elapsed_time:.2f} seconds.")
    print('')

if __name__ == "__main__":
    main()
