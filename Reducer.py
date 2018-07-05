#!/usr/bin/python

# A boolean circuit reducer

import math
import random
from pprint import pprint

class Reducer:

    def __init__(self, circuit):
        self.circuit = circuit
        self.file = open('/home/mitchell/Documents/syrup/syrup/simp/input.cnf','w+')
        self.variables = len(circuit)
        self.clauses = 0
        self.gates = self.countGates(circuit)
        self.inputs = self.variables - self.gates

    # Write the CNF of the circuit into a file
    def writeCNF(self, file):
        file.write('p cnf {} {}\n'.format(self.variables, self.clauses))
        self.gateCNF()
        file.write('{} 0'.format(self.variables))
        file.close()

    # CNF reduction
    def gateCNF(self):
        for x in self.circuit[self.inputs:]:
            if x.type == 'AND':
                self.andCNF(x)
            elif x.type == 'OR':
                self.orCNF(x)
            elif x.type == 'NOT':
                self.notCNF(x)

    # CNF reduction of an AND gate
    def andCNF(self, gate):
        if len(gate.inputs) == 1:
            inOne = int(gate.inputs[0][1:]) + 1
            inTwo = inOne
        else:
            inOne = int(gate.inputs[0][1:]) + 1
            inTwo = int(gate.inputs[1][1:]) + 1
        out = int(gate.output[1:]) + 1
        self.file.write('{} {} 0\n'.format(-out, inOne))
        self.file.write('{} {} 0\n'.format(-out, inTwo))
        self.file.write('{} {} {} 0\n'.format(-inOne, -inTwo, out))

    # CNF reduction of an OR gate
    def orCNF(self, gate):
        if len(gate.inputs) == 1:
            inOne = int(gate.inputs[0][1:]) + 1
            inTwo = inOne
        else:
            inOne = int(gate.inputs[0][1:]) + 1
            inTwo = int(gate.inputs[1][1:]) + 1
        out = int(gate.output[1:]) + 1
        self.file.write('{} {} {} 0\n'.format(-out, inOne, inTwo))
        self.file.write('{} {} 0\n'.format(-inOne, out))
        self.file.write('{} {} 0\n'.format(-inTwo, out))

    # CNF reduction of a NOT gate
    def notCNF(self, gate):
        inOne = int(gate.inputs[0][1:]) + 1
        out = int(gate.output[1:]) + 1
        self.file.write('{} {} 0\n'.format(-out, -inOne))
        self.file.write('{} {} 0\n'.format(out, inOne))

    def countGates(self, circuit):
        inputs = 0
        for x in circuit:
            if x.type == 'INPUT':
                inputs += 1
            elif x.type == 'AND' or x.type == 'OR':
                # AND and OR gates make up 3 clauses each
                self.clauses += 3
            elif x.type == 'NOT':
                # A NOT gate is made of 2 clauses
                self.clauses += 2
        # Add 1 for output of final gate
        self.clauses += 1
        gates = len(circuit) - inputs
        return gates
    