# EloHoops - NBA Game Prediction System

![Basketball](https://img.shields.io/badge/Sport-Basketball-orange)
![Python](https://img.shields.io/badge/Language-Python-blue)
![Elo](https://img.shields.io/badge/Algorithm-Elo-green)

EloHoops is a Python-based NBA game prediction system that uses the Elo rating algorithm to forecast the outcomes of NBA basketball games.

## Overview

This project implements the Elo rating system, originally developed for chess, to predict NBA game outcomes. The algorithm tracks team strength over time by updating ratings based on game results, where:
- Teams gain Elo points when they win games
- Teams lose Elo points when they lose games
- The amount of points exchanged is based on the expected outcome (upsets result in larger shifts)
- Home court advantage is factored into predictions

## Features

- **Elo Rating System**: Maintains and updates ratings for all NBA teams
- **NBA API Integration**: Fetches real NBA game data and schedules
- **Game Predictions**: Forecasts winners and win probabilities for upcoming games
- **Historical Analysis**: Uses previous season data to establish baseline ratings
- **Persistent Storage**: Saves updated Elo ratings for future predictions
- **Enhanced Excel Sheets**: Stores team Elo ratings and game predictions in beautifully formatted Excel sheets organized by date
- **NBA Team Filtering**: Ensures only official NBA teams (no G League or other teams) are tracked
- **Visual Indicators**: Color-coded probability values to easily identify favored teams

## Requirements

- Python 3.6+
- Required Packages:
  - pandas
  - numpy
  - nba_api
  - openpyxl

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/EloHoops.git
   cd EloHoops
   ```

2. Install dependencies:
   ```
   pip install pandas numpy nba_api openpyxl
   ```

## Usage

To predict NBA games for today:

```python
python nba_elo_predictor.py
```

To predict games for a custom date range, modify the function call at the bottom of the script:

```python
predict_games_for_range("YYYY-MM-DD", "YYYY-MM-DD")
```

## Data Storage

EloHoops stores data in two primary ways:

1. **JSON File (elo_ratings.json)**: Contains the latest Elo ratings for all NBA teams in a simple key-value format.

2. **Excel Workbook (nba_elo_tracker.xlsx)**: Contains detailed daily records organized by date in separate sheets, with each sheet including:
   - A table of all NBA team Elo ratings for that day, ranked by rating
   - A table of game predictions including home/away teams, their Elo ratings, predicted winner, and home team win probability
   - Professionally formatted tables with headers, borders, and alternating row colors
   - Color-coded win probabilities (green for home team favored, pink for away team favored)

Each date's data is stored in its own sheet, and the system will not overwrite existing sheets, preserving historical data.

## Understanding Win Probability

The "Home Team Win Probability" column in the predictions table shows the probability (from 0 to 1) that the home team will win:
- Values above 0.5 indicate the home team is favored (highlighted in green)
- Values below 0.5 indicate the away team is favored (highlighted in pink)
- The "Predicted Winner" column shows the team with the higher win probability

## How It Works

1. **Initialization**: The system initializes each team with a baseline Elo rating of 1500 if there's no existing rating
2. **Team Filtering**: Only official NBA teams are tracked and included in predictions
3. **Historical Calibration**: Previous season data is used to refine the ratings
4. **Game Prediction**: For upcoming games, the system:
   - Adds a home court advantage of 100 Elo points to the home team
   - Calculates the win probability using the Elo formula
   - Predicts the team with >50% win probability as the winner
5. **Rating Updates**: After games, ratings are updated based on:
   - Actual outcome
   - Expected outcome (based on pre-game ratings)
   - K-factor (set to 20) which controls how quickly ratings change
6. **Data Recording**: All data is saved to both the JSON file and the formatted Excel workbook with date-specific sheets

## Elo Formula

The Elo system uses the following formulas:

Expected win probability for Team A vs Team B:
```
P(A) = 1 / (1 + 10^((R_B - R_A)/400))
```

Rating update after a game:
```
R_new = R_old + K * (S - P)
```
Where:
- K = 20 (sensitivity factor)
- S = actual outcome (1 for win, 0 for loss)
- P = expected outcome (probability of winning)

## Future Improvements

- Web application interface
- Advanced statistics integration
- Machine learning enhancements
- Support for other sports leagues
- Betting odds comparison

## License

MIT License

## Author

Created by Abdillahi Nur