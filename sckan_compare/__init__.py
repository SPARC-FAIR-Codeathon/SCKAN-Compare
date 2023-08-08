"""
A package for retrieving and visualizing data contained in SCKAN
(e.g., across species, relationship to spinal segments) to highlight
similarities and differences in neuronal pathways

License: Apache License 2.0
"""

import os
import json
import pkg_resources
import numpy as np
import pandas as pd

from . import globals
from . import query
from .visualize import Visualizer


class SckanCompare(object):
    """
    Base class for accessing functionality
    """

    def __init__(self, species="Homo sapiens", endpoint=globals.BLAZEGRAPH_ENDPOINT):
        self.endpoint = endpoint
        self.region_dict = {}
        self.vis = None
        self.species = species
        self.load_json_file()

    def execute_query(self, query_string):
        # execute specified SPAQRL query and return result
        return query.sparql_query(query_string, endpoint=self.endpoint)


    def load_json_file(self):
        datapath = pkg_resources.resource_filename("sckan_compare", "data")
        if self.species == "Mus musculus":
            filepath = os.path.join(datapath, "coords_mouse.json")
        elif self.species == "Rattus norvegicus":
            filepath = os.path.join(datapath, "coords_rat.json")
        else:
            # default
            filepath = os.path.join(datapath, "coords_human.json")

        with open(filepath, encoding='utf-8-sig') as json_file:
            data = json.load(json_file)

        self.region_dict[self.species] = {}
        for item in data:
            self.region_dict[self.species][item["Name"]] = [int(item["X"]), int(item["Y"])]
   
    def reset_vis(self):
        self.vis = Visualizer(self.region_dict[self.species], self.species)
        return self.vis

    def add_connection(self, region_A=None, region_B=None, region_C=None, neuron=None):
        if not self.vis:
            self.vis = Visualizer(self.region_dict[self.species], self.species)

        if not region_A:
            raise ValueError("region_A needs to be specified!")
        if not region_B:
            raise ValueError("region_B needs to be specified!")

        if region_C:
            # A->C->B
            self.vis.draw_edge_ABC(region_A, region_B, region_C, neuron)
        else:
            # A->B
            self.vis.draw_edge_AB(region_A, region_B, neuron)


    def get_graph(self):
        return self.vis.get_figure()
    

    def get_unique_region_IRI(self, df_result):
        """
        :param df_result: dataframe
        :return: unique regions in form of hyperlinks
        """
        region_A = np.unique(df_result.loc[:,"A"])
        region_B = np.unique(df_result.loc[:,"B"])
        region_C = np.unique(df_result.loc[:,"C"])
        unique_regions = np.unique(np.concatenate((region_A, region_B, region_C)))
        return unique_regions

    
    def get_unique_regions (self, df_result):
        """
        :param df_result: dataframe
        :return: region labels
        """
        unique_regions = self.get_unique_region_IRI(df_result)
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
        result = self.execute_query(test_query)
        final_df = pd.DataFrame(result).loc[1:, :]

        # rest 100
        formatted_links = " ,".join(["<{}>".format(link) for link in unique_regions[100:200]])
        test_query = test_template.format(formatted_links)
        result = self.execute_query(test_query)
        final_df = pd.concat([final_df, pd.DataFrame(result).loc[1:, :]], ignore_index=True)

        # rest all
        formatted_links = " ,".join(["<{}>".format(link) for link in unique_regions[200:]])
        test_query = test_template.format(formatted_links)
        result = self.execute_query(test_query)
        final_df = pd.concat([final_df, pd.DataFrame(result).loc[1:, :]], ignore_index=True)

        final_df.drop_duplicates(subset=0, keep='first', inplace=True)
        return final_df
    
    # getting dataframe from queries
    def get_neuron_dataframe(self, result, species_name=None, phenotype_name=None):
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
                unique_regions_df = self.get_unique_regions(filtered_df)
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
                unique_regions_df = self.get_unique_regions(df_result)
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
                unique_regions_df = self.get_unique_regions(filtered_df)
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
                unique_regions_df = self.get_unique_regions(df_result)
                # Create a dictionary with the values from DataFrame 2 as keys and the replacement values as values
                replacement_dict = dict(zip(unique_regions_df[0], unique_regions_df[1]))

                # # Use the map function to replace the values in DataFrame 1
                df_result.loc[:, "Region_A"] = df_result.A.map(replacement_dict)
                df_result.loc[:, "Region_B"] = df_result.B.map(replacement_dict)
                df_result.loc[:, "Region_C"] = df_result.C.map(replacement_dict)

                # remove duplicate
                df_result = df_result.drop_duplicates()

                return df_result

    def projection_fibres_dataframe(self, result, species_name=None):
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
            unique_regions_df = self.get_unique_regions(filtered_df)
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
            unique_regions_df = self.get_unique_regions(df_result)
            # Create a dictionary with the values from DataFrame 2 as keys and the replacement values as values
            replacement_dict = dict(zip(unique_regions_df[0], unique_regions_df[1]))

            # # Use the map function to replace the values in DataFrame 1
            df_result.loc[:, "Region_A"] = df_result.A.map(replacement_dict)
            df_result.loc[:, "Region_B"] = df_result.B.map(replacement_dict)
            df_result.loc[:, "Region_C"] = df_result.C.map(replacement_dict)

            # remove duplicate
            df_result = df_result.drop_duplicates()

            return df_result

# visualising projections of neurons
import dash
import dash_cytoscape as cyto
import dash_html_components as html

def visualise_projection(result_df):
    
    # getting unique nodes
    a = np.unique(result_df.loc[:,'Neuron_1_Label'])
    b = np.unique(result_df.loc[:,'Neuron_2_Label'])
    unique_nodes= np.unique(np.concatenate((a,b)))
        
    nodes = []
    for node in unique_nodes:
        nodes.append({"data": {"id": node, "label": node}})
    
    # construct connections between these nodes as required
    edges = []
    for i in range(len(result_df)):
        item = {"data": {"source": result_df.iloc[i,0], "target": result_df.iloc[i,1]}}
        edges.append(item)
    
    elements = nodes + edges

    #defines styling for the plot
    default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "width": "mapData(size, 0, 100, 20, 60)",
            "height": "mapData(size, 0, 100, 20, 60)",
            "content": "data(label)",
            "font-size": "10px",
            "text-valign": "center",
            "text-halign": "center",}
    },
        {
            "selector": "edge",
            "style": {
             #'line-style': 'dashed',
            'target-arrow-color': 'black',
            'target-arrow-shape': 'vee',
            'curve-style' : 'straight',}
      }
    ]


    app = dash.Dash(__name__)
    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            elements=elements,
            stylesheet = default_stylesheet,
            style={'width': '100%', 'height': '400px', 'background-image': 'url(./sample_bg.png)'},
            layout={
                # 'name': 'preset'
                'name': 'cose'
                # 'name': 'random'
                #'name': 'circle'
                # 'name': 'grid'
            }
            
        )
    ])
    
    
    if __name__ == '__main__':
        app.run_server(debug=True, port=8051)
