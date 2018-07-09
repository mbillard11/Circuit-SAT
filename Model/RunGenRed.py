#!/usr/bin/python
#
# Author: Mitchell Billard
#
# Run the Generator, Reducer, and Solver. 
# Output a graph by uncommenting self.plotGraph()
# The n, m, d, and fanin values come from RunExp.py

import Generator
import Reducer
import math
import random
from pprint import pprint
import shutil
from subprocess import *
import matplotlib.pyplot as plt
import numpy as np


class RunGenRed:

    def __init__(self, numGates, numDepth, faninMax, nStart, nStop, nInc):

        # m
        self.numGates = numGates #int(input('Enter the number of gates: '))
        # d
        self.numDepth =  numDepth #int(input('Enter the depth: '))
        # fanin
        self.faninMax = faninMax
        self.nStart = nStart
        self.nStop = nStop
        self.nInc = nInc
        # Arrays for plotting graph
        self.nArr = []
        self.timeArr = []
        self.satAvg = 0

    def run(self):
        
        # Can change range and increments of n here 
        for x in range(self.nStart,self.nStop,self.nInc):
            avgTime = 0
            satRatio = 0
            satSum = 0

            # For every n run 10 instances 
            for y in range(10):

                # n
                numIn = x

                # Initalize a generator
                gen = Generator.Generator(numIn, self.numGates, self.faninMax, self.numDepth)
                gen.outputList()
                # Generate a circuit
                gen.generateCircuit()
                # Initalize a reducer using the circuit that was just generated
                red = Reducer.Reducer(gen.circuit)
                # Write the reduction into a file
                red.writeCNF(red.file)
                
                sat,time = self.solver()
                satSum += sat
                avgTime += time
            satRatio = satSum / 10.00          
            avgTime /= 10.00
            self.satAvg += satRatio
            self.timeArr.append(avgTime)
            self.nArr.append(x)

        self.satAvg *= 5
        
        # Print results to find interesting scenarios
        print('{:^10} {:^10} {:^10} {:^10} {:^10} {:^10.2}'.format(self.nStop - 1, self.numGates, self.numDepth, self.faninMax, int(self.satAvg), max(self.timeArr)))

        # Uncomment to show graph
        # self.plotGraph()

    
    def plotGraph(self):

        plt.figure(figsize=(8,6))
        plt.title('Time to Solve vs. n', fontsize = 22)

        plt.figtext(0.15,0.84,'Gates: {}'.format(self.numGates),bbox=dict(facecolor='blue', alpha=0.5))
        plt.figtext(0.15,0.79,'Depth: {}'.format(self.numDepth),bbox=dict(facecolor='blue', alpha=0.5))
        plt.figtext(0.15,0.74,'Max Fanin: {}'.format(self.faninMax),bbox=dict(facecolor='blue', alpha=0.5))
        plt.figtext(0.15,0.69,'{:.2f}% SAT'.format(self.satAvg),bbox=dict(facecolor='blue', alpha=0.5))
        
        plt.plot(np.unique(self.nArr), np.poly1d(np.polyfit(self.nArr, self.timeArr, 2))(np.unique(self.nArr)))
        plt.plot(self.nArr,self.timeArr,'ro')
        plt.xlabel('n')
        plt.ylabel('Time to Solve')

        plt.show()

    def solver(self):

        glucose = Popen("./glucose input.cnf output.cnf", cwd="/./home/mitchell/Documents/syrup/syrup/simp", shell = True, stdout=PIPE, encoding='utf8')
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