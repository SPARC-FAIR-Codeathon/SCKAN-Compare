"""
SPARQL query related functions
Adapted from: 
https://github.com/SciCrunch/sparc-curation/blob/master/docs/sckan-python.ipynb
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


example_query = """
# QUERY: List the Neuron Populations where Neurons at Region A Projects to B via C.
# This query returns any neuron population that has its soma located in Region A,
#                                                       axon terminal or axon sensory terminal located in Region B, and 
#                                                       axon located in region C.

PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>

SELECT DISTINCT ?Neuron_ID ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C
{
   ## ***************************** INSTRUCTIONS **************************************** 
   ## UNCOMMENT the lines by removing the hash symbol (#) before FILTER. 
   ## REPLACE the region name on the right side of the equality operator (=) 
   ## by your desired region name within quotes (all in lower case).
   ## ***********************************************************************************  

   ## For exact matching of the regions names
   # FILTER ( LCase(?Region_A) = 'nucleus ambiguus' )
   # FILTER ( LCase(?Region_B) = 'bronchiole parasympathetic ganglia' )
   # FILTER ( LCase(?Region_C) = 'vagus nerve' )
   
   ## For partial matching of region names (label or synonyms)
   # FILTER REGEX ( LCase(?Region_A), 'ambiguus' )
   # FILTER REGEX ( LCase(?Region_B), 'bronchiole parasympathetic' ) 
   # FILTER REGEX ( LCase(?Region_C), 'vagus' )
   
   # FILTER REGEX ( LCase(?Neuron_Label), 'bolew unbranched 25' ) # For partial matching of neuron label
                                                      # Replace 'bolew unbranched 25' within quotes.  

   ?Neuron_ID rdfs:label ?Neuron_Label;
               ilxtr:hasSomaLocation ?A;
               ilxtr:hasAxonLocation ?C;
              (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 
    
          ?A rdfs:label ?Region_A.
          ?B rdfs:label ?Region_B.
          ?C rdfs:label ?Region_C. 
}
ORDER BY ?Neuron_ID ?Region_A ?Region_B ?Region_C
LIMIT 50
"""