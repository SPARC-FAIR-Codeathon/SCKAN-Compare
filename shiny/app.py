
from shiny import App, Inputs, Outputs, Session, render, ui,  render_text
import shinyswatch
import pandas as pd
import utils
import plotly.express as px
#import the base class to access all features
from sckan_compare import SckanCompare
# access query sub-module; we can add all template queries in here and import as required
from sckan_compare import query
from sckan_compare.simplevis import SimpleVisualizer
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.graph_objs as go

import numpy as np
from urllib.parse import quote as url_quote


###
file_name = "organ_region.xlsx"
organ_region  = pd.read_excel(file_name)
neurons= utils.neuron_path_query() # get df all data query  ### uses package
df = px.data.tips()
cir = utils.neuron_circuit_role() # get hasCircuitRole query
phenotype = utils.neuron_path_phenotype_query()
sc = SckanCompare()
result = sc.execute_query(query.neuron_path_query)
#############################################################################################################################
app_ui = ui.page_fluid(
    ui.panel_title("SCKAN-Compare"),
    shinyswatch.theme.darkly(),

    ui.layout_sidebar(

        #sidebar
        ui.panel_sidebar(

            ui.input_select(
                "sp1", label="Select target Species",
                choices=["Homo sapiens", "Mus musculus","Rattus norvegicus"]
            ),
            ui.input_select(
                "sp2", label="And",
                choices=["Homo sapiens", "Mus musculus","Rattus norvegicus"]
            ),
            ui.input_select(
                "or1", label="Select target Start Organs",
                choices=["Face", "Gut", "Heart & large vessels", "Pelvic", "Reproductive System", "Spinal Cord"]
            ),
            ui.input_select(
                "or2", label=" End organ",
                choices=["Face", "Gut", "Heart & large vessels", "Pelvic", "Reproductive System", "Spinal Cord"]
            ),

        ),
        #main panel
        ui.panel_main(
            ui.navset_tab(
                ui.nav("Table", 
                       ui.tags.h4("The neuronal pathways linking the start region to the end region include the following:"),
                       ui.input_numeric("nb", "Number of rows to show", value=3),
                       ui.column(12, ui.output_text_verbatim("species1"), ui.output_table("table1")),
                       ui.column(12, ui.output_text_verbatim("species2"), ui.output_table("table2")),
 
                       ),
                ui.nav("Body Map", 
                         ui.tags.h4("The neuronal pathways linking the start region to the end region include multiple pathways."),
                         
                         ui.column(12,
                          ui.input_text("mst1","Select target start region", placeholder=""),
                          ui.input_text("emn1", "Select target end region", placeholder=""),
                          output_widget("map1")     
                                   ),
                         ui.column(12,
                          ui.input_text("mst2", "Select target start region", placeholder=""),
                          ui.input_text("men2", "Select target end region", placeholder=""),  
                          output_widget("map2") 
                                   ),
                         
                       ),
                ui.nav("Graphic", 
                         ui.tags.h4("The neuronal pathways linking the start region to the end region include multiple pathways."),
                         
                         ui.column(12,
                          ui.input_text("st1","Select target start region", placeholder="Eg. first sacral dorsal root ganglion"),
                          ui.input_text("en1", "Select target end region", placeholder="Eg. Arteriole in connective tissue of bladder dome"),
                          output_widget("Graph1")     
                                   ),
                         ui.column(12,
                          ui.input_text("st2", "Select target start region", placeholder=""),
                          ui.input_text("en2", "Select target end region", placeholder=""),  
                          output_widget("Graph2") 
                                   ),
                         
                       ),

            )
        ),
    ),

)

#############################################################################################################################
def server(input, output, session):
    @output
    @render.text
    def species1():
        return f"{input.sp1()}"
    
    @output
    @render.text
    def species2():
        return f"{input.sp2()}"
    
    @output
    @render.table
    def table1():
        # filter pathway target specie 1
        input_sp1 = input.sp1()
        sp1_pathway= utils.get_neuron_dataframe(neurons, species_name=input_sp1 , phenotype_name=None) ### uses package
        columns_to_keep = ["Neuron_Label", "Region_A", "Region_B", "Region_C"]
        sp1_pathway =sp1_pathway[columns_to_keep]
        #filter organs 
        organ_region_sp1  = organ_region [organ_region ['specie'] ==input_sp1]
        start_organ_sp1 = organ_region[(organ_region['organ'] == input.or1())] #
        end_organ_sp1 = organ_region[(organ_region['organ'] == input.or2())]
        # Convert region column in start_organ_sp1 df to _start_list
        start_list = start_organ_sp1['region'].tolist()
        end_list = end_organ_sp1['region'].tolist()
        filtered_data_sp1 = sp1_pathway[sp1_pathway['Region_A'].isin(start_list)]
        final_filtered_data_sp1 = filtered_data_sp1[filtered_data_sp1['Region_B'].isin(end_list)]      
                # Renaming  columns
        final_filtered_data_sp1  = final_filtered_data_sp1.rename(columns={
                'Region_A': 'Start Region',
                'Region_C': 'Intermediate Region',
                'Region_B': 'End Region'
            })
        final_filtered_data_sp1 = final_filtered_data_sp1.drop_duplicates(keep='first')
        #phenotype
        hasCircuitRole= utils.get_neuron_dataframe(cir, species_name=input_sp1, phenotype_name=None) # fiilter specie + their hasCircuitRole   
        hasNeuronalPhenotype = utils.get_neuron_dataframe(phenotype, species_name=input_sp1, phenotype_name=None) # fiilter specie + their hasNeuronalPhenotype
        columns_to_keep2 = ["Neuron_Label", "Region_A", "Region_B", "Region_C", "phenotype"]
        #

        hasNeuronalPhenotype=  hasNeuronalPhenotype[columns_to_keep2]        
        hasNeuronalPhenotype = hasNeuronalPhenotype.rename(columns={
                'Region_A': 'Start Region',
                'Region_C': 'Intermediate Region',
                'Region_B': 'End Region',
                'phenotype': 'Neuronal Phenotype'
            })      
        # Filter the rows with the same values in the specified columns
        final_filtered_data_sp1 = final_filtered_data_sp1.merge(
            hasNeuronalPhenotype,
            on=["Neuron_Label", "Start Region", "End Region", "Intermediate Region"],
            how="inner"
        )
        #
        hasCircuitRole=  hasCircuitRole[columns_to_keep2]
        hasCircuitRole =hasCircuitRole.rename(columns={
                'Region_A': 'Start Region',
                'Region_C': 'Intermediate Region',
                'Region_B': 'End Region',
                'phenotype': 'Circuit Role'
            })
        final_filtered_data_sp1 = final_filtered_data_sp1.merge(
                hasCircuitRole,
                on=["Neuron_Label", "Start Region", "End Region", "Intermediate Region"],
                how="left"  # Use "left" join to keep all rows from filtered_rows
            )
        # add hasCircuitRol data
        return final_filtered_data_sp1.head(input.nb())
    
    @output
    @render.table
    def table2():
        # filter pathway target specie 2
        input_sp2 =input.sp2()
        sp2_pathway= utils.get_neuron_dataframe(neurons, species_name=input_sp2 , phenotype_name=None)  ### uses package
        columns_to_keep = ["Neuron_Label", "Region_A", "Region_B", "Region_C"]
        sp2_pathway =  sp2_pathway[columns_to_keep]
        #filter organs 
        organ_region_sp2  = organ_region[organ_region ['specie'] ==input_sp2]
        start_organ_sp2 = organ_region[(organ_region['organ'] == input.or2())]
        end_organ_sp2 = organ_region[(organ_region['organ'] == input.or2())]
        # Convert region column in start_organ_sp1 df to _start_list
        start_list2 = start_organ_sp2['region'].tolist()
        end_list2 = end_organ_sp2['region'].tolist()
        filtered_data_sp2 = sp2_pathway[sp2_pathway['Region_A'].isin(start_list2)]
        final_filtered_data_sp2 = filtered_data_sp2[filtered_data_sp2['Region_B'].isin(end_list2)]
         # Renaming columns
        final_filtered_data_sp2 = final_filtered_data_sp2.rename(columns={
                'Region_A': 'Start Region',
                'Region_C': 'Intermediate Region',
                'Region_B': 'End Region'
            })
        final_filtered_data_sp2 = final_filtered_data_sp2.drop_duplicates(keep='first')
            #phenotype
        hasCircuitRole2= utils.get_neuron_dataframe(cir, species_name=input.sp2(), phenotype_name=None) # fiilter specie + their hasCircuitRole   
        hasNeuronalPhenotype2 = utils.get_neuron_dataframe(phenotype, species_name=input.sp2(), phenotype_name=None) # fiilter specie + their hasNeuronalPhenotype
        columns_to_keep2 = ["Neuron_Label", "Region_A", "Region_B", "Region_C", "phenotype"]
        #

        hasNeuronalPhenotype2=  hasNeuronalPhenotype2[columns_to_keep2]        
        hasNeuronalPhenotype2 = hasNeuronalPhenotype2.rename(columns={
                'Region_A': 'Start Region',
                'Region_C': 'Intermediate Region',
                'Region_B': 'End Region',
                'phenotype': 'Neuronal Phenotype'
            })      
        # Filter the rows with the same values in the specified columns
        final_filtered_data_sp2 = final_filtered_data_sp2.merge(
            hasNeuronalPhenotype2,
            on=["Neuron_Label", "Start Region", "End Region", "Intermediate Region"],
            how="inner"
        )
        #
        hasCircuitRole2=  hasCircuitRole2[columns_to_keep2]
        hasCircuitRole2 =hasCircuitRole2.rename(columns={
                'Region_A': 'Start Region',
                'Region_C': 'Intermediate Region',
                'Region_B': 'End Region',
                'phenotype': 'Circuit Role'
            })
        final_filtered_data_sp2 = final_filtered_data_sp2.merge(
            hasCircuitRole2,
            on=["Neuron_Label", "Start Region", "End Region", "Intermediate Region"],
            how="left"  # Use "left" join to keep all rows from filtered_rows
        )
        return final_filtered_data_sp2.head(input.nb())
    
    @output
    @render_widget
    def Graph1():
            # creating an instance of our class
            
            sc = SckanCompare(species=input.sp1())
            # to execute a SPARQL query

            result_df = sc.get_neuron_dataframe(result, species_name=input.sp1())
            selected_Region_A = input.st1() 
            selected_Region_B = input.en1() 
            simvis = SimpleVisualizer()
            fig = simvis.plot_figure(result_df, selected_Region_A, selected_Region_B)
            #fig.show()
            #fig
            return fig
    @output
    @render_widget
    def Graph2():
            # creating an instance of our class
            
            sc2 = SckanCompare(species=input.sp2())
            # to execute a SPARQL query
            #result2 = sc2.execute_query(query.neuron_path_query)
            result_df2 = sc2.get_neuron_dataframe(result, species_name=input.sp2())
            selected_Region_A = input.st2() 
            selected_Region_B = input.en2() 
            simvis = SimpleVisualizer()
            fig2 = simvis.plot_figure(result_df2, selected_Region_A, selected_Region_B)
            #fig.show()
            #fig
            return fig2
           
    @output
    @render_widget
    def map1():
            selected_region_A = input.mst1() 
            selected_region_B = input.men1() 
            sc3 = SckanCompare(species=input.sp1())
            # to execute a SPARQL query
            #result3 = sc3.execute_query(query.neuron_path_query)
            result_df3 = sc3.get_neuron_dataframe(result, species_name=input.sp1())
            sc3.reset_vis()
            req_df = result_df3[(result_df3.Region_A == selected_region_A) & (result_df3.Region_B == selected_region_B)]
            sc3.reset_vis()
            for i in range(len(req_df)):
                sc3.add_connection(
                    region_A=req_df.iloc[i, 3],
                    region_B=req_df.iloc[i, 5],
                    region_C=req_df.iloc[i, 7],
                    neuron=req_df.iloc[i, 1]
                )
            fig3  = sc3.get_graph()
            
            return fig3
    
    @output
    @render_widget
    def map2():
            selected_region_A = input.mst2() 
            selected_region_B = input.men2() 
            sc4 = SckanCompare(species=input.sp2())
            # to execute a SPARQL query
            #result2 = sc2.execute_query(query.neuron_path_query)
            result_df4 = sc4.get_neuron_dataframe(result, species_name=input.sp2())
            sc4.reset_vis()
            req_df4 = result_df4[(result_df4.Region_A == selected_region_A) & (result_df4.Region_B == selected_region_B)]
            sc4.reset_vis()
            for i in range(len(req_df4)):
                sc4.add_connection(
                    region_A=req_df4.iloc[i, 3],
                    region_B=req_df4.iloc[i, 5],
                    region_C=req_df4.iloc[i, 7],
                    neuron=req_df4.iloc[i, 1]
                )
            fig4  = sc4.get_graph()
            
            return fig4


app = App(app_ui, server)
