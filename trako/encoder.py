from .vtk2gltfi import *

class Encoder():

  @staticmethod
  def fromVtp(vtpfile, config=None, draco=True, verbose=True, coords_only=False):
    '''
    '''

    fibercluster = convert(vtpfile, config=config, verbose=verbose, coords_only=coords_only)
    gltf = fibercluster2gltf(fibercluster, draco=draco, config=config, verbose=verbose)

    return gltf
