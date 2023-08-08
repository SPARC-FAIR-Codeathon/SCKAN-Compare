import os
import pkg_resources
import numpy as np
import plotly.graph_objects as go
from PIL import Image

class SimpleVisualizer(object):

    def __init__(self):
        self.SCALE = 150
        self.MAX_Y = 900

        datapath = pkg_resources.resource_filename("sckan_compare", "data")
        node_A = Image.open(os.path.join(datapath, "node_A.png"))
        node_B = Image.open(os.path.join(datapath, "node_B.png"))
        node_C = Image.open(os.path.join(datapath, "node_C.png"))
        self.icons = {
            "node_A": node_A,
            "node_B": node_B,
            "node_C": node_C
        }

        self.fig = go.FigureWidget()
        self.fig.layout.hovermode = 'closest'
        self.fig.layout.hoverdistance = -1 #ensures no "gaps" for selecting sparse data

    def interpolate_coordinates(self, point1, point2, resolution=0.1):
        """
        Interpolate between two cartesian coordinates with a given resolution using NumPy.
        
        Parameters:
            point1 (tuple): First cartesian coordinate (x1, y1).
            point2 (tuple): Second cartesian coordinate (x2, y2).
            resolution (float): Interpolation resolution.
            
        Returns:
            tuple: Two lists of interpolated x and y coordinates.
        """
        x1, y1 = point1
        x2, y2 = point2
        
        num_steps = int(1 / resolution)
        t = np.linspace(0, 1, num_steps + 1)
        
        interpolated_x = x1 + (x2 - x1) * t
        interpolated_y = y1 + (y2 - y1) * t
        
        return list(interpolated_x), list(interpolated_y)    

    def plot_figure(self, df, region_A, region_B):
        req_df = df[(df.Region_A == region_A) & (df.Region_B == region_B)]
        list_region_C = req_df.Region_C.unique()

        self.MAX_X = self.SCALE * len(list_region_C)
        self.update_graph()

        # region_A background
        self.draw_block_bg(
            x0=(self.MAX_X/2)-100,
            y0=50,
            x1=(self.MAX_X/2)+100,
            y1=200,
            opacity=0.2,
            color="PaleTurquoise"
        )
        # region A icon
        self.draw_image(
            icon=self.icons["node_A"],
            x=self.MAX_X/2,
            y=125,
        )
        # region A label
        self.add_text(
            x=self.MAX_X/2-3,
            y=0,
            text=region_A
        )
        self.mark_node(x=self.MAX_X/2, y=125, label=region_A)
        
        # region_B background
        self.draw_block_bg(
            x0=(self.MAX_X/2)-100,
            y0=self.MAX_Y-200,
            x1=(self.MAX_X/2)+100,
            y1=self.MAX_Y-50,
            opacity=0.2,
            color="LightGreen"
        )
        # region B icon
        self.draw_image(
            icon=self.icons["node_B"],
            x=self.MAX_X/2-3,
            y=self.MAX_Y-125,
        )
        # region B label
        self.add_text(
            x=self.MAX_X/2,
            y=self.MAX_Y,
            text=region_B
        )
        self.mark_node(x=self.MAX_X/2, y=self.MAX_Y-125, label=region_B)


        # all region C and connections
        for i in range(0,len(list_region_C)):
            xtemp = (self.SCALE*i)+64
            ytemp = self.MAX_Y/2

            self.draw_image(
                icon=self.icons["node_C"],
                x=xtemp,
                y=ytemp,
            )
            self.add_text(
                x=xtemp,
                y=ytemp+100,
                text=req_df.iloc[i,7],
                fontsize=12
            )
            self.mark_node(x=xtemp, y=ytemp, label=req_df.iloc[i,7])
            p1 = (self.MAX_X/2, 125)
            p2 = (xtemp, ytemp)
            x_new, y_new = self.interpolate_coordinates(p1, p2)
            self.draw_connections(
                x=x_new,
                y=y_new,
                label=req_df.iloc[i,1],
                color="#FF0000"
            )
            p1 = (xtemp, ytemp)
            p2 = (self.MAX_X/2, self.MAX_Y-125)
            x_new, y_new = self.interpolate_coordinates(p1, p2)
            self.draw_connections(
                x=x_new,
                y=y_new,
                label=req_df.iloc[i,1],
                color="#FF0000"
            )
            
        return self.fig

    def update_graph(self):
        self.fig.update_xaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_yaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_yaxes(range = [self.MAX_Y, 0])
        self.fig.update_xaxes(range = [0, self.MAX_X])
        self.fig.update_layout(height=int(500))
        self.fig.update_layout(template="plotly_white")
        self.fig.update_layout(showlegend=False)


    def draw_block_bg(self, x0, y0, x1, y1, opacity, color):
        self.fig.add_shape(
            type="rect",
            xref="x", yref="y",
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            opacity=opacity,
            fillcolor=color,
            line_color=color,
        )

    def draw_image(self, icon, x, y):
        self.fig.add_layout_image(
            dict(
                source=icon,
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                x=x,
                y=y,
                sizex=128,
                sizey=128,
                opacity=1.0,
                layer="above"
            )
        )

    def draw_connections(self, x, y, label, color):
        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line_color=color,
                showlegend=False,
                text=label,
                hoverinfo="text",
                name=label,
            )
        )

    def add_text(self, x, y, text, fontsize=20):
        self.fig.add_annotation(
            x=x,
            y=y,
            xref="x",
            yref="y",
            text=text,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=fontsize,
                color="#000000"
                ),
            align="center",
        )

    def mark_node(self, x, y, label):
        self.fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode = "markers",
            marker_symbol="circle",
            text=label,
            hoverinfo="text",
            name=label,
        ))