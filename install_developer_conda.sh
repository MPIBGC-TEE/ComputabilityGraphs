# automatically created by  ../../scripts/create_install_scripts.py
# from setup.py , requirements.conda.extra and  requirements.src
    conda install -c conda-forge -y igraph bokeh networkx frozendict ipywidgets
    pip show testinfrastructure;ret=$? 
if [ $ret -eq 0 ]; then
    echo "allredy installed"
else 
    pip install -e git+https://github.com/MPIBGC-TEE/testinfrastructure.git#egg=testinfrastructure
fi 
    pip install -e .  