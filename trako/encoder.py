from .vtk2gltfi import *

class Encoder():

  @staticmethod
  def fromVtp(vtpfile, draco=True):
    '''
    '''
    
    fibercluster = convert(vtpfile)
    gltf = fibercluster2gltf(fibercluster, draco=draco)

    return gltf
