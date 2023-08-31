"""
A package for retrieving and visualizing data contained in SCKAN
(e.g., across species, relationship to spinal segments) to highlight
similarities and differences in neuronal pathways

License: Apache License 2.0
"""

import os
import json
import time
import pkg_resources

from . import globals
from . import query
from . import utils
from .cachemanager import CacheManager
from .anatomyvis import AntomyVis
from .blockvis import BlockVis


class SckanCompare(object):
    """
    Base class for accessing functionality
    """

    def __init__(self, endpoint=globals.BLAZEGRAPH_ENDPOINT, max_cache_days=globals.DEFAULT_MAX_CACHE_DAYS):
        """
        Initialize SckanCompare object.

        Parameters
        ----------
        endpoint : str, optional
            The Blazegraph endpoint URL. Defaults to globals.BLAZEGRAPH_ENDPOINT (https://blazegraph.scicrunch.io/blazegraph/sparql).
        max_cache_days : int, optional
            Maximum number of days to keep cached data. Defaults to globals.DEFAULT_MAX_CACHE_DAYS (7 days).
        """
        self.endpoint = endpoint

        self.cache_manager = CacheManager(os.path.join(
            os.path.dirname(__file__), 'api_cache'), max_cache_days)
        
        self.valid_species_list = self.get_valid_species().values()

    def get_valid_species(self):
        """
        Retrieve a list of valid species from the data source.

        Returns
        -------
        dict
            Dict with valid species URIs as keys and corresponding labels as values.
        """
        temp_species = self.execute_query(query.species_without_synonyms_query)
        # Note: query returns some synonyms for certain entries
        # TODO: Discuss with SPARC team why this is so
        # Temporary solution: additional manual mapping
        temp_dict = {}
        for item in temp_species[1:]:
            if item[1] in globals.DUPLICATE_SPECIES_RESOLVER.keys():
                temp_dict[item[0]] = globals.DUPLICATE_SPECIES_RESOLVER[item[1]]
            else:
                temp_dict[item[0]] = item[1]
        return temp_dict
    
    def get_valid_phenotypes(self):
        """
        Retrieve a list of valid phenotypes from the data source.

        Returns
        -------
        dict
            Dict with valid phenotypes URIs as keys and corresponding labels as values.
        """
        temp_phenotypes = self.execute_query(query.combined_phenotypes_all_species_query)
        temp_dict = {}
        for item in temp_phenotypes[1:]:
            temp_dict[item[0]] = item[1]
        return temp_dict
    
    def get_valid_phenotypes_circuit_role(self):
        """
        Retrieve a list of valid phenotypes with circuit role from the data source.

        Returns
        -------
        dict
            Dict with valid phenotypes URIs as keys and corresponding labels as values.
        """
        temp_phenotypes = self.execute_query(query.combined_circuit_role_phenotypes_all_species_query)
        temp_dict = {}
        for item in temp_phenotypes[1:]:
            temp_dict[item[0]] = item[1]
        return temp_dict

    def get_valid_regions_specify_species(self, species, region=None):
        """
        Retrieve a list of valid regions for a specific species from the data source.

        Parameters
        ----------
        species : str
            The species for which to retrieve valid regions.
        region: str, optional
            The region for which to retrieve valid regions.
            Valid values are: A, B, C or None. Defaults to None and returns all regions.

        Returns
        -------
        dict
            Dict of valid region URIs as keys and corresponding labels as values
        """
        if not species:
            raise ValueError("species needs to be specified!")
        if species not in self.valid_species_list:
            raise ValueError("Invalid species specified!")
        if species not in globals.AVAILABLE_SPECIES_MAPS.keys():
            raise ValueError("Not currently implemented for species = {}!".format(species))
        if not region:
            temp_regions = self.execute_query(query.combined_regions_specify_species_without_synonyms_query, species)
        elif region == "A":
            temp_regions = self.execute_query(query.regionsA_specify_species_with_synonyms_query, species)
        elif region == "B":
            temp_regions = self.execute_query(query.regionsB_specify_species_with_synonyms_query, species)
        elif region == "C":
            temp_regions = self.execute_query(query.regionsC_specify_species_with_synonyms_query, species)
        else:
            raise ValueError("Invalid region specified!")
        
        # mapping of region labels to URIs done based on stored JSON files for each species
        # TODO: currently works only for species with available JSON maps
        datapath = pkg_resources.resource_filename("sckan_compare", "data")
        filepath = os.path.join(datapath, globals.AVAILABLE_SPECIES_MAPS[species])
        with open(filepath, encoding='utf-8-sig') as json_file:
            data = json.load(json_file)
        region_map = {}
        for item in data:
            region_map[item["URL"]] = item["Name"]

        temp_dict = {}
        for item in temp_regions[1:]:
            if item[0] not in region_map.keys():
                # only considering regions present in current JSON maps
                # ignoring and dropping other regions
                # TODO: handle this in future
                continue
            temp_dict[item[0]] = region_map[item[0]]

        return temp_dict

    def execute_query(self, query_string, species=None, cached=True):
        """
        Execute a SPARQL query and return the result.

        Parameters
        ----------
        query_string : str
            The SPARQL query string to execute.
        species : str, optional
            The species to consider in the query, if applicable.
        cached : bool, optional
            Whether to use cached data if available. Defaults to False.

        Returns
        -------
        list
            The query result.
        """
        # identify if species placeholder present in query_string
        if "{species_param}" in query_string:
            if not species:
                raise ValueError("species needs to be specified!")
            if species not in self.valid_species_list:
                raise ValueError("Invalid species specified!")
            query_with_species = query_string.format(species_param=species)
        else:
            query_with_species = query_string

        if cached:
            cached_data = self.cache_manager.get_cached_data(
                query_with_species + self.endpoint)
            if cached_data:
                # to check for outdated cache
                cached_time, data = cached_data
                now = time.time()
                if (now - cached_time) > (self.cache_manager.max_cache_days * 86400):
                    # if outdated, remove the item; fetch afresh
                    self.cache.pop(query_with_species + self.endpoint)
                else:
                    # return cached data
                    return data
        data = query.sparql_query(query_with_species, endpoint=self.endpoint)
        # cache the result
        self.cache_manager.cache_data(query_with_species + self.endpoint, data)
        return data
    
    def replace_species_synonyms_dataframe(self, df):
        """
        Replace species synonyms in a DataFrame with unique labels.

        e.g. 'Rattus norvegicus' : http://purl.obolibrary.org/obo/NCBITaxon_10116
        has several synonyms, such as 'brown rat', 'Norway rat', 'rats', 'rat'.
        This method is used to map these synonyms to the parent label.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing species information.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with replaced species synonyms.
        """
        uri_label_dict = self.get_valid_species()

        # update values in dataframe
        if 'Species' in df.columns:
            df['Species'] = df['Species_link'].map(uri_label_dict)
        return df

    def replace_region_synonyms_dataframe(self, df, species):
        """
        Replace region synonyms in a DataFrame with unique labels.

        e.g. 'ovary' :  http://purl.obolibrary.org/obo/UBERON_0000992
        has several synonyms, such as 'animal ovary', 'female gonad', etc.
        This method is used to map these synonyms to the parent label.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing region information.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with replaced region synonyms.
        """
        if not species:
            raise ValueError("species needs to be specified!")
        if species not in self.valid_species_list:
            raise ValueError("Invalid species specified!")
        if species not in globals.AVAILABLE_SPECIES_MAPS.keys():
            raise ValueError("Not currently implemented for species = {}!".format(species))

        uri_label_dict = self.get_valid_regions_specify_species(species=species)

        # update values in dataframe
        if 'Region_A' in df.columns:
            df['Region_A'] = df['A'].map(uri_label_dict)
        if 'Region_B' in df.columns:
            df['Region_B'] = df['B'].map(uri_label_dict)
        if 'Region_C' in df.columns:
            df['Region_C'] = df['C'].map(uri_label_dict)
        return df

    def get_filtered_dataframe(self, result, species=None, filter_column=None, filter_value=None):
        """
        Create a filtered DataFrame from a query result.
        Replaces all synonyms for species and regions with unique labels,
        followed by the deletion of duplicate rows.

        Parameters
        ----------
        data : list
            The query result.
        species : str
            The species for which the data is provided.
        filter_column : str, optional
            The column to be filtered.
        filter_value : str, optional
            The value to be used for filtering column.

        Returns
        -------
        pandas.DataFrame
            The filtered DataFrame.
        """
        if not species:
            raise ValueError("species needs to be specified!")
        if species not in self.valid_species_list:
            raise ValueError("Invalid species specified!")
        if species not in globals.AVAILABLE_SPECIES_MAPS.keys():
            raise ValueError("Not currently implemented for species = {}!".format(species))
        
        # convert data to pandas dataframe with column names
        df_result = utils.get_dataframe(result)

        # replace duplicate instances of species name
        df_result = self.replace_species_synonyms_dataframe(df_result)

        # replace synonyms with unique labels for each region
        df_result = self.replace_region_synonyms_dataframe(df_result, species)

        # filter dataframe based on filter_column and filter_value
        if filter_column:
            if not filter_value:
                raise ValueError("filter_value not for specified column {}!".format(filter_column))
            df_result = utils.filter_dataframe(df_result, filter_column, filter_value)

        # remove duplicate rows based on all columns  
        df_result = df_result.drop_duplicates()

        return df_result

    def plot_dataframe_anatomy_vis(self, df, species=None, region_A=None, region_B=None, region_C=None):
        """
        Plot anatomical connectivity map based on a DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing connectivity information.
        species : str, optional
            The species for visualization.
        region_A : str, optional
            The source region for filtering.
        region_B : str, optional
            The target region for filtering.
        region_C : str, optional
            The intermediate region for filtering.

        Returns
        -------
        go.FigureWidget
            The Plotly figure widget.
        """
        # create AntomyVis object
        vis = AntomyVis(species)
        
        # plot all connections in dataframe
        vis.plot_dataframe(df)

        return vis.fig
    
    def plot_dataframe_block_vis(self, df, region_A=None, region_B=None):
        """
        Plot anatomical connectivity map based on a DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing connectivity information.
        species : str, optional
            The species for visualization.
        region_A : str, optional
            The source region for filtering.
        region_B : str, optional
            The target region for filtering.

        Returns
        -------
        go.FigureWidget
            The Plotly figure widget.
        """
        # create AntomyVis object
        vis = BlockVis()

        # plot all connections in dataframe
        vis.plot_figure(df, region_A, region_B)

        return vis.fig