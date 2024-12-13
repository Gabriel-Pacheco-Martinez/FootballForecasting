# Libraries
import csv

# My libraries
import basefunctions


# IGN scores
#   - This section of the code will
#     iterate over the predictions
#     and the actual season and calculate
#     results based on that
def evaluateSkill(teamsMid, teamsEnd, teamsRes):
    ignScore = 0

    # Iterate through keys
    for key in teamsEnd:
        # Position throughout the season
        posMid = teamsMid[key]['position']
        posEnd = teamsEnd[key]['position']
        teamsRes[key]['points'] = teamsEnd[key]['points']

        # Predicted form
        predicted = 1 if teamsRes[key]['prob'] > 0.5 else 0
        teamsRes[key]['predicted'] = predicted

        # Variable to check if kept form
        form = 1 if posEnd <= posMid + 2 else 0
        teamsRes[key]['actual'] = form

        result = 1 if predicted == form else 0

        currIgnScore = round(basefunctions.calculateIgnScore(teamsRes[key]['prob'], result), 2)
        teamsRes[key]['ignScore'] = currIgnScore
        ignScore += currIgnScore

    ignScore = round(ignScore, 2)
    return ignScore, teamsRes


# Results
#   - This section will calculate the probabilities
#     of the teams maintaining form based on the
#     weighted average sum of the three scores
def processProbabilities(teamsMid, neighbours):
    # Probabilities stored
    teamsRes = {}

    # Loop
    for key in teamsMid:

        # Check if team is an overachiever
        special = 1 if ((teamsMid[key]['points'] > (teamsMid[key]['pointsBetO'] + 4))
                        and (teamsMid[key]['position'] <= 7)) else 0

        # Mid-season weighted average sum
        midWAS = round(basefunctions.weightedAverageSum(
            teamsMid[key]['points'],
            teamsMid[key]['pointsBetO'],
            teamsMid[key]['pointsPerB']
        ))

        # Calculate the distance between the midWas and all the neighbours
        distances = {key: abs(key - midWAS) for key in neighbours}

        # Get "k" nearest neighbours
        k = 5
        nn = sorted(distances, key=distances.get)[:k]
        denominatorSum = sum(range(1, k + 1))
        numeratorSum = 0

        # Sum
        for i, n in enumerate(nn):
            prob = neighbours[n]['happened'] / neighbours[n]['events']
            numeratorSum += prob * (k - i)

        # Calculate probability
        proKeepForm = round(numeratorSum / denominatorSum, 2)

        teamsRes[key] = {'prob': proKeepForm,
                         'special': special}

    return teamsRes


# Climatology
#   - This section will calculate the probabilities
#     of the teams maintaining form based on climatology
def processProbabilitiesClimatology(teamsMid, neighbours):
    # Probabilities stored
    teamsClimatology = {}

    # Loop
    for key in teamsMid:

        # Check if team is an overachiever
        special = 1 if ((teamsMid[key]['points'] > (teamsMid[key]['pointsBetO'] + 4))
                        and (teamsMid[key]['position'] <= 7)) else 0

        # Use only betting odds points
        points = teamsMid[key]['pointsBetO']

        # Calculate the distance between the midWas and all the neighbours
        distances = {key: abs(key - points) for key in neighbours}

        # Get "k" nearest neighbours
        k = 5
        nn = sorted(distances, key=distances.get)[:k]
        denominatorSum = sum(range(1, k + 1))
        numeratorSum = 0

        # Sum
        for i, n in enumerate(nn):
            prob = neighbours[n]['happened'] / neighbours[n]['events']
            numeratorSum += prob * (k - i)

        # Calculate probability
        proKeepForm = round(numeratorSum / denominatorSum, 2)

        teamsClimatology[key] = {'prob': proKeepForm,
                                 'special': special}

    return teamsClimatology


# Iteration over file data
#   - Iterate over the rows of the current season
#     and calculate the probabilities of the team
#     maintaining form.
def processData(neighbours, currSeasonFile):
    teams = {}  # Teams to iterate over whole season
    teamsMid = {}  # Teams in the middle of the season
    teamsEnd = {}  # Teams at the end of the season
    teamsRes = {}  # Results of prob and IGN Scores
    teamsClim = {}  # Results of prob and IGN Scores for climatology

    with open(currSeasonFile, 'r') as file:

        csvReader = csv.reader(file)
        header = next(csvReader, None)

        # Go over the season
        count = 0
        for row in csvReader:
            count += 1  # One more game
            teams = basefunctions.processRow(row, teams)

            # We have reached mid-season
            if count == 153:
                teamsMid = basefunctions.processTeams(teams)
                teamsRes = processProbabilities(teamsMid, neighbours)
                teamsClim = processProbabilitiesClimatology(teamsMid, neighbours)
                basefunctions.printTeams(teamsMid)

        # We have concluded the season
        teamsEnd = basefunctions.processTeams(teams)

        # Calculate ign for my result and for climatology
        ignScoreRes, teamsRes = evaluateSkill(teamsMid, teamsEnd, teamsRes)
        ignScoreClim, teamsClim = evaluateSkill(teamsMid, teamsEnd, teamsClim)

        # Return maps and ign scores
        return ignScoreRes, teamsRes, ignScoreClim, teamsClim
