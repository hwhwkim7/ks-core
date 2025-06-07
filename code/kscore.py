import time
import queue

def run(G1, map, k, s, getNbrMap):
    results = {}

    # ===== Initial setup =====
    i_time = time.time()
    CS = {}
    VQ = queue.Queue()
    VQ1 = set()
    init_time = time.time() - i_time
    results['init_time'] = init_time

    # ===== First iteration: compute initial neighbor counts and enqueue under-threshold nodes =====
    f_time = time.time()
    f_n_time = 0
    for node in G1.nodes:
        n_time = time.time()
        nb = getNbrMap(G1, map, node, s)
        f_n_time += time.time() - n_time
        CS[node] = len(nb)
        if CS[node] < k:
            VQ.put(node)
            VQ1.add(node)
    frist_time = time.time() - f_time
    results['first_phase_total_time'] = frist_time
    results['first_phase_neighbour_time'] = f_n_time

    # ===== Second iteration: peeling process =====
    s_time = time.time()
    s_n_time = 0
    s_in_time = 0
    while_count = 0
    while not VQ.empty():
        while_count += 1
        v = VQ.get()
        VQ1.remove(v)
        n_time = time.time()
        nb = getNbrMap(G1, map, v, s)
        s_n_time += time.time() - n_time
        G1.del_node(v)
        del CS[v]
        inn_time = time.time()
        for w in nb:
            if w not in VQ1:
                CS[w] -= 1
                if CS[w] < k:
                    VQ.put(w)
                    VQ1.add(w)
        inner_time = time.time() - inn_time
        s_in_time += inner_time
    second_time = time.time() - s_time
    results['second_phase_total_time'] = second_time
    results['second_phase_neighbour_time'] = s_n_time
    results['second_phase_update_time'] = s_in_time
    results['num_peeling_iterations'] = while_count
    return G1, results