# When User Engagement Meets Structural Cohesiveness: A Decay-Driven Approach to Hypergraph Cores

This repository provides a complete implementation of a novel cohesive subgraph discovery model named $(k, s)$-core for hypergraphs.

The proposed model emphasises both structural cohesiveness and interaction strength, offering robustness against noisy, oversized hyperedges using a decay-based approach.

## Problem Overview

Traditional cohesive substructure discovery in hypergraphs often suffers from the influence of large, noisy hyperedges. Existing models such as nbr-$k$-core and $(k, g)$-core lack the flexibility to penalize weak co-occurrences.

To address this, the $(k, s)$-core model introduces:
	•	DCS (Decay-based Closeness Score): Quantifies interaction strength between nodes by penalizing large hyperedges.
	•	Strong Neighbors: Only neighbors with cumulative DCS $≥ s$ are considered.
	•	$(k, s)$-core: The maximal node set where each node has at least k strong neighbors.

## Code Structure
```
.
├── main.py            # Main
├── func.py            # Core utilities for hypergraph, DCS, and statistics
├── kscore.py          # Peeling algorithm to extract (k, s)-core
├── datasets/          # Directory for input .hyp hypergraph files
├── output.csv         # Output log (created after running)
```

## How to Run

### Requirements
- Python 3.8+
- pandas, psutil

### Example Usage
```
python main.py --network real/congress --k 6 --s 0.6 --method sum --output_path output.csv
```

### Arguments
| Parameter      | Description                                       |
|----------------|---------------------------------------------------|
| `--network`    | Relative path to dataset inside `datasets/`       |
| `--k`          | a neighbour threshold       |
| `--s`          | a decayed co-strength threshold             |
| `--c`          | a decaying factor      |
| `--method`     | DCS aggregation method: `sum`, `avg`, or `max`    |
| `--output_path`| Output file to store experiment results           |

### Datasets
- Housebills
- Congress
- [Instacart](https://www.cs.cornell.edu/~arb/data/uchoice-Instacart/)
- Gowalla
- [Amazon](https://www.cs.cornell.edu/~arb/data/amazon-reviews/)
- [Aminer](https://www.github.com/toggled/vldbsubmission)
**Note**: The Instacart, Amazon, and AMiner datasets are not uploaded due to file size limits. Please refer to the link above for access.

