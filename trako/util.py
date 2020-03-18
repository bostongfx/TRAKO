import numpy as np
import matplotlib.pyplot as plt
import vtk
from vtk.util import numpy_support


class Util:

  @staticmethod
  def error(points1, points2, clusters=3):

    distances = []

    if clusters==3:

      if len(points1) == 0 or len(points2) == 0:
          return (0,0,0,0),[]

      for i,p in enumerate(points1):

        p1 = points1[i]
        p2 = points2[i]

        if (np.any(np.isnan(p1))):
          p1 = np.nan_to_num(p1)
        if (np.any(np.isnan(p2))):
          p2 = np.nan_to_num(p2)

        dist = np.linalg.norm(p1-p2)

        distances.append(dist)

    if len(distances) == 0:
      return (0,0,0,0),[]

    return (np.min(distances), np.max(distances), np.mean(distances), np.std(distances)), distances

  @staticmethod
  def normalized_error(points1, points2, clusters=3):

    distances = []

    if clusters==3:

      min_p1 = np.min(points1)
      min_p2 = np.min(points2)
      min_p = min(min_p1, min_p2)
      max_p1 = np.max(points1)
      max_p2 = np.max(points2)
      max_p = max(max_p1, max_p2)

      for i,p in enumerate(points1):

        p1 = points1[i]
        p2 = points2[i]

        dist = np.linalg.norm(p1-p2)

        dist /= (max_p - min_p)

        distances.append(dist)

    return (np.min(distances), np.max(distances), np.mean(distances), np.std(distances)), distances


  @staticmethod
  def show_surroundings(points, index, window=3):

    start = max(0, index-window)
    end = min(len(points), index+window)

    return points[start : end]


  @staticmethod
  def plot(values, xlabel='X', ylabel='Y'):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.spines['bottom'].set_color('cyan')
    ax.spines['top'].set_color('cyan')
    ax.xaxis.label.set_color('cyan')
    ax.tick_params(axis='x', colors='cyan')
    ax.spines['left'].set_color('cyan')
    ax.spines['right'].set_color('cyan')
    ax.yaxis.label.set_color('cyan')
    ax.tick_params(axis='y', colors='cyan')

    plt.show()


  @staticmethod
  def loadvtp(a, fromfile=True):

    if fromfile:

      if a.endswith('vtp'):

          r = vtk.vtkXMLPolyDataReader()
          r.SetFileName(a)
          r.Update()
          polydata = r.GetOutput()

      elif a.endswith('vtk'):

          r = vtk.vtkPolyDataReader()
          r.SetFileName(a)
          r.Update()
          polydata = r.GetOutput()

    else:
      polydata = a

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

    for i in range(number_of_scalars):
        arr_name = pointdata.GetArrayName(i)
        scalar_names.append(str(arr_name))
        arr = pointdata.GetArray(i)

        number_of_components = arr.GetNumberOfComponents()
        data_type = arr.GetDataType()

        scalar_types.append((data_type, number_of_components))

        scalars.append(numpy_support.vtk_to_numpy(arr))


    #
    # properties are per streamline
    #
    celldata = polydata.GetCellData()
    number_of_properties = celldata.GetNumberOfArrays()
    properties = []
    property_types = []
    property_names = []

    for i in range(number_of_properties):
        arr_name = celldata.GetArrayName(i)
        property_names.append(str(arr_name))
        arr = celldata.GetArray(i)

        number_of_components = arr.GetNumberOfComponents()
        data_type = arr.GetDataType()

        property_types.append((data_type, number_of_components))

        properties.append(numpy_support.vtk_to_numpy(arr))

    out = {
      'points': points,
      'lines': lines,
      'number_of_streamlines': number_of_streamlines,
      'scalar_names': scalar_names,
      'scalars': scalars,
      'property_names': property_names,
      'properties': properties
    }

    return out
