import numpy as np
import runner

class Sprinter:

  @staticmethod
  def createtable(dataset, originalsize, tkoruns={}, selector=None, qfibruns=None, dpyruns=None):



    for r in tkoruns.keys():
        
    #     if r != 'default':
    #         continue
        
        tko_sizes = tkoruns[r][0]
        tko_errors = tkoruns[r][1]
        tko_stds = tkoruns[r][2]
        tko_advstats = tkoruns[r][3]

        if 0 in tko_sizes:
            tko_sizes.remove(0)
        if 0 in tko_errors:
            tko_errors.remove(0)
        if 0 in tko_stds:
            tko_stds.remove(0)

        run_name = r
        if run_name == 'qbponly{bits}':
          run_name = 'XYZ only'
        elif run_name == 'qbi{bits}':
          run_name = 'XYZ + Ind.'
        elif run_name == 'qbi_CL0_{bits}':
          run_name = 'XYZ + Ind. Level 0'
        elif run_name.endswith('binary'):
          run_name = 'XYZ + Ind. (Binary)'

        compressedsize = tko_sizes[selector]

        c_ratio = (1-float(compressedsize)/float(originalsize))*100
        c_factor = float(originalsize) / float(compressedsize)

        print('-'*20)
        print(r)
        print('size', compressedsize)
        print('ratio', c_ratio)
        print('c_factor', c_factor)


        min_e = tko_advstats[0][selector]
        print('min_e', min_e)
        max_e = tko_advstats[1][selector]
        print('max_e', max_e)
        if len(tko_errors) > 0:
          mean_e = tko_errors[selector]
          print('mean_e', mean_e)
          std = tko_stds[selector]
          print('std', std)
        else:
          mean_e = 0.
          std = 0.
          print('mean_e', 0)
          print('std',0)

        e_min_e = tko_advstats[2][selector]
        print('e_min_e', e_min_e)
        e_max_e = tko_advstats[3][selector]
        print('e_max_e', e_max_e)
        e_mean_e = tko_advstats[4][selector]
        print('e_mean_e', e_mean_e)
        e_std = tko_advstats[5][selector]
        print('e_std', e_std)
        c_time = tko_advstats[6][selector]
        print('c_time', c_time)
        d_time = tko_advstats[7][selector]
        print('d_time', d_time)
        print('-'*20)

        latexline = '~~~'+run_name+' & '+ \
                    str(np.round(compressedsize/1000000.,0)) + ' & '+ \
                    str(np.round(c_ratio,3))+'$\\times$' + ' & '+ \
                    str(np.round(c_factor,3))+'\\%' + ' & '+ \
                    str(np.round(min_e,3)) + ' & '+ \
                    str(np.round(max_e,3)) + ' & '+ \
                    str(np.round(mean_e,3)) + '$\\pm$' + str(np.round(std,3)) + ' & '+ \
                    str(np.round(e_min_e,3)) + ' & '+ \
                    str(np.round(e_max_e,3)) + ' & '+ \
                    str(np.round(e_mean_e,3)) + '$\\pm$' + str(np.round(e_std,3)) + ' & '+ \
                    str(np.round(c_time,3)) + ' & '+ \
                    str(np.round(d_time,3)) + '\\\\'

        print(latexline)

        '''
        \\textbf{qfib-data} & 2,017M \\\\
                ~~~qfib~\\cite{mercier2020qfib} & 410M & 8$\\times$ & 91.9 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 512.3 & 333.4\\
                ~~~zfib/dipy~\\cite{presseau2015new} & 410M & 8$\times$ & 91.9 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 512.3 & 333.4\\
                ~~~TRAKO & 410M & 8$\\times$ & 91.9 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 512.3 & 333.4\\
                ~~~TRAKO (binary) & 410M & 8$\times$ & 91.9 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 0.333 & 1.444 & 1.01$\\pm$2.22 & 512.3 & 333.4\\
        '''

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
        elif run_name.endswith('binary'):
          run_name = 'XYZ + Ind. (Binary)'
        plt.scatter(tko_sizes_, tko_errors, s = size, alpha=1, label='TRAKO ('+run_name+')')
        plt.errorbar(tko_sizes_, tko_errors, tko_stds, fmt='|', alpha=.5)


    for x,s in enumerate(longest_run):

      y = tko_errors[x]
      y += -0.02#y*0.05
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

    dpy_minerror = [np.inf]
    dpy_maxerror = [0]
    dpy_e_minerror = [np.inf]
    dpy_e_maxerror = [0]
    dpy_e_meanerror = [0]
    dpy_e_std = [0]

    dpy_ctime = [0]
    dpy_dtime = [0]

    for f in dpy_files:

        rundata = runner.Runner.dpy(f[0], f[1], force=False)


        c_time, d_time, sizestats, compressedsize, minerror, maxerror, meanerror, stderror, e_minerror, e_maxerror, e_meanerror, e_stderror = Sprinter.parse_rundata(rundata, False)


        dpy_minerror[0] = min(dpy_minerror[0], minerror)
        dpy_maxerror[0] = max(dpy_maxerror[0], maxerror)
        dpy_e_minerror[0] = min(dpy_e_minerror[0], e_minerror)
        dpy_e_maxerror[0] = max(dpy_e_maxerror[0], e_maxerror)
        dpy_e_meanerror[0] += e_meanerror
        dpy_e_std[0] += e_stderror

        dpy_sizes[0] += compressedsize
        dpy_errors[0] += meanerror
        dpy_stds[0] += stderror

    advancedstats = [dpy_minerror, dpy_maxerror, dpy_e_minerror, dpy_e_maxerror, \
                       dpy_e_meanerror, dpy_e_std, dpy_ctime, dpy_dtime]

    return dpy_sizes, dpy_errors, dpy_stds, advancedstats

  @staticmethod 
  def parse_rundata(rundata, binary=False):
    '''
    '''
    c_time = rundata[0]
    d_time = rundata[1]
    
    if binary:
      sizestats = rundata[-1]
    else:
      sizestats = rundata[2]


    compressedsize = sizestats[1]
    minerror = rundata[3][0]
    maxerror = rundata[3][1]
    meanerror = rundata[3][2]
    stderror = rundata[3][3]

    e_minerror = rundata[4][0]
    e_maxerror = rundata[4][1]
    e_meanerror = rundata[4][2]
    e_stderror = rundata[4][3]

    return c_time, d_time, sizestats, compressedsize, minerror, maxerror, meanerror, stderror, e_minerror, e_maxerror, e_meanerror, e_stderror


  @staticmethod
  def run_qfib(qfib_files, qfib_bits):
    qfib_sizes = [0]*len(qfib_bits)
    qfib_errors = [0]*len(qfib_bits)
    qfib_stds = [0]*len(qfib_bits)

    qfib_minerror = [np.inf]*len(qfib_bits)
    qfib_maxerror = [0]*len(qfib_bits)
    qfib_e_minerror = [np.inf]*len(qfib_bits)
    qfib_e_maxerror = [0]*len(qfib_bits)
    qfib_e_meanerror = [0]*len(qfib_bits)
    qfib_e_std = [0]*len(qfib_bits)

    qfib_ctime = [0]*len(qfib_bits)
    qfib_dtime = [0]*len(qfib_bits)

    for f in qfib_files:
        for i,b in enumerate(qfib_bits):
            rundata = runner.Runner.qfib(f[0], f[1], bits=b, force=False)

            c_time, d_time, sizestats, compressedsize, minerror, maxerror, meanerror, stderror, e_minerror, e_maxerror, e_meanerror, e_stderror = Sprinter.parse_rundata(rundata, False)



            qfib_minerror[i] = min(qfib_minerror[i], minerror)
            qfib_maxerror[i] = max(qfib_maxerror[i], maxerror)
            qfib_e_minerror[i] = min(qfib_e_minerror[i], e_minerror)
            qfib_e_maxerror[i] = max(qfib_e_maxerror[i], e_maxerror)
            qfib_e_meanerror[i] += e_meanerror
            qfib_e_std[i] += e_stderror


            qfib_sizes[i] += compressedsize
            qfib_errors[i] += meanerror
            qfib_stds[i] += stderror

            qfib_ctime[i] += c_time
            qfib_dtime[i] += d_time
    #         qfib_sizes.append(compressedsize)
    #         qfib_errors.append(meanerror)
    #         qfib_stds.append(stderror)
    for i,b in enumerate(qfib_bits):
        qfib_sizes[i] /= len(qfib_files)
        qfib_errors[i] /= len(qfib_files)
        qfib_stds[i] /= len(qfib_files)
        qfib_e_std[i] /= len(qfib_files)
        qfib_e_meanerror[i] /= len(qfib_files)

    advancedstats = [qfib_minerror, qfib_maxerror, qfib_e_minerror, qfib_e_maxerror, \
                       qfib_e_meanerror, qfib_e_std, qfib_ctime, qfib_dtime]

    return qfib_sizes, qfib_errors, qfib_stds, advancedstats

  @staticmethod
  def run_trako(config, tko_files, tko_bits, coords_only=True, binary=False):

      config_ = dict(config)

      tko_sizes = [0]*len(tko_bits)
      tko_errors = [0]*len(tko_bits)
      tko_stds = [0]*len(tko_bits)
      fails = [len(tko_files)]*len(tko_bits)

      tko_minerror = [np.inf]*len(tko_bits)
      tko_maxerror = [0]*len(tko_bits)
      tko_e_minerror = [np.inf]*len(tko_bits)
      tko_e_maxerror = [0]*len(tko_bits)
      tko_e_meanerror = [0]*len(tko_bits)
      tko_e_std = [0]*len(tko_bits)

      tko_ctime = [0]*len(tko_bits)
      tko_dtime = [0]*len(tko_bits)

      for j,f in enumerate(tko_files):
          for i,b in enumerate(tko_bits):

              config = dict(config_)
              config['name'] = config['name'].replace('{bits}', str(b)) # change name
              for c in config.keys():
                  if c=='name':
                      continue
                  config[c]['quantization_bits'] = b # update bits for config
              
              try:
                  rundata = runner.Runner.tko(f[0], f[1], config=config, coords_only=coords_only, force=False, binary=binary)
              except:
                  print('Failing..')
                  fails[i] -= 1
                  continue

              c_time, d_time, sizestats, compressedsize, minerror, maxerror, meanerror, stderror, e_minerror, e_maxerror, e_meanerror, e_stderror = Sprinter.parse_rundata(rundata, binary)



              tko_minerror[i] = min(tko_minerror[i], minerror)
              tko_maxerror[i] = max(tko_maxerror[i], maxerror)
              tko_e_minerror[i] = min(tko_e_minerror[i], e_minerror)
              tko_e_maxerror[i] = max(tko_e_maxerror[i], e_maxerror)
              tko_e_meanerror[i] += e_meanerror
              tko_e_std[i] += e_stderror

              tko_sizes[i] += compressedsize
              tko_errors[i] += meanerror
              tko_stds[i] += stderror

              tko_ctime[i] += c_time
              tko_dtime[i] += d_time
      #         tko_sizes.append(compressedsize)
      #         tko_errors.append(meanerror)
      #         tko_stds.append(stderror)

      for i,b in enumerate(tko_bits):
          if fails[i] == 0:
            continue
          tko_sizes[i] /= fails[i]#len(tko_files)
          tko_errors[i] /= fails[i]#len(tko_files)
          tko_stds[i] /= fails[i]#len(tko_files)
          tko_e_std[i] /= fails[i]
          tko_e_meanerror[i] /= fails[i]
          
      advancedstats = [tko_minerror, tko_maxerror, tko_e_minerror, tko_e_maxerror, \
                       tko_e_meanerror, tko_e_std, tko_ctime, tko_dtime]

      return tko_sizes, tko_errors, tko_stds, advancedstats

