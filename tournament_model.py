import random
# number of simulations to run
iterations = 1000
# number of players in a tournament
players = 19
# rounds before the top cut
rounds = 6
#top cut size
cut = 8


# percent of participants using an archetype.  Must add up to 100
meta = []
# planetman percent of playerbase
meta += [34]
# cc percent of playerbase
meta += [33]
# atk10 percent of playerbase
meta += [33]
bye = False
# Define Matchups here.  Number is the percentile chance of the first archetype beating the second.
Planetman_vs_CC = 80
Planetman_vs_Attack10 = 40
CC_vs_Attack10 = 80

Mirror_Match = 50
win_rates = {1: {1: Mirror_Match, 2: Planetman_vs_CC, 3: Planetman_vs_Attack10},
             2: {1: (100-Planetman_vs_CC), 2: Mirror_Match, 3: CC_vs_Attack10},
             3: {1: (100-Planetman_vs_Attack10), 2: Mirror_Match, 3: (100-CC_vs_Attack10)}}

if players % 2 == 1:
	bye = True
assert sum(meta) == 100


def roll():
	return random.randint(0, 99)


def get_record(player):
	return player[1]


def matchups(players, win_rates):
	players = sorted(players, key=get_record, reverse=True)
	for p in range(len(players))[0:-1:2]:
		p1 = players[p]
		p2 = players[p+1]
		chance = roll()
		if chance < win_rates[p1[0]][p2[0]]:
			p1[1] += 1
		else:
			p2[1] += 1
	if bye:
		#give bye to last place of previous round
		players[-1][1] += 1


def top_cut(players, meta, win_rates, top_cut):
	history = []
	for p in range(players):
		r = roll()
		if r < meta[0]:
			role = 1
		elif r < sum(meta[:2]):
			role = 2
		else:
			role = 3
		history.append([role, 0])

	for r in range(rounds):
		matchups(history, win_rates)
	return sorted(history, key=get_record, reverse=True)[:top_cut]

results = []
for c in range(cut):
	results.append({1: 0, 2: 0, 3: 0})
for i in range(iterations):
	tournament_results = top_cut(players, meta, win_rates, cut)
	for t in range(len(tournament_results)):
		results[t][tournament_results[t][0]] += 1
for r in results:
	for i in [1, 2, 3]:
		r[i] /= iterations / 100
		r[i] = str(r[i]) + '%'
	r['Planet Man'] = r.pop(1)
	r['CC Mod Cards'] = r.pop(2)
	r['Attack 10'] = r.pop(3)
print('top 8 cut printed in order of seeding.  Top seed to bottom seed')
for r in range(len(results)):
	print('seed {seed}: {result}'.format(seed=(r+1), result=results[r]))