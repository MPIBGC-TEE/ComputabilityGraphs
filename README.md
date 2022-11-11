![test_conda_developer_installation](https://github.com/MPIBGC-TEE/ComputabilityGraphs/workflows/test_conda_developer_installation/badge.svg)

## Purpose

We use the package to provide an explorative user interface for ipython or jupyter notebooks,
It computes: 
* what is computable  given a set of functions and a set of arguments.
* or which addiitional arguments are necessary to compute a desired result.


The package implements one central class 'CMTVS' (ConnectedMultiTypeVariableSet) 
which represents 
* a set of variables of a given unique type and 
* a set of type annotated functions (the normal python type hints) whose arguments and return values are of these types.
* In an application the types represent objects of the domain e.g. an  influx, an outlux or a content 
  of a reservoir which form the nodes of a graph.
* The functions are the edges that connect those types 
  e.g. a function that computes
  the content of a reservoir by adding the integrated influxes and substracting the integrated outfluxes is 
  the 'computable from' connection between the set of it'a argument types and it' resulttype.
* These connections can be exploited recursively in two ways:
  1. From a givens set of values (instances of the above types) and a set of functions we can build a computability graph
     forward by recursively updating what can be computed from the new results. (This is acutally rather simple and implemented 
     in a single recursive function).
     
  1. From a set of functions and a target type we can compute a recursive tree structure wich allows us to compute all ways
     in which the target variable can be computed.
 
  1. From a set of functions a set of given values and a target type, we can use the tree to compute which argument (types)  are still missing.
  1. These graphs can be visualized and are also used to automatically add methods for the CMTVS object for every (recursively) computable result type.
     Thus given a CMTVS instance e.g. ```my_cmtvs``` one can just type "." and "TAB" to be shown all the computable types.
    
 ## Application
 This makes it (a lot) easier to find out how a library computes a demanding result. e.g. the backward transit time distribution for a 
 system of pools. The function that finally computes the result takes arguments of rather complex structure.
 Normally a user would have to find this function in the docs and then trace backward how to compute the arguments and how they are computed and so on.
 This is a daunting task if one does not know the libraries underneath. 
 With this package we can immidaitly show all the ways  in which result can be computed (paths in the tree) and immidiatly do it if we have a sufficient
 set of start values for at least one of the paths.
 The package was developed to facilitate another package: The biogeochemical model data base https://github.com/MPIBGC-TEE/bgc_md2
   
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



