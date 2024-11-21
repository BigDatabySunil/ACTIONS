import pandas as pd
import re

def clean_column_data(value):
    """
    Cleans the column data by removing unwanted delimiters and extra spaces.

    Args:
        value (str): The original column value.

    Returns:
        str: Cleaned column value.
    """
    if isinstance(value, str):
        # 
        value = re.sub(r'[|!%&]', ' ', value)
        # Remove extra spaces
        value = re.sub(r'\s+', ' ', value).strip()
    return value
 # new function

def read_and_clean_employee_data(file_path):
    """
    Reads the employee data CSV file, removes inconsistent delimiters, and cleans the data.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned employee data.
    """
    # Read the file with flexible delimiters
    try:
        df = pd.read_csv(file_path, delimiter=',')
    except pd.errors.ParserError:
        # Fallback in case of unexpected delimiters
        df = pd.read_csv(file_path, delimiter='|')

    # Apply cleaning function to all string columns
    for col in df.columns:
        df[col] = df[col].apply(clean_column_data)

    # Convert Salary to numeric, handling invalid data
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')

    # Drop rows with missing or invalid data
    df = df.dropna()

    # Print first few rows for verification
    print("Cleaned Data:")
    print(df.head())

    return df


if __name__ == "__main__":
    file_path = r"C:\Users\sunil\Downloads\Actions\Actions\employee.csv"
    employee_df = read_and_clean_employee_data(file_path)
    print("Final Processed Data:")
    print(employee_df)

