import numpy as np
from qibo.models import Circuit
from qibo import gates
from qibo.config import raise_error
from qibo.models.circuit import Circuit
import math

nqubits=7
circuit = Circuit(nqubits)
for q1 in range(nqubits):
    circuit.add(gates.H(q1))
    for q2 in range(q1 + 1, nqubits):
        theta = math.pi / 2 ** (q2 - q1)
        circuit.add(gates.CU1(q2, q1, theta))

for i in range(nqubits // 2):
    circuit.add(gates.SWAP(i, nqubits - i - 1))

print(circuit.draw())