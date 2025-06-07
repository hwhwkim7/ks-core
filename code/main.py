import argparse
import psutil
import os
import time
import pandas as pd

import func
import kscore

# ===== Argument parsing =====
parser = argparse.ArgumentParser(description="Peeling Algorithm for Hypergraph nbr-(k,s)-core")
parser.add_argument("--network", help="Path to the network file", default='real/congress')
parser.add_argument("--k", type=int, help="Value of k",default=6)
parser.add_argument("--s", type=float, help="Value of s",default=0.6)
parser.add_argument("--c", type=float, help="Value of c",default=1)
parser.add_argument("--method", type=str, help="closeness metric",default='sum')
parser.add_argument("--output_path", type=str, default=f'../output.csv')
args = parser.parse_args()

# ===== Measure memory usage before execution =====
process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 * 1024)

# ===== Select method of DCS =====
if args.method == 'sum':
    getNbrMap = func.getNbrMap_sum
elif args.method == 'max':
    getNbrMap = func.getNbrMap_max
elif args.method == 'avg':
    getNbrMap = func.getNbrMap_avg

# ===== Load hypergraph from file =====
network = f'../datasets/{args.network}/network.hyp'
G = func.Hypergraph()
G.load_from_file(network)

# ===== Run the (k,s)-core peeling algorithm =====
start_time = time.time()
map = func.get_map(G, args.c)
ks_G, results = kscore.run(G, map, args.k, args.s, getNbrMap)
end_time = time.time()

# ===== Measure memory usage after execution =====
memory_after = process.memory_info().rss / (1024 * 1024)
memory_usage = memory_after - memory_before

# ===== Compute additional statistics =====
dataset = args.network.split('/')[1]
avg_DCS = func.get_avg_DCS(ks_G, map, getNbrMap, args.s)

# ===== Collect experiment results into a record =====
record = {
    'dataset': dataset,
    'algorithm': 'ks',
    'method': args.method,
    'k': args.k,
    's': args.s,
    'c': args.c,
    '#node': len(ks_G.nodes),
    '#edge': func.get_num_hyperedges(ks_G),
    'avg_degree': func.get_avg_degree(ks_G),
    'avg_cardinality': func.get_avg_cardinality(ks_G),
    'avg_DCS': avg_DCS,
    'memory_usage': memory_usage,
    'total_run_time': end_time - start_time,
    'init_time': results['init_time'],
    'first_phase_total_time': results['first_phase_total_time'],
    'first_phase_neighbour_time': results['first_phase_neighbour_time'],
    'second_phase_total_time': results['second_phase_total_time'],
    'second_phase_neighbour_time': results['second_phase_neighbour_time'],
    'second_phase_update_time': results['second_phase_update_time'],
    'num_peeling_iterations': results['num_peeling_iterations'],
}

# ===== Save results to CSV (append if exists, add header if new) =====
df = pd.DataFrame([record])
file_exists = os.path.isfile(args.output_path)
df.to_csv(args.output_path, mode='a', index=False, header=not file_exists)

print(f"Results written to {args.output_path}")
