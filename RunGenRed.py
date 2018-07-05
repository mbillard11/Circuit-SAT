#!/usr/bin/python

# Run the Generator and Reducer
# The max values are currently set arbitrarily, will be experimented with later

import Generator
import Reducer
import math
import random
from pprint import pprint
import shutil
from subprocess import *


def main():

    inMax = 10
    gateMax = 1000
    depthMax = 500
    faninMax = 2

    # n
    numIn = inMax
    #numIn = random.randint(1, inMax)

    # m
    numGates = gateMax
    #numGates = random.randint(1, gateMax)

    # d
    numDepth = depthMax
    #numDepth = random.randint(2,depthMax)


    # Initalize a generator
    gen = Generator.Generator(numIn, numGates, faninMax, numDepth)
    gen.outputList()
    # Generate a circuit
    gen.generateCircuit()

    # Initalize a reducer using the circuit that was just generated
    red = Reducer.Reducer(gen.circuit)
    # Write the reduction into a file
    red.writeCNF(red.file)

    print('Success with {} inputs!'.format(red.inputs))

    # Copy the file to the input file location of the SAT solver
    # This will vary depending on file architecture
    #shutil.copy('/home/mitchell/Desktop/Spring 2018/Comp6902/circuitCNF.txt', '/home/mitchell/Documents/syrup/syrup/simp/input.cnf')

    solver()


def solver():

    Popen("make", cwd="/./home/mitchell/Documents/syrup/syrup/simp", shell = True)
    Popen("./glucose input.cnf output.cnf", cwd="/./home/mitchell/Documents/syrup/syrup/simp", shell = True)

if __name__ == '__main__':
    main()