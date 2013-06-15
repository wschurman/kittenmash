# cluster similarity binary decision tree (probabilities), do bayesian stuff to
# get prob based on previous probs. compares the similarity of two clusters
# given the rest of the dataset being trained. Outputs to pickled.

# create some sort of hash thing to compare clusters. Similar enough clusters
# have the same hash and can be added to a node with similar clusters.

# because the data is sequential, each step down the tree is a step to the next
# cluster

import os
import pickle
from config import config
from collections import deque

SIMILARITY_THRESH = .5  # huh

SPATIAL_MULTIPLIER = .8
LENGTH_MULTIPLIER = .2


class TreeNode():
    """
    Decision tree node that stores a cluster of letters (and other similar
    clusters based on a threshold), and P(kitty) based on traversal to this node.
    """
    def __init__(self, cluster, val):
        self.clusters = [cluster]  # clusters with the same hash
        self.children = []  # child nodes, i.e. next in sequences
        self.num_true = 1 if val else 0  # 1 if cluster is kitty

    def __str__(self):
        child_list = []
        for k in self.children:
            child_list.append("(%s)" % k)

        return "\t%d[%s, %s]" % (self.numClustersInNode(), self.clusters, ''.join(child_list))  # make print better

    def to_list(self):
        child_list = []
        for k in self.children:
            child_list.append(k.to_list())

        return [self.clusters, child_list]

    def get_cluster_similarity(self, cluster):
        """
        Returns number between 0 and 1 indicating cluster
        similarity between cluster and clusters already in this node.
        """
        # note a massive amount of information loss by converting to sets:
        # lose all key repeat data, should probably compare number of repeated elems

        # short_circuit if no clusters
        if not len(self.clusters):
            return 1

        num_similar = []  # init to max
        num_elems = 0

        for k in self.clusters:
            num_similar.append(len(set(cluster) & set(k)))
            num_elems += len(k)

        # gets keyboard position similarity
        key_similarity = sum(num_similar) / len(num_similar)
        key_similarity_normalized = key_similarity / len(set(cluster))

        # need to take into account the number of elements
        avg_num_elem_in_known = num_elems / len(self.clusters)
        num_similarity = abs(len(cluster) - avg_num_elem_in_known)
        num_similarity_normalized = num_similarity / len(cluster)

        print "KS: ", key_similarity_normalized
        print "NS: ", num_similarity_normalized

        # this probably doesn't work
        return (key_similarity_normalized * SPATIAL_MULTIPLIER +
                num_similarity_normalized * LENGTH_MULTIPLIER)

    # tree methods
    def addChildCluster(self, c_cluster, c_val):
        print "Adding child cluster"
        print c_cluster

        child_c_best_sim = -1
        child_c_best = None
        for c in self.children:
            print "checking against:"
            print c
            c_sim = c.get_cluster_similarity(c_cluster)
            print "Sim:", c_sim
            if c_sim > child_c_best_sim:
                child_c_best_sim = c_sim
                child_c_best = c

        # if new cluster is similar enough to existing child,
        # add cluster to that child
        if child_c_best_sim > SIMILARITY_THRESH:
            child_c_best.addCluster(c_cluster, c_val)
        else:  # else, add a new child
            self.children.append(TreeNode(c_cluster, c_val))
            child_c_best = None

        # return child cluster that it was appended to
        return child_c_best if child_c_best else self.children[-1]

    def numClustersInNode(self):
        return len(self.clusters)

    def getChildren(self):
        return self.children

    # current node methods
    def addCluster(self, c_cluster, c_val):
        self.clusters.append(c_cluster)
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

        for cluster in model:  # for each cluster in the current model
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

        self.print_tree()

        output = open('pickled_out', 'wb')
        pickle.dump(self.decision_tree.to_list(), output, -1)
        output.close()

    def print_tree(self):
        s = ''
        print_queue = deque()
        cur_level = 0

        print_queue.append([0, self.decision_tree])

        while len(print_queue) > 0:
            [level, node] = print_queue.popleft()

            if not level == cur_level:
                s += "\n"
                cur_level = level
            s += str(node.clusters)

            for child in node.getChildren():
                print_queue.append([level + 1, child])

        print s
