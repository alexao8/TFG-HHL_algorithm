import numpy as np
import scipy
import qibo
from qibo.models import Circuit
from qibo.models import QFT
from qibo import gates
from qibo.config import raise_error
from qibo.models.circuit import Circuit
import qibo.backends
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

def QPE1(mqubits, operator, eigenvector):
    circuit = Circuit(mqubits+len(eigenvector))

    #The H gates are added to the firsts mqubits and the eigenvector is translated as a circuit
    for q in range(0,mqubits+len(eigenvector)):
        if q < mqubits: circuit.add(gates.H(q))
        elif eigenvector[q-mqubits] == 1: circuit.add(gates.X(q))

    #The U gates are set
    reps = 2**(mqubits-1)
    for q in range(mqubits):
        for i in range(reps):
            circuit.add(operator(*range(0+mqubits, len(eigenvector)+mqubits)).controlled_by(q))
        reps //= 2

     #Apply the IQFT
    qft = myQFT(mqubits)
    iqft = qft.invert()
    circuit.add(iqft.on_qubits(*range(0, mqubits)))

    return circuit


def QPE(mqubits, circuit, matrix = None, operator = None):
    qpe = Circuit(mqubits+circuit.nqubits)

    #The H gates are added to the firsts mqubits
    for q in range(0,mqubits):
        if q < mqubits: qpe.add(gates.H(q))                  
    
    #The circuit that gives the state that will be the input of the QPE is attached to the whole QPE circuit
    qpe.add(circuit.on_qubits(*range(mqubits,mqubits+circuit.nqubits)))

    #The U gates are set
    if (matrix is None):
      reps = 2**(mqubits-1)
      for q in range(mqubits):
          for i in range(reps):
              qpe.add(operator(*range(mqubits, circuit.nqubits+mqubits)).controlled_by(q))
          reps //= 2
    
    else:
      reps = 2**(mqubits-1)
      for q in range(mqubits):
          for i in range(reps):
              qpe.add(gates.Unitary(matrix,*range(mqubits, circuit.nqubits+mqubits)).controlled_by(q))
          reps //= 2


    #Apply the IQFT
    qft = QFT(mqubits)
    iqft = qft.invert()
    qpe.add(iqft.on_qubits(*range(0, mqubits)))

    return qpe


def transform_to_hamiltonian(matrix, t):
    # Step 1: Diagonalize A
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)

    # Step 2: Construct the diagonal matrix
    D = np.diag(eigenvalues)

    # Step 3: Construct the transformation matrix
    U = eigenvectors

    # Step 4: Express A as the sum of outer products
    A_decomposed = U @ D @ np.conjugate(U).T

    # Step 5: Exponential of A
    expD = np.exp(1j * D * t)

    for i in range(len(expD)):
      for j in range(len(expD)):
        if D[i][j] == 0: expD[i][j] = 0
    
    print(expD)
    # Step 6: Construct the Hamiltonian operator
    H = U @ expD @ np.conjugate(U).T
    return  H


def HHL(b_circuit, A, l, C):
    N = len(A)
    U = transform_to_hamiltonian(A,(3*np.pi/4))
    Uinv = np.linalg.inv(U)

    qpe = QPE(l, b_circuit, U)

    hhl = Circuit(qpe.nqubits+1)
    hhl.add(qpe.on_qubits(*range(1,hhl.nqubits)))

    theta = [math.pi, math.pi/3]
    for q in range(l):
        hhl.add(gates.CRY(q+1,0,theta[q]))
    
    c = Circuit(1)

    iqpe = (QPE(l, c, U)).invert()
    hhl.add(iqpe.on_qubits(*range(1,hhl.nqubits)))

    return hhl

def main():
    A = np.array([[1, (-1/3)],
                [(-1/3), 1]])
    b = Circuit(1)
    b.add(gates.X(0))
    hhl = HHL(b, A, 2, 1)
    hhl.add(gates.M(0))
    hhl.add(gates.M(3))
    simulated_final_state = hhl(nshots=1000)

    print(hhl.draw())
    print(simulated_final_state)
    probabilities = simulated_final_state.probabilities
    print(probabilities(qubits=[3,0]))
    #print(result.frequencies(binary=True, registers=False))
    #probabilities = result.state
    #print(probabilities)

if __name__ == "__main__":
    main()