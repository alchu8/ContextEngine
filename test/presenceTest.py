import csv
import datetime
import math
import numpy as np
import sys, os
import pickle
import time

## Append the paths to your algorithms here.
sys.path.insert(1, os.path.join(sys.path[0], '../python/Tesla'));
#sys.path.insert(1, os.path.join(sys.path[0], '../python/Knn'));
#sys.path.insert(1, os.path.join(sys.path[0], '../python/ALPR'));
#sys.path.insert(1, os.path.join(sys.path[0], '../python/VLR'));
sys.path.insert(1, os.path.join(sys.path[0], '../python'));


## Import your algorithms here.
from Tesla import Tesla
#from Knn import Knn
from ContextEngineBase import Complexity

## For different tests, these values will vary.
inputFilePath = "3192_bathroomPrescence_Input.csv"
outputFilePath = "3192_bathroomPrescence_Output.csv"
complexity = Complexity.thirdOrder;
numTrainingSamples = 5000;
numExecuteSamples = 6320;
numInputs = 2

inputFile = open(inputFilePath);
outputFile = open(outputFilePath);
inputReader = csv.reader(inputFile);
outputReader = csv.reader(outputFile);

## Change the name of the algorithm to test it out.
algorithmTest = Tesla(complexity, numInputs, 0, [0]*numInputs, {});
teslaTimestamps = {};
knnTimestamps = {};

for trainingSample in range(numTrainingSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        inputs = [float(x) for x in inputRow[0:numInputs]];
        output = float(outputRow[0]);

        firstTS = time.time();
        algorithmTest.addSingleObservation(inputs, output);
        secondTS = time.time();
        teslaTimestamps["load" + str(trainingSample)] = secondTS - firstTS;
print(str(trainingSample))
firstTS = time.time();
algorithmTest.train();
secondTS = time.time();
teslaTimestamps["train"] = secondTS - firstTS;

runningTotal = 0;
for executeSample in range(numExecuteSamples):
    inputRow = next(inputReader);
    outputRow = next(outputReader);
    if (len(inputRow) > 0):
        inputs = [float(x) for x in inputRow[0:numInputs]];
        output = float(outputRow[0]);

        firstTS = time.time();
        theor = algorithmTest.execute(inputs);
        secondTS = time.time();
        teslaTimestamps["test" + str(executeSample)] = secondTS - firstTS;
        teslaTimestamps["delta" + str(executeSample)] = abs(output - theor);
        runningTotal += output;
avgActual = runningTotal/(1.0*numExecuteSamples);

netLoadingTime = 0;
for i in range(numTrainingSamples):
    netLoadingTime += teslaTimestamps["load" + str(i)];

netExecuteTime = 0;
runningMAE = 0.0;
for i in range(numExecuteSamples):
    netExecuteTime += teslaTimestamps["test" + str(i)];
    runningMAE += teslaTimestamps["delta" + str(i)];

runningMAE = runningMAE/(1.0*avgActual*numExecuteSamples);

print("Loading time (tot): " + str(netLoadingTime) + " seconds");
print("Loading time (avg): " + str(netLoadingTime/(1.0*numTrainingSamples)) + " seconds");
print("Training time: " + str(teslaTimestamps["train"]) + " seconds");
print("Execute time (tot): " + str(netExecuteTime) + " seconds");
print("Execute time (avg): " + str(netLoadingTime/(1.0*numExecuteSamples)) + " seconds");
print("MAE: " + str(runningMAE));
