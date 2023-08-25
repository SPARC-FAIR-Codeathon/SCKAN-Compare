"""
Configuration and constants for SckanCompare package.

License: Apache License 2.0
"""

# Blazegraph endpoint URL
BLAZEGRAPH_ENDPOINT = "https://blazegraph.scicrunch.io/blazegraph/sparql"

# Default maximum number of days to keep cached data
DEFAULT_MAX_CACHE_DAYS = 7

# Mapping of species to their respective JSON coordinate maps
AVAILABLE_SPECIES_MAPS = {
    "Mus musculus": "coords_mouse.json",
    "Rattus norvegicus": "coords_rat.json",
    "Homo sapiens": "coords_human.json",
}