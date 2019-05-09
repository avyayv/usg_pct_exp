import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import numpy as np

X = []
Y = []

players = json.loads(open('5319research.json').read())

keqlow = 0.1
keqhigh = 0.6

kminmin = 5.0
kminmax = 50.0

for player in players:

    if 'BaseStats Regular+Season' not in player['nice_dict']:
        continue

    if (player['nice_dict']['BaseStats Regular+Season'][0]['PLAYER_HEIGHT_INCHES']) == None:
        continue

    for reg_szn in player['nice_dict']['Usage Regular+Season']:
        usg_rate_regular_season = (reg_szn['USG_PCT'])
        if 'Usage Playoffs' in player['nice_dict']:
            for playoff in player['nice_dict']['Usage Playoffs']:
                usg_rate_playoff = playoff['USG_PCT']
                if reg_szn['GP'] > 0:

                    reg_szn_val = ((reg_szn['MIN']/reg_szn['GP']) < kminmax) and ((reg_szn['MIN']/reg_szn['GP']) > kminmin)
                    playoff_val = (playoff['MIN']/playoff['GP']) < kminmax and (playoff['MIN']/playoff['GP']) > kminmin
                    usg_reg_szn_val = reg_szn['USG_PCT'] > keqlow and reg_szn['USG_PCT'] < keqhigh
                    usg_playoff_val = playoff['USG_PCT'] > keqlow and playoff['USG_PCT'] < keqhigh

                    if reg_szn['SEASON'] == playoff['SEASON'] and reg_szn_val and playoff_val and usg_reg_szn_val and usg_playoff_val:
                        X.append(usg_rate_regular_season*100)
                        Y.append(usg_rate_playoff*100)

X_ = []
for index,um in enumerate(X):
    X_.append([um, um])

lg = LinearRegression()
lg.fit(X_, Y)

Y2 = lg.predict(X_)

slope = (Y2[50]-Y2[0])/(X_[50][0]-X_[0][0])
print(slope)

plt.xlabel('Regular Season Usage Rate')
plt.ylabel('Playoffs Usage Rate')
plt.title('Playoff vs Regular Season Usage Rate')

plt.scatter(X,Y, c='0.8', s=1.0)
plt.plot(X_,Y2, c= 'black')

print(r2_score(Y, Y2))

plt.savefig('all.png')
plt.show()

#Slope = 1.009598264944422 ; R^2 = 0.808219749136905
#Slope = 0.9377207299741774 ; R^2 = 0.695027256005324
#Slope = 0.9070116452677446 ; R^2 = 0.5208970247035778
#Slope = 0.8772583897561517 ; R^2 = 0.292077202848962
