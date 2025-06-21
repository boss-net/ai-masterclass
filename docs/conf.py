# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'bosskit'
author = 'BossNet'
copyright = '2025, BossNet'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

autodoc_typehints = 'description'
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
}

# -- Options for autodoc ----------------------------------------------------
autoclass_content = 'both'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
