![test_conda_developer_installation](https://github.com/MPIBGC-TEE/ComputabilityGraphs/workflows/test_conda_developer_installation/badge.svg)

## Purpose

We use the package to provide an explorative user interface for jupyter notebooks,
It that computes 
* what is computable  given a set of functions and a set of arguments.
* or which addiitional arguments are necessary to compute a desired result.


The package implements one central class 'CMTVS' (ConnectedMultiTypeVariableSet) 
which represents 
* a set of variables of a given unique type and 
* a set of type annotated functions whose arguments and return values are of these types.

* In an application the types represent objects of the domain e.g. an  influx, an outlux or a content 
  of a reservoir which form the nodes of a graph.
* The functions are the edges that connect those types 
  e.g. a function that computes
  the content of a reservoir by adding the integrated influxes and substracting the integrated outfluxes is 
  the 'computable from' connection between the set of it'a argument types and it' resulttype.
* These connections can be exploited recursively in two ways:
  * 

 

   
## Installation (in developer mode)

   * Update conda
     ```
     conda update --all
     ```
   * Create a conda environment and run the install script:
     ```bash 
     conda create -y --name whatever python=3
     conda activate whatever 
     ./install_developer_conda.sh 
     ```
     This will install the dependencies and run ```python setup.py develop``` 

    * Run the tests.
      ```
      cd tests
      ./run_tests.py
      ```
      If you can run this script successfully, you have a working installation of ComputabilityGraphs and can run all functions. 
  
   
<!---
## Documentation
* The latest build of the package documentation can be found [here:](https://mpibgc-tee.github.io//).
--->

# Contribution
We try ;-) to keep the master green and develop new features or bug fixes in short lived branches that are then 
merged back into the master https://nvie.com/posts/a-successful-git-branching-model/
See also https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
https://git-scm.com/book/en/v2/Git-Tools-Submodules for the work on the dependencies.

* Example workflow to work on a feature branch `iss26-non-importable-models` you are asked to review 
  * `git branch -a` (shows all branches including remotes)
  * `git checkout --track origin/iss26-non-importable-models` (creates a local copy that you can test)
* Example to create your own feature branch (here to fix an issue )
  * `git checkout -b iss53`



