# Libraries
import os

import basefunctions
# My libraries
import nn
import cp

# Define league to be studied
leagueDataPathTrain = os.path.join(os.path.dirname(__file__), 'PremierLeague_Data_Train')
leagueDataPathTest = os.path.join(os.path.dirname(__file__), 'PremierLeague_Data_Test')

# Part 1: Nearest Neighbours
#   - Define the historical probabilities
#     based on obtained points in the past
mapNeighbours = nn.processData(leagueDataPathTrain)
print(f"Calculation of neighbours: {mapNeighbours}")

# Part 2: Calculate Probabilities
#   - Use the neighbours calculated previously
#     to calculate the probability of each team
#     maintaining its form
seasonToProcess = input("Enter season to study: ")
currSeasonPath = os.path.join(leagueDataPathTest, seasonToProcess + ".csv")
skillRes, teamsRes, skillClim, teamsClim = cp.processData(mapNeighbours, currSeasonPath)

# Part 3: Show Results
#   - Provide the results back to the user
#     with points information, predicted
#     actual, score and probabilities
basefunctions.printResults(skillRes, teamsRes)
basefunctions.printResults(skillClim, teamsClim)

# Future work
#Perform three dimensions analysis
