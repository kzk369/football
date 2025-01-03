from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime
import pandas as pd
import extract as ex
import predict as pr

app = Flask(__name__)

@app.route('/')
def home():
    """Home page with prediction form"""
    leagues = ex.get_leagues()
    return render_template('index.html', leagues=leagues)

@app.route("/get_teams", methods=["POST"])
def get_teams():
    league = request.json.get("league")
    teams = ex.get_teams(league)
    return {"teams": teams}

@app.route('/get_stats', methods=['POST'])
def get_stats():
    # Extract form data
    data = request.get_json()
    league = data.get('league')
    home_team = data.get('home_team')
    away_team = data.get('away_team')

    if home_team == away_team:
        if home_team == "Man United":
            return jsonify({"error": "GLORY GLORY MAN UNITED!"})
        return jsonify({"error": "Home and Away teams must be different!"})

    stats = pr.get_stats(league, home_team, away_team)

    # Perform operations with the form data
    # Example: return a message with the submitted data
    return jsonify({"stats": stats})

if __name__ == '__main__':
    app.run(debug=True)
