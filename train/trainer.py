# cluster similarity binary decision tree (probabilities), do bayesian stuff to
# get prob based on previous probs. compares the similarity of two clusters
# given the rest of the dataset being trained. Outputs to pickled.

# create some sort of hash thing to compare clusters. Similar enough clusters
# have the same hash and can be added to a node with similar clusters.

# because the data is sequential, each step down the tree is a step to the next
# cluster

import os, pickle
from collections import defaultdict
from config import config

SIMILARITY_THRESH = .8 # huh

SPATIAL_MULTIPLIER = .8
LENGTH_MULTIPLIER = .2

class TreeNode():
  """
  Decision tree node that stores a cluster of letters (and other similar
  clusters based on a threshold), and P(kitty) based on traversal to this node.
  """
  def __init__(self, cluster, val):
    self.clusters = [cluster] # clusters with the same hash
    self.children = [] # child nodes, i.e. next in sequences
    self.num_true = 1 if val else 0 # 1 if cluster is kitty


  def __str__(self):
    str_list = []
    for k in self.children:
      str_list.append("[%s]" % k)

    return "[%s, %s]" % (self.clusters, ''.join(str_list)) # make print better


  def get_cluster_similarity(self, cluster):
    """
    is cluster similar enough to known_clusters?
    """
    # note a massive amount of information loss by converting to sets:
    # lose all key repeat data, should probably compare number of repeated elems

    # short_circuit if no clusters
    if not len(self.clusters):
      return 1

    num_similar = [] # init to max
    num_elems = 0

    for k in self.clusters:
      num_similar.append(length(set(cluster) & set(k)))
      num_elems += len(k)

    # gets keyboard position similarity
    key_similarity = sum(num_similar) / len(num_similar)
    key_similarity_normalized = key_similarity / len(cluster)

    # need to take into account the number of elements
    avg_num_elem_in_known = num_elems / len(self.clusters)
    num_similarity = abs(len(cluster) - avg_num_elem_in_known)
    num_similarity_normalized = num_similarity / len(cluster)

    # this probably doesn't work
    return (key_similarity_normalized * SPATIAL_MULTIPLIER +
            num_similarity_normalized * LENGTH_MULTIPLIER)

  # tree methods
  def addChildCluster(self, c_cluster, c_val):
    child_c_best_sim = 0
    child_c_best = None
    for c in self.children:
      c_sim = c.get_cluster_similarity(c_cluster)
      if c_sim > child_c_best_sim:
        child_c_best_sim = c_sim
        child_c_best = c

    if child_c_best_sim > SIMILARITY_THRESH: # add cluster to existing child
      child_c_best.addCluster(c_cluster, c_val)
    else: #add new child
      self.children.append(TreeNode(c_cluster, c_val))

    return child_c_best if child_c_best else self.children[-1]

  def numClustersInNode(self):
    return len(self.clusters)

  def getChildren(self):
    return self.children

  # current node methods
  def addCluster(self, c_cluster, c_val):
    self.clusters.append(cluster)
    self.num_true += int(c_val)
    # do bayesian calc, combination, average, or similar thing to add prob to
    # self.p

  def getProb(self):
    return self.num_true / self.numClustersInNode()


class Trainer:
  """
  Trains a model based on a set of observations.
  """

  def __init__(self, input_folder, output_file):
    self.input_folder = input_folder
    self.output_file = output_file
    self.decision_tree = None

  def train_tree(self, model, val):
    cur_node = self.decision_tree

    for cluster in model:
      # set cur_node to the added child in the tree
      cur_node = cur_node.addChildCluster(cluster, val)

  def train(self):
    self.decision_tree = TreeNode(None, None)

    cur_type = None
    cur_model = None
    kitten_type = config("type_kitten")

    files = [f for f in os.listdir(self.input_folder)]
    for filename in files:
      fullpath = os.path.join(self.input_folder, filename)
      with open(fullpath, 'rb') as f:
        cur_type = pickle.load(f) == kitten_type
        cur_model = pickle.load(f)

      self.train_tree(cur_model, cur_type)

    print self.decision_tree

