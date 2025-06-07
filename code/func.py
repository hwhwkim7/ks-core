# ===== Node class: represents a single node in the hypergraph =====
class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.NodeCnt = 0
        self.EdgeCnt = 0
        self.Edge = set()

# ===== Hypergraph class: represents the overall hypergraph structure =====
class Hypergraph:
    def __init__(self):
        self.nodes = {}
        self.hyperedges = {}

    def load_from_file(self, file_path):
        """Loads hyperedges from file (comma or space separated)"""
        with open(file_path, 'r') as file:
            for line in file:
                if ',' in line:
                    current_nodes = {int(node.strip()) for node in line.strip().split(',')}
                else:
                    current_nodes = {int(node.strip()) for node in line.strip().split(' ')}

                self.add_hyperedge(current_nodes)

    def add_hyperedge(self, edge_nodes):
        """Adds a new hyperedge and updates node-hyperedge relations"""
        hyperedge_id = len(self.hyperedges) + 1
        self.hyperedges[hyperedge_id] = edge_nodes

        for node in edge_nodes:
            if node not in self.nodes:
                self.nodes[node] = Node(node)
            self.nodes[node].Edge.add(hyperedge_id)

    def del_node(self, node):
        """Deletes a node from the hypergraph and updates all connected hyperedges"""
        if node in self.nodes:
            for hyperedge in self.nodes[node].Edge:
                self.hyperedges[hyperedge].remove(node)
            del self.nodes[node]

    def del_edge(self, edge):
        """Deletes a hyperedge from the hypergraph"""
        if edge in self.hyperedges:
            for node in self.hyperedges[edge]:
                self.nodes[node].Edge.remove(edge)
            del self.hyperedges[edge]

# ===== Strength map generation =====
def get_map(G, c):
    """Assigns decayed-based weight to each hyperedge: 1 / |e|^c"""
    map = {}
    for id, edge_set in G.hyperedges.items():
        map[id] = 1/(len(edge_set))**c
    return map

# ===== Neighbor map methods =====
def getNbrMap_sum(G1, map, node, s):
    """Compute strong neighbors of a node using summation of DCS values."""
    cnt = {}
    for hyperedge in G1.nodes[node].Edge:
        for neighbor in G1.hyperedges[hyperedge]:
            if neighbor != node:
                if neighbor not in cnt:
                    cnt[neighbor] = 0
                cnt[neighbor] += map[hyperedge]
    ng = {node: count for node, count in cnt.items() if count >= s}
    return ng

def getNbrMap_avg(G1, map, node, s):
    """Compute strong neighbors of a node using average DCS values."""
    cnt = {}
    ccc = {}
    for hyperedge in G1.nodes[node].Edge:
        for neighbor in G1.hyperedges[hyperedge]:
            if neighbor != node:
                if neighbor not in cnt:
                    cnt[neighbor] = 0
                    ccc[neighbor] = 0
                cnt[neighbor] += map[hyperedge]
                ccc[neighbor] += 1
    ng = {node: cnt[node] / ccc[node] for node in cnt if ccc[node] > 0 and cnt[node] / ccc[node] >= s}
    return ng

def getNbrMap_max(G1, map, node, s):
    """Compute strong neighbors of a node using maximum DCS values."""
    cnt = {}
    for hyperedge in G1.nodes[node].Edge:
        for neighbor in G1.hyperedges[hyperedge]:
            if neighbor != node:
                if neighbor not in cnt:
                    cnt[neighbor] = 0
                if cnt[neighbor] < map[hyperedge]:
                    cnt[neighbor] = map[hyperedge]
    ng = {node: count for node, count in cnt.items() if count >= s}
    return ng

# ===== Statistics and metrics =====
def get_avg_DCS(G, map, getNbrMap, s):
    """Computes the average DCS among all strong neighbors in the graph"""
    num_node = len(G.nodes)
    if num_node == 0: return 0.0
    DCS_list = []
    for node in G.nodes:
        ng = getNbrMap(G, map, node, s)
        DCS_list.extend(ng.values())
    if len(DCS_list) == 0: return 0.0
    return sum(DCS_list) / len(DCS_list)

def get_num_hyperedges(G):
    """Counts the number of hyperedges with size ≥ 2"""
    count = 0
    for edge_nodes in G.hyperedges.values():
        if len(edge_nodes) >= 2:
            count += 1
    return count

def get_avg_cardinality(G):
    """Computes the average cardinality of hyperedges with size ≥ 2"""
    num_edge = 0
    sum_card = 0
    for edge in G.hyperedges.values():
        if len(edge) >= 2:
            sum_card += len(edge)
            num_edge += 1
    if num_edge == 0: return 0.0
    return sum_card / num_edge

def get_avg_degree(G):
    """Computes the average degree of all nodes (edges of size ≥ 2 only)"""
    num_node = len(G.nodes)
    if num_node == 0: return 0.0
    sum_deg = 0
    for node in G.nodes.values():
        for edge in node.Edge:
            if len(G.hyperedges[edge]) >= 2:
                sum_deg += 1
    return sum_deg / num_node