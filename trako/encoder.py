from .vtk2gltfi import *

class Encoder():

  @staticmethod
  def fromVtp(vtpfile, config=None, draco=True):
    '''
    '''
    
    fibercluster = convert(vtpfile, config=config)
    gltf = fibercluster2gltf(fibercluster, draco=draco, config=config)

    return gltf
