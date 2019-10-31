from .gltfi2vtk import *

class Decoder():

  @staticmethod
  def toVtp(vtpfile, draco=True):
    '''
    '''
    
    vtp = convert(vtpfile)
    # vtp = fibercluster2vtp(fibercluster, draco=draco)

    return vtp
