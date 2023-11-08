# progmat-2023
Linear Constraint Integer solving for a facility allocation problem

## Installation

```bash
conda config --add channels conda-forge
conda install gcg papilo scip soplex zimpl
pip install -r requirements.txt
```

## Usage

Run with 
```bash
python main.py data.txt SCIP
```
or
```bash
python main.py data.txt GUROBI
```
