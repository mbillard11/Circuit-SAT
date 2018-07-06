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
import matplotlib.pyplot as plt


def main():

    #inMax = 20
    gateMax = 10000
    depthMax = 4000
    faninMax = 2
    nArr = []
    timeArr = []

    for x in range(5,101,5):
        avgTime = 0

        for y in range(10):

            # n
            numIn = x
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

            #print('Success with {} inputs!'.format(red.inputs))

            # Copy the file to the input file location of the SAT solver
            # This will vary depending on file architecture
            #shutil.copy('/home/mitchell/Desktop/Spring 2018/Comp6902/circuitCNF.txt', '/home/mitchell/Documents/syrup/syrup/simp/input.cnf')
            
            
            sat,time = solver()
            avgTime += time
            nArr.append(x)
            timeArr.append(avgTime)

        #print('n: {:3} Average Time: {:5}'.format(x,avgTime))
    plt.title('Time to Solve vs. n')
    #plt.title('Gates: Depth: ',loc='right')
    plt.text(2,max(timeArr)*1.05,'Gates: {}'.format(gateMax),bbox=dict(facecolor='blue', alpha=0.5))
    plt.text(2,max(timeArr)*0.97,'Depth: {}'.format(depthMax),bbox=dict(facecolor='blue', alpha=0.5))
    #plt.text(2,0.03,'Depth: {}'.format(depthMax))
    #plt.legend((line1),('Gates'))
    plt.plot(nArr,timeArr)
    plt.xlabel('n')
    plt.ylabel('Time to Solve')
    plt.show()
    

def solver():

    #Popen("make", cwd="/./home/mitchell/Documents/syrup/syrup/simp", shell = True)
    #Popen("script", shell = True)

    glucose = Popen("./glucose input.cnf output.cnf", cwd="/./home/mitchell/Documents/syrup/syrup/simp", shell = True, stdout=PIPE)
    result = glucose.communicate()

    parse = result[0].find('Parse time')
    parseStart = parse + 11
    parseEnd = result[0].find('s',parseStart)
    parseTime = float(result[0][parseStart:parseEnd])

    simp = result[0].find('Simplification time')
    simpStart = simp + 20
    simpEnd = result[0].find('s',simpStart)
    simpTime = float(result[0][simpStart:simpEnd])

    cpu = result[0].find('CPU time')
    cpuStart = result[0].find(':',cpu) + 1
    cpuEnd = result[0].find('s',cpuStart)
    cpuTime = float(result[0][cpuStart:cpuEnd])

    unsat = result[0].find('UNSATISFIABLE')

    if unsat == -1:
        sat = 'Yes'
    else:
        sat = 'No'

    timeTotal = parseTime + simpTime + cpuTime

    #print(parse, parseTime, simp, simpTime, cpu, cpuTime, unsat)
    return sat,timeTotal

    #Popen("exit", shell = True)
    

if __name__ == '__main__':
    main()