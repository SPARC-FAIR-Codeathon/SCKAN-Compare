Basic Usage
===========

The functionality of the Python module can be accessed via the following classes:

#. SckanCompare
#. Visualizer
#. SimpleVisualizer

Detailed examples are available via the Jupyter notebook tutorials.
Here, we show a few example code snippets of their usage:

You can import each of the classes via::

    from sckan_compare import SckanCompare
    from sckan_compare.visualize import Visualizer
    from sckan_compare.simplevis import SimpleVisualizer

You can execute a SPARQL quey via::

    result = sc.execute_query(<<query string>>)

Simple block plot can be created via::

    simvis = SimpleVisualizer()
    fig = simvis.plot_figure(result_df, selected_Region_A, selected_Region_B)