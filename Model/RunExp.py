#!/usr/bin/python

# Run the Generator, Reducer, and Solver. Output results as a graph
# The n, m, and d values can be changed

import Generator
import Reducer
import RunGenRed
import math
import random
from pprint import pprint
import shutil
from subprocess import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    numGates = [3, 10, 100, 1000]
    numDepth = [2, 5, 10, 100, 1000]
    faninMax = [2,4,10,50]
    numIns = [[1,21,1],[5,101,5],[5,1001,50]]
    #nStop = [21,101,1011]
    #nInc = [1,5,50]
    print('{:10s} {:^10s} {:^10s} {:^10s} {:^10s} {:^10s}'.format('Max Inputs', 'Gates' ,'Depth',  'Fanin',  'SAT %',  'Max Time'))

    for n in numIns:
        nStart, nStop, nInc = n[0], n[1], n[2]
        for m in numGates:
            for d in numDepth:
                if d <= m:
                    for f in faninMax:
                        experiment = RunGenRed.RunGenRed(m, d, f, nStart, nStop, nInc)
                        experiment.run()


if __name__ == '__main__':
    main()