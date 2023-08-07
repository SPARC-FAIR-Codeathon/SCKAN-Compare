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