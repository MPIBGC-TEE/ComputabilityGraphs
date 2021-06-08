
![test_debian_pip_install](https://github.com/MPIBGC-TEE/bgc_md2/workflows/test_debian_pip_install/badge.svg)
![test_conda_developer_installation](https://github.com/MPIBGC-TEE/bgc_md2/workflows/test_conda_developer_installation/badge.svg)
## Installation

   * Update conda
     ```
     conda update --all
     ```
   * Create a conda environment and run the install script:
     ```bash 
     conda create -y --name bgc_md2 python=3
     conda activate bgc_md2
     ./install_developer_conda.sh 
     ```
     This will install the dependencies and run ```python setup.py develop``` for every subpackage so that your code changes 
     in one of these packages take mmediate effect.

    * Run the tests.
      ```
      cd tests
      ./run_tests.py
      ```
      If you can run this script successfully, you have a working installation of ComputabilityGraphs and can run all functions. 
  
   * Troubleshooting:
      * We noticed that in MacOS, it is necessary to update packages in the conda environment before running the tests successfully.
        Try to update conda ( ```conda update --all)``` and run the tests again.
        
   * Working with the installation:
      * pulling:
        Since you will nearly always pull with the ```--recurse-submodules``` flag   
        consider creating an alias
        ```
        git config alias.spull 'pull --recurse-submodules'
        ```
        which enables you to say  ```git spull``` to achieve the same effect
        
      * Tips to work with [git submodules:](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
   

## Documentation
* The latest build of the package documentation can be found [here:](https://mpibgc-tee.github.io/bgc_md2/).


## Objectives
1. Investigations of a single model (or modelrun).


# Contribution
We try to keep the master green and develop new features or bug fixes in short lived branches that are then 
merged back into the master https://nvie.com/posts/a-successful-git-branching-model/
See also https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
https://git-scm.com/book/en/v2/Git-Tools-Submodules for the work on the dependencies.

* Example workflow to work on a feature branch `iss26-non-importable-models` you are asked to review 
  * `git branch -a` (shows all branches including remotes)
  * `git checkout --track origin/iss26-non-importable-models` (creates a local copy that you can test)
* Example to create your own feature branch (here to fix an issue )
  * `git checkout -b iss53`

## various notes on implementation

* The 'Computers' and 'MVars' represent a set of types and strictly typed
  functions (including the return values).
  This has been implemented with the new python type annotations.  
  An advantage is that we can express our
  idea in a well defined and well documented way and avoid extra effort for the
  user..  
* The computibility graph is expensive to create and only changes if new
  `Computers` and `MVars` are created.  It should be cached, which encurages
  the use of immutable data structures. (since we can use functools )

   


