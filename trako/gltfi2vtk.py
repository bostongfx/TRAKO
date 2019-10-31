import pygltflib
from pygltflib import *

import DracoPy

import vtk
from vtk.util import numpy_support

import numpy as np

import collections


#
#
# MAP GLTF COMPONENT TYPE TO VTK DATATYPE
#
#
gltfComponentType_to_vtkDataType = {

  pygltflib.BYTE: vtk.VTK_CHAR,
  pygltflib.UNSIGNED_BYTE: vtk.VTK_UNSIGNED_CHAR,
  pygltflib.SHORT: vtk.VTK_SHORT,
  pygltflib.UNSIGNED_SHORT: vtk.VTK_UNSIGNED_SHORT,
  pygltflib.UNSIGNED_INT: vtk.VTK_UNSIGNED_INT,
  pygltflib.FLOAT: vtk.VTK_FLOAT

}

#
#
# MAP GLTF COMPONENT TYPE TO NUMPY DATATYPE
#
#
gltfComponentType_to_npDataType = {

  pygltflib.BYTE: np.int8,
  pygltflib.UNSIGNED_BYTE: np.uint8,
  pygltflib.SHORT: np.int16,
  pygltflib.UNSIGNED_SHORT: np.uint16,
  pygltflib.UNSIGNED_INT: np.uint32,
  pygltflib.FLOAT: np.float32

}

#
#
# MAP GLTF TYPE TO VTK NUMBEROFCOMPONENTS
#
#
gltfType_to_vtkNumberOfComponents = {
  
  pygltflib.SCALAR: 1,
  pygltflib.VEC2: 2,
  pygltflib.VEC3: 3,
  pygltflib.VEC4: 4
  # TODO MAT2, MAT3, MAT4

}

def convert(input, output=None):

  gltf = pygltflib.GLTF2.load_json(input)

  # get all attributes
  attributes = gltf.meshes[0].primitives[0].attributes

  polydata = vtk.vtkPolyData()

  for k,v in attributes.__dict__.items():

    if v:
      # valid attribute

      # grab accessor
      accessor = gltf.accessors[v]

      # grab bufferview
      bufferview = accessor.bufferView

      # grab buffer
      data = gltf.buffers[gltf.bufferViews[bufferview].buffer]

      # unpack data
      magic = 'data:application/octet-stream;base64,'
      bytes = base64.b64decode(data.uri[len(magic):])

      if bytes[0:5] != b'DRACO':
        print('Did not find Draco compressed data..')

      decoded_bytes = DracoPy.decode_point_cloud_buffer(bytes).points

      draco_points = DracoPy.decode_point_cloud_buffer(bytes).points
      number_of_elements = gltfType_to_vtkNumberOfComponents[accessor.type]
      datatype = gltfComponentType_to_npDataType[accessor.componentType]
      draco_points_reshaped = np.array(draco_points, dtype=datatype).reshape(int(len(draco_points)/number_of_elements), number_of_elements)
      
      # now we got the data.. let's create the vtkPolyData
      if k == 'POSITION':

        points = vtk.vtkPoints()
        points.SetData(numpy_support.numpy_to_vtk(draco_points_reshaped))

      elif k.startswith('_'):

        scalarname = k[1:]
        vtkArr = numpy_support.numpy_to_vtk(draco_points_reshaped)
        vtkArr.SetName(scalarname)
        polydata.GetPointData().AddArray(vtkArr)

        print('Restored', scalarname)

  return polydata

  # now the indices / cell data


