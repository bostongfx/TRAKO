# TRAKO

Trako compresses DTI streamlines from .vtp to smaller .tko files!

## Installation as PyPI package (recommended, preferably in a virtualenv)

`pip install trako`


## Manual installation

Please follow these steps with Miniconda or Anaconda installed:

```
# create environment
conda create --name TRAKO python=3.6
conda activate TRAKO
conda install numpy
conda install matplotlib
conda install -c anaconda vtk 
conda install -c conda-forge scikit-build 
pip install pygltflib
pip install prettytable

# get TRAKO
git clone git@github.com:haehn/TRAKO.git
cd TRAKO

# initialize DracoPy submodule
git submodule init
git submodule update

cd externals/DracoPy
# initialize Draco submodule
git submodule init
git submodule update
python setup.py install

cd ../../
```

## Usage
```
./trakofy.py -i DATA/example.vtp -o /tmp/test.tko
./untrakofy.py -i /tmp/test.tko -o /tmp/restored.vtp
./compare.py -a DATA/example.vtp -b /tmp/restored.vtp
```

