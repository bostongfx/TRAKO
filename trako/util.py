import numpy as np
import matplotlib.pyplot as plt

class Util:

  @staticmethod
  def error(points1, points2, clusters=3):

    distances = []

    if clusters==3:

      for i,p in enumerate(points1):

        p1 = points1[i]
        p2 = points2[i]

        dist = np.linalg.norm(p1-p2)

        distances.append(dist)

    return (np.min(distances), np.max(distances), np.mean(distances), np.std(distances)), distances

  @staticmethod
  def show_surroundings(points, index, window=3):

    start = max(0, index-window)
    end = min(len(points), index+window)

    return points[start : end]


  @staticmethod
  def plot(values, xlabel='X', ylabel='Y'):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.spines['bottom'].set_color('cyan')
    ax.spines['top'].set_color('cyan')
    ax.xaxis.label.set_color('cyan')
    ax.tick_params(axis='x', colors='cyan')
    ax.spines['left'].set_color('cyan')
    ax.spines['right'].set_color('cyan')
    ax.yaxis.label.set_color('cyan')
    ax.tick_params(axis='y', colors='cyan')

    plt.show()
