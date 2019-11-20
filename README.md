# TRAKO

Trako compresses DTI streamlines from .vtp to smaller .tko files!

## Installation as PyPI package (recommended, preferably in a virtualenv)

`pip install trako`


## Developer installation (comes with test data)

Please follow these steps with Miniconda or Anaconda installed:

```
# create environment
conda create --name TRAKO python=3.6
conda activate TRAKO

# get TRAKO
git clone git@github.com:haehn/TRAKO.git
cd TRAKO

python setup.py install
```

## Usage
```
./trakofy -i DATA/example.vtp -o /tmp/test.tko
./untrakofy -i /tmp/test.tko -o /tmp/restored.vtp
./tkompare -a DATA/example.vtp -b /tmp/restored.vtp
```

