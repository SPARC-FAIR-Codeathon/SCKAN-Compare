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

# Anatomy maps for species to draw background blocks
AVAILABLE_SPECIES_ANATOMY = {
    "Mus musculus": "anatomy_map_mouse_rat.json",
    "Rattus norvegicus": "anatomy_map_mouse_rat.json",
    "Homo sapiens": "anatomy_map_human.json",
}

# Manual workaround for duplicate species
# TODO: Discuss with SPARC team
DUPLICATE_SPECIES_RESOLVER = {
    "Mammalia": "Mammal",
    "mammals": "Mammal",
    "human": "Home sapiens",
    "Norway rat": "Rattus norvegicus",
    "brown rat": "Rattus norvegicus",
    "rat": "Rattus norvegicus",
    "rats": "Rattus norvegicus",
    "mouse": "Mus musculus",
    "house mouse": "Mus musculus",
    "vertebrates": "Vertebrata",
    "Vertebrata <vertebrates>": "Vertebrata",
}