# may require Scipy: http://fonnesbeck.github.com/ScipySuperpack/ for Mac 10.8

import os, time, sys, json, pickle
from config import config
from collections import deque
import Tkinter as tk

from scipy.cluster.vq import kmeans, vq, whiten

MAX_SEP_THRESH = config("min_key_cluster_separation_threshold_sec")

class Clusterer:
  """
  Clusters the raw keystroke records by max separation threshold clustering
  """
  def __init__(self, raw):
    self.raw_sequence = raw
    self.clustered_sequence = [[]]

  def strip_times(self, c):
    stripped_clusters = []

    for cluster in c:
      stripped_clusters.append([])
      for elem in cluster:
        stripped_clusters[-1].append(elem[1])
    return stripped_clusters

  def cluster(self):

    cur_t = self.raw_sequence[0][0] # init cur_t to first recorded time

    for elem in self.raw_sequence:
      if elem[0] - cur_t < MAX_SEP_THRESH:
        self.clustered_sequence[-1].append(elem)
      else:
        self.clustered_sequence.append([elem])
      cur_t = elem[0]

    return self.strip_times(self.clustered_sequence)


class Recorder:
  """
  Uses Tkinter window to listen to and record keystrokes
  """
  def __init__(self, filename):
    self.filename = filename
    self.root = None
    self.raw_sequence = deque()

  def key(self, event):
    if event.keysym == 'Escape':
      self.root.destroy()
      return
    self.raw_sequence.append([time.time(), event.char])

  def start(self):
    self.root = tk.Tk()
    print "Please focus the GUI and place a cat on the keyboard (esc to exit):"
    self.root.bind_all('<Key>', self.key)
    self.root.mainloop()

    c = Clusterer(self.raw_sequence)
    clusters = c.cluster()

    output = open(self.filename, 'wb')
    pickle.dump(clusters, output, -1)
    output.close()

    return clusters

