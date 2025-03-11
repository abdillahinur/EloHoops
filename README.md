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

## Requirements

- Python 3.6+
- Required Packages:
  - pandas
  - numpy
  - nba_api

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/EloHoops.git
   cd EloHoops
   ```

2. Install dependencies:
   ```
   pip install pandas numpy nba_api
   ```

## Usage

To predict NBA games for a specific date range:

```python
python nba_elo_predictor.py
```

By default, the script predicts games from March 11 to March 16, 2025. To change the date range, modify the following line in `nba_elo_predictor.py`:

```python
predict_games_for_range("YYYY-MM-DD", "YYYY-MM-DD")
```

## How It Works

1. **Initialization**: The system initializes each team with a baseline Elo rating of 1500 if there's no existing rating
2. **Historical Calibration**: Previous season data is used to refine the ratings
3. **Game Prediction**: For upcoming games, the system:
   - Adds a home court advantage of 100 Elo points to the home team
   - Calculates the win probability using the Elo formula
   - Predicts the team with >50% win probability as the winner
4. **Rating Updates**: After games, ratings are updated based on:
   - Actual outcome
   - Expected outcome (based on pre-game ratings)
   - K-factor (set to 20) which controls how quickly ratings change

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