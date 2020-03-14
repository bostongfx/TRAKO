#!/usr/bin/env python

import vtk
from vtk.util import numpy_support
import nibabel

import argparse
import glob
import numpy as np
import os


def convert(input, output, force=True, only_points=False):

  # print('Converting', len(input), 'files.')

  for file_i in input:

    if not os.path.exists(file_i):
      print('ERROR', 'Could not find file:', file_i)
      return

    # print('Converting', file_i)

    input_basename = os.path.basename(file_i)

    if input_basename.endswith('vtp'):

      r = vtk.vtkXMLPolyDataReader()
      r.SetFileName(file_i)
      r.Update()
      polydata = r.GetOutput()

    elif input_basename.endswith('vtk'):

      r = vtk.vtkPolyDataReader()
      r.SetFileName(file_i)
      r.Update()
      polydata = r.GetOutput()


    points = numpy_support.vtk_to_numpy(polydata.GetPoints().GetData())
    lines = numpy_support.vtk_to_numpy(polydata.GetLines().GetData())
    number_of_streamlines = polydata.GetLines().GetNumberOfCells()

    # if (number_of_streamlines == 0):

    #   print('ERROR', 'No streamlines in file:', file_i)
    #   continue

    #
    # scalars are per point
    #
    pointdata = polydata.GetPointData()
    number_of_scalars = pointdata.GetNumberOfArrays()
    scalars = []# np.zeros((points.shape[0], number_of_scalars))
    scalar_names = ['']*10#np.empty((10,20),dtype=np.byte)

    for i in range(number_of_scalars):
        arr_name = pointdata.GetArrayName(i)
        scalar_names[i] = str.encode(arr_name)[0:20]
        
        # print('Loading Scalar', arr_name)
        scalars.append(numpy_support.vtk_to_numpy(pointdata.GetArray(i)))


    #
    # properties are per streamline
    #
    celldata = polydata.GetCellData()
    number_of_properties = celldata.GetNumberOfArrays()
    properties = np.zeros((number_of_streamlines, number_of_properties),dtype=np.float32)
    property_names =['']*10# np.empty((10,20),dtype=np.byte)

    for i in range(number_of_properties):
        arr_name = celldata.GetArrayName(i)
        property_names[i] = str.encode(arr_name)[0:20]
        
        # print('Loading Property', arr_name)
        current_array = numpy_support.vtk_to_numpy(celldata.GetArray(i))

        if (current_array.ndim > 1):
            # print('  Warning: Combining Property', arr_name, '(mean)')
            current_array = np.mean(current_array)
            continue
        properties[:,i] = current_array
        

        
    #
    # convert to streamlines
    #
    streamlines = []
    i = 0
    current_fiber_id = 0
    line_length = 0
    if len(lines) > 0:
      line_length = lines[i]
    line_index = 0

    while (line_index<number_of_streamlines):
    #     print(line_index,'start',i+1,'len',line_length)
        
        current_line = lines[i+1+line_index:i+1+line_length+line_index]
        current_points = np.zeros((line_length, 3), dtype=np.float32)
        current_scalars = np.zeros((line_length, number_of_scalars), dtype=np.float32)
        current_properties = np.zeros((number_of_properties), dtype=np.float32)
    #     current_properties = np.zeros()
        
        for p_i, p in enumerate(current_line):
            current_points[p_i] = points[p]
            current_scalars[p_i] = scalars[p]  
        
        current_properties = properties[line_index]
        
        if only_points:
            streamlines.append((current_points, None, None))
        else:
            streamlines.append((current_points, current_scalars, current_properties))
        
        i += line_length
        line_index += 1
        if line_index < number_of_streamlines:
            line_length = lines[i+line_index]
            
            
    #
    # create header
    #
    hdr = {'vox_to_ras':np.eye(4), 
           'voxel_size':np.ones(3), 
           'dim':np.array([256,256,256]),
           'scalar_name':scalar_names,
           'property_name':property_names}


    with open(output, 'wb') as f:
        nibabel.trackvis.write(f, streamlines, hdr)

    # print('Written', output)


