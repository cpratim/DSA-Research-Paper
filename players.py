import json
from pprint import pprint
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from util.stats import *

'''
'mp_per_g',
'fg_per_g',
'fga_per_g',
'fg_pct',
'fg3_per_g',
'fg3a_per_g',
'fg3_pct',
'fg2_per_g',
'fg2a_per_g',
'fg2_pct',
'efg_pct',
'ft_per_g',
'fta_per_g',
'ft_pct',
'orb_per_g',
'drb_per_g',
'trb_per_g',
'ast_per_g',
'stl_per_g',
'blk_per_g',
'tov_per_g',
'pf_per_g',
'pts_per_g'
'''

with open('data/player_stats.json', 'r') as f:
		stats = json.load(f)
with open('data/player_box.json', 'r') as f:
	box = json.load(f)

def player_stat_impact():
	#ppg, fta_per_g, fg_pct, per, ws48, obpm
	
	arr = []
	for p in stats:
		stats_2021, stats_2022 = stats[p]['2021'], stats[p]['2022']
		box_2021, box_2022 = box[p]['2021'], box[p]['2022']

		minutes = float(stats_2021['mp_per_g'])
		adj = 48 / minutes
		ppg_diff = (float(stats_2022['pts_per_g']) * adj) - (float(stats_2021['pts_per_g']) * adj)
		fta_diff = (float(stats_2022['fta_per_g']) * adj) - (float(stats_2021['fta_per_g']) * adj)
		fgp_diff = (float(stats_2022['fg_pct']) - float(stats_2021['fg_pct'])) * 100

		per_diff = (float(box_2022['per']) - float(box_2021['per']))
		ws_diff = (float(box_2022['ws_per_48']) - float(box_2021['ws_per_48']))
		obpm_diff = float(box_2022['obpm']) - float(box_2021['obpm'])
		arr.append([ppg_diff, fta_diff, fgp_diff, per_diff, ws_diff, obpm_diff])
		print(p, round(ppg_diff, 2), round(fta_diff, 2), round(fgp_diff, 2), round(per_diff, 2), round(ws_diff, 2), round(obpm_diff, 2))
	arr = np.array(arr)
	print('Average', np.mean(arr, axis = 0))

def ftp_offensive_graph():
	X, y = [], []
	for p in stats:
		stats_2021, stats_2022 = stats[p]['2021'], stats[p]['2022']
		box_2021, box_2022 = box[p]['2021'], box[p]['2022']
		minutes = float(stats_2021['mp_per_g'])
		adj = 48 / minutes
		diff = (float(box_2022['obpm']) - float(box_2021['obpm']))
		X.append(float(stats_2022['fta_per_g']) * adj - float(stats_2021['fta_per_g']) * adj)
		y.append(diff)

	f = linregress_f(X, y)
	labels = list(stats.keys())
	plt.xlabel('Free Throw Attempts')
	plt.ylabel('Offensive Box Plus Minus')
	plt.title('FTA vs OBPM')
	print(correlation(X, y))
	fit_y = [f(min(X)), f(max(X))]
	plt.plot([min(X), max(X)], fit_y, color = 'red')
	plt.scatter(X, y)
	for x, _y, l in zip(X, y, labels):
		plt.annotate(l.split(' ')[-1], (x, _y))


	plt.show()


if __name__ == '__main__':
	ftp_offensive_graph()
	

