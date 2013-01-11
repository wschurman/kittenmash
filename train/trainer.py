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

SIMILARITY_THRESH = 10 # huh

def get_cluster_hash(cluster):
  """
  cluster is a list of letters, need to do comparison
  """
  return 1

class TreeNode():
  """
  Decision tree node that stores a cluster of letters (and other similar
  clusters based on a threshold), and P(kitty) based on traversal to this node.
  """
  def __init__(self, cluster, val):
    self.clusters = [cluster] # clusters with the same hash
    self.children = {} # child nodes, i.e. next in sequences
    self.num_true = 1 if val else 0 # 1 if cluster is kitty

  def __str__(self):
    str_list = []
    for k in self.children:
      str_list.append("[%s, %s]" % (k, str(self.children[k])))

    return "[%s, %s]" % (self.clusters, ''.join(str_list)) # make print better

  # tree methods
  def addChildCluster(self, c_cluster, c_val):
    c_hash = get_cluster_hash(c_cluster)

    if c_hash in self.children:
      self.children[c_hash].addCluster(c_cluster, c_val)
    else:
      self.children[c_hash] = TreeNode(c_cluster, c_val)

    return self.children[c_hash]

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

