leagues = ['English Premier League', 'Scottish Premier League', 'Serie A']
teams = {
    'English Premier League': sorted([
        'Burnley', 'Arsenal', 'Bournemouth', 'Brighton', 'Everton', 'Sheffield United',
        'Newcastle', 'Brentford', 'Chelsea', 'Man United', "Nott'm Forest", 'Fulham',
        'Liverpool', 'Wolves', 'Tottenham', 'Man City', 'Aston Villa', 'West Ham',
        'Crystal Palace', 'Luton', 'Ipswich', 'Leicester', 'Southampton'
    ]),
    'Scottish Premier League': sorted([
        'Celtic', 'Dundee', 'Livingston', 'St Johnstone', 'Kilmarnock', 'Hibernian',
        'Rangers', 'Ross County', 'St Mirren', 'Aberdeen', 'Hearts', 'Motherwell',
        'Dundee United'
    ]),
    'Serie A': sorted([
        'Empoli', 'Frosinone', 'Genoa', 'Inter', 'Roma', 'Sassuolo', 'Lecce', 'Udinese',
        'Torino', 'Bologna', 'Monza', 'Milan', 'Verona', 'Fiorentina', 'Juventus',
        'Lazio', 'Napoli', 'Salernitana', 'Cagliari', 'Atalanta', 'Parma', 'Venezia',
        'Como'
    ])
}



def get_leagues():
    return leagues

def get_teams(league):
    return teams[league]