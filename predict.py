import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import requests
import os

# Get last 5 games
def get_latest_games(team, trimmed_df, num_games=5):
    # Filter matches where the team is either home or away
    team_games = trimmed_df[(trimmed_df['HomeTeam'] == team) | (trimmed_df['AwayTeam'] == team)]
    
    # Sort by date in descending order to get the latest matches
    team_games = team_games.sort_values(by='Date', ascending=False)
    
    # Get the latest `num_games` matches
    latest_games = team_games.head(num_games)
    
    return latest_games


#Get last 5 Home/Away games
def get_latest_home_or_away_games(team, trimmed_df, num_games=5, location='home'):
    """
    Get the last `num_games` home or away games for a specific team.

    :param team: Name of the team.
    :param trimmed_df: The dataframe containing match data.
    :param num_games: Number of games to fetch.
    :param location: 'home' for home games, 'away' for away games.
    :return: A dataframe containing the filtered games.
    """
    if location == 'home':
        # Filter matches where the team is the home team
        team_games = trimmed_df[trimmed_df['HomeTeam'] == team]
    elif location == 'away':
        # Filter matches where the team is the away team
        team_games = trimmed_df[trimmed_df['AwayTeam'] == team]
    else:
        raise ValueError("Invalid location. Use 'home' or 'away'.")
    
    # Sort by date in descending order to get the latest matches
    team_games = team_games.sort_values(by='Date', ascending=False)
    
    # Get the latest `num_games` matches
    latest_games = team_games.head(num_games)
    
    return latest_games


 # Get last 2 H2H games
def get_last_2_h2h_games(team1, team2, trimmed_df):
    """
    Get the last 2 head-to-head (H2H) games between two teams.

    :param team1: Name of the first team.
    :param team2: Name of the second team.
    :param trimmed_df: The dataframe containing match data.
    :return: A dataframe containing the last 2 H2H games.
    """
    # Filter matches where both teams are involved
    h2h_games = trimmed_df[((trimmed_df['HomeTeam'] == team1) & (trimmed_df['AwayTeam'] == team2)) |
                            ((trimmed_df['HomeTeam'] == team2) & (trimmed_df['AwayTeam'] == team1))]
    
    # Sort by date in descending order to get the latest matches
    h2h_games = h2h_games.sort_values(by='Date', ascending=False)
    
    # Get the last 2 H2H games
    last_2_h2h_games = h2h_games.head(2)
    
    return last_2_h2h_games


# Get last 2 H2H Home/Away games
def get_last_2_h2h_home_or_away_games(team1, team2, trimmed_df):
    """
    Get the last 2 head-to-head (H2H) Home or Away games between two teams.

    :param team1: Name of the first team.
    :param team2: Name of the second team.
    :param trimmed_df: The dataframe containing match data.
    :return: A dataframe containing the last 2 H2H games.
    """
    # Filter matches where both teams are involved
    h2h_games = trimmed_df[((trimmed_df['HomeTeam'] == team1) & (trimmed_df['AwayTeam'] == team2))]
    
    # Sort by date in descending order to get the latest matches
    h2h_games = h2h_games.sort_values(by='Date', ascending=False)
    
    # Get the last 2 H2H games
    last_2_h2h_games = h2h_games.head(2)
    
    return last_2_h2h_games


# Function to calculate the last 5 match statistics for a given team.
def get_team_stats(team, latest_5_games):
    """
    Parameters:
    - team (str): The team for which to calculate the stats.
    - latest_5_games (DataFrame): The DataFrame containing match data.

    Returns:
    - dict: A dictionary with calculated statistics for the team.
    """
    results = [
        "Win" if (row['HomeTeam'] == team and row['FTR'] == 'H') or 
                 (row['AwayTeam'] == team and row['FTR'] == 'A') 
        else "Lose" if (row['HomeTeam'] == team and row['FTR'] == 'A') or 
                      (row['AwayTeam'] == team and row['FTR'] == 'H') 
        else "Draw"
        for _, row in latest_5_games.iterrows()
    ]
    
    goals_for = [
        row['FTHG'] if (row['HomeTeam'] == team) 
        else row['FTAG']
        for _, row in latest_5_games.iterrows()
    ]
    
    goals_against = [
        row['FTAG'] if (row['HomeTeam'] == team) 
        else row['FTHG']
        for _, row in latest_5_games.iterrows()
    ]
    
    goals = list(np.add(goals_for, goals_against))
    
    btts = [
        1 if (row['FTHG'] > 0 and row['FTAG'] > 0)
        else 0
        for _, row in latest_5_games.iterrows()
    ]
    
    shots_on_target_for = [
        row['HST'] if (row['HomeTeam'] == team) 
        else row['AST']
        for _, row in latest_5_games.iterrows()
    ]
    
    shots_on_target_against = [
        row['AST'] if (row['HomeTeam'] == team) 
        else row['HST']
        for _, row in latest_5_games.iterrows()
    ]
    
    corners_for = [
        row['HC'] if (row['HomeTeam'] == team) 
        else row['AC']
        for _, row in latest_5_games.iterrows()
    ]
    
    corners_against = [
        row['AC'] if (row['HomeTeam'] == team) 
        else row['HC']
        for _, row in latest_5_games.iterrows()
    ]
    
    corners = list(np.add(corners_for, corners_against))
    
    cards_for = [
        row['HY'] + row['HR'] if (row['HomeTeam'] == team) 
        else row['AY'] + row['AR']
        for _, row in latest_5_games.iterrows()
    ]
    
    cards_against = [
        row['AY'] + row['AR'] if (row['HomeTeam'] == team) 
        else row['HY'] + row['HR']
        for _, row in latest_5_games.iterrows()
    ]
    
    cards = list(np.add(cards_for, cards_against))

    # Returning the dictionary of stats
    team_stats = {
        "results": results,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goals": goals,
        "btts": btts,
        "shots_on_target_for": shots_on_target_for,
        "shots_on_target_against": shots_on_target_against,
        "corners_for": corners_for,
        "corners_against": corners_against,
        "corners": corners,
        "cards_for": cards_for,
        "cards_against": cards_against,
        "cards": cards,
    }

    return team_stats


# Function to calculate the last 2 h2h match statistics for given teams.
def get_h2h_stats(home_team, away_team, latest_games):
    """
    Parameters:
    - team (str): The team for which to calculate the stats.
    - latest_5_games (DataFrame): The DataFrame containing match data.

    Returns:
    - dict: A dictionary with calculated statistics for the team.
    """
    results = [
        home_team + " Win" if (row['HomeTeam'] == home_team and row['FTR'] == 'H') or 
                 (row['AwayTeam'] == home_team and row['FTR'] == 'A') 
        else away_team + " Win" if (row['HomeTeam'] == home_team and row['FTR'] == 'A') or 
                      (row['AwayTeam'] == home_team and row['FTR'] == 'H') 
        else "Draw"
        for _, row in latest_games.iterrows()
    ]
    
    home_goals = [
        row['FTHG'] if (row['HomeTeam'] == home_team) 
        else row['FTAG']
        for _, row in latest_games.iterrows()
    ]
    
    away_goals = [
        row['FTHG'] if (row['HomeTeam'] == away_team) 
        else row['FTAG']
        for _, row in latest_games.iterrows()
    ]
    
    goals = list(np.add(home_goals, away_goals))
    
    btts = [
        1 if (row['FTHG'] > 0 and row['FTAG'] > 0)
        else 0
        for _, row in latest_games.iterrows()
    ]
    
    shots_on_target_for = [
        row['HST'] if (row['HomeTeam'] == home_team) 
        else row['AST']
        for _, row in latest_games.iterrows()
    ]
    
    shots_on_target_against = [
        row['HST'] if (row['HomeTeam'] == away_team) 
        else row['AST']
        for _, row in latest_games.iterrows()
    ]
    
    corners_for = [
        row['HC'] if (row['HomeTeam'] == home_team) 
        else row['AC']
        for _, row in latest_games.iterrows()
    ]
    
    corners_against = [
        row['HC'] if (row['HomeTeam'] == away_team) 
        else row['AC']
        for _, row in latest_games.iterrows()
    ]
    
    corners = list(np.add(corners_for, corners_against))
    
    cards_for = [
        row['HY'] + row['HR'] if (row['HomeTeam'] == home_team) 
        else row['AY'] + row['AR']
        for _, row in latest_games.iterrows()
    ]
    
    cards_against = [
        row['HY'] + row['HR'] if (row['HomeTeam'] == away_team) 
        else row['AY'] + row['AR']
        for _, row in latest_games.iterrows()
    ]
    
    cards = list(np.add(cards_for, cards_against))

    # Returning the dictionary of stats
    home_team_name = home_team.lower().replace(' ', '_')
    away_team_name = away_team.lower().replace(' ', '_')
    h2h_stats = {
        "results": results,
        f"{home_team_name}_goals": home_goals,
        f"{away_team_name}_goals": away_goals,
        "goals": goals,
        "btts": btts,
        f"{home_team_name}_shots_on_target": shots_on_target_for,
        f"{away_team_name}_shots_on_target": shots_on_target_against,
        f"{home_team_name}_corners": corners_for,
        f"{away_team_name}_corners": corners_against,
        "corners": corners,
        f"{home_team_name}_cards": cards_for,
        f"{away_team_name}_cards": cards_against,
        "cards": cards,
    }

    return h2h_stats


# Function to calculate the last 2 h2h home/away match statistics for given teams.
def get_h2h_home_or_away_stats(home_team, away_team, latest_games):
    """
    Parameters:
    - team (str): The team for which to calculate the stats.
    - latest_5_games (DataFrame): The DataFrame containing match data.

    Returns:
    - dict: A dictionary with calculated statistics for the team.
    """
    results = [
        home_team + " Win" if (row['FTR'] == 'H')
        else away_team + " Win" if (row['FTR'] == 'A')
        else "Draw"
        for _, row in latest_games.iterrows()
    ]
    
    home_goals = [
        row['FTHG']
        for _, row in latest_games.iterrows()
    ]
    
    away_goals = [
        row['FTAG']
        for _, row in latest_games.iterrows()
    ]
    
    goals = list(np.add(home_goals, away_goals))
    
    btts = [
        1 if (row['FTHG'] > 0 and row['FTAG'] > 0)
        else 0
        for _, row in latest_games.iterrows()
    ]
    
    shots_on_target_for = [
        row['HST']
        for _, row in latest_games.iterrows()
    ]
    
    shots_on_target_against = [
        row['AST']
        for _, row in latest_games.iterrows()
    ]
    
    corners_for = [
        row['HC']
        for _, row in latest_games.iterrows()
    ]
    
    corners_against = [
        row['AC']
        for _, row in latest_games.iterrows()
    ]
    
    corners = list(np.add(corners_for, corners_against))
    
    cards_for = [
        row['HY'] + row['HR']
        for _, row in latest_games.iterrows()
    ]
    
    cards_against = [
        row['AY'] + row['AR']
        for _, row in latest_games.iterrows()
    ]
    
    cards = list(np.add(cards_for, cards_against))

    # Returning the dictionary of stats
    home_team_name = home_team.lower().replace(' ', '_')
    away_team_name = away_team.lower().replace(' ', '_')
    h2h_stats = {
        "results": results,
        f"{home_team_name}_goals": home_goals,
        f"{away_team_name}_goals": away_goals,
        "goals": goals,
        "btts": btts,
        f"{home_team_name}_shots_on_target": shots_on_target_for,
        f"{away_team_name}_shots_on_target": shots_on_target_against,
        f"{home_team_name}_corners": corners_for,
        f"{away_team_name}_corners": corners_against,
        "corners": corners,
        f"{home_team_name}_cards": cards_for,
        f"{away_team_name}_cards": cards_against,
        "cards": cards,
    }

    return h2h_stats


# Function to create pre-match stats dataset
def create_prematch_stats(home_team, away_team, df):

    # home team last 5 games
    home_latest_5_games = get_latest_games(home_team, df, num_games=5)
    home_team_stats = get_team_stats(home_team, home_latest_5_games)

    # away team last 5 games
    away_latest_5_games = get_latest_games(away_team, df, num_games=5)
    away_team_stats = get_team_stats(away_team, away_latest_5_games)

    # home team last 5 home games
    latest_5_home_games = get_latest_home_or_away_games(home_team, df, num_games=5, location='home')
    home_team_home_stats = get_team_stats(home_team, latest_5_home_games)
    
    # away team last 5 away games
    latest_5_away_games = get_latest_home_or_away_games(away_team, df, num_games=5, location='away')
    away_team_away_stats = get_team_stats(away_team, latest_5_away_games)

    # last 2 h2h games
    last_2_h2h_games = get_last_2_h2h_games(home_team, away_team, df)
    h2h_stats = get_h2h_stats(home_team, away_team, last_2_h2h_games)

    # last 2 h2h home-away games
    last_2_h2h_games_home_or_away = get_last_2_h2h_home_or_away_games(home_team, away_team, df)
    h2h_home_or_away_stats = get_h2h_home_or_away_stats(home_team, away_team, last_2_h2h_games_home_or_away)

    return list((home_team_stats, away_team_stats, home_team_home_stats, away_team_away_stats, h2h_stats, h2h_home_or_away_stats))


# Main
def get_stats(league, home_team, away_team):

    leagues = {"English Premier League": ['E0', 'epl'], "Scottish Premier League": ['SC0', 'spl'], "Serie A": ['I1', 'sa'], "Bundesliga": ['D1', 'bdl'], "LaLiga": ['SP1', 'llg'], "Ligue 1": ['F1', 'l1'], "Championship": ['E1', 'c']}

    # URL of the CSV file
    url = f'https://www.football-data.co.uk/mmz4281/2425/{leagues[league][0]}.csv'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a file in write-binary mode and save the content
        with open(os.path.join('resources', f'{leagues[league][0]}.csv'), 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")

    # Read old csv file
    df = pd.read_csv(os.path.join('resources', f'{leagues[league][1]}.csv'))
    # Find the index of the column 'DB'
    col_index = df.columns.get_loc('AR')
    # Trim the DataFrame to include columns up to 'DB'
    trimmed_df = df.iloc[:, :col_index + 1]

    # Read new csv file
    new_df = pd.read_csv(os.path.join('resources', f'{leagues[league][0]}.csv'))
    # Trim the DataFrame to include columns up to 'DB'
    trimmed_new_df = new_df.iloc[:, :col_index + 1]

    #Merge to find rows that are in df_new but not in df_old
    df_combined = pd.concat([trimmed_df, trimmed_new_df]).drop_duplicates(keep='first', ignore_index=True)
    # Convert 'Date' to datetime for sorting (if not already datetime)
    df_combined['Date'] = pd.to_datetime(df_combined['Date'], dayfirst=True)

    # Extract stats
    prematch_stats = create_prematch_stats(home_team, away_team, df_combined)

    # Data for last 5 games
    home_team_stats = prematch_stats[0]
    away_team_stats = prematch_stats[1]

    # Data for last 5 home games for home team
    home_team_home_stats = prematch_stats[2]
    # Data for last 5 away games for away team
    away_team_away_stats = prematch_stats[3]

    # Data for last 2 Head-to-Head games (H2H)
    if len(prematch_stats[5]['results']) == 0:
        h2h_stats = None
    else:
        h2h_stats = prematch_stats[4]
    # Data for last 2 Head-to-Head games where home team is home and away team is away (H2H)
    if len(prematch_stats[5]['results']) == 0:
        home_away_h2h_stats = None
    else:
        home_away_h2h_stats = prematch_stats[5]

    predictions = aggregate_team_specific_predictions(home_team, away_team, home_team_home_stats, away_team_away_stats, 
                                                      home_team_stats, away_team_stats, h2h_stats, home_away_h2h_stats)

    return predictions

def aggregate_team_specific_predictions(home_team, away_team, home_team_home_stats, away_team_away_stats, 
                                     home_team_stats, away_team_stats, h2h_stats, home_away_h2h_stats):
    # Define base weights
    base_weights = {
        'home_away_form': 0.25,
        'overall_form': 0.20,
        'opposition_form': 0.20,
        'h2h': 0.15,
        'home_away_h2h': 0.20
    }
    
    # Adjust weights if h2h stats are missing
    def redistribute_weights(weights, missing_keys):
        available_weights = {k: v for k, v in weights.items() if k not in missing_keys}
        total_to_redistribute = sum(weights[k] for k in missing_keys)
        factor = 1 + (total_to_redistribute / sum(available_weights.values()))
        return {k: v * factor for k, v in available_weights.items()}
    
    missing_stats = []
    if h2h_stats is None:
        missing_stats.append('h2h')
    if home_away_h2h_stats is None:
        missing_stats.append('home_away_h2h')
    
    weights = redistribute_weights(base_weights, missing_stats)

    # Calculate result probabilities with available stat types
    home_win_prob = 0
    if 'home_away_form' in weights:
        home_win_prob += (home_team_home_stats["results"].count("Win") / len(home_team_home_stats["results"])) * weights['home_away_form']
    if 'overall_form' in weights:
        home_win_prob += (home_team_stats["results"].count("Win") / len(home_team_stats["results"])) * weights['overall_form']
    if 'opposition_form' in weights:
        home_win_prob += (away_team_away_stats["results"].count("Lose") / len(away_team_away_stats["results"])) * weights['opposition_form']
    if 'h2h' in weights and h2h_stats:
        home_win_prob += (h2h_stats["results"].count(f"{home_team} Win") / len(h2h_stats["results"])) * weights['h2h']
    if 'home_away_h2h' in weights and home_away_h2h_stats:
        home_win_prob += (home_away_h2h_stats["results"].count(f"{home_team} Win") / len(home_away_h2h_stats["results"])) * weights['home_away_h2h']
    home_win_prob *= 100

    # Away win probability with adjusted weights
    away_win_prob = 0
    if 'home_away_form' in weights:
        away_win_prob += (away_team_away_stats["results"].count("Win") / len(away_team_away_stats["results"])) * weights['home_away_form']
    if 'overall_form' in weights:
        away_win_prob += (away_team_stats["results"].count("Win") / len(away_team_stats["results"])) * weights['overall_form']
    if 'opposition_form' in weights:
        away_win_prob += (home_team_home_stats["results"].count("Lose") / len(home_team_home_stats["results"])) * weights['opposition_form']
    if 'h2h' in weights and h2h_stats:
        away_win_prob += (h2h_stats["results"].count(f"{away_team} Win") / len(h2h_stats["results"])) * weights['h2h']
    if 'home_away_h2h' in weights and home_away_h2h_stats:
        away_win_prob += (home_away_h2h_stats["results"].count(f"{away_team} Win") / len(home_away_h2h_stats["results"])) * weights['home_away_h2h']
    away_win_prob *= 100

    # Draw probability with adjusted weights for missing h2h stats
    draw_weights = {
        'home_away_form': 0.30,
        'overall_form': 0.35,
        'h2h': 0.15,
        'home_away_h2h': 0.20
    }
    draw_weights = redistribute_weights(draw_weights, missing_stats)
    
    draw_prob = 0
    if 'home_away_form' in draw_weights:
        draw_prob += ((home_team_home_stats["results"].count("Draw") / len(home_team_home_stats["results"]) +
                      away_team_away_stats["results"].count("Draw") / len(away_team_away_stats["results"])) / 2) * draw_weights['home_away_form']
    if 'overall_form' in draw_weights:
        draw_prob += ((home_team_stats["results"].count("Draw") / len(home_team_stats["results"]) +
                      away_team_stats["results"].count("Draw") / len(away_team_stats["results"])) / 2) * draw_weights['overall_form']
    if 'h2h' in draw_weights and h2h_stats:
        draw_prob += (h2h_stats["results"].count("Draw") / len(h2h_stats["results"])) * draw_weights['h2h']
    if 'home_away_h2h' in draw_weights and home_away_h2h_stats:
        draw_prob += (home_away_h2h_stats["results"].count("Draw") / len(home_away_h2h_stats["results"])) * draw_weights['home_away_h2h']
    draw_prob *= 100

    # Normalize probabilities to sum to 100%
    total_prob = home_win_prob + away_win_prob + draw_prob
    home_win_prob = (home_win_prob / total_prob) * 100
    away_win_prob = (away_win_prob / total_prob) * 100
    draw_prob = (draw_prob / total_prob) * 100

    # BTTS probability with adjusted weights
    btts_weights = {
        'home_away_form': 0.40,  # Increased from 0.20 each
        'overall_form': 0.30,    # Increased from 0.15 each
        'h2h': 0.15,
        'home_away_h2h': 0.15
    }
    btts_weights = redistribute_weights(btts_weights, missing_stats)
    
    btts_prob = 0
    if 'home_away_form' in btts_weights:
        btts_prob += (np.mean(home_team_home_stats["btts"]) + np.mean(away_team_away_stats["btts"])) * (btts_weights['home_away_form'] / 2)
    if 'overall_form' in btts_weights:
        btts_prob += (np.mean(home_team_stats["btts"]) + np.mean(away_team_stats["btts"])) * (btts_weights['overall_form'] / 2)
    if 'h2h' in btts_weights and h2h_stats:
        btts_prob += np.mean(h2h_stats["btts"]) * btts_weights['h2h']
    if 'home_away_h2h' in btts_weights and home_away_h2h_stats:
        btts_prob += np.mean(home_away_h2h_stats["btts"]) * btts_weights['home_away_h2h']
    btts_prob *= 100

    # Helper function for team-specific stats calculation
    def calculate_team_stats(team, team_home_away_stats, team_stats, stat_name):
        weights = {
            'home_away_form': 0.30,
            'overall_form': 0.25,
            'h2h': 0.20,
            'home_away_h2h': 0.25
        }
        weights = redistribute_weights(weights, missing_stats)
        
        team_name_formatted = team.lower().replace(' ', '_')
        result = 0
        
        if 'home_away_form' in weights:
            result += np.mean(team_home_away_stats[f"{stat_name}_for"]) * weights['home_away_form']
        if 'overall_form' in weights:
            result += np.mean(team_stats[f"{stat_name}_for"]) * weights['overall_form']
        if 'h2h' in weights and h2h_stats:
            result += np.mean([h2h_stats[f"{team_name_formatted}_{stat_name}"]]) * weights['h2h']
        if 'home_away_h2h' in weights and home_away_h2h_stats:
            result += np.mean([home_away_h2h_stats[f"{team_name_formatted}_{stat_name}"]]) * weights['home_away_h2h']
            
        return result

    # Calculate team-specific statistics for both teams
    stats_categories = ['goals', 'shots_on_target', 'corners', 'cards']
    home_team_predicted_stats = {
        f"expected_{stat}": calculate_team_stats(home_team, home_team_home_stats, home_team_stats, stat)
        for stat in stats_categories
    }
    
    away_team_predicted_stats = {
        f"expected_{stat}": calculate_team_stats(away_team, away_team_away_stats, away_team_stats, stat)
        for stat in stats_categories
    }

    # Calculate expected total goals with adjusted weights
    total_goals_weights = {
        'home_away_form': 0.25,
        'overall_form': 0.25,
        'h2h': 0.20,
        'home_away_h2h': 0.30
    }
    total_goals_weights = redistribute_weights(total_goals_weights, missing_stats)
    
    expected_total_goals = 0
    if 'home_away_form' in total_goals_weights:
        expected_total_goals += ((np.mean(home_team_home_stats["goals"]) + np.mean(away_team_away_stats["goals"])) / 2) * total_goals_weights['home_away_form']
    if 'overall_form' in total_goals_weights:
        expected_total_goals += ((np.mean(home_team_stats["goals"]) + np.mean(away_team_stats["goals"])) / 2) * total_goals_weights['overall_form']
    if 'h2h' in total_goals_weights and h2h_stats:
        expected_total_goals += np.mean(h2h_stats["goals"]) * total_goals_weights['h2h']
    if 'home_away_h2h' in total_goals_weights and home_away_h2h_stats:
        expected_total_goals += np.mean(home_away_h2h_stats["goals"]) * total_goals_weights['home_away_h2h']

    return {
        "home_win_prob": home_win_prob,
        "away_win_prob": away_win_prob,
        "draw_prob": draw_prob,
        "btts_prob": btts_prob,
        "expected_total_goals": expected_total_goals,
        "home_team_stats": home_team_predicted_stats,
        "away_team_stats": away_team_predicted_stats
    }
