#!/usr/bin/python

# Run the Generator, Reducer, and Solver. Output results as a graph
# The n, m, and d values can be changed

import Generator
import Reducer
import math
import random
from pprint import pprint
import shutil
from subprocess import *
import matplotlib.pyplot as plt
import numpy as np


def main():

    # m
    numGates = int(input('Enter the number of gates: '))
    # d
    numDepth =  int(input('Enter the depth: '))
    # fanin
    faninMax = 2
    # Arrays for plotting graph
    nArr = []
    timeArr = []
    satAvg = 0

    # Can change range and increments of n here
    for x in range(5,1001,50):
        avgTime = 0
        satRatio = 0
        satSum = 0

        # For every n run 10 instances 
        for y in range(10):

            # n
            numIn = x

            # Initalize a generator
            gen = Generator.Generator(numIn, numGates, faninMax, numDepth)
            gen.outputList()
            # Generate a circuit
            gen.generateCircuit()
            # Initalize a reducer using the circuit that was just generated
            red = Reducer.Reducer(gen.circuit)
            # Write the reduction into a file
            red.writeCNF(red.file)
            
            sat,time = solver()
            satSum += sat
            avgTime += time
        satRatio = satSum / 10.00          
        avgTime /= 10.00
        satAvg += satRatio
        timeArr.append(avgTime)
        nArr.append(x)
        print('SAT Ratio={}'.format(satAvg))

    satAvg *= 5
    print('SAT Percent: {}%'.format(satAvg))
    plt.title('Time to Solve vs. n', fontsize = 22)

    plt.figtext(0.15,0.85,'Gates: {}'.format(numGates),bbox=dict(facecolor='blue', alpha=0.5))
    plt.figtext(0.15,0.8,'Depth: {}'.format(numDepth),bbox=dict(facecolor='blue', alpha=0.5))
    plt.figtext(0.15,0.75,'{}% SAT'.format(satAvg),bbox=dict(facecolor='blue', alpha=0.5))

    plt.plot(np.unique(nArr), np.poly1d(np.polyfit(nArr, timeArr, 2))(np.unique(nArr)))
    plt.plot(nArr,timeArr,'ro')
    plt.xlabel('n')
    plt.ylabel('Time to Solve')
    plt.show()
    

def solver():

    glucose = Popen("./glucose input.cnf output.cnf", cwd="/./home/mitchell/Documents/syrup/syrup/simp", shell = True, stdout=PIPE)
    result = glucose.communicate()

    # Get parse time from solver
    parse = result[0].find('Parse time')
    parseStart = parse + 11
    parseEnd = result[0].find('s',parseStart)
    parseTime = float(result[0][parseStart:parseEnd])

    # Get simplification time from solver
    simp = result[0].find('Simplification time')
    simpStart = simp + 20
    simpEnd = result[0].find('s',simpStart)
    simpTime = float(result[0][simpStart:simpEnd])

    # Get CPU time from solver
    cpu = result[0].find('CPU time')
    cpuStart = result[0].find(':',cpu) + 1
    cpuEnd = result[0].find('s',cpuStart)
    cpuTime = float(result[0][cpuStart:cpuEnd])

    # Find out if it was satisfiable
    unsat = result[0].find('UNSATISFIABLE')
    sat = 0
    if unsat == -1:
        sat = 1
    else:
        sat = 0

    timeTotal = parseTime + simpTime + cpuTime

    return sat,timeTotal


if __name__ == '__main__':
    main()