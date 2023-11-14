# progmat-2023
Linear Constraint Integer solving for a facility allocation problem

## Installation

### If you need to install conda

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
### If you already have conda
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
