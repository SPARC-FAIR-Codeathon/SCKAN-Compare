import pandas as pd

def get_dataframe(data_as_list):
    # convert data_as_list to pandas dataframe
    df = pd.DataFrame(data_as_list)
    #set column names equal to values in row index position 0
    df.columns = df.iloc[0]
    #remove first row from DataFrame
    df = df[1:]
    return df


def remove_duplicate_species(df):
    df = df.replace('Mammalia', 'Mammal')
    df = df.replace('mammals', 'Mammal')
    df = df.replace('Vertebrata <vertebrates>', 'Vertebrata')
    df = df.replace('vertebrates', 'Vertebrata')
    df = df.replace('human', 'Homo sapiens')
    df = df.replace('Norway rat', 'Rattus norvegicus')
    df = df.replace('brown rat', 'Rattus norvegicus')
    df = df.replace('rat', 'Rattus norvegicus')
    df = df.replace('rats', 'Rattus norvegicus')
    df = df.replace('mouse', 'Mus musculus')
    df = df.replace('house mouse', 'Mus musculus')
    return df


def get_species_name(projection_fibre=False):
    """
    :return: gets the (unique) name of all species in the dataset
    """
    species = ['Canis familiaris', 'Cavia porcellus', 'Homo sapiens', 'Mammal',
         'Mus musculus', 'Rattus norvegicus']

    if projection_fibre:
        species = ['Canis familiaris', 'Cavia porcellus', 'Homo sapiens', 'Mammal',
       'Mus musculus', 'Rattus norvegicus', 'Vertebrata']

    return species


def get_phenotype_neuron():
    """
    :return: gets unique phenotypes of neurons
    """
    phenotype = ['Enteric phenotype', 'Parasympathetic Post-Ganglionic phenotype',
          'Parasympathetic Pre-Ganglionic phenotype',
          'Parasympathetic phenotype', 'Post ganglionic phenotype',
          'Pre ganglionic phenotype',
          'Sympathetic Post-Ganglionic phenotype',
          'Sympathetic Pre-Ganglionic phenotype', 'Sympathetic phenotype']

    return phenotype

def get_circuit_roles():
    species = ['Homo sapiens', 'Mammal', 'Rattus norvegicus']
    circuit_roles = ['Motor phenotype', 'Sensory phenotype']
    return species, circuit_roles