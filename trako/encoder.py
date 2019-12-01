from .vtk2gltfi import *

class Encoder():

  @staticmethod
  def fromVtp(vtpfile, config=None, draco=True, verbose=True):
    '''
    '''

    fibercluster = convert(vtpfile, config=config, verbose=verbose)
    gltf = fibercluster2gltf(fibercluster, draco=draco, config=config, verbose=verbose)

    return gltf
