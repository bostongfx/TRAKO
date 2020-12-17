import pygltflib
from pygltflib import *

import TrakoDracoPy

import vtk
from vtk.util import numpy_support

import numpy as np
import os

import collections


#
#
# MAP VTK DATATYPE TO GLTF COMPONENT TYPE
#
#
vtkDataType_to_gltfComponentType = {

  vtk.VTK_CHAR: pygltflib.BYTE,
  vtk.VTK_UNSIGNED_CHAR: pygltflib.UNSIGNED_BYTE,
  vtk.VTK_SHORT: pygltflib.SHORT,
  vtk.VTK_UNSIGNED_SHORT: pygltflib.UNSIGNED_SHORT,
  vtk.VTK_INT: pygltflib.UNSIGNED_INT,
  vtk.VTK_UNSIGNED_INT: pygltflib.UNSIGNED_INT,
  vtk.VTK_FLOAT: pygltflib.FLOAT,
  vtk.VTK_DOUBLE: pygltflib.FLOAT

}

#
#
# MAP VTK NUMBEROFCOMPONENTS TO GLTF TYPE
#
#
vtkNumberOfComponents_to_gltfType = {
  
  1: pygltflib.SCALAR,
  2: pygltflib.VEC2,
  3: pygltflib.VEC3,
  4: pygltflib.VEC4
  # TODO MAT2, MAT3, MAT4

}



def convert(polydata, config=None, verbose=True, coords_only=False):
  '''
  Takes a vtk polydata and converts it to TKO.
  '''

  # remove degenerate (single point) lines
  # see https://github.com/bostongfx/TRAKO/issues/8
  cleaner = vtk.vtkCleanPolyData()
  cleaner.PointMergingOff()
  cleaner.SetInputData(polydata)
  cleaner.Update()
  polydata = cleaner.GetOutputDataObject(0)
  polydata.SetVerts(vtk.vtkCellArray())
  
  points = numpy_support.vtk_to_numpy(polydata.GetPoints().GetData())
  lines = numpy_support.vtk_to_numpy(polydata.GetLines().GetData())
  number_of_streamlines = polydata.GetLines().GetNumberOfCells()

  #
  # scalars are per point
  #
  pointdata = polydata.GetPointData()
  number_of_scalars = pointdata.GetNumberOfArrays()
  scalars = []
  scalar_types = []
  scalar_names = []

  if not coords_only:

    for i in range(number_of_scalars):
        arr_name = pointdata.GetArrayName(i)
        scalar_names.append(str(arr_name))
        arr = pointdata.GetArray(i)

        # arr.ComputeScalarRange()

        # print(arr)

        number_of_components = arr.GetNumberOfComponents()
        data_type = arr.GetDataType()

        scalar_types.append((data_type, number_of_components))

        if verbose:
          print('Loading scalar', arr_name)
        scalars.append(numpy_support.vtk_to_numpy(arr))

  #
  # properties are per streamline
  #
  celldata = polydata.GetCellData()
  number_of_properties = celldata.GetNumberOfArrays()
  properties = []
  property_types = []
  property_names = []

  if not coords_only:

    for i in range(number_of_properties):
        arr_name = celldata.GetArrayName(i)
        property_names.append(str(arr_name))
        arr = celldata.GetArray(i)

        # print(i, arr)

        number_of_components = arr.GetNumberOfComponents()
        data_type = arr.GetDataType()

        property_types.append((data_type, number_of_components))

        if verbose:
          print('Loading property', arr_name)
        properties.append(numpy_support.vtk_to_numpy(arr))


  #
  # convert to streamlines
  #
  ordered_indices = []
  ordered_scalars = []
  i = 0
  current_fiber_id = 0
  line_length = 0
  # sanity check
  if len(lines) > 0:
    line_length = lines[i]
  line_index = 0

  lines_just_length = []

  while (line_index<number_of_streamlines):

      lines_just_length.append(line_length)

      i += line_length
      line_index += 1
      if line_index < number_of_streamlines:
          line_length = lines[i+line_index]

  #
  # now, create fiber cluster data structure
  #
  fibercluster = {

    'number_of_streamlines': number_of_streamlines,
    'per_vertex_data': collections.OrderedDict(),
    'indices': lines_just_length, #ordered_indices
    'per_streamline_data': collections.OrderedDict()

  }

  fibercluster['per_vertex_data']['POSITION'] = {
    'componentType': vtkDataType_to_gltfComponentType[polydata.GetPoints().GetDataType()],
    'type': vtkNumberOfComponents_to_gltfType[polydata.GetPoints().GetData().GetNumberOfComponents()],
    'data': points#ordered_vertices
  }

  for i,s in enumerate(scalar_names):

    vtkdatatype = scalar_types[i][0]
    vtknumberofcomponents = scalar_types[i][1]

    thisdata = scalars[i]#[]

    if vtknumberofcomponents in vtkNumberOfComponents_to_gltfType:
      gltfType = vtkNumberOfComponents_to_gltfType[vtknumberofcomponents]
    else:
      # for now, we will just pass it through
      gltfType = vtknumberofcomponents

    fibercluster['per_vertex_data'][s] = {
      'componentType': vtkDataType_to_gltfComponentType[vtkdatatype],
      'type': gltfType,
      'data': thisdata
    }

  for i,p in enumerate(property_names):

    vtkdatatype = property_types[i][0]
    vtknumberofcomponents = property_types[i][1]

    thisdata = properties[i]#[]

    if vtknumberofcomponents in vtkNumberOfComponents_to_gltfType:
      gltfType = vtkNumberOfComponents_to_gltfType[vtknumberofcomponents]
    else:
      # for now, we will just pass it through
      gltfType = vtknumberofcomponents

    fibercluster['per_streamline_data'][p] = {
      'componentType': vtkDataType_to_gltfComponentType[vtkdatatype],
      'type': gltfType,
      'data': thisdata
    }

  return fibercluster


def fibercluster2gltf(fibercluster, draco=False, config=None, verbose=True):

  if config and draco:
    if verbose:
      print('Using custom configuration for Draco.')

  if (fibercluster['number_of_streamlines'] == 0):
    if verbose:
      print('No streamlines!')
    return GLTF2()

  gltf = GLTF2()
  scene = Scene()
  scene.nodes.append(0)
  gltf.scene = 0
  gltf.scenes.append(scene)




  # we need a bunch of buffers for all the attributes
  buffers = collections.OrderedDict()
  for attributename in fibercluster['per_vertex_data'].keys():
    buffers[attributename] = Buffer()

  # and of course a bunch of chunkers per attribute
  chunkers = collections.OrderedDict()
  for attributename in fibercluster['per_vertex_data'].keys():
    chunkers[attributename] = b""

  # and a bunch of bufferviews
  bufferviews = []
  # and a bunch of accessors
  accessors = []



  # we need stuff for properties as well
  p_buffers = collections.OrderedDict()
  for p_name in fibercluster['per_streamline_data'].keys():
    p_buffers[p_name] = Buffer()
  p_chunkers = collections.OrderedDict()
  for p_name in fibercluster['per_streamline_data'].keys():
    p_chunkers[p_name] = b""

  # and a bunch of bufferviews
  p_bufferviews = []
  # and a bunch of accessors
  p_accessors = []




  #
  # Start glTF setup
  #
  node = Node() # one fiber cluster has a node
  mesh = Mesh() # .. and a mesh
  node.mesh = 0

  custom_attributes = {}
  custom_attribute_index = 0
  for attributename in fibercluster['per_vertex_data'].keys():
    if attributename != 'POSITION':
      # this is custom
      attributename = '_'+attributename
    custom_attributes[attributename] = custom_attribute_index
    custom_attribute_index += 1

  primitive = Primitive()
  for attributeindex,attributename in enumerate(custom_attributes.keys()):
    # we need to update the indices increasingly
    custom_attributes[attributename] = attributeindex

  primitive.attributes = Attributes(**custom_attributes)
  primitive.mode = 1





  #
  # per-vertex values (position and scalars)
  #
  for attributeindex,attributename in enumerate(fibercluster['per_vertex_data'].keys()):

    componentType = fibercluster['per_vertex_data'][attributename]['componentType']
    aType = fibercluster['per_vertex_data'][attributename]['type']
    data = fibercluster['per_vertex_data'][attributename]['data']

    asciiType, npType = componentTypeConverter(componentType, verbose)


    chunk, bounds = packit(asciiType, npType, draco, data, config, attributename, verbose)

    # each attribute has a bufferview
    # and an accessor
    bufferview = BufferView()
    bufferview.target = ARRAY_BUFFER
    bufferview.buffer = attributeindex
    bufferview.byteOffset = 0
    bufferview.byteLength = len(chunk) 
    bufferviews.append(bufferview)

    chunkers[attributename] += chunk

    accessor = Accessor()
    accessor.bufferView = len(bufferviews)-1
    accessor.byteOffset = 0
    accessor.componentType = componentType
    accessor.count = len(data)
    accessor.type = aType
    accessor.min = list(bounds[0])
    accessor.max = list(bounds[1])
    accessors.append(accessor)






  #
  # indices
  #
  indices = np.array(fibercluster['indices'])
  asciiType = 'H' # always integer
  npType = int # always integer

  i_chunk, bounds = packit(asciiType, npType, draco, indices, config, 'INDICES', verbose)

  bufferview = BufferView()
  bufferview.target = ELEMENT_ARRAY_BUFFER
  bufferview.buffer = attributeindex+1 # this is last buffer.. for now only -> properties below
  bufferview.byteOffset = 0
  bufferview.byteLength = len(i_chunk)

  primitive.indices = len(accessors) # again, NOT last one!

  accessor = Accessor()
  accessor.bufferView = len(bufferviews) # the last buffer view
  accessor.byteOffset = 0
  accessor.componentType = UNSIGNED_SHORT
  accessor.count = len(indices)
  accessor.type = SCALAR
  accessor.min = list(bounds[0])
  accessor.max = list(bounds[1])











  #
  # per-fiber properties
  # 
  properties = {} # this will later hold our accessor id's for the property data
  for p_index,p_name in enumerate(fibercluster['per_streamline_data'].keys()):

    componentType = fibercluster['per_streamline_data'][p_name]['componentType']
    aType = fibercluster['per_streamline_data'][p_name]['type']
    data = fibercluster['per_streamline_data'][p_name]['data']

    asciiType, npType = componentTypeConverter(componentType, verbose)

    chunk, bounds = packit(asciiType, npType, draco, data, config, p_name, verbose)

    # we need a bufferview
    # and an accessor
    p_bufferview = BufferView()
    p_bufferview.target = ARRAY_BUFFER
    p_bufferview.buffer = attributeindex+1+p_index+1 # first scalars, then indices, then properties
    p_bufferview.byteOffset = 0
    p_bufferview.byteLength = len(chunk) 
    p_bufferviews.append(p_bufferview)

    p_chunkers[p_name] += chunk

    p_accessor = Accessor()
    p_accessor.bufferView = len(bufferviews) + len(p_bufferviews)
    p_accessor.byteOffset = 0
    p_accessor.componentType = componentType
    p_accessor.count = len(data)
    p_accessor.type = aType
    p_accessor.min = list(bounds[0])
    p_accessor.max = list(bounds[1])
    p_accessors.append(p_accessor)

    properties[p_name] = len(accessors) + len(p_accessors)


  primitive.extras = {'properties': properties}



  #
  # Setup glTF structure
  #

  # add this streamline to the mesh
  mesh.primitives.append(primitive)

  # now add the mesh to the scene
  gltf.meshes.append(mesh)
  gltf.nodes.append(node)

  # add the bufferviews and the accessors
  gltf.bufferViews += bufferviews + [bufferview] + p_bufferviews # per vertex, indices, per streamline
  gltf.accessors += accessors + [accessor] + p_accessors




  #
  # store all buffer data base64-encoded
  #
  for attributename in fibercluster['per_vertex_data'].keys():

    buffer = buffers[attributename]
    chunker = chunkers[attributename]

    buffer.uri = pygltflib.DATA_URI_HEADER
    buffer.uri += str(base64.b64encode(chunker), "utf-8")
    buffer.byteLength = len(chunker)

    gltf.buffers.append(buffer)


  # and now for the indices
  indexbuffer = Buffer()
  indexbuffer.uri = pygltflib.DATA_URI_HEADER
  indexbuffer.uri += str(base64.b64encode(i_chunk), "utf-8")
  indexbuffer.byteLength = len(i_chunk)
  gltf.buffers.append(indexbuffer)

  # and now for the properties
  for p_name in fibercluster['per_streamline_data'].keys():

    buffer = p_buffers[p_name]
    chunker = p_chunkers[p_name]

    buffer.uri = pygltflib.DATA_URI_HEADER
    buffer.uri += str(base64.b64encode(chunker), "utf-8")
    buffer.byteLength = len(chunker)

    gltf.buffers.append(buffer)


  return gltf







#
#
#
def componentTypeConverter(componentType, verbose):
  '''
  '''
  if componentType == pygltflib.FLOAT:
    asciiType = 'f'
    npType = float

  elif componentType == pygltflib.UNSIGNED_INT:
    asciiType = 'I'
    npType = int

  elif componentType == pygltflib.UNSIGNED_BYTE:
    asciiType = 'B'
    npType = int

  else:
    asciiType = 'f'
    npType = float
    if verbose:
      print('Type not supported!', componentType)

  return asciiType, npType



#
#
#
def config2dracoparameters(config, field, verbose=False):
  '''
  '''

  # default parameters
  position = False
  if (field == 'POSITION'):
    position = True

  sequential = True
  qb=14
  cl=1
  qrange=-1
  qorigin=None

  if config:

    if field in config or '*' in config:

      if not field in config:
        # use * config if name is not explicitly defined
        config[field] = dict(config['*']) 

      position = config[field]['position']
      sequential = config[field]['sequential']
      qb = config[field]['quantization_bits']
      cl = config[field]['compression_level']
      qrange = config[field]['quantization_range']
      qorigin = config[field]['quantization_origin']

      if verbose:
        print ('Custom config for', field)

  return (position, sequential, qb, cl, qrange, qorigin)


#
#
#
def packit(asciiType, npType, draco, data, config, field, verbose):
  '''
  data needs to be a numpy array
  '''
  if draco:

    bounds = [[],[]]
    if data.ndim > 1:
      for k in range(data.shape[1]):
        bounds[0].append(npType(np.min(data[:,k])))
        bounds[1].append(npType(np.max(data[:,k])))
    else:
      bounds = [[npType(np.min(data))], [npType(np.max(data))]]
      
    # we don't care about NaNs in the bounds
    # and they should be float no matter what
    bounds = np.nan_to_num(bounds, copy=False).astype(np.float) 

    position, sequential, qb, cl, qrange, qorigin = config2dracoparameters(config, field, verbose)

    #
    # replace NaN in a dirty way for now
    #
    if len(np.where(np.isnan(data))[0]) != 0:
      print('*** WARNING: Replacing NaN values with 0! ***')
      np.nan_to_num(data, copy=False)

    if len(data) == 0:
      if verbose:
        print('Scalar with length 0! Skipping..', field)
      chunk = b""
    else:
      chunk = TrakoDracoPy.encode_point_cloud_to_buffer(data.ravel(), position=position, sequential=sequential, 
        quantization_bits=qb, compression_level=cl, quantization_range=qrange, quantization_origin=qorigin)

  else:

    bounds = [[],[]]
    if data.ndim > 1:
      for k in range(data.shape[1]):
        bounds[0].append(npType(np.min(data[:,k])))
        bounds[1].append(npType(np.max(data[:,k])))
    else:
      bounds = [[npType(np.min(data))], [npType(np.max(data))]]

    bounds = bounds.astype(np.float)

    #
    # create bytestream for buffer
    #
    chunk = b""
    for index, values in enumerate(data):
      
      if not type(values) is np.ndarray:
        values = [values]

      pack = "<" + (asciiType*len(values))

      subChunk = struct.pack(pack, *values)
      chunk += subChunk


  return chunk, bounds
