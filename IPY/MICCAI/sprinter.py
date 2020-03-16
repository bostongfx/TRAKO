import numpy as np
import runner

class Sprinter:

  @staticmethod
  def bitsplot(plt, tkoruns={}, tko_bits = [6,7,8,9,10,11,12,13,14], qfibruns=None, dpyruns=None, xlim=None, ylim=(0,1), filename=None):
    '''
    '''
    plt.figure(num=None, figsize=(8, 6), dpi=240, facecolor='w', edgecolor='k')


    longest_run = 0
    longest = 0
    for r in tkoruns.keys():
        
    #     if r != 'default':
    #         continue
        
        tko_sizes = tkoruns[r][0]
        tko_errors = tkoruns[r][1]
        tko_stds = tkoruns[r][2]

        if 0 in tko_sizes:
            tko_sizes.remove(0)
        if 0 in tko_errors:
            tko_errors.remove(0)
        if 0 in tko_stds:
            tko_stds.remove(0)

        if len(tko_sizes) > longest:
          # print('lo',r)
          longest = len(tko_sizes)
          longest_run = tko_sizes
                
        
        tko_sizes_ = np.array(tko_sizes) / 1000000
    #     plt.scatter(tko_sizes_, tko_errors, s = np.array(tko_stds)*1000, alpha=1, label='TRAKO ('+r+')')
        size = 10
        if r=='default':
            size=70

        run_name = r
        if run_name == 'qbponly{bits}':
          run_name = 'XYZ only'
        elif run_name == 'qbi{bits}':
          run_name = 'XYZ + Ind.'
        elif run_name == 'qbi_CL0_{bits}':
          run_name = 'XYZ + Ind. Level 0'
        plt.scatter(tko_sizes_, tko_errors, s = size, alpha=1, label='TRAKO ('+run_name+')')
        plt.errorbar(tko_sizes_, tko_errors, tko_stds, fmt='|', alpha=.5)

    for x,s in enumerate(longest_run):

      y = tko_errors[x]
      y += y*0.05
      txt = tko_bits[x]
      x = tko_sizes_[x]
      x += x*0.01

      if ylim:
        if y<ylim[0]:
          continue
        if y>= ylim[1]:
          continue
      if xlim:
        if x<=xlim[0]:
          continue
        if x>=xlim[1]:
          continue


      
      plt.text(x, y, txt)


    if qfibruns:
      qfib_sizes = qfibruns[0]
      qfib_errors = qfibruns[1]
      qfib_stds = qfibruns[2]
      qfib_sizes_ = np.array(qfib_sizes) / 1000000
      plt.scatter(qfib_sizes_, qfib_errors, s = 10, color='black', alpha=1, label='QFib')
      plt.errorbar(qfib_sizes_, qfib_errors, qfib_stds, fmt='|', color='black', alpha=.5)
      plt.ticklabel_format(style='plain', axis='both', scilimits=(0, 0))

    import matplotlib.ticker as mticker    
    plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%d MB'))

    if ylim:
      plt.ylim(ylim[0], ylim[1])

    if xlim:
      plt.xlim(xlim[0], xlim[1])

    # plt.axvline(x=input_size/1000000, color='red', linestyle='--')

    plt.xlabel('Data Size [MB]')
    plt.ylabel('Mean Absolute Error [MAE]')
    plt.legend()

    if filename:
      a = plt.savefig(filename)

    plt.show()



  @staticmethod
  def run_dpy(dpy_files):
    dpy_sizes = [0]
    dpy_errors = [0]
    dpy_stds = [0]
    for f in dpy_files:

        rundata = runner.Runner.dpy(f[0], f[1], force=False)
        c_time = rundata[0]
        d_time = rundata[1]
        sizestats = rundata[2]
        compressedsize = sizestats[1]
        meanerror = rundata[3][2]
        stderror = rundata[3][3]
        print(rundata)
        print(meanerror, stderror)

        dpy_sizes[0] += compressedsize
        dpy_errors[0] += meanerror
        dpy_stds[0] += stderror

    return dpy_sizes, dpy_errors, dpy_stds

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
            # print(rundata)
            # print(meanerror, stderror)
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
  def run_trako(config, tko_files, tko_bits, coords_only=True):

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
                  rundata = runner.Runner.tko(f[0], f[1], config=config, coords_only=coords_only, force=False)
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

