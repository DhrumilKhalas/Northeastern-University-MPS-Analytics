"""
Module 2 Assignment - File Import Functions


Copyright (c) 2021 -- This is the 2021 Spring B version of the Template
Licensed
Written by Dhrumil Shaileshkumar Khalas

# you can also rely on the docstring documentation from pandas on how to format dosctrings:
# https://pandas.pydata.org/pandas-docs/stable/development/contributing_docstring.html

This script contains functions to import data from different file formats: CSV, TXT, JSON, and Excel. 
Each function takes the file path as input, imports the data into an appropriate Python data structure, and returns it.

"""

import pandas
import json

def import_csv(file_path: str) -> pandas.DataFrame:
    """
    Import a CSV file into a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the CSV data.
    """
    df = pandas.read_csv(
        filepath_or_buffer=file_path,
        sep=",",
        header=0,
        encoding="utf-8",
        dtype=str,
        na_values=["", "NA", "NaN"]
    )
    return df


def import_txt(file_path: str) -> list:
    """
    Import a TXT file into a Python list (one element per line).

    Parameters
    ----------
    file_path : str
        Path to the TXT file.

    Returns
    -------
    list
        List containing lines of the TXT file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.readlines()
    return [line.strip() for line in data]


def import_json(file_path: str) -> dict:
    """
    Import a JSON file into a Python dictionary.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Returns
    -------
    dict
        Dictionary containing the JSON data.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def import_excel(file_path: str, sheet_name: str = "financials") -> pandas.DataFrame:
    """
    Import an Excel file into a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the Excel file.
    sheet_name : str, optional
        Sheet name to import (default is "financials").

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the Excel data.
    """
    df = pandas.read_excel(
        io=file_path,
        sheet_name=sheet_name,
        header=0,
        dtype=str,
        na_values=["", "NA", "NaN"],
        engine="openpyxl"
    )
    return df


if __name__ == "__main__":
    # Main functions to Run
    csv_data = import_csv("Neural_data.csv")
    txt_data = import_txt("network_data.txt")
    json_data = import_json("nested_data.json")
    excel_data = import_excel("Excel_report.xlsx", sheet_name="financials")

    # Data is returned and stored in variables, not printed.