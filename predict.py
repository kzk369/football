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
    
    # Uncomment if you want to calculate GK saves
    # gk_saves_for = list(np.subtract(shots_on_target_for, goals_for)) 
    # gk_saves_against = list(np.subtract(shots_on_target_against, goals_against))

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
        # Uncomment if you want to calculate GK saves
        # "gk_saves_for": gk_saves_for,
        # "gk_saves_against": gk_saves_against,
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
    
    # Uncomment if you want to calculate GK saves
    # gk_saves_for = list(np.subtract(shots_on_target_for, goals_for)) 
    # gk_saves_against = list(np.subtract(shots_on_target_against, goals_against))

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
        # Uncomment if you want to calculate GK saves
        # "gk_saves_for": gk_saves_for,
        # "gk_saves_against": gk_saves_against,
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
    
    # Uncomment if you want to calculate GK saves
    # gk_saves_for = list(np.subtract(shots_on_target_for, goals_for)) 
    # gk_saves_against = list(np.subtract(shots_on_target_against, goals_against))

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
        # Uncomment if you want to calculate GK saves
        # "gk_saves_for": gk_saves_for,
        # "gk_saves_against": gk_saves_against,
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

    leagues = {"English Premier League": ['E0', 'epl'], "Scottish Premier League": ['SC0', 'spl'], "Serie A": ['I1', 'sa']}

    # URL of the CSV file
    url = f'https://www.football-data.co.uk/mmz4281/2425/{leagues[league][0]}.csv'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a file in write-binary mode and save the content
        with open(os.path.join('resources', f'{leagues[league][0]}.csv'), 'wb') as file:
            file.write(response.content)
        print("CSV file has been downloaded successfully.")
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
    h2h_stats = prematch_stats[4]
    # Data for last 2 Head-to-Head games where home team is home and away team is away (H2H)
    home_away_h2h_stats = prematch_stats[5]

    predictions = aggregate_team_specific_predictions(home_team, away_team, home_team_home_stats, away_team_away_stats, 
                                                      home_team_stats, away_team_stats, h2h_stats, home_away_h2h_stats)

    return predictions

# # URL of the CSV file
# url = 'https://www.football-data.co.uk/mmz4281/2425/E0.csv'

# # Send a GET request to the URL
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Open a file in write-binary mode and save the content
#     with open('e0.csv', 'wb') as file:
#         file.write(response.content)
#     print("CSV file has been downloaded successfully.")
# else:
#     print(f"Failed to retrieve the file. Status code: {response.status_code}")
    
# # Read old csv file
# df = pd.read_csv('epl.csv')
# # Find the index of the column 'DB'
# col_index = df.columns.get_loc('AR')
# # Trim the DataFrame to include columns up to 'DB'
# trimmed_df = df.iloc[:, :col_index + 1]

# # Read new csv file
# new_df = pd.read_csv('e0.csv')
# # Trim the DataFrame to include columns up to 'DB'
# trimmed_new_df = new_df.iloc[:, :col_index + 1]

# #Merge to find rows that are in df_new but not in df_old
# df_combined = pd.concat([trimmed_df, trimmed_new_df]).drop_duplicates(keep='first', ignore_index=True)
# # Convert 'Date' to datetime for sorting (if not already datetime)
# df_combined['Date'] = pd.to_datetime(df_combined['Date'], dayfirst=True)

# # Set teams using user input
# home_team = input("\nEnter Home Team: ").title()
# away_team = input("\nEnter Away Team: ").title()

# if home_team == "Nott'M Forest":
#     home_team = "Nott'm Forest"
# elif away_team == "Nott'M Forest":
#     away_team = "Nott'm Forest"

# # Extract stats
# prematch_stats = create_prematch_stats(home_team, away_team, df_combined)

# # Data for last 5 games
# home_team_stats = prematch_stats[0]
# away_team_stats = prematch_stats[1]

# # Data for last 5 home games for home team
# home_team_home_stats = prematch_stats[2]
# # Data for last 5 away games for away team
# away_team_away_stats = prematch_stats[3]

# # Data for last 2 Head-to-Head games (H2H)
# h2h_stats = prematch_stats[4]
# # Data for last 2 Head-to-Head games where home team is home and away team is away (H2H)
# home_away_h2h_stats = prematch_stats[5]


# Calculations
def calculate_averages_and_probs(stats):
    averages = {}
    probabilities = {}
    for key, values in stats.items():
        if isinstance(values[0], (int, float)):
            averages[key] = np.mean(values)
        elif isinstance(values[0], str):
            total_games = len(values)
            probabilities[key] = {outcome: values.count(outcome) / total_games * 100 for outcome in set(values)}
    return averages, probabilities

def aggregate_team_specific_predictions(home_team, away_team, home_team_home_stats, away_team_away_stats, 
                                     home_team_stats, away_team_stats, h2h_stats, home_away_h2h_stats):
    # Calculate base averages and probabilities for all stat types
    home_avg, home_probs = calculate_averages_and_probs(home_team_home_stats)
    away_avg, away_probs = calculate_averages_and_probs(away_team_away_stats)
    home_overall_avg, home_overall_probs = calculate_averages_and_probs(home_team_stats)
    away_overall_avg, away_overall_probs = calculate_averages_and_probs(away_team_stats)
    h2h_avg, h2h_probs = calculate_averages_and_probs(h2h_stats)
    home_away_h2h_avg, home_away_h2h_probs = calculate_averages_and_probs(home_away_h2h_stats)

    # Calculate result probabilities with all stat types
    # Home win probability (25% home form, 20% overall form, 20% away opposition form, 15% h2h, 20% home/away h2h)
    home_win_prob = (
        (home_team_home_stats["results"].count("Win") / len(home_team_home_stats["results"])) * 0.25 +
        (home_team_stats["results"].count("Win") / len(home_team_stats["results"])) * 0.20 +
        (away_team_away_stats["results"].count("Lose") / len(away_team_away_stats["results"])) * 0.20 +
        (h2h_stats["results"].count(f"{home_team} Win") / len(h2h_stats["results"])) * 0.15 +
        (home_away_h2h_stats["results"].count(f"{home_team} Win") / len(home_away_h2h_stats["results"])) * 0.20
    ) * 100

    # Away win probability (25% away form, 20% overall form, 20% home opposition form, 15% h2h, 20% home/away h2h)
    away_win_prob = (
        (away_team_away_stats["results"].count("Win") / len(away_team_away_stats["results"])) * 0.25 +
        (away_team_stats["results"].count("Win") / len(away_team_stats["results"])) * 0.20 +
        (home_team_home_stats["results"].count("Lose") / len(home_team_home_stats["results"])) * 0.20 +
        (h2h_stats["results"].count(f"{away_team} Win") / len(h2h_stats["results"])) * 0.15 +
        (home_away_h2h_stats["results"].count(f"{away_team} Win") / len(home_away_h2h_stats["results"])) * 0.20
    ) * 100

    # Draw probability (30% combined home/away draw rate, 35% overall draw rate, 15% h2h, 20% home/away h2h)
    draw_prob = (
        ((home_team_home_stats["results"].count("Draw") / len(home_team_home_stats["results"]) +
          away_team_away_stats["results"].count("Draw") / len(away_team_away_stats["results"])) / 2) * 0.30 +
        ((home_team_stats["results"].count("Draw") / len(home_team_stats["results"]) +
          away_team_stats["results"].count("Draw") / len(away_team_stats["results"])) / 2) * 0.35 +
        (h2h_stats["results"].count("Draw") / len(h2h_stats["results"])) * 0.15 +
        (home_away_h2h_stats["results"].count("Draw") / len(home_away_h2h_stats["results"])) * 0.20
    ) * 100

    # Normalize probabilities to sum to 100%
    total_prob = home_win_prob + away_win_prob + draw_prob
    home_win_prob = (home_win_prob / total_prob) * 100
    away_win_prob = (away_win_prob / total_prob) * 100
    draw_prob = (draw_prob / total_prob) * 100

    # Calculate BTTS probability (20% each team's home/away, 15% each team's overall, 15% h2h, 15% home/away h2h)
    btts_prob = (
        np.mean(home_team_home_stats["btts"]) * 0.20 +
        np.mean(away_team_away_stats["btts"]) * 0.20 +
        np.mean(home_team_stats["btts"]) * 0.15 +
        np.mean(away_team_stats["btts"]) * 0.15 +
        np.mean(h2h_stats["btts"]) * 0.15 +
        np.mean(home_away_h2h_stats["btts"]) * 0.15
    ) * 100

    # Calculate team-specific statistics for home team
    home_team_predicted_stats = {
        "expected_goals": (
            np.mean(home_team_home_stats["goals_for"]) * 0.30 +
            np.mean(home_team_stats["goals_for"]) * 0.25 +
            np.mean([h2h_stats[f"{home_team.lower().replace(' ', '_')}_goals"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{home_team.lower().replace(' ', '_')}_goals"]]) * 0.25
        ),
        "shots_on_target": (
            np.mean(home_team_home_stats["shots_on_target_for"]) * 0.30 +
            np.mean(home_team_stats["shots_on_target_for"]) * 0.25 +
            np.mean([h2h_stats[f"{home_team.lower().replace(' ', '_')}_shots_on_target"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{home_team.lower().replace(' ', '_')}_shots_on_target"]]) * 0.25
        ),
        "corners": (
            np.mean(home_team_home_stats["corners_for"]) * 0.30 +
            np.mean(home_team_stats["corners_for"]) * 0.25 +
            np.mean([h2h_stats[f"{home_team.lower().replace(' ', '_')}_corners"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{home_team.lower().replace(' ', '_')}_corners"]]) * 0.25
        ),
        "cards": (
            np.mean(home_team_home_stats["cards_for"]) * 0.30 +
            np.mean(home_team_stats["cards_for"]) * 0.25 +
            np.mean([h2h_stats[f"{home_team.lower().replace(' ', '_')}_cards"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{home_team.lower().replace(' ', '_')}_cards"]]) * 0.25
        )
    }

    # Calculate team-specific statistics for away team
    away_team_predicted_stats = {
        "expected_goals": (
            np.mean(away_team_away_stats["goals_for"]) * 0.30 +
            np.mean(away_team_stats["goals_for"]) * 0.25 +
            np.mean([h2h_stats[f"{away_team.lower().replace(' ', '_')}_goals"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{away_team.lower().replace(' ', '_')}_goals"]]) * 0.25
        ),
        "shots_on_target": (
            np.mean(away_team_away_stats["shots_on_target_for"]) * 0.30 +
            np.mean(away_team_stats["shots_on_target_for"]) * 0.25 +
            np.mean([h2h_stats[f"{away_team.lower().replace(' ', '_')}_shots_on_target"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{away_team.lower().replace(' ', '_')}_shots_on_target"]]) * 0.25
        ),
        "corners": (
            np.mean(away_team_away_stats["corners_for"]) * 0.30 +
            np.mean(away_team_stats["corners_for"]) * 0.25 +
            np.mean([h2h_stats[f"{away_team.lower().replace(' ', '_')}_corners"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{away_team.lower().replace(' ', '_')}_corners"]]) * 0.25
        ),
        "cards": (
            np.mean(away_team_away_stats["cards_for"]) * 0.30 +
            np.mean(away_team_stats["cards_for"]) * 0.25 +
            np.mean([h2h_stats[f"{away_team.lower().replace(' ', '_')}_cards"]]) * 0.20 +
            np.mean([home_away_h2h_stats[f"{away_team.lower().replace(' ', '_')}_cards"]]) * 0.25
        )
    }

    # Calculate expected total goals (25% home/away average, 25% overall average, 25% h2h, 25% home/away h2h)
    expected_total_goals = (
        ((np.mean(home_team_home_stats["goals"]) + np.mean(away_team_away_stats["goals"])) / 2) * 0.25 +
        ((np.mean(home_team_stats["goals"]) + np.mean(away_team_stats["goals"])) / 2) * 0.25 +
        np.mean(h2h_stats["goals"]) * 0.20 +
        np.mean(home_away_h2h_stats["goals"]) * 0.30
    )

    return {
        "home_win_prob": home_win_prob,
        "away_win_prob": away_win_prob,
        "draw_prob": draw_prob,
        "btts_prob": btts_prob,
        "expected_total_goals": expected_total_goals,
        "home_team_stats": home_team_predicted_stats,
        "away_team_stats": away_team_predicted_stats
    }

# # Generate predictions using all available stats
# predictions = aggregate_team_specific_predictions(
#     home_team,
#     away_team,
#     home_team_home_stats,
#     away_team_away_stats,
#     home_team_stats,
#     away_team_stats,
#     h2h_stats,
#     home_away_h2h_stats
# )

# # Output predictions
# print(f"Predictions for {home_team} (Home) vs. {away_team} (Away):")
# print("\nResult Probabilities:")
# print(f"\n{home_team} Win: {predictions['home_win_prob']:.2f}%")
# print(f"{away_team} Win: {predictions['away_win_prob']:.2f}%")
# print(f"Draw: {predictions['draw_prob']:.2f}%")
# print(f"Both Teams to Score (BTTS) Probability: {predictions['btts_prob']:.2f}%")
# print(f"\nExpected Goals:")
# print(f"\nExpected Total Goals: {predictions['expected_total_goals']:.2f}")
# print(f"{home_team} Expected Goals: {predictions['home_team_stats']['expected_goals']:.2f}")
# print(f"{away_team} Expected Goals: {predictions['away_team_stats']['expected_goals']:.2f}")
# print(f"\nTeam Statistics Predictions:")
# print(f"\n{home_team} expected shots on target: {predictions['home_team_stats']['shots_on_target']:.2f}")
# print(f"{away_team} expected shots on target: {predictions['away_team_stats']['shots_on_target']:.2f}")
# print(f"Expected Total Corners: {predictions['home_team_stats']['corners']+predictions['away_team_stats']['corners']:.2f}")
# print(f"{home_team} expected corners: {predictions['home_team_stats']['corners']:.2f}")
# print(f"{away_team} expected corners: {predictions['away_team_stats']['corners']:.2f}")
# print(f"Expected Total Cards: {predictions['home_team_stats']['cards']+predictions['away_team_stats']['cards']:.2f}")
# print(f"{home_team} expected cards: {predictions['home_team_stats']['cards']:.2f}")
# print(f"{away_team} expected cards: {predictions['away_team_stats']['cards']:.2f}")


# Visuals

# Team color pairings
team_colors = {
    'Arsenal': {'home_color': 'Red', 'away_color': 'Pan African'},  # Updated: Black with red/green accents
    'Aston Villa': {'home_color': 'Claret', 'away_color': 'White'},  # Updated: White with claret/blue stripes
    'Bournemouth': {'home_color': 'Cherry Red', 'away_color': 'Green Purple'},  # Updated: Pizza shirt inspired
    'Brentford': {'home_color': 'Red', 'away_color': 'Light Pink'},  # Updated: Pink with purple accents
    'Brighton': {'home_color': 'Royal Blue', 'away_color': 'Gold Navy'},  # Updated: Gold with navy pinstripes
    'Chelsea': {'home_color': 'Royal Blue', 'away_color': 'Guava Ice'},  # Updated: Orange-tinted
    'Crystal Palace': {'home_color': 'Royal Blue', 'away_color': 'Yellow Blue'},  # Updated: Yellow and blue
    'Everton': {'home_color': 'Royal Blue', 'away_color': 'Black Yellow'},  # Updated: Black with yellow trim
    'Fulham': {'home_color': 'White', 'away_color': 'Black Red'},  # Updated: Black and red stripes
    'Ipswich': {'home_color': 'Blue', 'away_color': 'Maroon Gold'},  # Updated: Maroon with gold details
    'Leicester': {'home_color': 'Blue', 'away_color': 'Black Orange'},  # Updated: Black with orange/red pattern
    'Liverpool': {'home_color': 'Red', 'away_color': 'Night Forest'},  # Updated: Dark green with teal
    'Man City': {'home_color': 'Sky Blue', 'away_color': 'Neon Yellow Navy'},  # Updated: Yellow/navy stripes
    'Man United': {'home_color': 'Red', 'away_color': 'Royal Navy'},  # Updated: Royal blue with navy pattern
    'Newcastle': {'home_color': 'Black', 'away_color': 'Burgundy Navy'},  # Updated: Burgundy/navy hoops
    "Nott'm Forest": {'home_color': 'Garibaldi Red', 'away_color': 'Grey Pink'},  # Updated: Grey with pink
    'Southampton': {'home_color': 'Red', 'away_color': 'Fizzy Yellow'},  # Updated: Yellow with navy trim
    'Tottenham': {'home_color': 'White', 'away_color': 'Light Blue'},  # Updated: Light blue stripes
    'West Ham': {'home_color': 'Claret', 'away_color': 'Black Accent'},  # Updated: Black with claret/blue
    'Wolves': {'home_color': 'Old Gold', 'away_color': 'Black Gold'}  # Updated: Black with gold accents
}

color_name_to_hex = {
    # Home colors
    'Red': '#FF0000',
    'Cherry Red': '#960018',
    'Garibaldi Red': '#DB0007',
    'White': '#FFFFFF',
    'Royal Blue': '#002366',
    'Sky Blue': '#87CEEB',
    'Black': '#000000',
    'Old Gold': '#CFB53B',
    'Claret': '#7B1FA2',
    'Blue': '#0000FF',
    
    # Away colors
    'Pan African': '#000000',  # Base color (has red/green accents)
    'Light Pink': '#FFB6C1',
    'Gold Navy': '#FFD700',  # Base gold color
    'Guava Ice': '#FF9980',
    'Yellow Blue': '#FFD700',  # Base yellow color
    'Black Yellow': '#000000',  # Base black color
    'Black Red': '#000000',  # Base for striped pattern
    'Maroon Gold': '#800000',
    'Black Orange': '#000000',  # Base for patterned design
    'Night Forest': '#004D40',
    'Neon Yellow Navy': '#FFFF00',  # Base neon yellow
    'Royal Navy': '#4169E1',
    'Burgundy Navy': '#800020',  # Base burgundy color
    'Grey Pink': '#808080',  # Base grey color
    'Fizzy Yellow': '#FFFF66',
    'Light Blue': '#ADD8E6',
    'Black Accent': '#000000',  # Base black color
    'Black Gold': '#000000'  # Base black color
}

def get_team_color(team_name, is_home, team_colors):
    if team_name not in team_colors:
        return '#808080'  # Default gray if team not found
    
    color_name = team_colors[team_name]['home_color'] if is_home else team_colors[team_name]['away_color']
    return color_name_to_hex.get(color_name, '#808080')

def create_form_visualizations(prematch_stats, home_team, away_team, team_colors):
    # Get team colors
    home_color = get_team_color(home_team, True, team_colors)
    away_color = get_team_color(away_team, False, team_colors)
    
    # 1. Last 5 Games Results
    fig_results = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'{home_team} Last 5 Games', f'{away_team} Last 5 Games')
    )
    
    # Home team results
    results_home = prematch_stats[0]['results']
    colors_home = ['green' if x == 'Win' else 'yellow' if x == 'Draw' else 'red' for x in results_home]
    
    fig_results.add_trace(
        go.Bar(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=[1]*5, marker_color=colors_home,
               text=results_home, textposition='auto', name=home_team),
        row=1, col=1
    )
    
    # Away team results
    results_away = prematch_stats[1]['results']
    colors_away = ['green' if x == 'Win' else 'yellow' if x == 'Draw' else 'red' for x in results_away]
    
    fig_results.add_trace(
        go.Bar(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=[1]*5, marker_color=colors_away,
               text=results_away, textposition='auto', name=away_team),
        row=2, col=1
    )
    
    fig_results.update_layout(
        title='Last 5 Games Results',
        showlegend=False,
        paper_bgcolor='#F5F5DC',
        height=400
    )
    fig_results.show()
    
    # 2. Goals Analysis
    fig_goals = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Goals Scored', 'Goals Conceded')
    )
    
    fig_goals.add_trace(
        go.Bar(name=home_team, x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], 
               y=prematch_stats[0]['goals_for'], marker_color=home_color),
        row=1, col=1
    )
    fig_goals.add_trace(
        go.Bar(name=away_team, x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], 
               y=prematch_stats[1]['goals_for'], marker_color=away_color),
        row=1, col=1
    )
    
    fig_goals.add_trace(
        go.Bar(name=home_team, x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], 
               y=prematch_stats[0]['goals_against'], marker_color=home_color),
        row=1, col=2
    )
    fig_goals.add_trace(
        go.Bar(name=away_team, x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], 
               y=prematch_stats[1]['goals_against'], marker_color=away_color),
        row=1, col=2
    )
    
    fig_goals.update_layout(
        title='Goals Analysis - Last 5 Games',
        barmode='group',
        paper_bgcolor='#F5F5DC',
        height=400
    )
    fig_goals.show()
    
    # 3. Performance Metrics
    fig_metrics = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Shots on Target', 'Corners', 'Cards', 'BTTS')
    )
    
    # Shots on Target
    fig_metrics.add_trace(
        go.Scatter(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=prematch_stats[0]['shots_on_target_for'],
                  name=f'{home_team} For', line=dict(color=home_color)),
        row=1, col=1
    )
    fig_metrics.add_trace(
        go.Scatter(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=prematch_stats[1]['shots_on_target_for'],
                  name=f'{away_team} For', line=dict(color=away_color)),
        row=1, col=1
    )
    
    # Corners
    fig_metrics.add_trace(
        go.Scatter(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=prematch_stats[0]['corners_for'],
                  name=f'{home_team} For', line=dict(color=home_color)),
        row=1, col=2
    )
    fig_metrics.add_trace(
        go.Scatter(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=prematch_stats[1]['corners_for'],
                  name=f'{away_team} For', line=dict(color=away_color)),
        row=1, col=2
    )
    
    # Cards
    fig_metrics.add_trace(
        go.Scatter(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=prematch_stats[0]['cards_for'],
                  name=home_team, line=dict(color=home_color)),
        row=2, col=1
    )
    fig_metrics.add_trace(
        go.Scatter(x=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'], y=prematch_stats[1]['cards_for'],
                  name=away_team, line=dict(color=away_color)),
        row=2, col=1
    )
    
    # BTTS
    fig_metrics.add_trace(
        go.Bar(x=[home_team, away_team],
               y=[sum(prematch_stats[0]['btts'])/5*100, 
                  sum(prematch_stats[1]['btts'])/5*100],
               marker_color=[home_color, away_color],
               text=[f"{sum(prematch_stats[0]['btts'])/5*100:.0f}%",
                     f"{sum(prematch_stats[1]['btts'])/5*100:.0f}%"],
               textposition='auto',
               name="Probability"),
        row=2, col=2
    )
    
    fig_metrics.update_layout(
        title='Performance Metrics - Last 5 Games',
        height=600,
        paper_bgcolor='#F5F5DC',
        showlegend=True
    )
    fig_metrics.show()
    
    # 4. Last 5 Games Form Analysis
    if len(prematch_stats) > 4:
        fig_l5 = go.Figure()
        
        l5f_stats = prematch_stats[0]
        
        # Create table for H2H stats
        fig_l5 = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'],
                fill_color='#E5ECF6',
                align='left'
            ),
            cells=dict(
                values = [
                            # Heading row
                            ['Result', 'Goals', f"{home_team} Goals", "Opposition Goals", 'BTTS', 'Corners', f"{home_team} Corners", "Opposition Corners", 'Cards', f"{home_team} Cards", "Opposition Cards"],
                            # Data rows
                            *[
                                [
                                    l5f_stats['results'][i],
                                    l5f_stats['goals'][i],
                                    l5f_stats["goals_for"][i],
                                    l5f_stats["goals_against"][i],
                                    'Yes' if l5f_stats['btts'][i] else 'No',
                                    l5f_stats['corners'][i],
                                    l5f_stats["corners_for"][i],
                                    l5f_stats["corners_against"][i],
                                    l5f_stats['cards'][i],
                                    l5f_stats["cards_for"][i],
                                    l5f_stats["cards_against"][i]
                                ]
                                for i in range(0, 5)  # Index from 1 to 4
                            ]
                        ],
                align='left'
            )
        )])
        
        fig_l5.update_layout(
            title=f'{home_team} Form Analysis - Last 5 Games',
            height=500
        )
        fig_l5.show()

        fig_l5 = go.Figure()
        
        lfa_stats = prematch_stats[3]
        
        # Create table for H2H stats
        fig_l5 = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'],
                fill_color='#E5ECF6',
                align='left'
            ),
            cells=dict(
                values = [
                            # Heading row
                            ['Result', 'Goals', f"{away_team} Goals", "Opposition Goals", 'BTTS', 'Corners', f"{away_team} Corners", "Opposition Corners", 'Cards', f"{away_team} Cards", "Opposition Cards"],
                            # Data rows
                            *[
                                [
                                    lfa_stats['results'][i],
                                    lfa_stats['goals'][i],
                                    lfa_stats["goals_for"][i],
                                    lfa_stats["goals_against"][i],
                                    'Yes' if lfa_stats['btts'][i] else 'No',
                                    lfa_stats['corners'][i],
                                    lfa_stats["corners_for"][i],
                                    lfa_stats["corners_against"][i],
                                    lfa_stats['cards'][i],
                                    lfa_stats["cards_for"][i],
                                    lfa_stats["cards_against"][i]
                                ]
                                for i in range(0, 5)  # Index from 1 to 4
                            ]
                        ],
                align='left'
            )
        )])
        
        fig_l5.update_layout(
            title=f'{away_team} Form Analysis - Last 5 Games',
            height=500
        )
        fig_l5.show()

     # 4. Home/Away Analysis
    if len(prematch_stats) > 4:
        fig_h = go.Figure()
        
        h_stats = prematch_stats[2]
        
        # Create table for H2H stats
        fig_h = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'],
                fill_color='#E5ECF6',
                align='left'
            ),
            cells=dict(
                values = [
                            # Heading row
                            ['Result', 'Goals', f"{home_team} Goals", "Opposition Goals", 'BTTS', 'Corners', f"{home_team} Corners", "Opposition Corners", 'Cards', f"{home_team} Cards", "Opposition Cards"],
                            # Data rows
                            *[
                                [
                                    h_stats['results'][i],
                                    h_stats['goals'][i],
                                    h_stats["goals_for"][i],
                                    h_stats["goals_against"][i],
                                    'Yes' if h_stats['btts'][i] else 'No',
                                    h_stats['corners'][i],
                                    h_stats["corners_for"][i],
                                    h_stats["corners_against"][i],
                                    h_stats['cards'][i],
                                    h_stats["cards_for"][i],
                                    h_stats["cards_against"][i]
                                ]
                                for i in range(0, 5)  # Index from 1 to 4
                            ]
                        ],
                align='left'
            )
        )])
        
        fig_h.update_layout(
            title=f'{home_team} Home Form Analysis - Last 5 Games',
            height=500
        )
        fig_h.show()

        fig_a = go.Figure()
        
        a_stats = prematch_stats[3]
        
        # Create table for H2H stats
        fig_a = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'],
                fill_color='#E5ECF6',
                align='left'
            ),
            cells=dict(
                values = [
                            # Heading row
                            ['Result', 'Goals', f"{away_team} Goals", "Opposition Goals", 'BTTS', 'Corners', f"{away_team} Corners", "Opposition Corners", 'Cards', f"{away_team} Cards", "Opposition Cards"],
                            # Data rows
                            *[
                                [
                                    a_stats['results'][i],
                                    a_stats['goals'][i],
                                    a_stats["goals_for"][i],
                                    a_stats["goals_against"][i],
                                    'Yes' if a_stats['btts'][i] else 'No',
                                    a_stats['corners'][i],
                                    a_stats["corners_for"][i],
                                    a_stats["corners_against"][i],
                                    a_stats['cards'][i],
                                    a_stats["cards_for"][i],
                                    a_stats["cards_against"][i]
                                ]
                                for i in range(0, 5)  # Index from 1 to 4
                            ]
                        ],
                align='left'
            )
        )])
        
        fig_a.update_layout(
            title=f'{away_team} Away Form Analysis - Last 5 Games',
            height=500
        )
        fig_a.show()
    
    # 5. Head-to-Head Analysis
    if len(prematch_stats) > 4:
        fig_h2h = go.Figure()
        
        h2h_stats = prematch_stats[4]
        
        # Create table for H2H stats
        fig_h2h = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Game 1', 'Game 2'],
                fill_color='#E5ECF6',
                align='left'
            ),
            cells=dict(
                values=[
                    ['Result', 'Goals', f"{home_team} Goals", f"{away_team} Goals", 'BTTS', 'Corners', f"{home_team} Corners", f"{away_team} Corners", 'Cards', f"{home_team} Cards", f"{away_team} Cards"],
                    [h2h_stats['results'][0], 
                     h2h_stats['goals'][0],
                     h2h_stats[f"{home_team.lower().replace(' ', '_')}_goals"][0],
                     h2h_stats[f"{away_team.lower().replace(' ', '_')}_goals"][0],
                     'Yes' if h2h_stats['btts'][0] else 'No',
                     h2h_stats['corners'][0],
                     h2h_stats[f"{home_team.lower().replace(' ', '_')}_corners"][0],
                     h2h_stats[f"{away_team.lower().replace(' ', '_')}_corners"][0],
                     h2h_stats['cards'][0],
                    h2h_stats[f"{home_team.lower().replace(' ', '_')}_cards"][0],
                     h2h_stats[f"{away_team.lower().replace(' ', '_')}_cards"][0]],
                    [h2h_stats['results'][1],
                     h2h_stats['goals'][1],
                     h2h_stats[f"{home_team.lower().replace(' ', '_')}_goals"][1],
                     h2h_stats[f"{away_team.lower().replace(' ', '_')}_goals"][1],
                     'Yes' if h2h_stats['btts'][1] else 'No',
                     h2h_stats['corners'][1],
                     h2h_stats[f"{home_team.lower().replace(' ', '_')}_corners"][1],
                     h2h_stats[f"{away_team.lower().replace(' ', '_')}_corners"][1],
                     h2h_stats['cards'][1],
                    h2h_stats[f"{home_team.lower().replace(' ', '_')}_cards"][1],
                     h2h_stats[f"{away_team.lower().replace(' ', '_')}_cards"][1]]
                ],
                align='left'
            )
        )])
        
        fig_h2h.update_layout(
            title='Head-to-Head Analysis - Last 2 Games',
            height=500
        )
        fig_h2h.show()

    if len(prematch_stats) > 4:
        fig_h2h_ha = go.Figure()
        
        h2h_ha_stats = prematch_stats[5]
        
        # Create table for H2H stats
        if len(h2h_ha_stats['results']) > 1:
            
            fig_h2h_ha = go.Figure(data=[go.Table(
                header=dict(
                    values=['Metric', 'Game 1', 'Game 2'],
                    fill_color='#E5ECF6',
                    align='left'
                ),
                cells=dict(
                    values=[
                        ['Result', 'Goals', f"{home_team} Goals", f"{away_team} Goals", 'BTTS', 'Corners', f"{home_team} Corners", f"{away_team} Corners", 'Cards', f"{home_team} Cards", f"{away_team} Cards"],
                        [h2h_ha_stats['results'][0], 
                         h2h_ha_stats['goals'][0],
                         h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_goals"][0],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_goals"][0],
                         'Yes' if h2h_ha_stats['btts'][0] else 'No',
                         h2h_ha_stats['corners'][0],
                         h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_corners"][0],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_corners"][0],
                         h2h_ha_stats['cards'][0],
                        h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_cards"][0],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_cards"][0]],
                        [h2h_ha_stats['results'][1],
                         h2h_ha_stats['goals'][1],
                         h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_goals"][1],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_goals"][1],
                         'Yes' if h2h_ha_stats['btts'][1] else 'No',
                         h2h_ha_stats['corners'][1],
                         h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_corners"][1],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_corners"][1],
                         h2h_ha_stats['cards'][1],
                        h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_cards"][1],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_cards"][1]]
                    ],
                    align='left'
                )
            )])
        else:
            fig_h2h_ha = go.Figure(data=[go.Table(
                header=dict(
                    values=['Metric', 'Game 1'],
                    fill_color='#E5ECF6',
                    align='left'
                ),
                cells=dict(
                    values=[
                        ['Result', 'Goals', f"{home_team} Goals", f"{away_team} Goals", 'BTTS', 'Corners', f"{home_team} Corners", f"{away_team} Corners", 'Cards', f"{home_team} Cards", f"{away_team} Cards"],
                        [h2h_ha_stats['results'][0], 
                         h2h_ha_stats['goals'][0],
                         h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_goals"][0],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_goals"][0],
                         'Yes' if h2h_ha_stats['btts'][0] else 'No',
                         h2h_ha_stats['corners'][0],
                         h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_corners"][0],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_corners"][0],
                         h2h_ha_stats['cards'][0],
                        h2h_ha_stats[f"{home_team.lower().replace(' ', '_')}_cards"][0],
                         h2h_ha_stats[f"{away_team.lower().replace(' ', '_')}_cards"][0]]
                    ],
                    align='left'
                )
            )])
        
        fig_h2h_ha.update_layout(
            title=f"Head-to-Head {home_team} (Home) vs {away_team} (Away) Analysis - Last {len(h2h_ha_stats['results'])} Game{'s'*(len(h2h_ha_stats['results'])-1)}",
            height=500
        )
        fig_h2h_ha.show()


def create_visualizations(predictions, home_team, away_team, team_colors):
    # Get team colors
    home_color = get_team_color(home_team, True, team_colors)
    away_color = get_team_color(away_team, False, team_colors)
    
    # 1. Probability Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = predictions['home_win_prob'],
        title = {'text': f"{home_team} Win Probability"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': home_color},
            'steps': [
                {'range': [0, 30], 'color': 'lightgray'},
                {'range': [30, 70], 'color': 'gray'},
                {'range': [70, 100], 'color': 'darkgray'}
            ],
        }
    ))
    fig_gauge.update_layout(
        height=300,
        paper_bgcolor='#F5F5DC',
        template='plotly_white'
    )
    fig_gauge.show()

    # 2. Result Probabilities Pie Chart
    fig_pie = go.Figure(data=[go.Pie(
        labels=[f'{home_team} Win', f'{away_team} Win', 'Draw'],
        values=[predictions['home_win_prob'], 
                predictions['away_win_prob'], 
                predictions['draw_prob']],
        hole=.3,
        marker_colors=[home_color, away_color, '#808080']
    )])
    fig_pie.update_layout(
        title='Match Result Probabilities',
        paper_bgcolor='#F5F5DC'
    )
    fig_pie.show()

    # 3. Team Statistics Comparison
    fig_stats = go.Figure(data=[
        go.Bar(name=home_team, x=['Shots on Target', 'Corners', 'Cards'], 
               y=[predictions['home_team_stats']['shots_on_target'],
                  predictions['home_team_stats']['corners'],
                  predictions['home_team_stats']['cards']],
               marker_color=home_color),
        go.Bar(name=away_team, x=['Shots on Target', 'Corners', 'Cards'], 
               y=[predictions['away_team_stats']['shots_on_target'],
                  predictions['away_team_stats']['corners'],
                  predictions['away_team_stats']['cards']],
               marker_color=away_color)
    ])
    fig_stats.update_layout(
        title='Predicted Team Statistics Comparison',
        barmode='group',
        paper_bgcolor='#F5F5DC'
    )
    fig_stats.show()

    # 4. BTTS and Goals Prediction
    fig_goals = make_subplots(rows=1, cols=2, 
                             specs=[[{"type": "indicator"}, {"type": "indicator"}]])

    fig_goals.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=predictions['btts_prob'],
            title={'text': "Both Teams to Score Probability (%)"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': '#228B22'}},
            domain={'row': 0, 'column': 0}
        ),
        row=1, col=1
    )

    fig_goals.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=predictions['expected_total_goals'],
            title={'text': "Expected Total Goals"},
            gauge={'axis': {'range': [0, 5]},
                   'bar': {'color': '#228B22'}},
            domain={'row': 0, 'column': 1}
        ),
        row=1, col=2
    )
    
    fig_goals.update_layout(
        height=300,
        paper_bgcolor='#F5F5DC',
        template='plotly_white'
    )
    fig_goals.show()

    # 5. Historical Form Comparison Table
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=['Metric', home_team, away_team],
            fill_color='#E5ECF6',
            align='left',
            font=dict(color=['black', 'black', 'black']),
            line_color='darkslategray',
            fill=dict(color=['#E5ECF6', home_color, away_color])
        ),
        cells=dict(
            values=[
                ['Win Probability', 'Expected Goals', 'Expected Shots on Target', 'Expected Cards', 'Expected Corners'],
                [f"{predictions['home_win_prob']:.1f}%", 
                 f"{predictions['home_team_stats']['expected_goals']:.2f}",
                 f"{predictions['home_team_stats']['shots_on_target']:.2f}",
                 f"{predictions['home_team_stats']['cards']:.2f}",
                 f"{predictions['home_team_stats']['corners']:.2f}"],
                [f"{predictions['away_win_prob']:.1f}%",
                 f"{predictions['away_team_stats']['expected_goals']:.2f}",
                 f"{predictions['away_team_stats']['shots_on_target']:.2f}",
                 f"{predictions['away_team_stats']['cards']:.2f}",
                 f"{predictions['away_team_stats']['corners']:.2f}"]
            ],
            align='left',
            fill_color='white',
            line_color='darkslategray'
        ))
    ])
    fig_table.update_layout(
        title='Team Performance Comparison',
        template='plotly_white'
    )
    fig_table.show()

def print_match_summary(predictions, home_team, away_team):
    print(f"\n=== {home_team} vs {away_team} Prediction Summary ===")
    print(f"\nMost Likely Result: ", end="")
    max_prob = max(predictions['home_win_prob'], predictions['away_win_prob'], predictions['draw_prob'])
    if max_prob == predictions['home_win_prob']:
        print(f"{home_team} Win ({predictions['home_win_prob']:.1f}%)")
    elif max_prob == predictions['away_win_prob']:
        print(f"{away_team} Win ({predictions['away_win_prob']:.1f}%)")
    else:
        print(f"Draw ({predictions['draw_prob']:.1f}%)")
    
    print(f"\nKey Predictions:")
    print(f"- Expected Total Goals: {math.ceil(predictions['expected_total_goals'])}")
    print(f"- Individual Expected Goals: {home_team} {round(predictions['home_team_stats']['expected_goals'])}, {away_team} {round(predictions['away_team_stats']['expected_goals'])}")
    print(f"- BTTS Probability: {predictions['btts_prob']:.1f}%")
    print(f"- Expected Shots on Target: {home_team} {round(predictions['home_team_stats']['shots_on_target'])}, {away_team} {round(predictions['away_team_stats']['shots_on_target'])}")
    print(f"- Expected Corners: {home_team} {round(predictions['home_team_stats']['corners'])}, {away_team} {round(predictions['away_team_stats']['corners'])}")
    print(f"- Expected Cards: {home_team} {round(predictions['home_team_stats']['cards'])}, {away_team} {round(predictions['away_team_stats']['cards'])}")


# # Generate visualizations and print summary
# create_form_visualizations(prematch_stats, home_team, away_team, team_colors)
# create_visualizations(predictions, home_team, away_team, team_colors)
# print_match_summary(predictions, home_team, away_team)