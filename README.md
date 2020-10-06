# TRAKO

**Trako compresses DTI streamlines from .vtp to smaller .tko files!**

## Installation as PyPI package (recommended, preferably in a virtualenv)

`pip install trako`

## Usage
```
./trakofy -i DATA/example.vtp -o /tmp/test.tko
./untrakofy -i /tmp/test.tko -o /tmp/restored.vtp
./tkompare -a DATA/example.vtp -b /tmp/restored.vtp
```

Diffusion Tensor Imaging (DTI) allows to estimate the brain's white matter tracts. Fiber tracking methods then produce clusters of streamlines that are 3D fiber bundles. Each fiber in these bundles is a line with X,Y,Z coordinates (floats) but researchers may attach many different scalars to each coordinate (per-vertex). Each scalar can be of arbitrary dimension, size, and data type. Researchers may also attach many different property values to individual streamlines (per-fiber). Adding scalars and properties can result in large streamline files.

Trako is a new file format that stores streamlines and associated per-vertex and per-fiber data as glTF containers with compression. We use the Draco algorithm to compress X,Y,Z coordinates, scalars, and properties.

### Custom parameters

Trako allows a detailed configuration of encoding parameters. Customizations can be configured in a JSON file to specify different parameters for different attributes.

We include an example configuration `DATA/test.conf`.
```
{
    
  'POSITION': {
    'position':True,
    'sequential':True,
    'quantization_bits':14,
    'compression_level':1,
    'quantization_range':-1,
    'quantization_origin':None
  },
  'INDICES': {
    'position':False,
    'sequential':True,
    'quantization_bits':14,
    'compression_level':1,
    'quantization_range':-1,
    'quantization_origin':None
  },
  'RTOP2': { # configure custom settings per attribute name
    'position':False,
    'sequential':True,
    'quantization_bits':20,
    'compression_level':1,
    'quantization_range':-1,
    'quantization_origin':None
  }

}
```

This configuration configures a scalar named RTOP2 with a higher bitrate than other attributes. It is also possible to use a generic configuration (for example to reduce the quantization bitrate for all attributes) as follows:


```
{
    
  '*': {
    'position':False,
    'sequential':True,
    'quantization_bits':11,
    'compression_level':1,
    'quantization_range':-1,
    'quantization_origin':None
  }

}
```

The configuration is only relevant during compression and can be used as follows:

```
./trakofy -i DATA/example.vtp -o /tmp/test.tko -c DATA/test.conf
```

## Experiments

<table>
  <tr>
    <td><img src="https://github.com/haehn/TRAKO/blob/master/IPY/newplot(3).png?raw=true"></td>
    <td><img src="https://github.com/haehn/TRAKO/blob/master/IPY/newplot(4).png?raw=true"></td>
  </tr>
</table>

We compared Trako and common streamline file formats (VTK, TrackVis) on data of two subjects  with 800 fiber clusters each. The data includes multiple per-fiber and per-vertex scalar values. Trako yields an average compression ratio of 3.2 and reduces the data size from 2974 Megabytes to 941 Megabytes.

<table>
  <tr>
    <td><img src="https://github.com/haehn/TRAKO/blob/master/IPY/newplot(6).png?raw=true"></td>
    <td><img src="https://github.com/haehn/TRAKO/blob/master/IPY/newplot(5).png?raw=true"></td>
  </tr>
</table>

We also used Trako to compress a single whole brain tractography dataset with 153,537 streamlines. Trako reduces the data size from 543 Megabytes to 267 Megabytes (compression factor 2.02).

<table>
  <tr>
    <td><img src="https://github.com/haehn/TRAKO/blob/master/IPY/newplot(2).png?raw=true"></td>
    <td><img src="https://github.com/haehn/TRAKO/blob/master/IPY/newplot(1).png?raw=true"></td>
  </tr>
</table>

With default parameters, Trako uses lossy compression for position data and per-vertex/per-fiber scalar values with a mean relative loss of less than 0.0001 (besides RGB values as EmbeddingColor). We show the relative information loss for two subjects with 800 fiber clusters each on the left, and the relative information loss for a single whole brain tractography dataset on the right.

## Visualization using WebGL

We provide JavaScript parsers to visualize Trako (.TKO) files with <a href='https://bostongfx.github.io/TRAKO/WEB/threejs.html'>Three.js</a>, <a href='https://bostongfx.github.io/TRAKO/WEB/vtkjs.html'>Vtk.js</a>, and <a href='https://bostongfx.github.io/TRAKO/WEB/xtk.html'>XTK</a>.

And, <a href='https://slicedrop.com'>SliceDrop</a> supports Trako too! Just drag'n'drop the .TKO files in the browser to view them.

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

## Trako @ MICCAI 2020

Please cite TRAKO as follows:
```
@inproceedings{haehn2020trako,
  title={TRAKO: Efficient Transmission of Tractography Data for Visualization},
  author={Haehn, Daniel and Franke, Loraine and Zhang, Fan and Karayumak, Suheyla Cetin and Pieper, Steve and O'Donnell, Lauren and Rathi, Yogesh},
  abstract={Fiber tracking produces large tractography datasets that are tens of gigabytes in size consisting of millions of streamlines. Such vast amounts of data require formats that allow for efficient storage, transfer, and visualization. We present TRAKO, a new data format based on the Graphics Layer Transmission Format (glTF) that enables immediate graphical and hardware-accelerated processing. We integrate a state-of-the-art compression technique for vertices, streamlines, and attached scalar and property data. We then compare TRAKO to existing tractography storage methods and provide a detailed evaluation on eight datasets. TRAKO can achieve data reductions of over 28x without loss of statistical significance when used to replicate analysis from previously published studies. },
  booktitle={Medical Image Computing and Computer-Assisted Intervention (MICCAI)},
  pages={XXX--XXX},
  year={2020},
  supplemental={http://danielhaehn.com/papers/haehn2020trako_supplemental.pdf},
  organization={Springer, Cham},
  code={https://github.com/bostongfx/TRAKO/},
  data={https://github.com/bostongfx/TRAKO/},
  website={https://pypi.org/project/trako/}
}
```
And here is the preprint: https://danielhaehn.com/papers/?haehn2020trako
