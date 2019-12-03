from .gltfi2vtk import *

class Decoder():

  @staticmethod
  def toVtp(tkoFile, draco=True, verbose=True):
    '''
    '''
    
    vtp = convert(tkoFile, verbose=verbose)

    return vtp
