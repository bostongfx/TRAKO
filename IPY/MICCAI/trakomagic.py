import trako as TKO
import time
import os
import vtk

def trakomagic(input, compressed, restored, config=None, coordinate_stats=False):

  #
  # trakofy
  #
  t0 = time.time()
  tko = TKO.Encoder.fromVtp(input, config=config, verbose=False)
  try:
    tko.save(compressed)
  except:
    return tko
  c_time = time.time()-t0

  #
  # getstats
  #
  inputdata = TKO.Util.loadvtp(input)
  number_of_streamlines = inputdata['number_of_streamlines']
  originalsize = os.path.getsize(input)
  compressedsize = os.path.getsize(compressed)

  #
  # untrakofy
  #
  t0 = time.time()

  restored_polydata = TKO.Decoder.toVtp(compressed, verbose=False)

  w = vtk.vtkXMLPolyDataWriter()
  w.SetFileName(restored)
  w.SetInputData(restored_polydata)
  w.Update()

  d_time = time.time()-t0

  stats = {}
  if coordinate_stats:
    original_points = inputdata['points']
    restored_points = numpy_support.vtk_to_numpy(restored_polydata.GetPoints().GetData())


    error = TKO.Util.error(original_points, restored_points)[0]
    # print('Max error', stats[1])
    # print('Mean error', stats[2])
    # print('Min error', stats[0])
    c_ratio = (1-float(compressedsize)/float(originalsize))*100
    c_factor = float(originalsize) / float(compressedsize)

    stats = {
      'error': error,
      'c_ratio': c_ratio,
      'c_factor': c_factor
    }

  return {
    'input': input,
    'compressed': compressed,
    'restored': restored,
    'config': config,
    'originalsize': originalsize,
    'compressedsize': compressedsize,
    'c_time': c_time,
    'd_time': d_time,
    'number_of_streamlines': number_of_streamlines,
    'stats': stats
  }


