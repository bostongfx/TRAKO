import pygltflib
from pygltflib import *

import TrakoDracoPy

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

def convert(input, output=None, verbose=True):

  gltf = pygltflib.GLTF2.load_json(input)


  polydata = vtk.vtkPolyData()

  # return empty polydata if there are no streamlines
  if len(gltf.meshes) == 0:
    return polydata

  # get all attributes
  attributes = gltf.meshes[0].primitives[0].attributes

  # get all properties
  if 'properties' in gltf.meshes[0].primitives[0].extras:
    properties = gltf.meshes[0].primitives[0].extras['properties']
  else:
    properties = {}


  #
  # position
  #
  draco_points_reshaped = decode(gltf, attributes.POSITION)

  points = vtk.vtkPoints()
  points.SetData(numpy_support.numpy_to_vtk(draco_points_reshaped))
  polydata.SetPoints(points)

  #
  # scalars
  #
  for k,v in attributes.__dict__.items():

    if v:
      # valid attribute

      draco_points_reshaped = decode(gltf, v)

      scalarname = k[1:]
      vtkArr = numpy_support.numpy_to_vtk(draco_points_reshaped)
      vtkArr.SetName(scalarname)
      polydata.GetPointData().AddArray(vtkArr)

      if verbose:
        print('Restored scalar', scalarname)

  #
  #
  # now the indices / cell data
  #
  #
  a_indices = gltf.meshes[0].primitives[0].indices
  draco_points = decode(gltf, a_indices, reshape=False)


  # make ints...
  indices = np.round(draco_points).astype(np.int)

  # convert to cell data
  celldata = []
  startrange = 0

  for i in indices:
      
      celldata.append(i)
      endrange = i
      
      celldata += list(range(startrange,startrange+endrange))
      
      startrange = startrange+endrange


  cellArray = vtk.vtkCellArray()
  cellArray.SetCells(len(indices),numpy_support.numpy_to_vtkIdTypeArray(np.array(celldata)))

  polydata.SetLines(cellArray)

  #
  # properties
  #
  for k,v in properties.items():

    if v:
      # valid property

      draco_points_reshaped = decode(gltf, v)

      p_name = k
      vtkArr = numpy_support.numpy_to_vtk(draco_points_reshaped)
      vtkArr.SetName(p_name)
      polydata.GetCellData().AddArray(vtkArr)

      if verbose:
        print('Restored property', p_name)

  return polydata

def decode(gltf, accessor_id, reshape=True):
  '''
  '''

  # grab accessor
  accessor = gltf.accessors[accessor_id]

  # grab bufferview
  bufferview = accessor.bufferView

  # grab buffer
  data = gltf.buffers[gltf.bufferViews[bufferview].buffer]

  # unpack data
  magic = 'data:application/octet-stream;base64,'
  bytes = base64.b64decode(data.uri[len(magic):])

  if bytes[0:5] != b'DRACO':
    print('Did not find Draco compressed data..')

  bytestart = gltf.bufferViews[bufferview].byteOffset
  byteend = bytestart + gltf.bufferViews[bufferview].byteLength
  sub_bytes = bytes[bytestart:byteend]

  draco_points = TrakoDracoPy.decode_point_cloud_buffer(sub_bytes).points

  if not reshape:
    return draco_points


  if accessor.type in gltfType_to_vtkNumberOfComponents:
    number_of_elements = gltfType_to_vtkNumberOfComponents[accessor.type]
  else:
    # work around
    number_of_elements = accessor.type

  datatype = gltfComponentType_to_npDataType[accessor.componentType]
  draco_points_reshaped = np.array(draco_points, dtype=datatype).reshape(int(len(draco_points)/number_of_elements), number_of_elements)

  return draco_points_reshaped
