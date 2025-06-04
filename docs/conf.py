# Configuration file for the Sphinx documentation builder.

project = 'Gamma Delta Sense'
copyright = '2025, JurisGPT'
author = 'JurisGPT'
version = '1.0.0'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'en'
master_doc = 'index'
source_suffix = '.rst'

# CRITICAL: Use built-in theme (NOT sphinx_rtd_theme)
html_theme = 'alabaster'
html_static_path = []

html_theme_options = {
    'description': 'Immunology Knowledge Base Development & Monitoring System',
    'github_user': 'jurisgpt',
    'github_repo': 'gamma_delta_sense',
    'github_banner': True,
    'show_powered_by': False,
}

html_show_sphinx = False
html_show_copyright = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
