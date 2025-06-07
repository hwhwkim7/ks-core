# When User Engagement Meets Structural Cohesiveness: A Decay-Driven Approach to Hypergraph Cores
*Under submission to CIKM 2025*
  
This repository provides a complete implementation of a novel cohesive subgraph discovery model named $(k, s)$-core for hypergraphs.

The proposed model emphasises both structural cohesiveness and interaction strength, offering robustness against noisy, oversized hyperedges using a decay-based approach.

## Code Structure
```
.
├── code/
│   ├── main.py       # Entry point for the program
│   ├── func.py       # Core utilities for hypergraph processing, DCS computation, and statistics
│   └── kscore.py     # Peeling algorithm implementation for (k, s)-core extraction
├── datasets/         # Directory containing input .hyp hypergraph files
└── output.csv        # Output log file generated after execution
```

## How to Run

### Requirements
- Python 3.8+
```
pip install pandas psutil
```

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
| `--method`     | $DCS$ aggregation method: `sum`, `avg`, or `max`    |
| `--output_path`| Output file to store experiment results           |

### Datasets
- Housebills
- Congress
- [Instacart](https://www.cs.cornell.edu/~arb/data/uchoice-Instacart/)
- Gowalla
- [Amazon](https://www.cs.cornell.edu/~arb/data/amazon-reviews/)
- [Aminer](https://www.github.com/toggled/vldbsubmission)

*Note*: The Instacart, Amazon, and AMiner datasets are not uploaded due to file size limits. Please refer to the link above for access.

