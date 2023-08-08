import numpy as np
import pandas as pd
import io
import csv
import requests
from urllib.parse import quote as url_quote


# function to run sparql in python
def query(query, variables=None, **kwargs):
    endpoint = 'https://blazegraph.scicrunch.io/blazegraph/sparql' # blazegraph endpoint
    # Convert variables to a URL-friendly format
    variable_str = ''
    if variables:
        variable_str = '&'.join([f'{key}={url_quote(str(val), safe="")}' for key, val in variables.items()])

    qq = url_quote(query, safe='')
    url = f'{endpoint}?query={qq}&{variable_str}'
    headers = {'Accept': 'text/csv'}
    resp = requests.get(url, headers=headers)
    return list(csv.reader(io.StringIO(resp.text)))


# for pre-processing/ helper functions
def get_unique_region_IRI (df_result):
    """
    :param df_result: dataframe
    :return: unique regions in form of hyperlinks
    """
    region_A = np.unique(df_result.loc[:,"A"])
    region_B = np.unique(df_result.loc[:,"B"])
    region_C = np.unique(df_result.loc[:,"C"])
    unique_regions = np.unique(np.concatenate((region_A, region_B, region_C)))
    return unique_regions

def get_unique_regions (df_result):
    """
    :param df_result: dataframe
    :return: region labels
    """

    # ?annotation rdfs:subClassOf+ [rdf:type owl:Restriction ;
    #                         owl:onProperty partOf: ;
    #                         owl:someValuesFrom/rdfs:label ?organ].

    # FILTER (?Target_Organ in ( 'heart', 'ovary', 'brain', 'urethra', 'esophagus', 'skin of body', 'lung', 'liver',
    #                         'lower urinary tract', 'urinary tract', 'muscle organ','gallbladder', 'colon', 'kidney',
    #                         'large intestine' ,'small intestine', 'stomach', 'spleen', 'urinary bladder',
    #                         'penis', 'clitoris', 'pancreas'))
    # ?annotation ilxtr:isPartOf+/rdfs:label ?organ
    unique_regions = get_unique_region_IRI(df_result)
    test_template = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
    PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>

    SELECT DISTINCT ?annotation ?label 
    WHERE {{
        ?annotation rdfs:label ?label. 

        FILTER (?annotation IN ({}))
    }}
    ORDER BY ?annotation ?label 
    """

    # first 100
    formatted_links = " ,".join(["<{}>".format(link) for link in unique_regions[:100]])
    test_query = test_template.format(formatted_links)
    result = query(test_query)
    final_df = pd.DataFrame(result).loc[1:, :]

    # rest 100
    formatted_links = " ,".join(["<{}>".format(link) for link in unique_regions[100:200]])
    test_query = test_template.format(formatted_links)
    result = query(test_query)
    final_df = pd.concat([final_df, pd.DataFrame(result).loc[1:, :]], ignore_index=True)

    # rest all
    formatted_links = " ,".join(["<{}>".format(link) for link in unique_regions[200:]])
    test_query = test_template.format(formatted_links)
    result = query(test_query)
    final_df = pd.concat([final_df, pd.DataFrame(result).loc[1:, :]], ignore_index=True)

    final_df.drop_duplicates(subset=0, keep='first', inplace=True)
    return final_df

## variables
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


## queries
# modified from:https://github.com/smtifahim/sckan-query-examples/blob/main/example-queries/sckan-sparql-query-examples.ipynb

def neuron_path_query():

    test_query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
    PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
    PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

    SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
    {

       ?Neuron_IRI rdfs:label ?Neuron_Label;
                   ilxtr:hasSomaLocation ?A;
                   ilxtr:hasAxonLocation ?C;
                  (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

       ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

        ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
        ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
        ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    }
    ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species

    """
    result = query(test_query)
    return result

def neuron_path_phenotype_query():

    test_query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
    PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
    PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

    SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
    {

       ?Neuron_IRI rdfs:label ?Neuron_Label.

       ?Neuron_IRI rdfs:label ?Neuron_Label;
                       ilxtr:hasSomaLocation ?A;
                       ilxtr:hasAxonLocation ?C;
                      (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

       ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
       ?Neuron_IRI ilxtr:hasNeuronalPhenotype ?phenotype_link.

       ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
       ?phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?phenotype.
       ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
       ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
       ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

    }
    ORDER BY ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
    """
    result = query(test_query)
    return result


def neuron_circuit_role():
    test_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
        PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

        SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
        {

           ?Neuron_IRI rdfs:label ?Neuron_Label.

           ?Neuron_IRI rdfs:label ?Neuron_Label;
                           ilxtr:hasSomaLocation ?A;
                           ilxtr:hasAxonLocation ?C;
                          (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

           ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
           ?Neuron_IRI ilxtr:hasCircuitRole ?phenotype_link.

           ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
           ?phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?phenotype.
           ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
           ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
           ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

        }
        ORDER BY ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
        """
    result = query(test_query)
    return result

def projection_fibres():

    test_query = """
    SELECT DISTINCT ?Neuron_1_IRI ?Neuron_1_Label
                    ?Neuron_2_IRI ?Neuron_2_Label ?Species
    WHERE
    {
       ?Neuron_1_IRI ilxtr:hasSomaLocation ?Neuron_1_A;
                   (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Neuron_1_B .
    
       ?Neuron_2_IRI ilxtr:hasSomaLocation ?Neuron_2_A;
                   (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ??Neuron_2_B .
    
       ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
       ?Neuron_1_IRI ilxtr:hasForwardConnection ?Neuron_2_IRI .
    
       ?Neuron_1_IRI rdfs:label ?Neuron_1_Label .
       ?Neuron_2_IRI rdfs:label ?Neuron_2_Label .
    
       ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    
    
    }
        """

    result = query(test_query)
    return result


# getting dataframe from queries
def get_neuron_dataframe(result, species_name=None, phenotype_name=None):
    """

    :param result: from queries
    :param species_name: takes only subset for circuit_role (check get_circuit_roles), all from get_species_name
    :param phenotype_name: from get_phenotype_neuron or from get_circuit_roles
    :return:
    """

    df_result = pd.DataFrame(result)
    # get column names right
    df_result.columns = df_result.loc[0, :].to_list()
    df_result = df_result.loc[1:, :]

    # replace duplicate instances of species name
    df_result = df_result.replace('Mammalia', 'Mammal')
    df_result = df_result.replace('mammals', 'Mammal')
    df_result = df_result.replace('Vertebrata <vertebrates>', 'Vertebrata')
    df_result = df_result.replace('vertebrates', 'Vertebrata')
    df_result = df_result.replace('human', 'Homo sapiens')
    df_result = df_result.replace('Norway rat', 'Rattus norvegicus')
    df_result = df_result.replace('brown rat', 'Rattus norvegicus')
    df_result = df_result.replace('rat', 'Rattus norvegicus')
    df_result = df_result.replace('rats', 'Rattus norvegicus')
    df_result = df_result.replace('mouse', 'Mus musculus')
    df_result = df_result.replace('house mouse', 'Mus musculus')

    if phenotype_name:

        if species_name:
            filtered_df = df_result[(df_result.Species == species_name)]
            unique_regions_df = get_unique_regions(filtered_df)
            # Create a dictionary with the values from DataFrame 2 as keys and the replacement values as values
            replacement_dict = dict(zip(unique_regions_df[0], unique_regions_df[1]))

            # # Use the map function to replace the values in DataFrame 1
            filtered_df.loc[:, "Region_A"] = filtered_df.A.map(replacement_dict)
            filtered_df.loc[:, "Region_B"] = filtered_df.B.map(replacement_dict)
            filtered_df.loc[:, "Region_C"] = filtered_df.C.map(replacement_dict)

            # remove duplicate
            filtered_df = filtered_df.drop_duplicates()
            filtered_df = filtered_df[(filtered_df.phenotype == phenotype_name)]

            return filtered_df

        else:
            unique_regions_df = get_unique_regions(df_result)
            # Create a dictionary with the values from DataFrame 2 as keys and the replacement values as values
            replacement_dict = dict(zip(unique_regions_df[0], unique_regions_df[1]))

            # # Use the map function to replace the values in DataFrame 1
            df_result.loc[:, "Region_A"] = df_result.A.map(replacement_dict)
            df_result.loc[:, "Region_B"] = df_result.B.map(replacement_dict)
            df_result.loc[:, "Region_C"] = df_result.C.map(replacement_dict)

            # remove duplicate
            df_result = df_result.drop_duplicates()
            df_result = df_result[(df_result.phenotype == phenotype_name)]

            return df_result

    else:

        if species_name:
            filtered_df = df_result[(df_result.Species == species_name)]
            unique_regions_df = get_unique_regions(filtered_df)
            # Create a dictionary with the values from DataFrame 2 as keys and the replacement values as values
            replacement_dict = dict(zip(unique_regions_df[0], unique_regions_df[1]))

            # # Use the map function to replace the values in DataFrame 1
            filtered_df.loc[:, "Region_A"] = filtered_df.A.map(replacement_dict)
            filtered_df.loc[:, "Region_B"] = filtered_df.B.map(replacement_dict)
            filtered_df.loc[:, "Region_C"] = filtered_df.C.map(replacement_dict)

            # remove duplicate
            filtered_df = filtered_df.drop_duplicates()

            return filtered_df

        else:
            unique_regions_df = get_unique_regions(df_result)
            # Create a dictionary with the values from DataFrame 2 as keys and the replacement values as values
            replacement_dict = dict(zip(unique_regions_df[0], unique_regions_df[1]))

            # # Use the map function to replace the values in DataFrame 1
            df_result.loc[:, "Region_A"] = df_result.A.map(replacement_dict)
            df_result.loc[:, "Region_B"] = df_result.B.map(replacement_dict)
            df_result.loc[:, "Region_C"] = df_result.C.map(replacement_dict)

            # remove duplicate
            df_result = df_result.drop_duplicates()

            return df_result


def projection_fibres_dataframe(result, species_name=None):
    """

        :param result: from queries
        :param species_name: takes only subset for circuit_role (check get_circuit_roles), all from get_species_name
        :param phenotype_name: from get_phenotype_neuron or from get_circuit_roles
        :return:
        """

    df_result = pd.DataFrame(result)
    # get column names right
    df_result.columns = df_result.loc[0, :].to_list()
    df_result = df_result.loc[1:, :]

    # replace duplicate instances of species name
    df_result = df_result.replace('Mammalia', 'Mammal')
    df_result = df_result.replace('mammals', 'Mammal')
    df_result = df_result.replace('Vertebrata <vertebrates>', 'Vertebrata')
    df_result = df_result.replace('vertebrates', 'Vertebrata')
    df_result = df_result.replace('human', 'Homo sapiens')
    df_result = df_result.replace('Norway rat', 'Rattus norvegicus')
    df_result = df_result.replace('brown rat', 'Rattus norvegicus')
    df_result = df_result.replace('rat', 'Rattus norvegicus')
    df_result = df_result.replace('rats', 'Rattus norvegicus')
    df_result = df_result.replace('mouse', 'Mus musculus')
    df_result = df_result.replace('house mouse', 'Mus musculus')

    if species_name:
        filtered_df = df_result[(df_result.Species == species_name)]
        # remove duplicate
        filtered_df = filtered_df.drop_duplicates()

        return filtered_df

    else:
        # remove duplicate
        df_result = df_result.drop_duplicates()

        return df_result
