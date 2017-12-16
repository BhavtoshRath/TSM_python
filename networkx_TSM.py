import networkx as nx
import re
import math
import csv


inv = 1
iter_count = 10
delimiter = ','
normChoice = 1

input_file = ''
output_file = ''

G = nx.DiGraph()
with open('soc-Epinions1_ip_test.txt') as infile:
    for line in infile:
        print line
        l_spl = re.split(',', line.rstrip())
        if len(l_spl) == 3:
            # G.add_weighted_edges_from(l_spl[0], l_spl[1], float(l_spl[2]))
            G.add_edge(int(l_spl[0]), int(l_spl[1]), weight = float(l_spl[2]))
        elif len(l_spl) == 2:
            # G.add_weighted_edges_from(l_spl[0], l_spl[1], 1)
            G.add_edge(int(l_spl[0]), int(l_spl[1]), weight=1)


vertices = G.nodes()

hti = {}
htw = {}

for node in vertices:
 hti[node] = 1 /float(len(vertices))
 htw[node] = 1 /float(len(vertices))


def calcScores(vs, s, n, other_sc, flag):
 if flag == 'ti':
     for vertex in vs:
         s += inver(other_sc.get(vertex))*G[n][vertex]['weight']
 elif flag == 'tw':
     for vertex in vs:
         s += inver(other_sc.get(vertex))*G[vertex][n]['weight']
 return s


def inver(a):
 return 1/float(1+a**inv)


def normalize(userScores, choice):
 score_list = userScores.values()
 min_val = min(score_list)
 max_val = max(score_list)
 if choice == 0:  # min-max
     for user in userScores:
         userScores[user] = (userScores[user] - min_val)/float(max_val - min_val)


 elif choice == 1: # sum-of-squares
     norm_den = sum(i**2 for i in score_list)
     norm_den = math.sqrt(norm_den)
     for user in userScores:
         userScores[user] = userScores[user]/float(norm_den)

 return userScores



i = 0
while(i < iter_count):
 for node in vertices:
         """Calculate Scores for Trustingness"""
         # vsti = g.neighbors(node, mode=OUT)
         vsti = [ind[1] for ind in G.out_edges(node)]
         sc = calcScores(vsti, hti.get(node), node, htw, 'ti')
         hti[node] = sc

 for node in vertices:
         """Calculate Scores for Trustworthiness"""
         # vstw = g.neighbors(node, mode=IN)
         vstw = [ind[0] for ind in G.in_edges(node)]
         sc = calcScores(vstw, htw.get(node), node, hti, 'tw')
         htw[node] = sc

 i += 1

norm_hti = normalize(hti, normChoice)
norm_htw = normalize(htw, normChoice)

with open(output_file, 'w') as f:
    writer = csv.writer(f)
    for i in vertices:
        print i, ' , ',norm_hti[i], ' , ' ,norm_htw[i]
        l = []
        l.append(i)
        l.append(norm_hti[i])
        l.append(norm_htw[i])
        writer.writerow(l)