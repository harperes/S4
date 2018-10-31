"""
$: /usr/bin/mpirun -n 4 /home/harperes/miniconda3/bin/python3 mpi_test.py
"""
import sys
print(sys.version)
import numpy as np
import S4
from mpi4py import MPI

comm = MPI.COMM_WORLD

print(f"Hello! I am rank {comm.rank} from {comm.size} running in total...")

comm.Barrier()
