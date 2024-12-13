import math
from scipy.stats import skellam
from tabulate import tabulate
from colorama import Fore, Style


# Function:
#   - Update hashmaps of teams depending
#     on new each row read
def updateTeams(teamsMap, HT, AT, ptsHome, ptsAway, ptsBOHome, ptsBOAway, ptsPBHome, ptsPBAway):
    # For home team
    if HT in teamsMap:
        teamsMap[HT] = {
            'points': teamsMap[HT]['points'] + int(ptsHome),
            'pointsBetO': teamsMap[HT]['pointsBetO'] + float(ptsBOHome),
            'pointsPerB': teamsMap[HT]['pointsPerB'] + float(ptsPBHome),
            'position': None,
        }
    else:
        teamsMap[HT] = {
            'points': int(ptsHome),
            'pointsBetO': float(ptsBOHome),
            'pointsPerB': float(ptsPBHome),
            'position': None,
        }

    # For visiting team
    if AT in teamsMap:
        teamsMap[AT] = {
            'points': teamsMap[AT]['points'] + int(ptsAway),
            'pointsBetO': teamsMap[AT]['pointsBetO'] + float(ptsBOAway),
            'pointsPerB': teamsMap[AT]['pointsPerB'] + float(ptsPBAway),
            'position': None,
        }
    else:
        teamsMap[AT] = {
            'points': int(ptsAway),
            'pointsBetO': float(ptsBOAway),
            'pointsPerB': float(ptsPBAway),
            'position': None,
        }

    # Return
    return teamsMap


# Function:
#   - Calculate the points that a team
#     should have obtained based on
#     performance
def performancePointsCalculation(HST, AST):
    # Shots on target * conversion rate
    lambdaHome = max(0.01, float(HST) * 0.15)
    lambdaAway = max(0.01, float(AST) * 0.15)

    # Calculate using skellam distribution
    probDraw = skellam.pmf(0, lambdaHome, lambdaAway)  # P(D = 0)
    probHomeWin = 1 - skellam.cdf(0, lambdaHome, lambdaAway)  # P(D > 0)
    probAwayWin = skellam.cdf(-1, lambdaHome, lambdaAway)  # P(D < 0)

    # Calculate probabilities
    totalProb = probDraw + probHomeWin + probAwayWin
    probHomeWin /= totalProb
    probAwayWin /= totalProb
    probDraw /= totalProb

    # Points calculation
    ptsPerHome = 3 * probHomeWin + 1 * probDraw
    ptsPerAway = 3 * probAwayWin + 1 * probDraw

    return ptsPerHome, ptsPerAway


# Function:
#   - Read a row and process the
#     information that comes in
#     this row
def processRow(row, teams):
    div, HT, AT, FTHG, FTAG, HS, AS, HST, AST, BOH, BOD, BOA = row

    # Calculate points Normal
    ptsHome, ptsAway = (3, 0) if FTHG > FTAG else (1, 1) if FTHG == FTAG else (0, 3)

    # Calculate points based on betting odds (BO/Betting odds)
    ptsBOHome = 3 * (1 / float(BOH)) + 1 * (1 / float(BOD))
    ptsBOAway = 3 * (1 / float(BOA)) + 1 * (1 / float(BOD))

    # Calculate points based on performance (PB/Performance based)
    ptsPBHome, ptsPBAway = performancePointsCalculation(HST, AST)

    # Update teams
    teams = updateTeams(teams, HT, AT, ptsHome, ptsAway, ptsBOHome, ptsBOAway, ptsPBHome, ptsPBAway)

    # Return
    return teams


# Function:
#   - Order teams based on their
#     points
def processTeams(teams):
    # Sort based of points
    teams = dict(sorted(teams.items(), key=lambda item: item[1]['points'], reverse=True))

    # Give positions
    position = 1
    for key in teams:
        teams[key]['position'] = position
        position += 1

    return teams


# Function:
#   - Calculate the weighted average
#     sum of the three scores
def weightedAverageSum(points, pointsBet, pointsPer):
    # Weights
    wPoints = 0.3  # Weight for actual points
    wBET = 0.3  # Weight for betting odds
    wPER = 0.4  # Weight for performance odds

    # Result
    result = ((wPER * pointsPer + wBET * pointsBet + wPoints * points) / (wPER + wBET + wPoints))

    return result


# Function:
#   - This function calculates the
#     ignScore.
def calculateIgnScore(p, result):
    if result == 0:
        p = 1 - p

    maxP = max(p, 0.0000625)

    IGNpoints = 25 * (1 + math.log2(maxP))

    return IGNpoints


# Function:
#   - Print the results of prediction
#     and ignScores obtained back to the
#     user
def printResults(skill, teamsRes):
    teamsRes = processTeams(teamsRes)

    # Prepare data for the table
    table_data = [
        [
            f"\033[92m{teamsRes[key]['position']}\033[0m" if teamsRes[key]['special'] == 1 else teamsRes[key][
                'position'],
            f"\033[92m{key}\033[0m" if teamsRes[key]['special'] == 1 else key,
            f"\033[92m{teamsRes[key]['predicted']}\033[0m" if teamsRes[key]['special'] == 1 else teamsRes[key][
                'predicted'],
            f"\033[92m{teamsRes[key]['prob']}\033[0m" if teamsRes[key]['special'] == 1 else teamsRes[key]['prob'],
            f"\033[92m{teamsRes[key]['actual']}\033[0m" if teamsRes[key]['special'] == 1 else teamsRes[key]['actual'],
            f"\033[92m{teamsRes[key]['ignScore']}\033[0m" if teamsRes[key]['special'] == 1 else teamsRes[key][
                'ignScore']
        ]
        for key in teamsRes
    ]
    # Define headers
    headers = ["Position", "Team", "Predicted", "Prob", "Actual", "IGN Score"]

    # Print the formatted table
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # Print the skill score
    print(Fore.CYAN + f"\nSkill score: {skill}" + Style.RESET_ALL)


# Function:
#   - Print hashmaps of teams at mid-season
#     and ending of the season.
def printTeams(teams):
    print(Fore.LIGHTBLUE_EX + "======================" + Style.RESET_ALL)
    for key in teams:
        print(f"{teams[key]['position']}.-{key}: "
              f"{teams[key]['points']} pts | "
              f"{teams[key]['pointsBetO']:.2f} BO pts | "
              f"{teams[key]['pointsPerB']:.2f} PER pts")
