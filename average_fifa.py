import random
import numpy
import os
import sys
import math
import collections
legend = {
	0:'aggression',
	1:'acceleration',
	2:'attack bias',
	3:'agility',
	4:'ball',
	5:'awareness',
	6:'fitness',
	7:'creativity',
	8:'passing',
	9:'heading',
	10:'reaction',
	11:'pass bias',
	12:'shot power',
	13:'shot bias',
	14:'speed',
	15:'shot accuracy',
	16:'tackle'
}
def gimme_values(*vals,**kwargs):
	auto  = False
	role = kwargs.get('role','n/a')
	verbose = kwargs.get('verbose',True)
	role_distros = { #new
	'GK': [10,3,5,4,0,6,12,14,8,16,9,1,11,7,15,2,13],
	'SW': [16,0,14,10,1,6,11,8,13,5,12,2,4,9,7,3,15],
	'LB': [1,14,16,0,8,13,11,6,2,9,7,5,3,4,10,12,15],
	'LCB':[16,0,9,14,10,5,6,12,8,3,4,15,11,1,7,13,2],
	'CB': [16,0,9,10,5,6,12,8,3,4,15,11,1,14,7,13,2],
	'RCB':[16,0,14,9,10,5,6,12,8,3,4,15,11,1,7,13,2],
	'RB': [1,14,2,13,8,16,0,12,11,6,9,15,3,4,5,10,7],
	'LM': [8,4,16,14,11,5,6,13,7,0,1,3,12,10,15,9,2],
	'LCM':[7,14,11,8,5,4,6,13,0,16,2,10,12,9,3,15,1],
	'CM': [7,11,8,5,4,6,13,0,16,2,10,12,9,3,14,15,1],
	'RCM':[7,11,14,8,5,4,6,13,0,16,2,10,12,9,3,15,1],
	'RM': [8,4,14,2,11,13,7,15,16,5,6,0,9,1,3,12,10],
	'LF': [14,1,2,8,13,11,7,15,12,4,3,10,0,5,9,6,16],
	'CF': [15,2,13,9,12,1,0,3,14,8,7,16,5,11,6,4,10],
	'RF': [14,4,13,8,2,11,3,7,1,15,12,10,0,5,9,6,16],
	}
	if role == 'n/a':
		w = [x for x in range(17)]
		random.shuffle(w)
		role_distros['n/a'] = w
		del w
	b = [x*4+39 for x in range(16)]
	val = range(39,100)
	combs_coll=set()
	for w in b:
		x = 17
		combs = []
		combs_b = []
		while True:
			for i in range(x):
				combs.append(99)
				combs_b.append(39)
			for y in range(17-x):
				combs.append(w)
				combs_b.append(w)
			combs_coll.add(tuple(combs))
			combs_coll.add(tuple(combs_b))
			x-=1
			combs=[]
			combs_b = []
			if x == -1:
				break
	dt = {}
	for f in combs_coll:
		dt.setdefault(math.floor(sum(f)/len(f)),[[],[]])[0].append(sorted(f)[0])
		dt.setdefault(math.floor(sum(f)/len(f)),[[],[]])[1].append(sorted(f)[-1])
	for x,y in dt.items():
		dt[x]=(math.floor((sorted(y[0])[0]-39)/4),math.floor((sorted(y[1])[-1]-39)/4))

	list = []
	if len(vals)>0:
		average = str(vals[0])
	else:
		average = str(input('Input desired average: '))
	try:
		params = average.split('.')[1]
	except:
		params = ''
	#Params:
		#[s]: +speed, +acceleration * max
		#[f]: +agility, +attack bias * 4, +ball, +creativity * 3, +pass bias * 3, +passing * 5, +acceleration, -tackle * 8, -aggression * 12, -fitness * 2
		#[b]: +aggression * 3, +awareness, +fitness, +heading * 5, +tackle * 2, +shot power * 2, -acceleration * 3, -creativity * 8
		#[n]: +acceleration * 11, +agility * 13, +ball * 10, +shot accuracy  * 3, +speed  * 5, -tackle*4, -heading * 10
		#[o]: +attack bias * 2, +awareness * 3, +heading * 5, +reaction, +shot bias * 8, +shot accuracy * 8
		#[t]: +shot power * 6, +shot bias * 8, +shot accuracy * 6
		#[d]: +aggression * 3, -attack bias * 7, -creativity * 8, +reaction * 6, -shot bias * 5, +tackle * 8
		#[a]: +attack bias * 9, +creativity * 3, +pass bias * 3, +shot bias * 7, -tackle * 5
		#[u]: -attack bias * 13, -creativity * 13, -pass bias * 13, -shot bias * 13, -aggression * 13, -awareness * 13

	for p in params:
		boost = False
		if p == "s": boost = [[14,16], [1,15]]
		if p == "f": boost = [[2,1], [3,4], [4,1], [7,3], [11,3], [8,5], [1,2], [16,-8], [0,-10], [6,-2]]
		if p == "b": boost = [[0,3], [5,1], [6,1], [9,5], [16,2], [12,2], [1,-3], [7,-8]]
		if p == "n": boost = [[1,11], [3,13], [4,10], [14,5], [15,3], [9,-4], [16, -8]]
		if p == "o": boost = [[2,2], [5,3], [9,5], [10,1], [13,8], [15,8]]
		if p == "t": boost = [[12,6],[13,8],[15,6]]
		if p == "d": boost = [[0,3],[2,-7],[7,-8],[10,6],[13,-5],[16,8]]
		if p == "a": boost = [[2,9],[7,3],[11,3],[13,7],[16,-5]]
		if p == "u": boost = [[2,-13],[7,-13],[11,-13],[13,-13],[0,-13],[5,-13]]
		if not boost: continue
		boost = sorted(boost, key=lambda x:role_distros[role].index(x[0]))
		for x in boost:
			feat,offset = x[0], x[1]
			role_distros[role].insert(x if ((x:=role_distros[role].index(feat)-offset) >=0 and x < len(role_distros[role])) else 0 if x < 0 else len(role_distros[role]), role_distros[role].pop(role_distros[role].index(feat)))


	average = int(average.split('.')[0])
	st_de = input('Limit standard deviation? [*m*uch/*e*nough/*l*ittle/m*i*nimum/*n*o] ').upper()
	k = dt.get(average, dt[71])
	b = b[k[0]:k[1]+1]
	
	#shrink to limit standard deviation
	av_scale = math.floor((average-39)/4)*4+39
	min_index= b.index(av_scale)
	max_index = b.index(av_scale)
	if st_de != 'N':
		if st_de == 'E' or len(st_de) == 0:
			min_index-=3
			max_index+=4
		elif st_de == 'L':
			min_index-=3
			max_index+=7
		elif st_de == 'I':
			min_index-=5
			max_index+=7
		elif st_de == 'M':
			min_index-=2
			max_index+=3
		if min_index < 0: min_index=0
		if max_index>len(b):max_index =len(b)
		b=b[min_index:max_index]
	else:
		if average == 39: b=b[0:3]
		if average == 43: b=b[0:7]
		if average == 47: b=b[0:11]
		if average == 87: b=b[-14:]
		if average == 91: b=b[-9:]
		if average == 95: b=b[-6:]
	a = [x for x in range(len(b))]

	while True:
		for i in range(17):
			random.shuffle(a)
			list.append(b[a[0]])
		av = math.floor(sum(list)/len(list))
		if av == average:
			list = sorted(list, reverse=True)


			temp_list = [None]*17
			for i,x in enumerate(role_distros[role]):
				temp_list[x] = list[i]
			list = temp_list
			del temp_list
			print('\nNew values:\n\n  ','\n  '.join(['{0:25}{1}'.format(legend[e]+':', y) for (e,y) in enumerate(list)]),'\n\nAverage: ',str(av)+', ','standard deviation: ',str(numpy.std(list)), '\n', sep='')
			return(list)
			break
		else:
			list = []