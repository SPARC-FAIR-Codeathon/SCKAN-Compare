Installation
============

If you are relying on Python packages for several, independent projects, we recommend that you make use
of separate environments for each project. In this way, you can safely update and install packages for
one of your projects without affecting the others. Both, ``conda`` and ``pip`` support installation in
environments -- for more explanations see the respective instructions below.

Standard install
----------------
We recommend installing into a separate "virtual environment", see the
`Python Packaging User Guide <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_
for more information.
SCKAN-Compare is included in the PyPI package index: https://pypi.org/project/SCKAN-compare/
You can therefore install it with the ``pip`` utility::

   pip install sckan-compare

In rare cases where your current environment does not have access to the ``pip`` utility, you first
have to install ``pip`` via::
   
   python -m ensurepip

Development install
-------------------
If you wish to contribute to the development of SCKAN-Compare, the easiest way of setting up your environment
would be as follows::

   git clone https://github.com/SPARC-FAIR-Codeathon/2023-team-4
   cd 2023-team-4
   pip install -e .

Installing with the -e flag will allow changes to the source files to be immediately reflected in your environment.
