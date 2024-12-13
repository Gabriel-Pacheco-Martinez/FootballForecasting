# Libraries
import os
import csv
import pandas as pd

# My libraries
import basefunctions


# Process neighbours
def processNeighbours(teamsMid, teamsEnd, neighbours):
    for key in teamsEnd:
        # Position throughout the season
        posMid = teamsMid[key]['position']
        posEnd = teamsEnd[key]['position']

        # Mid-season weighted average sum
        midWAS = round(basefunctions.weightedAverageSum(
            teamsMid[key]['points'],
            teamsMid[key]['pointsBetO'],
            teamsMid[key]['pointsPerB']
        ))

        # Variable to check if kept form
        form = 1 if posEnd <= posMid + 2 else 0

        # If statement
        if midWAS in neighbours:
            neighbours[midWAS] = {'events': neighbours[midWAS]['events'] + 1,
                                  'happened': neighbours[midWAS]['happened'] + form}
        else:
            neighbours[midWAS] = {'events': 1,
                                  'happened': 1}

        # Verification
        # print(f"{key} was {posMid} and finished {posEnd} with: {midWAS}, form = {form}")
        # print(f"Current state of neighbours: {neighbours}")

    return neighbours


# Process all data
def processData(leagueDataPath):
    neighbours = {}

    for currSeason in os.listdir(leagueDataPath):
        currSeasonFile = os.path.join(leagueDataPath, currSeason)
        teams = {}
        teamsMid = {}
        teamsEnd = {}

        with open(currSeasonFile, 'r') as file:
            # Read file and skip header
            csvReader = csv.reader(file)
            header = next(csvReader, None)

            # Go through the season
            count = 0
            for row in csvReader:
                count += 1  # One more game
                teams = basefunctions.processRow(row, teams)

                if count == 153:
                    teamsMid = basefunctions.processTeams(teams)
                    # basefunctions.printTeams(teamsMid)

            teamsEnd = basefunctions.processTeams(teams)
            # basefunctions.printTeams(teamsEnd)

        neighbours = processNeighbours(teamsMid, teamsEnd, neighbours)

    return neighbours
