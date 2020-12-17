from .vtk2gltfi import *

class Encoder():

  @staticmethod
  def fromVtp(vtpfile, config=None, draco=True, verbose=True, coords_only=False):
    '''
    '''

    extension = os.path.splitext(vtpfile)[1].lower()

    if extension == '.vtp':

      r = vtk.vtkXMLPolyDataReader()
      r.SetFileName(vtpfile)
      r.Update()
      polydata = r.GetOutput()

    elif extension == '.vtk':

      r = vtk.vtkPolyDataReader()
      r.SetFileName(vtpfile)
      r.Update()
      polydata = r.GetOutput()

    else:

      raise Error('Invalid input format.')

    fibercluster = convert(polydata, config=config, verbose=verbose, coords_only=coords_only)
    gltf = fibercluster2gltf(fibercluster, draco=draco, config=config, verbose=verbose)

    return gltf
