# TFG-HHL_algorithm
This repository contain the documentation and code of the Bachelor's thesis of Alex Aleman. This thesis studies the HHL algorithm and implements it using Qibo, an open-source python framework for programming quantum computers in a high level.

## Files in this repository

### qft.py
the `qft.py` file is the file that defines the Quantum Fourier Transform. Given a number that is the number of qubits, this file returns the circuit of the QFT when executed.


### qpe.py
the `qpe.py` file is the file that defines the Quantum Phase EStimation. Given a number that is the number of qubits, this file returns the circuit of the QPE when executed. This circuite uses the Quantum Fourier Transform. Currently if this file is executed, the output will be a circuit of 4 qubits that uses the T gate as unitary operator. This can be changed to any other operator (for one or more qubits) and other number of qubits for the circuit.

## Requirements
In order to use this repository the needed requirements to be installed are:
- `Pyhton3`
- `Qibo`

## Autor
Alexandre Alemany Orfila

[alexao8](https://github.com/alexao8)
