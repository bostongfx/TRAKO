import runner

class Sprinter:

  @staticmethod
  def run_qfib(qfib_files, qfib_bits):
    qfib_sizes = [0]*len(qfib_bits)
    qfib_errors = [0]*len(qfib_bits)
    qfib_stds = [0]*len(qfib_bits)
    for f in qfib_files:
        for i,b in enumerate(qfib_bits):
            rundata = runner.Runner.qfib(f[0], f[1], bits=b, force=False)
            c_time = rundata[0]
            d_time = rundata[1]
            sizestats = rundata[2]
            compressedsize = sizestats[1]
            meanerror = rundata[3][2]
            stderror = rundata[3][3]
            
            # if meanerror > 2:
            #     continue
            qfib_sizes[i] += compressedsize
            qfib_errors[i] += meanerror
            qfib_stds[i] += stderror
    #         qfib_sizes.append(compressedsize)
    #         qfib_errors.append(meanerror)
    #         qfib_stds.append(stderror)
    for i,b in enumerate(qfib_bits):
        qfib_sizes[i] /= len(qfib_files)
        qfib_errors[i] /= len(qfib_files)
        qfib_stds[i] /= len(qfib_files)

    return qfib_sizes, qfib_errors, qfib_stds

  @staticmethod
  def run_trako(config, tko_files, tko_bits):

      config_ = dict(config)

      tko_sizes = [0]*len(tko_bits)
      tko_errors = [0]*len(tko_bits)
      tko_stds = [0]*len(tko_bits)
      fails = [len(tko_files)]*len(tko_bits)
      for j,f in enumerate(tko_files):
          for i,b in enumerate(tko_bits):

              config = dict(config_)
              config['name'] = config['name'].replace('{bits}', str(b)) # change name
              for c in config.keys():
                  if c=='name':
                      continue
                  config[c]['quantization_bits'] = b # update bits for config
              
              try:
                  rundata = runner.Runner.tko(f[0], f[1], config=config, coords_only=True, force=False)
              except:
                  fails[i] -= 1
                  continue
              c_time = rundata[0]
              d_time = rundata[1]
              sizestats = rundata[2]
              compressedsize = sizestats[1]
              meanerror = rundata[3][2]
              stderror = rundata[3][3]
              tko_sizes[i] += compressedsize
              tko_errors[i] += meanerror
              tko_stds[i] += stderror
      #         tko_sizes.append(compressedsize)
      #         tko_errors.append(meanerror)
      #         tko_stds.append(stderror)
      for i,b in enumerate(tko_bits):
          if fails[i] == 0:
            continue
          tko_sizes[i] /= fails[i]#len(tko_files)
          tko_errors[i] /= fails[i]#len(tko_files)
          tko_stds[i] /= fails[i]#len(tko_files)
          
      return tko_sizes, tko_errors, tko_stds

