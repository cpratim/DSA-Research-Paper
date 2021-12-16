import json
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from scipy.stats import linregress

def correlation(x, y):
	return np.corrcoef(x, y)[0, 1]

with open('data/game_stats.json', 'r') as f:
	df = json.load(f)

X, y = [], []
for match, stats in df.items():
	home, away = stats['home'], stats['away']
	if home['mp'] != away['mp'] != '240': continue
	try:
		ft_dif = float(home['fta'])  - float(away['fta'])
		pt_dif = float(home['pts']) - float(away['pts'])
		if abs(pt_dif) > 10: continue
	except:
		continue

	X.append(ft_dif)
	y.append(pt_dif)

c = 0
for f, p in zip(X, y):
	if f * p > 0:
		c += 1

print(c / len(X))

slope, intercept, r, p, std = linregress(X, y)
f = lambda x: x*slope + intercept
fit_y = [f(min(X)), f(max(X))]

plt.xlabel('Free Throw Attempts')
plt.ylabel('Point Differential')
plt.title('FTA vs Point Differential')
print(correlation(X, y))
plt.plot([min(X), max(X)], fit_y, color = 'red')
plt.scatter(X, y)

plt.show()