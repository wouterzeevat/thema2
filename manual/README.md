# Manuals

## Notebooks

This folder contains the Jupyter Notebook files (*.ipynb) used as manuals for the `pypovray` project.

To edit these manuals, start a notebook server in this folder or one level higher with: `jupyter notebook`. This will start a server and open a webbrowser pointing to a file listing of this folder. `jupyter` can be simply installed with `pip install jupyter`. 

Note that the code examples shown in the manual require the `povray` package which is up one level. You need to move the manual file(s) to the project root folder to be able to run the included code. Also note that in a few cases the Python output has been manually edited to remove (absolute) file paths and other non-public information.

## Converting

Run the `convert.sh` script to create rendered HTML versions of all manuals in the `manual/html` folder.