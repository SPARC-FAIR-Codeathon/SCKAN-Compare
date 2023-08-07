import numpy as np
import plotly.graph_objects as go

class Visualizer(object):

    def __init__(self, region_dict):
        self.region_dict = region_dict

        self.SCALE = 50
        self.MAX_X = 43
        self.MAX_Y = 18
        self.NODE_RADIUS = 0.2

        self.fig = go.FigureWidget()
        self.fig.layout.hovermode = 'closest'
        self.fig.layout.hoverdistance = -1 #ensures no "gaps" for selecting sparse data

        self.fig.update_xaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_yaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        # # self.fig.update_yaxes(
        # #     scaleanchor="x", scaleratio=1)
        self.fig.update_yaxes(range = [self.MAX_Y+3, 0])
        self.fig.update_xaxes(range = [0, self.MAX_X])
        self.fig.update_layout(height=int(500))

        self.draw_background()

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

    def draw_background(self):
        self.draw_rect(1, 3, 4, 4, "#4051BF", "#C5CAE9")
        self.draw_rect(2, 4, 3, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(5, 3, 1, 4, "#4051BF", "#C5CAE9")
        self.draw_rect(6, 5, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(7, 4, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(8, 5, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 4, 8, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 4, 12, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(30, 4, 5, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(35, 4, 5, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(40, 4, 1, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 6, 11, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(10, 7, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(13, 7, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(17, 7, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(19, 8, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(19, 8, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_poly([6,8,8,7,7,6,6], [9,9,11,11,10,10,9], "#4051BF", "#C5CAE9")
        self.draw_rect(18, 9, 3, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(21, 9, 2, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 11, 10, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(29, 11, 12, 2, "#4051BF", "#C5CAE9")
        self.draw_rect(39, 13, 1, 1, "#4051BF", "#C5CAE9")
        self.draw_rect(18, 14, 23, 2, "#4051BF", "#C5CAE9")
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
        x = [x1+0.5, x2+0.5]
        y = [y1+0.5, y2+0.5]
        x_new = np.arange(x1+0.5, x2+0.5, 0.1 if x1<x2 else -0.1)
        y_new = np.interp(x_new, x, y)
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
        x = [x1+0.5, x3+0.5]
        y = [y1+0.5, y3+0.5]
        x_new = np.arange(x1+0.5, x3+0.5, 0.1 if x1<x3 else -0.1)
        y_new = np.interp(x_new, x, y)
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
        x = [x3+0.5, x2+0.5]
        y = [y3+0.5, y2+0.5]
        x_new = np.arange(x3+0.5, x2+0.5, 0.1 if x3<x2 else -0.1)
        y_new = np.interp(x_new, x, y)
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