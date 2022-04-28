
from math import log, sqrt
from node import Node
import numpy as np

def replicate_node(node: Node, i: int):
        A = np.linalg.inv(np.array([[1, node.get_nu().get_zero_price(1)], 
                                    [1, node.get_nd().get_zero_price(1)]]))
        b = np.array([node.get_nu().get_zero_price(i-1), node.get_nd().get_zero_price(i-1)])
        x = np.matmul(A, b)
        y = np.array([node.get_zero_price(1), node.get_zero_price(2)])
        d = np.matmul(y, x)
        node.set_zero_price(i, d)

def replicate(node: Node, i: int, t: int):
    if node:
        if node.get_t() == t:
            replicate_node(node, i)
        else:
            if node.has_nu():
                replicate(node.get_nu(), i, t)
            if node.has_nd():
                replicate(node.get_nd(), i, t)
            replicate_node(node, i)

class Model:
    def __init__(self, depth=7, h=1, l=0.313, mu=0.027, phi=0.294388, r=0.01754, sigma=0.007397):
        self.params = dict()

        self.params["depth"] = depth
        self.params["h"] = h
        self.params["lambda"] = l
        self.params["mu"] = mu
        self.params["phi"] = phi
        self.params["r"] = r
        self.params["sigma"] = sigma

        self.STEP_SIZE = self.params["sigma"] * sqrt(-2 * log(self.params["phi"]) * self.params["h"])

    def build_model(self):
        root: Node = Node(0)
        root.set_zero_rate(1, self.params["r"])

        # h-year and 2h-year
        queue = list()
        queue.append(root)
        while len(queue) > 0:
            node: Node = queue.pop(0)
            if node.get_t() == self.params["depth"]:
                break
            
            # "up"
            node.set_nu(Node(node.get_t()+1))
            node.get_nu().set_zero_rate(1, node.get_zero_rate(1) + self.STEP_SIZE)
            queue.append(node.get_nu())

            # "down"
            node.set_nd(Node(node.get_t()+1))
            node.get_nd().set_zero_rate(1, node.get_zero_rate(1) - self.STEP_SIZE)
            queue.append(node.get_nd())

            (pu, pd) = self.calc_pu_pd(node.get_zero_rate(1))
            rp = self.params["lambda"] / 2 * sqrt(self.params["h"]) * (node.get_nd().get_zero_price(1) - node.get_nu().get_zero_price(1))
            node.set_zero_price(2, node.get_zero_price(1) * (pu * node.get_nu().get_zero_price(1) + pd * node.get_nd().get_zero_price(1) - rp))
        
        # 3h-year, 4h-year, etc. 
        if self.params["depth"] > 1:
            for i in range(3, self.params["depth"]+2):
                replicate(root, i, self.params["depth"]-i+1)

        return root

    def calc_pu_pd(self, r):
        pu = 0.5 + ((self.params["mu"] - r) * (sqrt(-self.params["h"] * log(self.params["phi"])))) / (self.params["sigma"] * sqrt(8))
        pu = 1 if pu > 1 else 0 if pu < 0 else pu
        return (pu, 1-pu)
