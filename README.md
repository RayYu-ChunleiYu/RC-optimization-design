# Optimization Design for RC (Reinforced Concrete) Structures

This repository is created for the lecture on "Fundamentals of Concrete Structures" at Wuhan University.


# How to run 
## Download python (Required version 3.12.7 )
### Anaconda 
#### Download anaconda
Go anaconda official page to download anaconda and install it 
https://www.anaconda.com/

#### use anaconda to create python virutal environment
``` pwsh
conda create -n ConcreteOpt python=3.12.7
```
### Python 
Go to python official page to download python and install
https://www.python.org/

## Enviorment set-up  

Install third-party package that used in the project and 
### Python installed from Anaconda
``` pwsh
conda activate ConcreteOpt # acitvate created python virtual environment
pip install -r requirement.txt # install packages
```
### Pyhton installed from Python official 

``` pwsh
pip install -r requirement.txt # install packages
```

## Run opt python script

``` pwsh
python opt_design_beam.py # example to carry out beam design optimization
```

# Files

## Main Entry Files
- **opt_design_beam.py**: Script for the optimization design of reinforced concrete beams.
- **opt_design_column.py**: Script for the optimization design of reinforced concrete columns.
- **opt_design_fibermodel.py**: Script for the optimization design of reinforced concrete simply supported bridge decks.

## Dependency Files
- **ConstrainAlg.py**: Base Python class for constraint algorithms, inherited by `ConstrainGA` and `ConstrainPSO`.
- **ConstrainPSO.py**: Python class for the constraint Particle Swarm Optimization (PSO) algorithm.
- **ConstrainGA.py**: Python class for the constraint Genetic Algorithm (GA) algorithm.
- **State.py**: Python class for storing solution states.
- **FiberModelOpt**: Directory where the compiled fibermodel binary application is stored, and the cache directory where fibermodel optimization calculations are stored.

## Environment File
- **requirements.txt**: Python environment file