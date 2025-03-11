from nba_api.stats.endpoints import scoreboardv2, leaguegamefinder
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from nba_api.stats.static import teams

# Elo Rating Constants
K_FACTOR = 20         # Sensitivity of Elo adjustments
HOME_ADVANTAGE = 100    # Home team Elo boost
ELO_FILE = "elo_ratings.json"  # File to persist Elo ratings

# Fetch all NBA teams and create mappings
nba_teams = teams.get_teams()
TEAM_ID_MAP = {team["id"]: team["full_name"] for team in nba_teams}
TEAM_ABBREV_MAP = {team["abbreviation"]: team["full_name"] for team in nba_teams}

def expected_win_prob(r_team, r_opponent):
    return 1 / (1 + 10 ** ((r_opponent - r_team) / 400))

def update_elo(r_team, r_opponent, outcome):
    expected = expected_win_prob(r_team, r_opponent)
    change = K_FACTOR * (outcome - expected)
    return r_team + change

def predict_winner(home_team, away_team, elo_ratings):
    home_elo = elo_ratings.get(home_team, 1500) + HOME_ADVANTAGE
    away_elo = elo_ratings.get(away_team, 1500)
    home_win_prob = expected_win_prob(home_elo, away_elo)
    return home_team if home_win_prob > 0.5 else away_team, home_win_prob

def load_elo_ratings():
    if os.path.exists(ELO_FILE):
        with open(ELO_FILE, "r") as f:
            return json.load(f)
    return {}

def save_elo_ratings(elo_ratings):
    with open(ELO_FILE, "w") as f:
        json.dump(elo_ratings, f)

def initialize_elo_ratings():
    print("Initializing Elo ratings from season history...")
    elo_ratings = load_elo_ratings()
    if not elo_ratings:
        elo_ratings = {team: 1500 for team in TEAM_ABBREV_MAP.values()}
    
    # Fetch season history (using last season as reference)
    season_str = f"{datetime.today().year - 1}-{str(datetime.today().year)[-2:]}"
    game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season_str)
    games = game_finder.get_data_frames()[0]
    
    print("Available columns in game data:", games.columns.tolist())
    
    # Group by GAME_ID to pair home and away rows for each game
    grouped = games.groupby("GAME_ID")
    for game_id, group in grouped:
        if len(group) < 2:
            continue  # Skip incomplete games
        
        # Identify home and away rows based on the MATCHUP string
        home_game = group[group["MATCHUP"].str.contains("vs.")]
        away_game = group[group["MATCHUP"].str.contains("@")]
        
        if home_game.empty or away_game.empty:
            continue
        
        home_row = home_game.iloc[0]
        away_row = away_game.iloc[0]
        
        home_team = home_row["TEAM_NAME"]
        away_team = away_row["TEAM_NAME"]
        home_score = home_row["PTS"]
        away_score = away_row["PTS"]
        
        if pd.isna(home_score) or pd.isna(away_score):
            continue
        
        outcome = 1 if home_score > away_score else 0
        
        home_team_rating = elo_ratings.get(home_team, 1500) + HOME_ADVANTAGE
        away_team_rating = elo_ratings.get(away_team, 1500)
        
        new_home_rating = update_elo(home_team_rating, away_team_rating, outcome)
        new_away_rating = update_elo(away_team_rating, home_team_rating, 1 - outcome)
        
        # Remove home advantage after update for storage
        elo_ratings[home_team] = round(new_home_rating - HOME_ADVANTAGE, 2)
        elo_ratings[away_team] = round(new_away_rating, 2)
        
        print(f"Updated Elo for game {game_id}: {home_team} ({elo_ratings[home_team]}) vs {away_team} ({elo_ratings[away_team]})")
    
    save_elo_ratings(elo_ratings)
    return elo_ratings

def fetch_nba_games(start_date, end_date):
    try:
        games = []
        date_cursor = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        
        while date_cursor <= end_date_obj:
            formatted_date = date_cursor.strftime("%Y-%m-%d")
            scoreboard_data = scoreboardv2.ScoreboardV2(game_date=formatted_date).get_dict()
            game_result_sets = scoreboard_data.get("resultSets", [])
            
            if game_result_sets:
                game_data = game_result_sets[0]["rowSet"]
                for game in game_data:
                    home_team_id = game[6]
                    away_team_id = game[7]
                    home_team_name = TEAM_ID_MAP.get(home_team_id, "Unknown")
                    away_team_name = TEAM_ID_MAP.get(away_team_id, "Unknown")
                    games.append({"date": formatted_date, "home_team": home_team_name, "away_team": away_team_name})
            
            date_cursor += timedelta(days=1)
        
        return games
    except Exception as e:
        print("Error fetching NBA games:", e)
        return []

def process_games(games, elo_ratings):
    predictions_by_day = {}
    for game in games:
        date = game['date']
        home_team = game['home_team']
        away_team = game['away_team']
        
        pred_winner, win_prob = predict_winner(home_team, away_team, elo_ratings)
        
        if date not in predictions_by_day:
            predictions_by_day[date] = []
        
        predictions_by_day[date].append([home_team, away_team, pred_winner, round(win_prob, 3)])
    
    return predictions_by_day

def predict_games_for_range(start_date, end_date):
    print(f"Predicting games from {start_date} to {end_date}...\n")
    
    elo_ratings = initialize_elo_ratings()
    
    print("\nCurrent Elo Ratings:")
    elo_df = pd.DataFrame(elo_ratings.items(), columns=["Team", "Elo Rating"]).sort_values(by="Elo Rating", ascending=False)
    print(elo_df.to_string(index=False))
    
    games = fetch_nba_games(start_date, end_date)
    predictions_by_day = process_games(games, elo_ratings)
    save_elo_ratings(elo_ratings)
    
    print("\nPredictions for the Selected Date Range:")
    for date, games in predictions_by_day.items():
        print(f"\n📅 **{date}**")
        df = pd.DataFrame(games, columns=['Home_Team', 'Away_Team', 'Predicted_Winner', 'Win_Probability'])
        print(df.to_string(index=False))

if __name__ == "__main__":
    # Predict games from March 11 to March 16
    predict_games_for_range("2025-03-11", "2025-03-16")
