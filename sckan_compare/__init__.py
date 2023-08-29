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
from .visualize import Visualizer


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
        self.anatomy_map_dict = {}

        self.cache_manager = CacheManager(os.path.join(
            os.path.dirname(__file__), 'api_cache'), max_cache_days)
        
        self.valid_species_list = self.get_valid_species_list()

    def get_valid_species_list(self):
        """
        Retrieve a list of valid species from the data source.

        Returns
        -------
        list
            List of valid species.
        """
        temp_species = self.execute_query(query.species_without_synonyms_query)
        # Note: query returns some synonyms for certain entries
        # TODO: Discuss with SPARC team why this is so
        # Temporary solution: additional manual mapping
        species_list = []
        for item in temp_species[1:]:
            if item[1] in globals.DUPLICATE_SPECIES_RESOLVER.keys():
                species_list.append(globals.DUPLICATE_SPECIES_RESOLVER[item[1]])
            else:
                species_list.append(item[1])
        return sorted(list(set(species_list)))
    
    def get_valid_regions_all_species(self):
        """
        Retrieve a list of valid regions for all species from the data source.

        Returns
        -------
        list
            List of valid regions for all species.
        """
        temp_regions = self.execute_query(query.combined_regions_all_species_without_synonyms_query)
        return [item[0] for item in temp_regions]

    def get_valid_regions_for_species(self, species):
        """
        Retrieve a list of valid regions for a specific species from the data source.

        Parameters
        ----------
        species : str
            The species for which to retrieve valid regions.

        Returns
        -------
        list
            List of valid regions for the specified species.
        """
        temp_regions = self.execute_query(query.combined_regions_specify_species_without_synonyms_query, species)
        return [item[0] for item in temp_regions]

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
        output = self.execute_query(query.species_without_synonyms_query)
        uri_label_dict = {}
        # first element is column labels, so ignore
        for item in output[1:]:
            if item[0] in uri_label_dict:
                # Note: query returns some synonyms for certain entries
                # TODO: Discuss with SPARC team why this is so
                # Temporary solution:
                # -> Handling this now by picking shortest label
                if len(item[1]) >= len(uri_label_dict[item[0]]):
                    continue
            uri_label_dict[item[0]] = item[1]
        
        # update values in dataframe
        if 'Species' in df.columns:
            df['Species'] = df['Species_link'].map(uri_label_dict)
        return df

    def replace_region_synonyms_dataframe(self, df):
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

        output = self.execute_query(query.combined_regions_all_species_without_synonyms_query)
        uri_label_dict = {}
        # first element is column labels, so ignore
        for item in output[1:]:
            # Note: query returns some synonyms for certain entries
            # TODO: Discuss with SPARC team why this is so
            # Temporary solution: additional manual mapping
            if item[1] in globals.DUPLICATE_SPECIES_RESOLVER.keys():
                uri_label_dict[item[0]] = globals.DUPLICATE_SPECIES_RESOLVER[item[1]]
            else:
                uri_label_dict[item[0]] = item[1]

        # update values in dataframe
        if 'Region_A' in df.columns:
            df['Region_A'] = df['A'].map(uri_label_dict)
        if 'Region_B' in df.columns:
            df['Region_B'] = df['B'].map(uri_label_dict)
        if 'Region_C' in df.columns:
            df['Region_C'] = df['C'].map(uri_label_dict)
        return df

    def get_filtered_dataframe(self, result):
        """
        Create a filtered DataFrame from a query result.
        Replaces all synonyms for species and regions with unique labels,
        followed by the deletion of duplicate rows.

        Parameters
        ----------
        result : list
            The query result.

        Returns
        -------
        pandas.DataFrame
            The filtered DataFrame.
        """
        # convert data to pandas dataframe with column names
        df_result = utils.get_dataframe(result)

        # replace duplicate instances of species name
        df_result = utils.remove_duplicate_species(df_result)

        # replace synonyms with unique labels for each region
        df_result = self.replace_region_synonyms(df_result)

        # remove duplicate rows based on all columns  
        df_result = df_result.drop_duplicates()

        return df_result

    def load_json_species_map(self, species=None):
        """
        Load a JSON species map for visualization.

        Parameters
        ----------
        species : str, optional
            The species for which to load the map.

        Raises
        ------
        ValueError
            If an invalid species is specified.
        """
        if not species:
            raise ValueError("species needs to be specified!")
        if species not in self.valid_species:
            raise ValueError("Invalid species specified!")
        if species not in globals.AVAILABLE_SPECIES_MAPS.keys():
            raise ValueError("{} visual map not currently available!".format(species))
        
        datapath = pkg_resources.resource_filename("sckan_compare", "data")
        filepath = os.path.join(datapath, globals.AVAILABLE_SPECIES_MAPS[species])

        with open(filepath, encoding='utf-8-sig') as json_file:
            data = json.load(json_file)

        self.anatomy_map_dict[species] = {}
        for item in data:
            self.anatomy_map_dict[species][item["Name"]] = [
                int(item["X"]), int(item["Y"])]

    def add_connection(self, vis_obj, region_A=None, region_B=None, region_C=None, neuron=None):
        """
        Add a connection to a visualization object.

        Parameters
        ----------
        vis_obj : Visualizer
            The visualization object.
        region_A : str, optional
            The source region of the connection.
        region_B : str, optional
            The target region of the connection.
        region_C : str, optional
            An intermediate region for connections.
        neuron : str, optional
            The associated neuron.

        Raises
        ------
        ValueError
            If required parameters are missing.
        """
        if not region_A:
            raise ValueError("region_A needs to be specified!")
        if not region_B:
            raise ValueError("region_B needs to be specified!")

        if region_C:
            # A->C->B
            vis_obj.draw_edge_ABC(region_A, region_B, region_C, neuron)
        else:
            # A->B
            vis_obj.draw_edge_AB(region_A, region_B, neuron)

    def plot_dataframe_connectivity(self, df, species=None, region_A=None, region_B=None, region_C=None):
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
        Visualizer
            The visualization object.
        """
        # load the species specific visual map
        self.load_json_species_map(species)

        # create visualizer object
        vis = Visualizer(self.anatomy_map_dict[species], species)
        
        # add all connections specified in dataframe
        for idx in range(df.shape[0]):
            if 'Region_C' in df.columns:
                self.add_connection(vis,
                                    region_A=df.iloc[idx,3],
                                    region_B=df.iloc[idx,5],
                                    region_C=df.iloc[idx,7],
                                    neuron=df.iloc[idx,1])
            else:
                self.add_connection(vis,
                                    region_A=df.iloc[idx,3],
                                    region_B=df.iloc[idx,5],
                                    neuron=df.iloc[idx,1])
        return vis