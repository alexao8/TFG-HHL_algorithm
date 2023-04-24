import numpy as np
from qibo.models import Circuit
from qibo import gates
from qibo.config import raise_error
from qibo.models.circuit import Circuit
import math


def myQFT(nqubits):
    circuit = Circuit(nqubits)
    for q1 in range(nqubits):
        circuit.add(gates.H(q1))
        for q2 in range(q1 + 1, nqubits):
            theta = math.pi / 2 ** (q2 - q1)
            circuit.add(gates.CU1(q2, q1, theta))

    for i in range(nqubits // 2):
        circuit.add(gates.SWAP(i, nqubits - i - 1))

    return circuit

def QPE(mqubits, operator, eigenvector):
    circuit = Circuit(mqubits+len(eigenvector))

    for ev in range(len(eigenvector)):
        if eigenvector[ev] == 1: circuit.add(gates.X(mqubits+ev))

    for q in range(mqubits):
        circuit.add(gates.H(q))
        circuit.add(operator(*range(0+mqubits, len(eigenvector)+mqubits)).controlled_by(q))

    qft = myQFT(mqubits)
    iqft = qft.invert()
    circuit.add(iqft.on_qubits(*range(0, mqubits)))

    return circuit

def main():
    print(3)
    qpe = QPE(3,gates.T, [1])
    print(qpe.draw())

if __name__ == "__main__":
    main()