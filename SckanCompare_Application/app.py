from shiny import App, render, App, Session, reactive, ui
import shinyswatch
from shinywidgets import output_widget, render_widget
from sckan_compare import SckanCompare
from sckan_compare import query
import numpy as np
import pandas as pd
#
species_choices = {"Homo sapiens": "Human", "Mus musculus": "Mouse", "Rattus norvegicus": "Rat"}#from organ_region df
viz_choices = {"T": "Table",  "M": "Map", "G": "Graph"}
columns_to_keep = ["Neuron_Label", "Region_A", "Region_B", "Region_C"]
#
sc = SckanCompare()
result = sc.execute_query(query.neuron_path_all_species_query)
#phenotype = sc.execute_query(query.neuron_path_phenotype_all_species_query) 
#cir = sc.execute_query(query.neuron_circuit_role_all_species_query)

#############################################################################################################################

app_ui = ui.page_fluid(
    ui.panel_title("SCKAN-Compare"),
    shinyswatch.theme.darkly(),
    ui.layout_sidebar(
        #sidebar
        ui.panel_sidebar(
            ui.input_select(  "sp1", label="Select target Species", choices= species_choices),
            ui.input_select( "sp2", label="And", choices= species_choices  ),
            ui.tags.h4("Select target start and end regions for"), ui.output_text_verbatim("species1"),
            ui.input_text("rgst1","Select target start region", placeholder="Eg. first sacral dorsal root ganglion"), #delete
            ui.input_text("rgen1", "Select target end region", placeholder="Eg. Arteriole in connective tissue of bladder dome"), #delete
            ui.tags.h4("Select target start and end regions for"), ui.output_text_verbatim("species2"),
            ui.input_text("rgst2","Select target start region", placeholder="Eg. first sacral dorsal root ganglion"),
            ui.input_text("rgen2", "Select target end region", placeholder="Eg. Arteriole in connective tissue of bladder dome"),
            ui.input_radio_buttons("viz_type", "Visualization Option", viz_choices),
            #ui.p(ui.input_action_button("submit_bt", "Submit")),  # submit button not working yet
        ),
        #main panel
        ui.panel_main(
            ui.tags.h4("The neuronal pathways linking the start region to the end region include the following:"),
            #sp1
            ui.tags.h5('First Species Result'), 
                ui.column(12,  ui.output_table("Table1") ),
                ui.column(12,  output_widget("map1") ),
                ui.column(12,output_widget("Graph1") ),
                #ui.input_numeric("nb", "Number of rows to show", value=3),
                #ui.column(12, "specie 1", ui.output_table("table1")),
                        
           #sp2
            ui.tags.h5('Second Species Result'), 
                ui.column(12,  ui.output_table("Table2") ),
                ui.column(12, output_widget("map2")  ),
                ui.column(12, output_widget("Graph2") ),    
                #ui.input_numeric("nb", "Number of rows to show", value=3),
                #ui.column(12, "specie 2", ui.output_table("table2")),

        ),
    ),

)
def server(input, output, session):

        @output
        @render.text
        def species1():
            return f"{input.sp1()}"
        
        @output
        @render.text
        def species2():
            return f"{input.sp2()}"
#######################
# # here code to input regions list
########################         

        @output
        @render.table
        def Table1():
            #input_regionA_sp1 = "pelvic ganglion" # change to input  #################here
            #input_regionB_sp1 = "reproductive structure" # change to input  #################here 
            input_regionA_sp1 = input.rgst1()
            input_regionB_sp1 = input.rgen1()
            result_df = sc.get_filtered_dataframe(result, species=input.sp1())
            #hasNeuronalPhenotype = sc.get_filtered_dataframe(phenotype, species=input.sp1()) 
            #regions_specie1 = regions[regions['Specie']==input.sp1()] # filter specie
            if input.viz_type() == "T":                
                #input_sp1 = input.sp1()
                #result_df1 = sc.get_filtered_dataframe(result, species=input.sp1())
                #selected_Region_A = input.rgst1()
                #selected_Region_B = input.rgen1()
                final_plus_pheno = result_df[(result_df.Region_A == input_regionA_sp1) & (result_df.Region_B == input_regionB_sp1)]
                final_plus_pheno =final_plus_pheno[columns_to_keep]
                final_plus_pheno =final_plus_pheno.rename(columns={
                                'Region_A': 'Start Region',
                                'Region_C': 'Intermediate Region',
                                'Region_B': 'End Region',
                            })
                final_plus_pheno
            else:
                final_plus_pheno = None
            return final_plus_pheno
        
        @output
        @render.table
        def Table2():
            input_regionA_sp2 = input.rgst2()
            input_regionB_sp2 = input.rgen2()
            result_df1 = sc.get_filtered_dataframe(result, species=input.sp2())
            #hasNeuronalPhenotype = sc.get_filtered_dataframe(phenotype, species=input.sp2()) 
           # regions_specie2 = regions[regions['Specie']==input.sp2()] # filter specie
            if input.viz_type() == "T":                
                final_plus_pheno2 = result_df1[(result_df1.Region_A == input_regionA_sp2) & (result_df1.Region_B == input_regionB_sp2)]
                final_plus_pheno2 =final_plus_pheno2[columns_to_keep]
                final_plus_pheno2 =final_plus_pheno2.rename(columns={
                                'Region_A': 'Start Region',
                                'Region_C': 'Intermediate Region',
                                'Region_B': 'End Region',
                            })
                final_plus_pheno2
            else:
                final_plus_pheno2 = None
            return final_plus_pheno2
        
        @output
        @render_widget
        def map1():
            selected_Region_A = input.rgst1()
            selected_Region_B = input.rgen1()
            result_df = sc.get_filtered_dataframe(result, species=input.sp1())
            #hasCircuitRole= sc.get_filtered_dataframe(cir, species=input_sp1)  
            if input.viz_type() == "M":
                req_df = result_df[(result_df.Region_A == selected_Region_A) & (result_df.Region_B == selected_Region_B)]
                fig = sc.plot_dataframe_anatomy_vis(req_df, species=input.sp1())
            elif input.viz_type() == "G":
                fig = sc.plot_dataframe_block_vis(result_df, selected_Region_A, selected_Region_B)  
            else:
                fig = None
            return fig    

           
        @output
        @render_widget
        def map2():
            selected_Region_A = input.rgst2()
            selected_Region_B = input.rgen2()
            result_df2 = sc.get_filtered_dataframe(result, species=input.sp2())
            if input.viz_type() == "M":
                req_df2 = result_df2[(result_df2.Region_A == selected_Region_A) & (result_df2.Region_B == selected_Region_B)]
                fig = sc.plot_dataframe_anatomy_vis(req_df2, species=input.sp2())
            elif input.viz_type() == "G":
                fig = sc.plot_dataframe_block_vis(result_df2, selected_Region_A, selected_Region_B)     
            else:
                fig = None
            return fig


               



app = App(app_ui, server)
