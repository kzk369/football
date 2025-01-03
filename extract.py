leagues = ['English Premier League', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Scottish Premier League', 'Championship']
teams = {
    'English Premier League': sorted([
        'Arsenal', 'Bournemouth', 'Brighton', 'Everton', 
        'Newcastle', 'Brentford', 'Chelsea', 'Man United', "Nott'm Forest", 'Fulham',
        'Liverpool', 'Wolves', 'Tottenham', 'Man City', 'Aston Villa', 'West Ham',
        'Crystal Palace', 'Ipswich', 'Leicester', 'Southampton'
    ]),
    'Scottish Premier League': sorted([
        'Celtic', 'Dundee', 'St Johnstone', 'Kilmarnock', 'Hibernian',
        'Rangers', 'Ross County', 'St Mirren', 'Aberdeen', 'Hearts', 'Motherwell',
        'Dundee United'
    ]),
    'Serie A': sorted([
        'Empoli', 'Genoa', 'Inter', 'Roma', 'Lecce', 'Udinese',
        'Torino', 'Bologna', 'Monza', 'Milan', 'Verona', 'Fiorentina', 'Juventus',
        'Lazio', 'Napoli', 'Cagliari', 'Atalanta', 'Parma', 'Venezia',
        'Como'
    ]),
    'Bundesliga': sorted([
        'Werder Bremen', 'Augsburg', 'Hoffenheim', 'Leverkusen', 'Stuttgart', 'Wolfsburg', 
        'Dortmund', 'Union Berlin', 'Ein Frankfurt', 'RB Leipzig', 
        'Freiburg', 'Heidenheim', "M'gladbach", 'Mainz', 'Bayern Munich', 'St Pauli', 
        'Holstein Kiel'
    ]),
    'LaLiga': sorted([
        'Sevilla', 'Sociedad', 'Las Palmas', 'Ath Bilbao', 'Celta', 'Villarreal', 
        'Getafe', 'Ath Madrid', 'Mallorca', 'Valencia', 'Osasuna', 'Girona', 'Barcelona', 
        'Betis', 'Alaves', 'Vallecano', 'Real Madrid', 'Valladolid', 'Espanol', 'Leganes'
    ]),
    'Ligue 1': sorted([
        'Nice', 'Marseille', 'Paris SG', 'Brest', 'Montpellier', 'Nantes', 'Rennes', 
        'Strasbourg', 'Lyon', 'Toulouse', 'Lille', 'Le Havre', 'Reims', 'Monaco', 
        'Lens', 'Auxerre', 'Angers', 'St Etienne'
    ]),
    'Championship': sorted([
        'Sheffield Weds', 'Blackburn', 'Bristol City', 'Middlesbrough', 'Norwich', 'Plymouth', 'Stoke', 
        'Swansea', 'Watford', 'Leicester', 'Leeds', 'Sunderland', 'Coventry', 'Cardiff', 
        'Hull', 'Ipswich', 'Millwall', 'Preston', 'Southampton', 'West Brom', 
        'QPR', 'Oxford', 'Luton', 'Derby', 'Portsmouth', 'Burnley', 'Sheffield United'
    ])
}



def get_leagues():
    return leagues

def get_teams(league):
    return teams[league]