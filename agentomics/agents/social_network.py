import networkx as nx

class SocialNetwork :

    def __init__ (self ,households ):
        self .graph =nx .Graph ()
        self .graph .add_nodes_from (households )

    def add_connections (self ,connections ):
        self .graph .add_edges_from (connections )

    def get_neighbors (self ,household ):
        return list (self .graph .neighbors (household ))