from math import exp, log
from sys import exit

class Node:
    def __init__(self, t, nu=None, nd=None):
        self.nu: Node = nu # "up" node
        self.nd: Node = nd # "down" node
        self.t: int = t # t=0, t=1, etc.
        self.zero_quotes = list()
    
    # Setters
    def set_nu(self, nu):
        self.nu = nu
    
    def set_nd(self, nd):
        self.nd = nd

    def set_zero_rate(self, i, r):
        if i < 1:
            exit("i=%d < 1" % i)

        self.zero_quotes.insert(i-1, [r, exp(-r * i)])

    def set_zero_price(self, i, d):
        if i < 1:
            exit("i=%d < 1" % i)
        
        self.zero_quotes.insert(i-1, [-log(d) / i, d])

    # Getters
    def get_nu(self):
        return self.nu

    def get_nd(self):
        return self.nd

    def get_t(self):
        return self.t

    def get_zero_rate(self, i):
        if i < 1:
            exit("i=%d < 1" % i)
        elif i > len(self.zero_quotes):
            exit("i=%d > len" % i)

        return self.zero_quotes[i-1][0]
    
    def get_zero_rates(self):
        return [r for [r, _] in self.zero_quotes]

    def get_zero_price(self, i):
        if i < 1:
            exit("i=%d < 1" % i)
        elif i > len(self.zero_quotes):
            exit("i=%d > len" % i)

        return self.zero_quotes[i-1][1]

    def get_zero_prices(self):
        return [d for [_, d] in self.zero_quotes]

    def get_zero_quotes(self):
        return self.zero_quotes

    def get_zero_deltas(self):
        return [i * self.get_zero_price(i) / 100 for i in range(1, len(self.get_zero_prices())+1)]
        
    # Checkers
    def has_nu(self):
        return self.nu is not None
    
    def has_nd(self):
        return self.nd is not None

    # Print
    def print_node_with_zero_rates(self):
        print("t=%d" % self.t)
        for i in range(0, len(self.zero_quotes)):
            print("r_{%d, %d}=%f%%" % (self.t, self.t+i+1, self.get_zero_rate(i+1) * 100))

    def print_zero_rates_as_csv(self):
        for i in range(0, len(self.zero_quotes)):
            print("%d,%f" % (i+1, self.get_zero_rate(i+1) * 100))

    def print_node_with_zero_prices(self):
        print("t=%d" % self.t)
        for i in range(0, len(self.zero_quotes)):
            print("d_{%d, %d}=%f" % (self.t, self.t+i+1, self.get_zero_price(i+1)))

    def print_zero_prices_as_csv(self):
        for i in range(0, len(self.zero_quotes)):
            print("%d,%f" % (i+1, self.get_zero_price(i+1)))
    
    def print_node_with_zero_rates_and_prices(self):
        print("t=%d" % self.t)
        for i in range(0, len(self.zero_quotes)):
            print("(r_{%d, %d}=%f%%, d_{%d, %d}=%f)" % (self.t, self.t+i+1, self.get_zero_rate(i+1) * 100, self.t, self.t+i+1, self.get_zero_price(i+1)))
    
    def print_tree(self, level=0):
        if self:
            if self.has_nu(): 
                self.get_nu().print_tree(level+1)
            
            print(' ' * 10 * level + '-> ' + "t=%d" % self.t)
            for i in range(0, len(self.zero_quotes)):
                print(' ' * 10 * level + '   ' + "(r_{%d, %d}=%f%%, d_{%d, %d}=%f)" % (self.t, self.t+i+1, self.get_zero_rate(i+1) * 100, self.t, self.t+i+1, self.get_zero_price(i+1)))

            if self.has_nd():
                self.get_nd().print_tree(level+1)
    