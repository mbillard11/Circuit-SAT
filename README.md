# Circuit-SAT
## Mitchell Billard, Adebayo Emmanuel Adeoya ##

## Table of Contents
* Introduction
* How To Run
* Report

## Introduction
The Circuit	Satisfiability problem (also	known	as CIRCUIT-SAT, Circuit-SAT, CSAT,	etc.)	is the decision	problem of	determining	whether	a	given Boolean circuit has	an	assignment	of its	inputs	that	makes	the	output	True/False. This report was created for the course COMP 6902.

## How To Run
Run RunExp.py. For a single experiment, input the desired values into line 27. [RunGenRed.RunGenRed(*Values Here*)].
If you want to run all experiments, comment out lines 27 & 28, and uncomment lines 31-38.
A miniSAT solver using DIMACS must be already installed. We used the syrup solver that can be found [here](http://www.satcompetition.org/).
The location of the file that the reducer opens must be changed to the input.cnf of your SAT solver (line 13 in Reducer.py). 

## Report
The final report for this project is found [here](https://github.com/mbillard11/Circuit-SAT/blob/master/Write-Up/Circuit-SAT_Report.pdf).
