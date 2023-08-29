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


def get_species_name(projection_fibre=False):
    """
    Get a list of unique species names.

    Parameters
    ----------
    projection_fibre : bool, optional
        Whether to include projection fibre species. Defaults to False.

    Returns
    -------
    list
        List of unique species names.
    """
    species = ['Canis familiaris', 'Cavia porcellus', 'Homo sapiens', 'Mammal',
         'Mus musculus', 'Rattus norvegicus']

    if projection_fibre:
        species = ['Canis familiaris', 'Cavia porcellus', 'Homo sapiens', 'Mammal',
       'Mus musculus', 'Rattus norvegicus', 'Vertebrata']

    return species


def get_phenotype_neuron():
    """
    Get a list of unique neuron phenotypes.

    Returns
    -------
    list
        List of unique neuron phenotypes.
    """
    phenotype = ['Enteric phenotype', 'Parasympathetic Post-Ganglionic phenotype',
          'Parasympathetic Pre-Ganglionic phenotype',
          'Parasympathetic phenotype', 'Post ganglionic phenotype',
          'Pre ganglionic phenotype',
          'Sympathetic Post-Ganglionic phenotype',
          'Sympathetic Pre-Ganglionic phenotype', 'Sympathetic phenotype']

    return phenotype

def get_circuit_roles():
    """
    Get species and circuit roles.

    Returns
    -------
    tuple
        A tuple containing a list of species and a list of circuit roles.
    """
    species = ['Homo sapiens', 'Mammal', 'Rattus norvegicus']
    circuit_roles = ['Motor phenotype', 'Sensory phenotype']
    return species, circuit_roles