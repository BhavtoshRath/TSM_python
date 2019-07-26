import re
import math
import csv
import copy
import pickle
import igraph

inv = 0.359
iter_count = 20
normChoice = 0

def TSM(graph, vertices, cur_dir = './'):
  print('Calculating TSM scores.')

  hti = {}
  htw = {}

  for node in vertices:
    hti[node] = 1 #/float(len(vertices))
    htw[node] = 1 #/float(len(vertices))

  i = 0
  while(i < iter_count):
    print('Iteration ', i+1, ' in progress...')
    
    prev_hti = copy.deepcopy(hti); prev_htw = copy.deepcopy(htw)

    for node in vertices:
      """Calculate Scores for Trustingness"""
      vsti = graph.neighbors(node, mode='OUT')
      sc = calcScores(graph, vsti, 0, node, prev_htw, 'ti')
      hti[node] = sc

    for node in vertices:
      """Calculate Scores for Trustworthiness"""
      vstw = graph.neighbors(node, mode='IN')
      sc = calcScores(graph, vstw, 0, node, prev_hti, 'tw')
      htw[node] = sc

    hti = normalize(hti, normChoice)
    htw = normalize(htw, normChoice)
    i += 1
  
  TSM_scores = {}
  for node in vertices:
    TSM_scores[node] = (hti[node], htw[node])
  pickle.dump(TSM_scores, open(cur_dir + '/Concatenated/TSM_scores', 'wb'))


def calcScores(G, vs, s, n, other_sc, flag):
  ########################################################
  ############## ASSUMES WEIGHT = 1 ALWAYS ###############
  ########################################################

  s = 0
  if flag == 'ti':
    for vertex in vs:
      s += inver(other_sc.get(vertex))*1 #edges[(n, vertex)]
  elif flag == 'tw':
    for vertex in vs:
      s += inver(other_sc.get(vertex))*1 #edges[(vertex, n)]
  return s

def inver(a):
  return 1/float(1+a**inv)

def normalize(userScores, choice):
  score_list = userScores.values()
  if choice == 0:  # min-max
    min_val = min(score_list)
    max_val = max(score_list)
    for user in userScores:
      userScores[user] = (userScores[user] - min_val)/float(max_val - min_val)

  elif choice == 1: # sum-of-squares
    norm_den = sum(i**2 for i in score_list)
    norm_den = math.sqrt(norm_den)
    for user in userScores:
      userScores[user] = userScores[user]/float(norm_den)

  return userScores

if __name__ == '__main__':
  # G = igraph.Graph([(1, 3), (4, 1), (2, 3), (3, 5), (2, 5)], directed = True)
  # TSM('sample', G, [1, 2, 3, 4, 5])

  edges = [(1, 0), (2, 0), (3, 0), (4, 0)]
  edges += [(5, 1), (6, 1), (7, 2), (8, 2), (9, 2), (10, 3), (11, 3), (12, 3), (13, 4), (14, 4), (15, 4)]
  # edges += [(16, 11), (17, 12), (17, 13), (18, 14)]
  G = igraph.Graph(edges, directed = True)
  TSM('sample', G, list(range(0, 16)))

  # edges = {}
  # vertices = set()
  # with open(input_file, 'r') as inptr:
  #   for line in inptr:
  #     l_spl = re.split(',', line.rstrip())
  #     if len(l_spl) == 2:
  #       try:
  #         edges[tuple(id_dict[l_spl[0]], id_dict[l_spl[1]])] = 1
  #         vertices.add(id_dict(l_spl[0]))
  #         vertices.add(id_dict(l_spl[1]))
  #       except KeyError:
  #         continue

  # G = igraph.Graph(edges.keys(), directed = True)
  # TSM('sample', G = G, vertices = list(vertices))
