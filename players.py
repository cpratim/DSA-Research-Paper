import json
from pprint import pprint

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


if __name__ == '__main__':

	with open('data/top_scorers.json', 'r') as f:
		d = json.load(f)

	stats = list(d['Zach LaVine']['2021'].keys())
	pprint(stats)
