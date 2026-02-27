# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys


os.environ["PORT"] = "1111"
os.environ["LOG_LEVEL"] = "info"
os.environ["RELATIONAL_DB_TYPE"] = "placeholder"
os.environ["RELATIONAL_DB_HOST"] = "placeholder"
os.environ["RELATIONAL_DB_PORT"] = "1111"
os.environ["RELATIONAL_DB_USER"] = "placeholder"
os.environ["RELATIONAL_DB_PASSWORD"] = "placeholder"
os.environ["RELATIONAL_DB_NAME"] = "placeholder"
os.environ["NOSQL_DB_HOST"] = "placeholder"
os.environ["NOSQL_DB_PORT"] = "1111"
os.environ["NOSQL_DB_USER"] = "placeholder"
os.environ["NOSQL_DB_PASSWORD"] = "placeholder"
os.environ["NOSQL_DB_NAME"] = "placeholder"
os.environ["VECTOR_DB_HOST"] = "placeholder"
os.environ["VECTOR_DB_PORT"] = "1111"
os.environ["VECTOR_DB_APIKEY"] = "placeholder"
os.environ["VECTOR_DB_COLLECTION_NAME"] = "placeholder"
os.environ["EMBEDDER_HOST"] = "placeholder"
os.environ["EMBEDDER_PORT"] = "1111"
os.environ["EMBEDDER_NAME"] = "placeholder"

# for x in os.walk('../../src'):
#   sys.path.insert(0, x[0])

# It must point to the root folder, the one containing src
sys.path.insert(0, "..")

project = "python-api-template"
copyright = "2024, Mirco Quintavalla"
author = "Mirco Quintavalla"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.coverage"]

autosummary_generate = True  # Turn on sphinx.ext.autosummary

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
