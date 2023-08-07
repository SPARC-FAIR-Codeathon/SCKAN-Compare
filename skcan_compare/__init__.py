"""
A package for retrieving and visualizing data contained in SCKAN
(e.g., across species, relationship to spinal segments) to highlight
similarities and differences in neuronal pathways

License: Apache License 2.0
"""

import os
import json
import pkg_resources

from . import globals
from . import query
from .visualize import Visualizer


class SkcanCompare(object):
    """
    Base class for accessing functionality
    """

    def __init__(self, endpoint=globals.BLAZEGRAPH_ENDPOINT):
        self.endpoint = endpoint
        self.region_dict = {}
        self.vis = None

    def execute_query(self, query_string):
        # execute specified SPAQRL query and return result
        return query.sparql_query(query_string, endpoint=self.endpoint)


    def load_json_file(self, species="human"):
        if species == "human":
            datapath = pkg_resources.resource_filename("skcan_compare", "data")
            filepath = os.path.join(datapath, "coords_human.json")
        else:
            # todo: add other species
            return

        with open(filepath, encoding='utf-8-sig') as json_file:
            data = json.load(json_file)

        self.region_dict[species] = {}
        for item in data:
            self.region_dict[species][item["Name"]] = [int(item["X"]), int(item["Y"])]

    def init_vis(self, species=None):
        if species not in self.region_dict.keys():
            self.load_json_file(species=species)
        if not self.vis:
            self.vis = Visualizer(self.region_dict[species])
        return self.vis

    def add_connection(self, species=None, region_A=None, region_B=None, region_C=None, neuron=None):
        vis = self.init_vis(species)

        if not region_A:
            raise ValueError("region_A needs to be specified!")
        if not region_B:
            raise ValueError("region_B needs to be specified!")

        if region_C:
            # A->C->C
            vis.draw_edge_ABC(region_A, region_B, region_C, neuron)
        else:
            # A->B
            vis.draw_edge_AB(region_A, region_B, neuron)

        return vis.get_figure()