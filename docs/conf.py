# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'Gamma Delta Sense'
copyright = '2025, JurisGPT'
author = 'JurisGPT'

version = '1.0.0'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # For Google-style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'en'
master_doc = 'index'
source_suffix = '.rst'
source_encoding = 'utf-8-sig'

# -- Options for HTML output -------------------------------------------------
# Using Read the Docs theme
html_theme = 'sphinx_rtd_theme'

# Theme options
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}

html_static_path = ['_static']  # Create this directory if needed

# Add any paths that contain custom static files (such as style sheets)
# They are copied after the builtin static files
html_css_files = [
    'custom.css',
]

# Add any paths that contain custom themes here, relative to this directory
html_theme_path = []

html_show_sphinx = False
html_show_copyright = True
htmlhelp_basename = 'GammaDeltaSensedoc'

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True

