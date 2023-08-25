Web App
=======

The web app is a Python-based app developed using 'Shiny for Python'. Shiny makes it easy to build web applications with Python code. It enables you to customize the layout and style of your application and dynamically respond to events, such as a button press, or dropdown selection. The examples on this site are rendered in the browser using Pyodide, but you can also install shiny to use it with your own projects.

We leveraged this functionality to provide a GUI interface to users to readily access the features of SCKAN-Compare. The app can also be run locally. You will need to install some packages for this. These can be installed as follows::

   pip install shiny
   pip install --upgrade shiny htmltools
   pip install shinyswatch
   pip install shinywidgets

Once the environrment is setup, the app can be launched via::

    shiny run --reload

The above command should be run in the directory containing the file `app.py`, which contains the source code for the app.

