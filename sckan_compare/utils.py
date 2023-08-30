"""
Utility methods for SckanCompare package.

License: Apache License 2.0
"""

import pandas as pd
from . import globals


def get_dataframe(data_as_list):
    """
    Convert a list of data to a pandas DataFrame.

    Parameters
    ----------
    data_as_list : list
        List of data to be converted.

    Returns
    -------
    pandas.DataFrame
        The converted DataFrame.
    """
    # convert data_as_list to pandas dataframe
    df = pd.DataFrame(data_as_list)
    #set column names equal to values in row index position 0
    df.columns = df.iloc[0]
    #remove first row from DataFrame
    df = df[1:]
    return df

def filter_dataframe(df, column, value):
    """
    Filter a DataFrame based on value in specific column.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be filtered.
    column : str
        The column to be filtered.
    value : str
        The value to be used for filtering column.

    Returns
    -------
    pandas.DataFrame
        The filtered DataFrame.
    """
    # check if column exists in DataFrame
    if column not in df.columns:
        raise ValueError('Column {} not found in DataFrame.'.format(column))
    # filter DataFrame based on value in column
    df = df[df[column] == value]
    return df

def remove_duplicate_species(df):
    """
    Replace various species synonyms with standard species names in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing species information.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with replaced species synonyms.
    """
    for item in globals.DUPLICATE_SPECIES_RESOLVER:
        df = df.replace(item, globals.DUPLICATE_SPECIES_RESOLVER[item])
    return df