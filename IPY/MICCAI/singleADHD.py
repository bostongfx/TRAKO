#!/usr/bin/env python 
import os, sys
import pickle
import trakomagic as M
import time


def run(which):
  SUBJECT = which+'/'#'103_reg_reg_outlier_removed/'
  BLACKLIST = 'tracts_commissural'
  DATAFOLDER = '/home/fan/ADHD/cluster_atlas_01_00002_remove_outliers/'
  # DATAFOLDER = '/home/haehn/Dropbox/TKOTEST/'
  DATAFOLDER_TKO = DATAFOLDER[:-1]+'_TKO/'
  DATAFOLDER_RESTORED = DATAFOLDER[:-1]+'_RESTORED/'
  STATSFOLDER = DATAFOLDER[:-1]+'_STATS/'
  DATAFOLDER += SUBJECT
  DATAFOLDER_TKO += SUBJECT
  DATAFOLDER_RESTORED += SUBJECT
  STATSFILE = STATSFOLDER+SUBJECT[:-1]+'.p'

  originalsize = []
  compressedsize = []
  number_of_streamlines = []
  c_time = []
  d_time = []

  t0 = time.time()
  for root, dirs, files in os.walk(DATAFOLDER):
      for name in files:
          
          if name.endswith('.vtp'):
              input = os.path.join(root, name)
  #             if BLACKLIST in input:
  #                 continue
  #             print(input)
              compressed = input.replace(DATAFOLDER, DATAFOLDER_TKO).replace('.vtp','.tko')
              restored = input.replace(DATAFOLDER, DATAFOLDER_RESTORED)
              
              if not os.path.exists(os.path.dirname(compressed)):
                  os.makedirs(os.path.dirname(compressed))
              if not os.path.exists(os.path.dirname(restored)):
                  os.makedirs(os.path.dirname(restored))

  #             try:
              stats = M.trakomagic(input, compressed, restored, config=None)
              originalsize.append(stats['originalsize'])
              compressedsize.append(stats['compressedsize'])
              number_of_streamlines.append(stats['number_of_streamlines'])
              c_time.append(stats['c_time'])
              d_time.append(stats['d_time'])
  #             except:
  #                 print('skipping', input)
  #                 continue
              
              print(input,'done')
          
  print('All set after',time.time()-t0,'seconds.')

  if not os.path.exists(STATSFOLDER):
      os.makedirs(STATSFOLDER)
  with open(STATSFILE, 'wb') as f:
      pickle.dump({'originalsize':originalsize,
                   'compressedsize':compressedsize,
                   'number_of_streamlines':number_of_streamlines,
                   'c_time':c_time,
                   'd_time':d_time}, f)


if __name__ == "__main__":

  print('running', sys.argv[1])
  run(sys.argv[1])
  print('all done. <3')
