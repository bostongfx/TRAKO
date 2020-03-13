import trako as TKO
import time
import os
import vtk

def trakomagic(input, compressed, restored, config=None):

  #
  # trakofy
  #
  t0 = time.time()
  tko = TKO.Encoder.fromVtp(input, config=config, verbose=False)
  tko.save(compressed)
  c_time = time.time()-t0

  #
  # getstats
  #
  poly_a = TKO.Util.loadvtp(input)
  number_of_streamlines = poly_a['number_of_streamlines']
  originalsize = os.path.getsize(input)
  compressedsize = os.path.getsize(compressed)
  poly_a = TKO.Util.loadvtp(input)

  #
  # untrakofy
  #
  t0 = time.time()

  polydata = TKO.Decoder.toVtp(compressed, verbose=False)

  w = vtk.vtkXMLPolyDataWriter()
  w.SetFileName(restored)
  w.SetInputData(polydata)
  w.Update()

  d_time = time.time()-t0


  return {
    'input': input,
    'compressed': compressed,
    'restored': restored,
    'config': config,
    'originalsize': originalsize,
    'compressedsize': compressedsize,
    'c_time': c_time,
    'd_time': d_time,
    'number_of_streamlines': number_of_streamlines
  }
