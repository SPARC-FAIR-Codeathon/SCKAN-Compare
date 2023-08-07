import numpy as np
import plotly.graph_objects as go

class Visualizer(object):

    def __init__(self, region_dict, species):
        self.region_dict = region_dict
        self.species = species

        self.SCALE = 50
        self.MAX_X = 43
        self.MAX_Y = 18
        self.NODE_RADIUS = 0.2

        self.fig = go.FigureWidget()
        self.fig.layout.hovermode = 'closest'
        self.fig.layout.hoverdistance = -1 #ensures no "gaps" for selecting sparse data

        self.fig.update_xaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_yaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_layout(showlegend=False)
        # # self.fig.update_yaxes(
        # #     scaleanchor="x", scaleratio=1)
        self.fig.update_yaxes(range = [self.MAX_Y+3, 0])
        self.fig.update_xaxes(range = [0, self.MAX_X])
        self.fig.update_layout(height=int(500))

        if (self.species == "Mus musculus") or (self.species == "Rattus norvegicus"):
            self.draw_background_mouse_rat()
        else:
            # default
            self.draw_background_human()


    def draw_rect(self,
                start_x,
                start_y,
                width=1,
                height=1,
                color_border="#4051BF",
                color_fill="#C5CAE9",
                tooltiptext="<set name>"):
        self.fig.add_trace(go.Scatter(
            x=[start_x,start_x+width,start_x+width,start_x, start_x],
            y=[start_y,start_y,start_y+height,start_y+height, start_y],
            mode ="lines",
            fill="toself",
            line_color=color_border,
            fillcolor=color_fill,
            text=tooltiptext,
            hoveron = "fills",
            hoverinfo = "text",
            showlegend=False
        ))

    def draw_poly(self,
                xlist,
                ylist,
                color_border="#4051BF",
                color_fill="#C5CAE9",
                tooltiptext="<set name>"):
        self.fig.add_trace(go.Scatter(
            x=xlist,
            y=ylist,
            mode ="lines",
            fill="toself",
            line_color=color_border,
            fillcolor=color_fill,
            text=tooltiptext,
            hoveron = "fills",
            hoverinfo = "text",
            showlegend=False
        ))

    def draw_background_human(self):
        self.draw_rect(1, 3, 4, 4, "#4051BF", "#C5CAE9")
        self.draw_rect(5, 3, 1, 4, "#4051BF", "#C5CAE9")
        self.draw_rect(6, 5, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(7, 4, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(8, 5, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 2, 31, 1, "#4051BF", "#C5CAE9")        
        self.draw_rect(10, 3, 8, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 3, 12, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(30, 3, 5, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(35, 3, 5, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(40, 3, 1, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 5, 31, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 6, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(13, 6, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(17, 6, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 6, 23, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 7, 3, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(35, 7, 3, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(16, 8, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(19, 8, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_poly([6,8,8,7,7,6,6], [9,9,11,11,10,10,9], "#4051BF", "#C5CAE9")
        self.draw_rect(18, 9, 3, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(21, 9, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(29, 13, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 11, 10, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(29, 11, 12, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(22, 13, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 14, 23, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(37, 16, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(40, 16, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(35, 17, 6, 2, "#4051BF", "#C5CAE9")

    def draw_background_mouse_rat(self):
        self.draw_rect(24, 2, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(26, 2, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(1, 3, 4, 4, "#4051BF", "#C5CAE9")
        self.draw_rect(5, 3, 1, 4, "#4051BF", "#C5CAE9")
        self.draw_rect(6, 5, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(7, 4, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(8, 5, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 3, 8, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 3, 13, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(31, 3, 6, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(37, 3, 4, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(41, 3, 1, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 5, 31, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 6, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(13, 6, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(17, 6, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 6, 23, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 7, 3, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(35, 7, 3, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(6, 8, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(15, 8, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(19, 8, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_poly([6,8,8,7,7,6,6], [9,9,11,11,10,10,9], "#4051BF", "#C5CAE9")
        self.draw_rect(18, 9, 3, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(21, 9, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(29, 13, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(40, 10, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 11, 10, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(29, 11, 12, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(22, 13, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(24, 13, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 14, 23, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(37, 16, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(40, 16, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(35, 17, 6, 2, "#4051BF", "#C5CAE9")


    def mark_node(self,
                  region,
                  color_border="#FF0000",
                  color_fill="#FFFF00",
                  small=False):
        x = self.region_dict[region][0] + 0.5
        y = self.region_dict[region][1] + 0.5
        size_factor = 7 if small else 5
        self.fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode = 'markers',
            marker_symbol = 'circle',

            marker_size = int(self.SCALE/size_factor),
            marker=dict(
                color=color_fill,
                line=dict(
                    color=color_border,
                    width=2
                )
            ),
            text=region,
            hoverinfo="text",
            name=region
        ))

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

    def draw_edge_AB(self,
                     region1,
                     region2,
                     neuron=None):
        # From A to B
        default_linewidth = 2
        x1, y1 = self.region_dict[region1]
        x2, y2 = self.region_dict[region2]
        self.mark_node(region1)
        self.mark_node(region2)
        # self.fig.add_trace(go.Scatter(
        #     x=[x1+0.5, x2+0.5],
        #     y=[y1+0.5, y2+0.5],
        #     mode = 'lines',
        #     text=neuron,
        #     meta="main",
        #     hoverinfo="text",
        #     name=neuron,
        #     line_color="#FF0000",
        #     line={"width":default_linewidth}
        # ))

        # interpolate line for adding hover text on line (to display neuron name)
        p1 = (x1+0.5, y1+0.5)
        p2 = (x2+0.5, y2+0.5)
        x_new, y_new = self.interpolate_coordinates(p1, p2)
        self.fig.add_trace(go.Scatter(
            x=x_new,
            y=y_new,
            mode = 'lines',
            text=neuron,
            hoverinfo="text",
            name=neuron,
            line_color="#FF0000",
            line={"width":default_linewidth},
            showlegend=False
        ))
        # ax.plot((x1, x2), (y1, y2), linewidth=2, color='firebrick')

    def draw_edge_ABC(self,
                      region1,
                      region2,
                      region3,
                      neuron=None):
        # From A to B via C
        default_linewidth = 2
        x1, y1 = self.region_dict[region1]
        x2, y2 = self.region_dict[region2]
        x3, y3 = self.region_dict[region3]
        self.mark_node(region1)
        self.mark_node(region2)
        self.mark_node(region3, color_border="#000000", color_fill="#00FF00", small=True)
        # self.fig.add_trace(go.Scatter(
        #     x=[x1+0.5, x3+0.5, x2+0.5],
        #     y=[y1+0.5, y3+0.5, y2+0.5],
        #     mode = 'lines',
        #     text=neuron,
        #     hoverinfo="text",
        #     name=neuron,
        #     # line_shape="spline",
        #     line_color="#FF0000",
        #     line={"width":default_linewidth}
        # ))

        # interpolate line for adding hover text on line (to display neuron name)
        # first part of line: A to C
        p1 = (x1+0.5, y1+0.5)
        p2 = (x3+0.5, y3+0.5)
        x_new, y_new = self.interpolate_coordinates(p1, p2)
        self.fig.add_trace(go.Scatter(
            x=x_new,
            y=y_new,
            mode = 'lines',
            text=neuron,
            hoverinfo="text",
            name=neuron,
            # line_shape="spline",
            line_color="#FF0000",
            line={"width":default_linewidth},
            showlegend=False
        ))

        # second part of line: C to B
        p1 = (x3+0.5, y3+0.5)
        p2 = (x2+0.5, y2+0.5)
        x_new, y_new = self.interpolate_coordinates(p1, p2)
        self.fig.add_trace(go.Scatter(
            x=x_new,
            y=y_new,
            mode = 'lines',
            text=neuron,
            hoverinfo="text",
            name=neuron,
            # line_shape="spline",
            line_color="#FF0000",
            line={"width":default_linewidth},
            showlegend=False
        ))

    def show_figure(self):
        self.fig.show(config= {'displaylogo': False})

    def get_figure(self):
        return self.fig
