#!/usr/bin/python

# A boolean circuit generator
# This program has many parameters that can be experimented with and changed

import math
import random
from pprint import pprint

class Generator:

    def __init__(self, numIn, numGates, fanin, depth):
        self.numIn = numIn
        self.numGates = numGates
        self.fanin = fanin
        self.depth = depth
        self.circuit = []
        self.outputs = []
        # -1 to allow for output gate zm
        self.gatesPerLayer = (self.numGates) // (self.depth - 1)
        self.gatesLastLayer = (self.numGates - 1) % (self.gatesPerLayer)

    # Make a list of all the possible outputs
    def outputList(self):
        for x in range(self.numIn + self.numGates):
            self.outputs.append('z'+str(x))
        return self.outputs

    # Generate a random boolean circuit
    def generateCircuit(self):
        # Add all the input gates
        for x in range(self.numIn):
            gate = Gate(0, x, 'INPUT', 1, None, self.outputs[x])
            self.circuit.append(gate)
        # Generate each layer of the circuit
        for x in range(1, self.depth - 1):
            self.generateLayer(x)
        # Generate the last layer
        self.generateLastLayer()
        # Generate the final output gate
        self.circuit.append(self.randOutGate())
        # Write the generated circuit to a file
        file = open('circuit.txt','w+')
        for y in self.circuit:
            file.write(str(vars(y))+'\n')
        file.close()

    def generateLayer(self, layer):
        for x in range(self.gatesPerLayer):
            gate = self.randGate(layer, x)
            self.circuit.append(gate)

    # Last layer has its own function due to potentially having a different 
    # number of gates from the other layers
    def generateLastLayer(self):
        if self.gatesLastLayer == 0:
            self.gatesLastLayer = self.gatesPerLayer
        for x in range(self.gatesLastLayer):
            gate = self.randGate(self.depth-1, x)
            self.circuit.append(gate)

    # Generate a random gate
    def randGate(self, layer, num):
        gateType = random.choice(['AND','OR','NOT'])
        gate = Gate(layer, num, gateType, None, None, None)
        gate.fanin = self.randFanin(gate.type)
        gate.inputs = self.randInputs(gate.layer, gate.fanin)
        gate.output = self.outputs[self.numIn+(self.gatesPerLayer*(layer-1))+num]
        return gate

    # Generate a random gate for the final output
    def randOutGate(self):
        gateType = random.choice(['AND','OR','NOT'])
        gate = Gate(self.depth, 0, gateType, None, None, None)
        gate.fanin = self.randFanin(gate.type)
        gate.inputs = self.randInputs(gate.layer, gate.fanin)
        gate.output = self.outputs[len(self.outputs)-1]
        return gate

    # A function for setting max fanin
    def randFanin(self, type):
        # Options for increaseing fanin has been disabled until future experimentation
        fanMax = min(self.fanin, self.gatesPerLayer)
        if type == 'NOT':
            #fanin = random.randint(1,fanMax)
            fanin = 1
        else:
            #fanin = random.randint(2,fanMax)
            fanin = 2
        return fanin

    # Randomly pick inputs from the previous layer
    def randInputs(self, layer, fanin):
        inputs = []
        # First layer uses circuit inputs
        if layer == 1:
            choices = self.outputs[:self.numIn]
        # Layer at max depth (i.e. output gate) uses inputs from last "real" layer
        elif layer == self.depth:
            choices = self.outputs[self.numIn + self.gatesPerLayer*(layer-2):self.numIn + self.gatesPerLayer*(layer-2)+ self.gatesLastLayer]
        else:
            choices = self.outputs[self.numIn + self.gatesPerLayer*(layer-2):self.numIn + self.gatesPerLayer*(layer-1)]
        for x in range(fanin):
            if len(choices) == 0:
                break
            else:
                choice = random.choice(choices)
                choices.remove(choice)
                inputs.append(choice)
        return inputs


class Gate:

    def __init__(self, layer, num, type, fanin, inputs, output):
        self.layer = layer
        self.num = num
        self.type = type
        self.fanin = fanin
        self.inputs = inputs 
        self.output = output