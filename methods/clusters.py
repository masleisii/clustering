#!/usr/bin/env python
# -*- coding: utf-8 -*-


class bicluster:
	def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):

		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance




def readfile(filename):

	lines = [line for line in open(filename)]

	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	
	for line in lines[1:]:

		p = line.strip().split('\t')
		
		rownames.append(p[0])
		data.append([float(x) for x in p[1:]])

		
	return rownames, colnames, data


from math import sqrt

def pearson(v1,v2):
	
	sum1 = sum(v1)
	sum2 = sum(v2) 

	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])

	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

	num = pSum - (sum1 * sum2 / len(v1))
	den = sqrt((sum1Sq - pow(sum1,2) / len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))
 
	if den == 0: return 0


	return 1.0 -num /den



def hcluster(rows, distance = pearson):
	
	distances = {}
	currentclustid = -1
	# クラスタは最初は行たち

	clust = [bicluster(rows[i], id = i) for i in range(len(rows))]

	while len(clust) > 1:

		lowestpair = (0,1)
		closest = distance(clust[0].vec, clust[1].vec)

		# すべての組をループし、最も距離の近い組を探す
		for i in range(len(clust)):
			for j in range(i + 1, len(clust)):
				if (clust[i].id, clust[j].id) not in distances:
					distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)	
			
				d = distances[(clust[i].id, clust[j].id)]

				if d < closest:
					closest = d
					lowestpair = (i, j)
			
		# ２つのクラスタの平均を計算する
		mergevec = [
			(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0

			for i in range(len(clust[0].vec))]
		# 新たなクラスタを作る				
		newcluster = bicluster(mergevec, left = clust[lowestpair[0]],
					right = clust[lowestpair[1]],
					distance = closest, id = currentclustid)
	
		# 元のセットではないクラスタのIDは負にする
		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)
	
	return clust[0]



def printclust(clust, labels = None, n = 0):

	# 階層型のレイアウトにするためにインデントする
	for i in range(n): print ' ',
	if clust.id < 0:

		# 負のidはこれが枝であることを示している
		print '-'
	else:
		# 正のidはこれが終端であることを示している

		if labels == None: print clust.id
		else: print labels[clust.id]
	
	# 右と左の枝を表示する
	if clust.left != None: printclust(clust.left, labels = labels, n = n + 1)
	if clust.right != None: printclust(clust.right, labels = labels, n = n + 1)


		
		
