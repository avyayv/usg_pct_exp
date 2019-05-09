import json

players = json.loads(open('5319research.json').read())

keqlow = 0.1
keqhigh = 0.6

kminmin = 5.0
kminmax = 35.0

X = []
Y = []

for player in players:

    if 'BaseStats Regular+Season' not in player['nice_dict']:
        continue

    if (player['nice_dict']['BaseStats Regular+Season'][0]['PLAYER_HEIGHT_INCHES']) == None:
        continue

    for index, reg_szn in enumerate(player['nice_dict']['Usage Regular+Season']):
        usg_rate_regular_season = (reg_szn['USG_PCT'])
        if 'Usage Playoffs' in player['nice_dict']:
            for playoff in player['nice_dict']['Usage Playoffs']:
                usg_rate_playoff = playoff['USG_PCT']
                if reg_szn['GP'] > 0:
                    basic_stats = player['nice_dict']['Base Regular+Season'][index]
                    ageandstuff = player['nice_dict']['BaseStats Regular+Season'][index]

                    eoffrating = player['nice_dict']['Advanced Regular+Season'][index]['eOFF_RATING']
                    edefrating = player['nice_dict']['Advanced Regular+Season'][index]['eDEF_RATING']

                    reg_szn_val = ((reg_szn['MIN']/reg_szn['GP']) < kminmax) and ((reg_szn['MIN']/reg_szn['GP']) > kminmin)
                    playoff_val = (playoff['MIN']/playoff['GP']) < kminmax and (playoff['MIN']/playoff['GP']) > kminmin
                    usg_reg_szn_val = reg_szn['USG_PCT'] > keqlow and reg_szn['USG_PCT'] < keqhigh
                    usg_playoff_val = playoff['USG_PCT'] > keqlow and playoff['USG_PCT'] < keqhigh
                    if reg_szn['SEASON'] == playoff['SEASON'] and reg_szn_val and playoff_val and usg_reg_szn_val and usg_playoff_val:
                        X.append([usg_rate_regular_season, eoffrating, edefrating, basic_stats['PTS']/basic_stats['MIN'], basic_stats['REB']/basic_stats['MIN'], basic_stats['FG_PCT'], basic_stats['AST']/basic_stats['MIN'], basic_stats['FG3_PCT']])
                        Y.append([usg_rate_playoff])
