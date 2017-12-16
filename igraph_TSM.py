from igraph import *
import re
import math
import csv


inv = 1
iter_count = 10
delimiter = '\t'
normChoice = 1

input_file = 'data/soc-Epinions1_ip.txt'
output_file = 'results/soc-Epinions1_ip_TS.txt'

g = Graph(directed=True)
vertices_set = set()
edges = dict()
f = open(input_file, 'r')
lines = f.readlines()
for line in lines:
    l_spl = re.split(delimiter, line.rstrip())
    l = []
    vertices_set.add(int(l_spl[0]))
    l.append(int(l_spl[0]))
    vertices_set.add(int(l_spl[1]))
    l.append(int(l_spl[1]))
    if len(l_spl) == 2:  # Un-weighted graph
        edges[tuple(l)] = 1
    else:  # Weighted graph
        edges[tuple(l)] = int(l_spl[2])


vertices = list(vertices_set)

g = Graph(vertex_attrs={"label": vertices}, edges=edges.keys(), directed=True)
print 'Graph generated. Calculating scores...'

hti = {}
htw = {}

for node in vertices:
    hti[node] = 1 /float(len(vertices))
    htw[node] = 1 /float(len(vertices))


def calcScores(vs, s, n, other_sc, flag):
    if flag == 'ti':
        for vertex in vs:
            s += inver(other_sc.get(vertex))*edges[(n, vertex)]
    elif flag == 'tw':
        for vertex in vs:
            s += inver(other_sc.get(vertex))*edges[(vertex, n)]
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
    print 'Iteration ', i+1, ' in progress...'
    for node in vertices:
            """Calculate Scores for Trustingness"""
            vsti = g.neighbors(node, mode=OUT)
            sc = calcScores(vsti, hti.get(node), node, htw, 'ti')
            hti[node] = sc

    for node in vertices:
            """Calculate Scores for Trustworthiness"""
            vstw = g.neighbors(node, mode=IN)
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







