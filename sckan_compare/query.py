"""
SPARQL queries for SckanCompare package.

License: Apache License 2.0
"""

import io
import csv
import requests
from urllib.parse import quote as url_quote

def procq(res):
    _, (str_count,) = res
    return int(str_count)

def sparql_query(query, *, endpoint, **kwargs):
    qq = url_quote(query, safe='')
    url = f'{endpoint}?query={qq}'
    headers = {'Accept': 'text/csv'}
    resp = requests.get(url, headers=headers)
    return list(csv.reader(io.StringIO(resp.text)))


example_query_specify_species = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                ilxtr:hasAxonLocation ?C;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""

example_query_all_species = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                ilxtr:hasAxonLocation ?C;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
}}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""

# Note: this still returns some synonyms for certain entries
# TODO: Discuss with SPARC team why this is so
species_without_synonyms_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Species_link ?Species
{
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Species_link rdfs:label ?Species.
    
}
ORDER BY ?Species_link ?Species
"""

species_with_synonyms_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Species_link ?Species
{
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    
}
ORDER BY ?Species_link ?Species
"""

regionsA_specify_species_with_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Species_link ?Region_A
{{
    ?Neuron_IRI ilxtr:hasSomaLocation ?A;
                ilxtr:isObservedInSpecies ?Species_link.
    
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    
    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Species_link ?Region_A
"""

regionsB_specify_species_with_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Species_link ?Region_B
{{
    ?Neuron_IRI (ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B;
                ilxtr:isObservedInSpecies ?Species_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Species_link ?Region_B
"""

regionsC_specify_species_with_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Species_link ?Region_C
{{
    ?Neuron_IRI ilxtr:hasAxonLocation ?C;
                ilxtr:isObservedInSpecies ?Species_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Species_link ?Region_C
"""

combined_regions_specify_species_without_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Region_URI ?Region
{{

    ?Neuron_IRI (ilxtr:hasSomaLocation | ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Region_URI. 
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Region_URI rdfs:label ?Region.
    
    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Region_URI ?Region
"""

combined_regions_specify_species_with_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Region_URI ?Region
{{

    ?Neuron_IRI (ilxtr:hasSomaLocation | ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Region_URI. 
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Region_URI (rdfs:label | oboInOwl:hasExactSynonym) ?Region.
    
    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Region_URI ?Region
"""

combined_regions_all_species_without_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Region_URI ?Region
{{

    ?Neuron_IRI (ilxtr:hasSomaLocation | ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Region_URI. 
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?Region_URI rdfs:label ?Region.
}}
ORDER BY ?Region_URI ?Region
"""

combined_regions_all_species_with_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Region_URI ?Region
{{

    ?Neuron_IRI (ilxtr:hasSomaLocation | ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Region_URI. 
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?Region_URI (rdfs:label | oboInOwl:hasExactSynonym) ?Region.
}}
ORDER BY ?Region_URI ?Region
"""

combined_phenotypes_all_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Phenotype_link ?Phenotype
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasNeuronalPhenotype ?Phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?Phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
}}
ORDER BY ?Phenotype_link ?Phenotype
"""

combined_phenotypes_specify_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Phenotype_link ?Phenotype
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasNeuronalPhenotype ?Phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?Phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Phenotype_link ?Phenotype
"""

combined_circuit_role_phenotypes_all_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Phenotype_link ?Phenotype
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasCircuitRole ?Phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?Phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
}}
ORDER BY ?Phenotype_link ?Phenotype
"""

combined_circuit_role_phenotypes_specify_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Phenotype_link ?Phenotype
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasCircuitRole ?Phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?Phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Phenotype_link ?Phenotype
"""

neuron_path_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                ilxtr:hasAxonLocation ?C;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""

neuron_path_phenotype_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link ?Phenotype_link ?Phenotype
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label.

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasSomaLocation ?A;
                    ilxtr:hasAxonLocation ?C;
                    (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasNeuronalPhenotype ?Phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?Phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Phenotype_link ?Phenotype
"""

neuron_circuit_role_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link ?Phenotype_link ?Phenotype
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label.

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasSomaLocation ?A;
                    ilxtr:hasAxonLocation ?C;
                    (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasCircuitRole ?Phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?Phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?Phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Phenotype_link ?Phenotype
"""

projection_fibres_query = """
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

app_query = """
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
   
   ?Neuron_IRI ilxtr:isObservedInSpecies/rdfs:label ?Species.
   ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    
}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""