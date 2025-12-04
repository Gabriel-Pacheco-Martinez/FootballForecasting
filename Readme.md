<!-- PROJECT HEADER -->
<h1>
<p align="center">
  <br> Football Prediction: Mid-Season Overachievers
</p>
</h1>

<p align="center">
  <br />
  <a href="#overview">Overview</a>
  ·
  <a href="#repository-contents">Repository contents</a>
  ·
  <a href="#instructions">Instructions</a>
  ·
  <a href="#running-scripts">Running Scripts</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13.2-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-Apache%202.0-green?style=flat-square" alt="License">
</p>

## Overview
This project explores a model designed to predict whether football teams can maintain their mid-season form by incorporating performance metrics and bookmaker odds. The model outperformed climatology in 4 out of 5 cases, demonstrating the limitations of relying solely on bookmaker odds. Instead, it highlights the importance of considering expected goals and other key performance metrics.

While the model provides a solid foundation, its current limitation lies in always predicting positive outcomes with varying certainty. Future iterations aim to integrate additional parameters, such as player injuries, mental states, and in-match dominance factors, alongside alternative classification techniques to improve reliability.

This project serves as a stepping stone for better forecasting methodologies and understanding which factors most influence a team's ability to maintain form.

## Repository contents
1. **main.py**
    - Main script of the project. Links all other files together.

2. **nn.py**
   - Provides all the nearest neighbours for the k-nn classifier

3. **cp.py**
   - Goes over the data for the current season being studied

4. **basefunctions.py**
   - File with supporting functions for the project

## Instructions
Install the required Python packages:
```bash
pip install -r requirements.txt
```

Resources needed: 
- Two folders as indicated below are needed. Inside each excel file at least one of the betting odds needs to be changed 
to have header names "BOH", "BOD", "BOA" for home, draw and away. Please set as many files as desired from the page https://www.football-data.co.uk/ 
on the training set. Only one file from the testing folder can be run at once.
```
project/
├── PremierLeague_Data_Test/
│   ├── 2015-2015.csv
    ...
├── PremierLeague_Data_Train/
│   ├── 2003-2004.csv
│   ├── 2004-2005.csv
    ...
```

## Running scripts
- Simply run main.py after installing the required libraries and preparing the two folders with the specified data as described above.
- Once run a message will appear. Enter a season as shown below:
```bash
Enter season to study: 2022-2023
```