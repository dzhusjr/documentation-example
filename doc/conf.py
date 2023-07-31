# Configuration file for the Sphinx documentation builder.
import os
import sys
import ast

sys.path.insert(0, os.path.abspath("../source"))

#check if .rst file exists for each module in the /source directory
def generate_rst_file(file):
    with open(f"{file}.rst", "w") as f:
        print(os.path.abspath(f"{file}.rst"),"created")
        f.write(f"""{file}\n==========\n\n.. automodule:: {file}\n   :members:""")
    with open("index.rst", "a") as f:
        f.write(f"{file}\n   ")

#remove .rst file if no relative .py file exists
def remove_rst_file(file):
    os.remove(f"{file}.rst")
    with open("index.rst", "r") as f:
        contents = f.read()
    contents.replace(f"{file}\n   ", "")
    with open("index.rst", "w") as f:
        f.write(contents)

#leave only defs and classes in .py files
def extract_functions_and_classes(file):
    with open(file, 'r') as f:
        code = ast.parse(f.read())

    functions = [node for node in ast.walk(code) if isinstance(node, (ast.FunctionDef,ast.ClassDef))]

    with open(file, 'w') as f:
        for function in functions:
            f.write(ast.unparse(function))
            f.write('\n\n')

#add missing .rst files for modules
modules = [f.split(".")[0] for f in os.listdir("../source") if f.endswith(".py")]
for module in modules:
    extract_functions_and_classes("../source/"+module+".py")	
    if not os.path.exists(f"{module}.rst"):
        generate_rst_file(module)

#remove extra .rst files if module was deleted
rst_files = [f.split(".")[0] for f in os.listdir(".") if f.endswith(".rst") and f != "index.rst"]
extra_rst_files = list(set(rst_files) - set(modules))
for file in extra_rst_files:
    remove_rst_file(file+".rst")


# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'documentation-example'
copyright = '2023, dzhusjr'
author = 'dzhusjr'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = ["sphinx.ext.autodoc"]

source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
