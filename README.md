# progmat-2023
Linear Constraint Integer solving for a facility allocation problem

## Installation
You'll need to install the solvers locally, depending on the one you want to use

### Using Conda for Solvers
```bash
conda config --add channels http://conda.anaconda.org/gurobi
conda install gurobi
```

```bash
conda config --add channels conda-forge
conda install gcg papilo scip soplex zimpl
```

### Install pulp
```bash
python -m pip install pulp
```

## Usage

Run with 
```bash
python facility_location.py <filename> [solver_name] [relaxed "true" or "false"]
```
For example, to run the toy.txt problem, using the GUROBI solver, run
```bash
python facility_location.py toy.txt scip
```
