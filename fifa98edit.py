#imports
print('Loading libraries...')
import os
import struct
import textwrap
import sys
import re
import math
import shutil
import platform
import random
import numpy
import copy
from average_fifa import *
from functools import reduce
from display_jerseys import *
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import colorsys
import json

def colorize_feats(filename, colour):
	if colour == 0:
		hs = -7
		ss = -15
		vs = 6
	elif colour == 1:
		hs = 0
		ss = 1
		vs = 1
	elif colour == 2:
		hs = 9
		ss = 21
		vs = -13
	elif colour == 3:
		hs = -13
		ss = -4
		vs = -23
	elif colour == "brown":
		hs = 0
		ss = 1
		vs = 1
	elif colour == "BLack":
		hs = 0
		ss = -7
		vs = -40
	elif colour == "blond":
		hs = 18
		ss = 58
		vs = 28
	elif colour == "red":
		hs = -6
		ss = 58
		vs = 28
	im = Image.open(filename)
	ld = im.load()
	width, height = im.size
	for y in range(height):
		for x in range(width):
			r,g,b,a = ld[x,y]
			h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
			h = (h + hs/360.0) % 1.0
			s = s + ss*s/100
			v = v + vs*v/100
			r,g,b = colorsys.hsv_to_rgb(h, s, v)
			ld[x,y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999), a)
	return im

#init states
jerseys = False
debug = False
table = False
case_sensitive = False
lang = [None]
custom_jerseys = [[]]

#platform-specific settings
if platform.system() == 'Windows':
	import colorama
	colorama.init()
	clear_screen = "cls"
	unix = ''
	hair_cl_d = {'blond':'\033[48;5;103m  \033[0m','brown':'\033[48;5;33m▒▒\033[0m','red':'\033[48;5;41m  \033[0m','BLack':'\033[48;5;90m▒▒\033[0m'}
	skin_cl_d = ['\033[48;5;107m  \033[0m','\033[48;5;103m  \033[0m','\033[48;5;33m▒▒\033[0m','\033[48;5;90m▒▒\033[0m']
	cesc = [
		'\033[95;47m▒▒',
		'\033[41m  ',
		'\033[91;40m▒▒',
		'\033[91;43m▒▒',
		'\033[31;43m▒▒',
		'\033[33;41m▒▒',
		'\033[33;103m▒▒',
		'\033[97;43m▒▒',
		'\033[43m  ',
		'\033[102m  ',
		'\033[42m  ',
		'\033[34;42m▒▒',
		'\033[104m  ',
		'\033[44m  ',
		'\033[30;44m▒▒',
		'\033[34;40m▒▒',
		'\033[105;97m▒▒',
		'\033[105m  ',
		'\033[45m  ',
		'\033[107m  ',
		'\033[100m  ',
		'\033[30;100m▒▒',
		'\033[0;90m▒▒'
	]
else:	
	home = os.path.expanduser('~')
	gamepath = ["/Applications/fifa98.app/Contents/Resources/drive_c/Program Files/FIFA RTWC 98/common"]
	clear_screen = "clear && printf '\e[3J'"
	unix = './'
	cesc = [
		'\033[48;5;204m  ',
		'\033[48;5;124m  ',
		'\033[48;5;52m  ',
		'\033[48;5;208m  ',
		'\033[48;5;202m  ' ,
		'\033[48;5;1m  ',
		'\033[48;5;220m  ',
		'\033[48;5;214m  ',
		'\033[48;5;136m  ',
		'\033[48;5;76m  ',
		'\033[48;5;28m  ',
		'\033[48;5;22m  ',
		'\033[48;5;32m  ',
		'\033[48;5;25m  ',
		'\033[48;5;19m  ',
		'\033[48;5;18m  ',
		'\033[48;5;134m  ',
		'\033[48;5;91m  ',
		'\033[48;5;56m  ',
		'\033[48;5;15m  ',
		'\033[48;5;249m  ',
		'\033[48;5;241m  ',
		'\033[48;5;237m  '
	]
	hair_cl_d = {'blond':'\033[48;5;11m  \033[0m','brown':'\033[48;5;52m  \033[0m','red':'\033[48;5;208m  \033[0m','BLack':'\033[48;5;0m  \033[0m'}
	skin_cl_d = ['\033[48;5;224m  \033[0m','\033[48;5;223m  \033[0m','\033[48;5;130m  \033[0m','\033[48;5;52m  \033[0m']

#constants
roles = ['GK','SW','LB','CB','RB','LM','CM','RM','LF','CF','RF']
hair_cl = ['blond','brown','red','BLack']
skin_cl = ['fairer','fair','dark','darker']
faces = ['type 1','type 2','type 3','type 4','type 5','type 6','type 7']
beards = ['beard only','mouche','moustache','three-day','full','goatee','clean']
hairs = ['afro','receding','tidy','high fade','curly','long back','parted','long front','monk','machine cut','bald/shaven']

nation_codes = {1: 8, 2: 12, 3: 39, 16: 44, 17: 46, 18: 64, 19: 342, 32: 343, 33: 344, 34: 50, 35: 19, 48: 15, 49: 29, 50: 48, 51: 14, 64: 53, 65: 35, 66: 65, 67: 23, 80: 201, 81: 11, 82: 'Serbia', 83: 299, 96: 9, 97: 52, 98: 43, 99: 41, 112: 305, 113: 202, 114: 18, 115: 306, 128: 330, 129: 331, 130: 332, 131: 333, 144: 10, 145: 25, 146: 17, 147: 16, 160: 38, 161: 191, 162: 24, 163: 278, 176: 193, 177: 20, 178: 345, 179: 47, 192: 40, 193: 28, 194: 13, 195: 37, 208: 63, 209: 298, 210: 208, 211: 285, 224: 275, 225: 27, 226: 30, 227: 273, 240: 42, 241: 32, 242: 34, 243: 281, 256: 199, 257: 'Mali', 258: 257, 259: 194, 272: 286, 273: 288, 274: 269, 275: 66, 288: 200, 289: 302, 290: 303, 291: 49, 304: 22, 305: 307, 306: 308, 307: 309, 320: 310, 321: 311, 322: 312, 323: 313, 336: 31, 337: 314, 338: 315, 339: 316, 352: 317, 353: 318, 354: 319, 355: 320, 368: 26, 369: 21, 370: 321, 371: 322, 384: 323, 385: 196, 386: 45, 387: 324, 400: 325, 401: 326, 402: 327, 403: 328, 416: 329, 417: 241, 418: 243, 419: 237, 432: 242, 433: 244, 434: 239, 435: 240, 448: 238, 449: 248, 450: 249, 451: 250, 464: 251, 465: 247, 466: 252, 467: 245, 480: 255, 481: 246, 482: 254, 483: 253, 496: 256, 497: 258, 498: 259, 499: 195, 512: 260, 513: 261, 514: 33, 515: 6, 528: 334, 529: 335, 530: 336, 531: 341, 544: 36, 545: 340, 546: 337, 547: 338, 560: 339, 561: 289, 562: 290, 563: 291, 576: 51, 577: 292, 578: 293, 579: 294, 592: 295, 593: 296, 594: 297, 595: 300, 608: 301, 609: 304, 610: 7, 611: 263, 624: 265, 625: 267, 626: 270, 627: 272, 640: 276, 641: 262, 642: 277, 643: 279, 656: 266, 657: 280, 658: 282, 659: 283, 672: 284, 673: 268, 674: 287, 675: 271, 688: 274, 689: 264, 690: 192}
nations = {}

leagues = {
	0: [113, 132, 116, 127, 112, 131, 124, 115, 228, 125, 129, 114, 128, 123, 122, 130, 229, 349, 356, 126],
	1: [85, 94, 87, 355, 93, 357, 354, 139, 92, 91, 88, 140, 89, 234, 86, 90, 138, 137],
	2: [204, 205, 0, 2, 5, 1, 150, 152, 149, 203, 3, 207, 154, 153, 206, 151, 4, 148],
	3: [119,103,109,102,156,118,117,105,104,107,106,108,155,351,350,120,121,230],
	4: [69,60,54,358,159,158,58,59,61,62,57,67,68,70,55,160,197,56,157,198],
	5: [73, 84, 79, 134, 72, 360, 76, 81, 136, 74, 77, 80, 133, 83, 75, 78, 82, 135],
	6: [71, 223, 225, 222, 215, 212, 218, 214, 221, 211, 219, 220, 226, 217, 224, 216, 227, 213, 209, 210],
	7: [175, 163, 165, 164, 166, 162, 161, 168, 167, 170, 174, 171, 169, 172, 173],
	8: [95, 100, 111, 110, 233, 96, 99, 232, 353, 97, 352, 177, 178, 101, 231, 176, 98, 179],
	9: [143, 144, 359, 142, 145, 236, 147, 146, 235, 141],
	10: [180, 347, 185, 187, 189, 346, 348, 182, 181, 186, 183, 190, 188, 184],
}
league_teams = reduce(lambda x,y: x + y[1], leagues.items(), [])

tactics = [
	'5-4-1',
	'5-3-2',
	'4-5-1',
	'1-3-4-2',
	'1-3-3-3',
	'4-4-2',
	'4-3-3',
	'3-5-2',
	'3-4-3'
]

bank = 2.78125

stadiums = [
	'Olympiastadion',
	'Azteca',
	'Camp Nou',
	'Tokyo Olympic',
	'Wembley',
	'Maracana',
	'San Siro',
	'Ellis Park (SAF)',
	'Parc des Princes',
	'Rose Bowl',
	'Sydney Football Stadium',
	'Jamsil Olympic',
	'Amsterdam Arena',
	'Hasely Crawford (T&T)',
	'Råsunda',
	'Ahmadou Ahidjo'
]

colours = [
	'pink',
	'red',
	'bordeaux',
	'saffron',
	'orange',
	'brown',
	'yellow',
	'gold',
	'bronze',
	'light green',
	'medium green',
	'dark green',
	'sky blue',
	'light blue',
	'blue',
	'navy',
	'lilac',
	'purple',
	'violet',
	'white',
	'silver',
	'grey',
	'black'
]
shorts = [
	'plain',
	'hor.trim',
	'ver.stripe'
]
socks = [
	'plain',
	'trim',
	'stripes'
]
jersey_types = [
	'collar',
	'plain',
	'collar and sleeves',
	'collar and armholes',
	'England 98',
	'Arsenal 90s',
	'Ajax',
	'narrow vertical line',
	'horizontal line',
	'shoulders and sleeves',
	'sgl vert stripes chest',
	'dbl vert stripes shld',
	'AS Roma 97-98',
	'Cagliari',
	'collar, shld, sleeves',
	'Sampdoria',
	'bibe',
	'Scandinavian cross',
	'horizontal stripes',
	'thin horizontal stripes',
	'low vertical stripes',
	'vertical stripes',
	'Udinese 90s',
	'double stripes on sides',
	'Germany 94',
	'Croatia',
	'Siena 2004-05',
	'dbl vert stripes chest',
	'Perugia 98-99',
	'diagonal top right',
	'diagonal top left',
	'belly swoosh',
	'chest swooshes'
]
strategia = [
	'+2 att',
	'+1 att',
	'bal',
	'+1 def',
	'+2 def'
]

fieldopedia = {
	'Name': {'short': 'Name', 'width': 16, 'db': 'name', 'align':'l'},
	'ID': {'short': 'ID', 'width': 5, 'db': 'id', 'align':'c'},
	'Nation': {'short': 'Nation', 'width': 21, 'db': 'country', 'align':'l'},
	'Hair Type': {'short': 'H', 'width': 1, 'db': 'hair type', 'align':'c'}, 
	'Hair Colour': {'short': 'HC', 'width': 2, 'db': 'hair colour', 'align':'c'},  
	'Skin Colour': {'short': 'SC', 'width': 2, 'db': 'skin colour', 'align':'c'},
	'Face': {'short': 'F', 'width': 1, 'db': 'face', 'align':'c'}, 
	'Beard': {'short': 'B', 'width': 1, 'db': 'beard', 'align':'c'},
	'Price': {'short': '$$$', 'width': 7, 'db': 'price', 'align':'r'},
	'Jersey': {'short': 'Jers', 'width': 4, 'db': 'jersey', 'align':'r'},
	'Role': {'short': 'Role', 'width': 4, 'db': 'role', 'align':'c'},
	'Aggression': {'short': 'Aggr', 'width': 4, 'db': 'aggression', 'align':'c'},
	'Acceleration': {'short': 'Accl', 'width': 4, 'db': 'acceleration', 'align':'c'},
	'Attack Bias': {'short': 'AttB', 'width': 4, 'db': 'attack bias', 'align':'c'},
	'Agility': {'short': 'Agil', 'width': 4, 'db': 'agility', 'align':'c'},
	'Ball Control': {'short': 'Ball', 'width': 4, 'db': 'ball', 'align':'c'},
	'Awareness': {'short': 'Awar', 'width': 4, 'db': 'awareness', 'align':'c'},
	'Fitness': {'short': 'Fitn', 'width': 4, 'db': 'fitness', 'align':'c'},
	'Creativity': {'short': 'Crea', 'width': 4, 'db': 'creativity', 'align':'c'},
	'Passing': {'short': 'Pass', 'width': 4, 'db': 'passing', 'align':'c'},
	'Heading': {'short': 'Head', 'width': 4, 'db': 'heading', 'align':'c'},
	'Reaction': {'short': 'Reac', 'width': 4, 'db': 'reaction', 'align':'c'},
	'Pass Bias': {'short': 'PBia', 'width': 4, 'db': 'pass bias', 'align':'c'},
	'Shot Power': {'short': 'SPow', 'width': 4, 'db': 'shot power', 'align':'c'},
	'Shot Bias': {'short': 'SBia', 'width': 4, 'db': 'shot bias', 'align':'c'},
	'Speed': {'short': 'Spee', 'width': 4, 'db': 'speed', 'align':'c'},
	'Shot Accuracy': {'short': 'SAcc', 'width': 4, 'db': 'shot accuracy', 'align':'c'},
	'Tackle': {'short': 'Tack', 'width': 4, 'db': 'tackle', 'align':'c'},
	'Average': {'short': 'AV', 'width': 4, 'db': 'average', 'align':'c'},
	'Index FCDBPENG': {'short': 'InFPE', 'width': 5, 'db': 'index_fcdbpeng', 'align':'r'},
	'Index FCDB': {'short': 'InFCDB', 'width': 6, 'db': 'index_fcdb', 'align':'r'},
	'Team': {'short': 'Team', 'width': 13, 'db': 'team', 'align':'l'},
	'International': {'short': '', 'width': 0, 'db': 'international', 'align':'l'}
}

field_order = ['Name','ID','Nation','Hair Type','Hair Colour','Skin Colour','Face','Beard','Price','Jersey','Role','Aggression','Acceleration','Attack Bias','Agility','Ball Control','Awareness','Fitness','Creativity','Passing','Heading','Reaction','Pass Bias','Shot Power','Shot Bias','Speed','Shot Accuracy','Tackle','Average','Index FCDBPENG','Index FCDB','Team','International']

skill_fields = field_order[11:28]
ai_fields =[x-11 for x in [11,13,22,24]]

fs_left = ['{0}{1}'.format(fieldopedia[k]['short'],(fieldopedia[k]['width']-len(fieldopedia[k]['short']))*' ') for k in fieldopedia.keys() if len(fieldopedia[k]['short'])>0]
fs_right = ['{1}{0}'.format(fieldopedia[k]['short'],(fieldopedia[k]['width']-len(fieldopedia[k]['short']))*' ') for k in fieldopedia.keys() if len(fieldopedia[k]['short'])>0]
fs_center = ['{1}{0}{2}'.format(fieldopedia[k]['short'],math.floor((fieldopedia[k]['width']-len(fieldopedia[k]['short']))/2)*' ',math.ceil((fieldopedia[k]['width']-len(fieldopedia[k]['short']))/2)*' ') for k in fieldopedia.keys() if len(fieldopedia[k]['short'])>0]

#graphics
border='+%s+'%'+'.join(['='*fieldopedia[x]['width'] for x in field_order[:-1]])
inner_line='|%s|'%'+'.join(['―'*fieldopedia[x]['width'] for x in field_order[:-1]])

#functions
def save(where, what):
	shutil.copyfile(where, where+'.bak')
	output = open(where, 'wb+')
	output.write(what)
	output.close()

def align(t,f):
	if str(t).find('\033') == -1:
		al = fieldopedia[f]['align']
		t = str(t)
		if fieldopedia[f]['width'] == 1:
			t = '{:X}'.format(int(t))
		if len(t) > fieldopedia[f]['width']:
			t = t[:fieldopedia[f]['width']-2] + '..'
		if al == 'l':	
			return '{0}{1}'.format(t, (fieldopedia[f]['width']-len(t))*' ')
		elif al == 'r':
			return '{1}{0}'.format(t, (fieldopedia[f]['width']-len(t))*' ')
		elif al == 'c':
			return '{1}{0}{2}'.format(t, math.floor((fieldopedia[f]['width']-len(t))/2)*' ', math.ceil((fieldopedia[f]['width']-len(t))/2)*' ')
	else:
		return t

def cpdb():
	global players
	pl_temp = copy.deepcopy(players)
	players_db = {}
	for x in pl_temp:
		id = x['id']
		del x['id']
		players_db.setdefault(id, x)
	del pl_temp
	return players_db

def load_database(**args):
	if args.get('load',0) > 0: return
	global players, teams, league_list, nations
	
	#load player names
	print('\033[KLoading names...', end ='')
	players = []
	nomi = open(f_nomi, 'r+b')
	nomi.seek(28,0)
	n_indexes = []
	init_byte = struct.unpack("<h", nomi.read(2))[0]+20
	end_names = init_byte
	nomi.seek(28,0)
	while True:
		if nomi.tell() == end_names:
			break
		n_indexes.append(struct.unpack("<l", nomi.read(4))[0]+20)
	for _ in n_indexes:
		nomi.seek(_,0)
		string = b''
		while True:
			new_char = nomi.read(1)
			if new_char != b'\x00':
				string += new_char
			else:
				if len(string) > 0:
					players.append({'name':string.decode('unicode_escape'), 'index_fcdbpeng': _})
				break
	nomi.close()

	#load league names
	squadre = open(f_squadre, 'r+b')
	league_list = []
	string = b''
	squadre.seek(8,0)
	init_size_list = struct.unpack("<h", squadre.read(2))[0]+8
	squadre.seek(20,0)
	how_many = struct.unpack("<h", squadre.read(2))[0]
	squadre.seek(init_size_list,0)
	init_byte = struct.unpack("<h", squadre.read(2))[0]+20
	squadre.seek(init_byte,0)
	zerocount = 0
	string = b''
	while True:
		new_char = squadre.read(1)
		if new_char == b'\x00':
			zerocount +=1
			league_list.append(string.decode('unicode-escape'))
			string = b''
		else:
			string += new_char
		if zerocount == how_many:
			break
	league_list = league_list[:len(leagues)] + ['National Teams'] + league_list[len(leagues):]
	
	#load team names
	teams = []
	print('\r\033[KLoading team names...', end = '')
	team_indexes = []
	#beginning of namelist
	squadre.seek(12,0)
	init_byte = struct.unpack("<h", squadre.read(2))[0]
	squadre.seek(init_byte+8, 0)
	while True:
		team_indexes.append(init_byte + struct.unpack("<l", squadre.read(4))[0])
		if squadre.tell() == team_indexes[0]+4: break
	for w, team_index in enumerate(team_indexes):
		string = b''
		squadre.seek(team_index, 0)
		temp_list = []
		while True:
			current_idx = squadre.tell()
			try:
				next_one = team_indexes[w+1]
			except:
				next_one = 20000
			if current_idx < next_one:
				new_char = squadre.read(1)
				if not new_char:
					break
				elif new_char != b'\x00':
					string += new_char
				else:
					if len(string) > 0:	
						temp_list.append(string.decode('unicode_escape'))
						string = b''
			else:
				break
		if len(temp_list) > 0:
			teams.append({'names': temp_list, 'index_fcdbpeng': team_index, 'db_position': w})
			for nation_id, pos in nation_codes.items():
				if pos == w:
					nations.setdefault(nation_id, temp_list[-1])
					teams[-1].setdefault('nation', nation_id)
	for nation_id, pos in nation_codes.items():
		if not type(pos) == int: nations.setdefault(nation_id, pos)
	squadre.close()
	#loading database
	print('\r\033[KLoading parameters...\r', end = '')
	valori = open(f_valori, 'r+b')
	valori.seek(12,0)
	init_teams = struct.unpack("<h", valori.read(2))[0]+8
	valori.seek(16,0)
	init_byte = struct.unpack("<h", valori.read(2))[0]+8
	valori.seek(init_teams, 0)
	
	#retrieve team data
	squad = b''
	sq_idx = 0
	sq_itr = 0
	while True:
		sq_idx = valori.tell()
		squad = valori.read(64)
		if valori.tell() >= init_byte:
			break
		else:
			teams[sq_itr]['index_fcdb'] = sq_idx
			teams[sq_itr]['squad'] = list(set(["{:04X}".format(int.from_bytes(squad[i:i+2] , 'big')) for i in range(24,64,2) if int.from_bytes(squad[i:i+2] , 'big') != 0]))
			teams[sq_itr]['id'] = ((int.from_bytes(squad[1:2], 'big') & 7) << 8) + int.from_bytes(squad[0:1], 'big')
			teams[sq_itr]['bank'] = int((((int.from_bytes(squad[1:2], 'big') & 248) >> 3) + (int.from_bytes(squad[2:3], 'big') << 5) + ((int.from_bytes(squad[3:4], 'big') & 15) << 13)) * bank)
			teams[sq_itr]['stadium'] = stadiums[int.from_bytes(squad[3:4], 'big') >> 4]
			teams[sq_itr]['first shirt'] = jersey_types[int.from_bytes(squad[5:6], 'big') >> 2]
			teams[sq_itr]['first shirt - colour 1'] = int.from_bytes(squad[4:5], 'big') & 31
			teams[sq_itr]['first shirt - colour 2'] = ((int.from_bytes(squad[5:6], 'big') & 3) << 3) + (int.from_bytes(squad[4:5], 'big') >> 5)
			teams[sq_itr]['first shirt - colour 3'] = int.from_bytes(squad[6:7], 'big') & 31
			teams[sq_itr]['first shorts'] = shorts[int.from_bytes(squad[7:8], 'big') >> 6]
			teams[sq_itr]['first shorts - colour 1'] = (int.from_bytes(squad[6:7], 'big') >> 5) + ((int.from_bytes(squad[7:8], 'big') & 3) << 3)
			teams[sq_itr]['first shorts - colour 2'] = int.from_bytes(squad[8:9], 'big') & 31
			teams[sq_itr]['first socks'] = socks[int.from_bytes(squad[11:12], 'big') >> 6]
			teams[sq_itr]['first socks - colour 1'] = (int.from_bytes(squad[8:9], 'big') >> 5) + ((int.from_bytes(squad[9:10], 'big') & 3) << 3)
			teams[sq_itr]['first socks - colour 2'] = int.from_bytes(squad[10:11], 'big') & 31
			teams[sq_itr]['second shirt']  = jersey_types[int.from_bytes(squad[13:14], 'big') >> 2]
			teams[sq_itr]['second shirt - colour 1'] = int.from_bytes(squad[12:13], 'big') & 31
			teams[sq_itr]['second shirt - colour 2'] = ((int.from_bytes(squad[13:14], 'big') & 3) << 3) + (int.from_bytes(squad[12:13], 'big') >> 5)
			teams[sq_itr]['second shirt - colour 3'] = int.from_bytes(squad[14:15], 'big') & 31
			teams[sq_itr]['second shorts'] = shorts[int.from_bytes(squad[15:16], 'big') >> 6]
			teams[sq_itr]['second shorts - colour 1'] = (int.from_bytes(squad[14:15], 'big') >> 5) + ((int.from_bytes(squad[15:16], 'big') & 3) << 3)
			teams[sq_itr]['second shorts - colour 2'] = int.from_bytes(squad[16:17], 'big') & 31
			teams[sq_itr]['second socks'] = socks[(int.from_bytes(squad[19:20], 'big') >> 4) & 3]
			teams[sq_itr]['second socks - colour 1'] = (int.from_bytes(squad[16:17], 'big') >> 5) + ((int.from_bytes(squad[17:18], 'big') & 3) << 3)
			teams[sq_itr]['second socks - colour 2'] = int.from_bytes(squad[18:19], 'big') & 31
			teams[sq_itr]['strategy'] = strategia[int.from_bytes(squad[17:18], 'big') >> 5]
			teams[sq_itr]['tactics'] = tactics[int.from_bytes(squad[21:22], 'big') >> 2]
			teams[sq_itr]['roster size'] = (int.from_bytes(squad[22:23], 'big') & 15) * 2
			teams[sq_itr]['league'] = len(leagues)
			for nn,l in leagues.items():
				if sq_itr in l:
					teams[sq_itr]['league'] = nn
		sq_itr+=1
	#retrieve player data
	valori.seek(init_byte, 0)
	current_idx = init_byte
	iterations = 0
	bit_idx = 0
	string = b''
	while True:
		new_char = valori.read(1)
		if not new_char:
			players[iterations]['index_fcdb']=current_idx
			break
		else:
			string += new_char
			if valori.tell() == current_idx + 21:
				players[iterations]['index_fcdb']=current_idx
				string = new_char
				current_idx = valori.tell()-1
				iterations += 1
				bit_idx = 0
			if bit_idx == 0:
				players[iterations]['id'] = int.from_bytes(new_char, 'big')
			if bit_idx == 1:
				players[iterations]['id'] = ((int.from_bytes(new_char, 'big') & 63) << 8) + players[iterations]['id']
				players[iterations]['id'] = "{:04X}".format(int.from_bytes(players[iterations]['id'].to_bytes(2, 'little'), 'big'))
				players[iterations]['team'] = '---'
				players[iterations]['team_id'] = -1
				players[iterations]['international'] = []
				players[iterations]['international_id'] = []
				for t in teams:
					if players[iterations]['id'] in t['squad']:
						if t['db_position'] in league_teams:
							players[iterations]['team'] = t['names'][-1]
							players[iterations]['team_id'] = t['db_position']
						else:
							players[iterations]['international'].append(t['names'][-1])
							players[iterations]['international_id'].append(t['nation'])
				players[iterations]['nation'] = (int.from_bytes(new_char, 'big') & 192) >> 6
			if bit_idx == 2:
				players[iterations]['nation'] = (int.from_bytes(new_char, 'big') << 4) + players[iterations]['nation']
				players[iterations]['country'] = nations[players[iterations]['nation']]
			if bit_idx == 3: players[iterations]['starting'] = int.from_bytes(new_char, 'big')
			if bit_idx == 4:
				players[iterations]['price'] = int.from_bytes(new_char, 'big')
			if bit_idx == 5:
				players[iterations]['price'] = (int.from_bytes(new_char, 'big') << 8) + players[iterations]['price']		
			if bit_idx == 6:
				hair = int.from_bytes(new_char, 'big') >> 4
				hair_c = hair_cl[(int.from_bytes(new_char, 'big') & 12) >> 2]
				skin_c = int.from_bytes(new_char, 'big') & 3
				players[iterations]['hair type'] = hair
				players[iterations]['hair colour'] = hair_c
				players[iterations]['skin colour'] = skin_c
			if bit_idx == 7:
				face = int.from_bytes(new_char, 'big') >> 3
				beard = int.from_bytes(new_char, 'big') & 7
				players[iterations]['face'] = face
				players[iterations]['beard'] = beard
			if bit_idx == 8:
				players[iterations]['aggression'] = ((int.from_bytes(new_char, 'big') & 240) >> 4)*4+39
				players[iterations]['acceleration'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 9:
				players[iterations]['attack bias'] = ((int.from_bytes(new_char, 'big') & 240) >> 4)*4+39
				players[iterations]['agility'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 10:
				players[iterations]['ball'] = ((int.from_bytes(new_char, 'big') & 240)>>4)*4+39
				players[iterations]['awareness'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 11:
				players[iterations]['fitness'] = ((int.from_bytes(new_char, 'big') & 240)>>4)*4+39
				players[iterations]['creativity'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 12:
				players[iterations]['passing'] = ((int.from_bytes(new_char, 'big') & 240)>>4)*4+39
				players[iterations]['heading'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 13:
				players[iterations]['reaction'] = ((int.from_bytes(new_char, 'big') & 240)>>4)*4+39
				players[iterations]['pass bias'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 14:
				players[iterations]['shot power'] = ((int.from_bytes(new_char, 'big') & 240)>>4)*4+39
				players[iterations]['shot bias'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 15:
				players[iterations]['speed'] = ((int.from_bytes(new_char, 'big') & 240)>>4)*4+39
				players[iterations]['shot accuracy'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 16:
				players[iterations]['jersey'] = ((int.from_bytes(new_char, 'big') & 240)>>4)
				players[iterations]['tackle'] = (int.from_bytes(new_char, 'big') & 15)*4+39
			if bit_idx == 17:
				players[iterations]['role'] = roles[((int.from_bytes(new_char, 'big') & 240)>>4)]
				players[iterations]['jersey'] = (int.from_bytes(new_char, 'big') & 15)*16 + players[iterations]['jersey']
			if bit_idx == 18:
				players[iterations]['average']  = math.floor(sum([players[iterations][fieldopedia[r]['db']] for r in skill_fields])/len(skill_fields))
			bit_idx +=1
			
		if debug == True:
			binary = []
			for bit in string:
				binary.append("{0:08b}".format(bit).upper())
			players[iterations]['binary'] = binary
	if debug == True:
		print('Detecting problems...\n')
		team_db = {}
		name_db = {}
		for x in players:
			team_db.setdefault(x['team_id'], []).append((x['team'],x['jersey'],x['name'],x['index_fcdb']))
			name_db.setdefault(x['name'],set()).add(x['id'])
		for team,values in team_db.items():
			if team == -1: continue
			if team not in league_teams: continue
			if len(values) not in [12,14,16,18,20]:
				print('%s has %s players'%(values[0][0], len(values)))
			val = []
			for j in values:
				val.append(j[1])
			un_val = set(val)
			if len(un_val) < len(val):
				print(values[0][0], 'has conflicting jerseys')
				for p in un_val:
					val.remove(p)
				for j in values:
					if j[1] in val:
						new_jersey = j[1]
						while True:
							new_jersey += 1
							if new_jersey > 99: new_jersey-=99
							if new_jersey not in un_val:
								un_val.add(new_jersey)
								val.remove(j[1])
								break
						if input('\tThe new jersey for %s is %s [yn]: '%(j[2], new_jersey)) == 'y':
							edit_player(j[3],field='j',value=new_jersey)
		for dupl_name,howmany in name_db.items():
			if len(howmany) > 1:
				dupl_teams = [y['team'] for y in players if y['id'] in howmany and y['team_id'] not in league_teams]
				dupl_purged = list(filter(lambda b: b!= '---', dupl_teams))
				if len(dupl_purged) > 1:
					print('There are %s players named %s, in %s'%(len(howmany),dupl_name, ', '.join(dupl_purged)))
					
def search_players(a,field,*laconic, **kwargs):	
	results = []
	if not laconic:
		if debug == True:
			print()
			print('|%s|%s'%(30*'=',20*'====|'))
			print('|%s%s%s|%s|'%(13*' ','NAME',13*' ','|'.join(["{:4d}".format(x) for x in range(20)])))
		if table == True:
			print()
			print(border)
			print('|%s|'%'|'.join(fs_center))
			fields = [set(),[],set(),[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	for b in str(a).split('/'):
		for x in players:
			what = b.strip()
			where = str(x.get(field, ''))
			if field.upper() == 'INTERNATIONAL' and len(where) > 2: where = where[1:-1]
			if case_sensitive == False:
				what = what.upper()
				where = where.upper()
			found = what == where if kwargs.get('strict', False) else what in where
			if where[0]+where[-1] == "[]": found = str(what) in [str(_) for _ in eval(where)]
			if found:
				if not laconic:
					if debug == True:
						print('|%s|%s'%(30*'-',20*'----|'))
						print('|%s%s|%s|'%(x['name'],(30-len(x['name']))*' ','|'.join([w[:4] for w in x['binary']])))
						print('|%s|%s|'%(30*' ','|'.join([w[4:] for w in x['binary']])))
					else:
						if table == False:
							int_string = ', '.join(x['international'])
							print('\n%s'%('#'*40))
							print('Name:',x['name'], sep='\t\t\t')
							print(40*'#')
							print('ID:',x['id'], sep='\t\t\t')
							print('Nation:',x['country'], sep='\t\t\t')
							print('Hair Type:',hairs[x['hair type']], sep='\t\t')
							print('Hair Colour:',x['hair colour'].lower(), sep='\t\t')
							print('Skin Colour:',skin_cl[x['skin colour']], sep='\t\t')
							print('Face:',faces[x['face']], sep='\t\t\t')
							print('Beard:',beards[x['beard']], sep='\t\t\t')
							print(40*'#')
							print('Price:',x['price'], sep='\t\t\t')
							print('Jersey:',x['jersey'], sep='\t\t\t')
							print('Role:',x['role'], sep='\t\t\t')
							print(40*'#')
							print('Speed:',x['speed'], sep='\t\t\t')
							print('Acceleration:',x['acceleration'], sep='\t\t')
							print('Agility:',x['agility'], sep='\t\t')
							print('Aggression:',x['aggression'], sep='\t\t')
							print('Attack Bias:',x['attack bias'], sep='\t\t')
							print('Ball Control:',x['ball'], sep='\t\t')
							print('Awareness:',x['awareness'], sep='\t\t')
							print('Fitness:',x['fitness'], sep='\t\t')
							print('Creativity:',x['creativity'], sep='\t\t')
							print('Passing:',x['passing'], sep='\t\t')
							print('Pass Bias:',x['pass bias'], sep='\t\t')
							print('Heading:',x['heading'], sep='\t\t')
							print('Reaction:',x['reaction'], sep='\t\t')
							print('Tackle:',x['tackle'], sep='\t\t\t')
							print('Shot Bias:',x['shot bias'], sep='\t\t')
							print('Shot power:',x['shot power'], sep='\t\t')
							print('Shot accuracy:',x['shot accuracy'], sep='\t\t')
							print(40*'#')
							print('AVERAGE:', x['average'], sep ='\t\t')
							print(40*'#')
							print('Team:', x['team'], sep ='\t\t\t')
							print('International:', int_string, sep ='\t\t')
							print(40*'#')
							print('Index FCDBPENG',x['index_fcdbpeng'], sep='\t\t')
							print('Index FCDB',x['index_fcdb'], sep='\t\t')
							print(40*'#')
							print()
						else:
							team_string = "{:<10}".format(x['team'])
							international = ['','']
							for n in x['international_id']:
								if n != x['nation']:
									international[1] = ' (%s*)'%nations[n]
								if n == x['nation']:
									international[0] = '*'
							international = ''.join(international)
								
							if len(team_string)>10:team_string=team_string[:8]+'..'
							
							print(inner_line)
							tbl_row ='|'
							for g in field_order[:-1]:
								cell_content = x[fieldopedia[g]['db']]
								if g == 'Hair Colour' :cell_content = hair_cl_d[cell_content]
								if g == 'Skin Colour' :cell_content = skin_cl_d[cell_content]
								if g == 'Nation': cell_content += international
								tbl_row += align(cell_content,g)
								tbl_row += '|'
							print(tbl_row)
							
							fields_off = ['Name','ID','Hair Type','Hair Colour','Skin Colour','Face','Beard','Role','Index FCDBPENG','Index FCDB','Team','International']
							cy = 0
							for f in field_order:
								if f not in fields_off:
									try:
										fields[cy].add(x[fieldopedia[f]['db']])
									except:
										fields[cy].append(x[fieldopedia[f]['db']])
									cy+=1
									
					results.append((x['name'], x['index_fcdb']))
				else:
					results = [x[fieldopedia[g]['db']] for g in skill_fields]
					results += [x['hair colour'],x['skin colour'],x['face'],x['beard'],x['hair type'],x['jersey'],x['role'],x['name'],x['index_fcdbpeng'],players.index(x)]
	if not laconic:
		if debug == True:
			print('|%s|%s'%(30*'=',20*'====|'))
			print()
			print('Legend: 0.1 = ID; 1.1.1 = Nation, 1.1.2 = ID, 1.2 = ID; 2 = Nation; 3 = In starting lineup; 4 and 5 = Price; 6.1 = Hair, 6.2.1 = Hair Colour 6.2.2 = Skin Colour; 7.1 = Face, 7.2 = Beard; 8.1 = Aggression, 8.2 = Acceleration; 9.1 = Attack Bias, 9.2 = Agility; 10.1 = Ball, 10.2 = Awareness; 11.1 = Fitness, 11.2 = Creativity; 12.1 = Passing, 12.2 = Heading; 13.1 = Reaction, 13.2 = Pass Bias; 14.1 = Shot Power, 14.2 = Shot Bias; 15.1 = Speed, 15.2 = Shot Accuracy; 16.1 = Jersey (low), 16.2 = Tackle; 17.1 = Role, 17.2 = Jersey (high); 18 and 19 = ?')
			print()
		if table == True:
			if len(results) == 0:
				print(inner_line)
				print('| No results%s|'%((sum([fieldopedia[c]['width'] for c in fieldopedia.keys()])+len(fieldopedia.keys())-13)*' '))
				print(border)
				return results
			conflict = 'ok'
			if len(fields[2]) != len(fields[1]): conflict = '!!'
			print(border)
			if not debug:
				for e,data in enumerate(fields):
					if e == 0: fields[e] = "{:>{width}}".format("%s nations"%len(fields[0]),width=fieldopedia['Nation']['width'])
					if e == 1: fields[e] = align(math.floor(sum(fields[e])/len(fields[e])),'Price')
					if e == 2: fields[e] = align(conflict, 'Average')
					if e > 2:  fields[e] = align(math.floor(sum(fields[e])/len(fields[e])),'Average')
			
			frag_border = ' '
			summary = ' '
			cy = 0
			for f in field_order:
				if f in fields_off:
					if frag_border[:-1] == ' ':
						frag_border = frag_border[:-1]+' '*(fieldopedia[f]['width']+2)
						summary = summary[:-1]+' '*(fieldopedia[f]['width']+2)
					else:
						frag_border += ' '*(fieldopedia[f]['width']+1)
						summary += ' '*(fieldopedia[f]['width']+1)
				else:
					summary = summary[:-1]+'|'
					summary += fields[cy]
					summary	+= '|'
					cy += 1
					frag_border = frag_border[:-1]+'+'
					frag_border += '='*fieldopedia[f]['width']
					frag_border += '+'
			print(summary,frag_border,sep='\n')
			print()
	return results
	
def edit_player(modify,**args):
	global f_valori, f_nomi, roles, nations
	vals_already = search_players(modify, 'index_fcdb', True, strict=True)
	valori = open(f_valori, 'r+b')
	temp_file = b''
	mod_offset=int(modify)
	what_to_edit = args.get('field', False)
	valid = True
	while True:
		if what_to_edit == False: what_to_edit = input("""
Parameter to edit:
	+-------------------------+
	| [0] aggression (%s)     |
	| [1] acceleration (%s)   |
	| [2] attack bias (%s)    |
	| [3] agility (%s)        |
	| [4] ball (%s)           |
	| [5] awareness (%s)      |
	| [6] fitness (%s)        |
	| [7] creativity (%s)     |
	| [8] passing (%s)        |
	| [9] heading (%s)        |
	| [10] reaction (%s)      |
	| [11] pass bias (%s)     |
	| [12] shot power (%s)    |
	| [13] shot bias (%s)     |
	| [14] speed (%s)         |
	| [15] shot accuracy (%s) |
	| [16] tackle (%s)        |
	| [*] all                 |
	+-------------------------+
	| [n]ame                  |
	| [j]ersey (%s)           |
	| [r]ole (%s)             |
	| countr[y]               |
	+-------------------------+
	| [f]ace                  |
	| [s]kin colour           |
	| [h]air                  |
	| hair c[o]lour           |
	| [b]eard                 |
	+-------------------------+
	| [c]ancel                |
	+-------------------------+
	: """%(eval(','.join(["'%s'"%'{:0>2}'.format(str(x)) for x in vals_already[:17]+vals_already[22:-3]]))))
		if len(what_to_edit) == 0:
			what_to_edit = False
			continue
		if what_to_edit == 'c':
			return mod_offset
		elif what_to_edit == 'n':
			n_prompt = 'name'
			if (new_name := args.get('value', None)) is None:
				while True:
					new_name = input('\nEnter %s (hit return to cancel): '%n_prompt)
					if len(new_name) == 0: return mod_offset
					if len(new_name) < 16:
						break
					n_prompt='max 15 characters (%s input),'%len(new_name) 
			nomi = open(f_nomi, 'r+b')
			db_name_offset = int(vals_already[-2])
			onl = len(vals_already[-3])
			nnl = len(new_name)
			nomi.seek(28,0)
			end_prelim_byte = struct.unpack("<h", nomi.read(2))[0]+20
			nomi.seek(0,0)
			#copy initial bit
			temp_file =nomi.read(28)
			last_iter = vals_already[-1]
			db_offset = 0
			while True:
				new_index = struct.unpack("<l", nomi.read(4))[0]
				temp_file += struct.pack("<l", new_index+db_offset)
				if nomi.tell() == (last_iter+1)*4+28:
					db_offset = nnl-onl
				if nomi.tell() == end_prelim_byte:
					break
			temp_file += nomi.read(db_name_offset-nomi.tell())
			temp_file += bytes(new_name, 'iso-8859-1')
			temp_file += b'\x00'
			while True:
				new_char = nomi.read(1)
				if new_char == b'\x00':
					break
			temp_file += nomi.read()
			save(f_nomi, temp_file)
			nomi.close()
			load_database()
		elif what_to_edit == 'j':
			new_jersey = int(args.get('value', 100))
			if new_jersey == 100: new_jersey = int(inputPlus('\nEnter new jersey (hit return to cancel)',[_ for _ in range(1,101)], entC=True)[0])
			if new_jersey == 100: return mod_offset
			jersey_bit = [0,0]
			jersey_bit[1] = math.floor(new_jersey/16)
			jersey_bit[0] = (new_jersey-(jersey_bit[1]*16))<<4
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 16:
					temp_file += valori.read(1)
				if bit == 16:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 15)+jersey_bit[0]
					temp_file += bytes([temp_bit])
				if bit == 17:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 240)+jersey_bit[1]
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'r':
			if (new_role := args.get('value', None)) is None:
				new_role = int(inputPlus('\nEnter new role ($OPTIONLIST_l$$CANCEL$)', roles, sep=', ', c=True)[0]) 
				if new_role == len(roles): return mod_offset
				else: new_role = new_role << 4
			else: 
				new_role=roles.index(new_role)<<4
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 17:
					temp_file += valori.read(1)
				if bit == 17:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 15)+new_role
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'y':
			countries = {}
			for k,v in nations.items(): countries.setdefault(v.upper(),[]).append(k)
			duplicates = [k for k,_ in countries.items() if len(_) > 1]
			if len(duplicates) > 0:
				print('The following country name is a duplicate: %s. Fix the problem before proceeding'%', '.join(duplicates))
				break
			else:
				countries = {x:y[0] for x,y in countries.items()}
			new_country= args.get('value', '')
			if new_country.upper() not in countries.keys():
				print('\n')
				nl  = '\n' if platform.system() == 'Windows' else ''
				while True:
					new_country = input('\033[1A\033[KEnter new country (hit return to cancel; [l]ist countries): ')
					if new_country.upper() in countries.keys():
						break
					elif new_country == '': return mod_offset
					elif new_country == 'l':
						col = 0
						clist = [_.title() for _ in sorted(countries.keys())]
						col_height = 30
						col_width = 21
						left_spacing = 50
						upward_offset = 37
						print('\033[{0}A\033[{3}C{1:^{2}}'.format(upward_offset, 'COUNTRIES', col_width * math.ceil(len(clist)/col_height), left_spacing))
						for w,_ in enumerate(clist):
							if w % col_height == 0 and w > 0:
								print('\033[%sA'%col_height, end = '')
								col += 1
							print('%s\033[E\033[%sC%s'%(nl, str(left_spacing+col_width*col),_),end='')
						print('\n'*(upward_offset-col_height-2+(col_height-len(clist)%col_height)))
			new_country = countries[new_country.upper()]
			nc_b1 = (new_country & 3) << 6
			nc_b2 = new_country >> 4
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			for bit in range(20):
				if bit < 1:
					temp_file += valori.read(1)
				if bit == 1:
					nc_b1 = (int.from_bytes(valori.read(1), 'big') & 63) + nc_b1
					temp_file += bytes([nc_b1])
				if bit == 2:
					temp_file += bytes([nc_b2])
					valori.seek(1,1)
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'st':
			starting = args.get('value',None)
			starting = 128 if starting is None else 180
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			for bit in range(20):
				if bit < 3:
					temp_file += valori.read(1)
				if bit == 3:
					temp_file += bytes([starting])
					valori.seek(1,1)
			temp_file+=valori.read()
			save(f_valori, temp_file)
		elif what_to_edit == 'f':
			new_face = args.get('value', None)
			if new_face is None:
				print('\nSelect new face')
				face_sel = tk.Tk()
				face_sel.geometry('+0+0')
				photo = []
				def callback(n):
					global c
					c = int(n['text'])
					face_sel.destroy()
					if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				for f in range(0,7):
					col_img = colorize_feats("FifaStyles/fs0%s.png"%f, vals_already[-9])
					hair = colorize_feats("FifaStyles/hs{:02}.png".format(vals_already[-6]), vals_already[-10])
					f_hair = colorize_feats("FifaStyles/fh{:02}.png".format(vals_already[-7]), vals_already[-10])
					col_img.paste(hair,(0,0),hair)
					col_img.paste(f_hair,(0,0),f_hair)
					col_img = ImageTk.PhotoImage(image = col_img)	
					photo.append(col_img)
					btn = tk.Button(text = '%s'%f, image = photo[f], width=50, height=46)
					if f == vals_already[-8]:
						btn['highlightthickness']=4
						btn['highlightcolor']="#37d3ff"
						btn['highlightbackground']="#37d3ff"
						btn['borderwidth']=4
					btn['command'] = lambda b=btn: callback(b)
					btn.pack()
				tk.mainloop()
				try:
					new_face = c
				except:
					new_face = vals_already[-8]
				print('Face selected: %s'%faces[new_face])
			new_face = int(new_face) << 3
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 7:
					temp_file += valori.read(1)
				if bit == 7:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 7)+new_face
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'b':
			new_beard = args.get('value', None)
			if new_beard is None:
				print('\nSelect new facial hair')
				face_sel = tk.Tk()
				face_sel.geometry('+0+0')
				photo = []
				def callback(n):
					global c
					c = int(n['text'])
					face_sel.destroy()
					if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				for f in range(0,7):
					col_img = colorize_feats("FifaStyles/fs0%s.png"%vals_already[-8], vals_already[-9])
					hair = colorize_feats("FifaStyles/hs{:02}.png".format(vals_already[-6]), vals_already[-10])
					f_hair = colorize_feats("FifaStyles/fh{:02}.png".format(f), vals_already[-10])
					col_img.paste(hair,(0,0),hair)
					col_img.paste(f_hair,(0,0),f_hair)
					col_img = ImageTk.PhotoImage(image = col_img)	
					photo.append(col_img)
					btn = tk.Button(text = '%s'%f, image = photo[f], width=50, height=46)
					if f == vals_already[-7]:
						btn['highlightthickness']=4
						btn['highlightcolor']="#37d3ff"
						btn['highlightbackground']="#37d3ff"
						btn['borderwidth']=4
					btn['command'] = lambda b=btn: callback(b)
					btn.pack()
				tk.mainloop()
				try:
					new_beard = c
				except:
					new_beard = vals_already[-7]
				print('Facial hair selected: %s'%beards[new_beard])
			new_beard = int(new_beard)
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 7:
					temp_file += valori.read(1)
				if bit == 7:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 56)+new_beard
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'h':
			new_hair = args.get('value', None)
			if new_hair is None:
				print('\nSelect new hairstyle')
				face_sel = tk.Tk()
				face_sel.geometry('+0+0')
				photo = []
				def callback(n):
					global c
					c = int(n['text'])
					face_sel.destroy()
					if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				for f in range(0,11):
					col_img = colorize_feats("FifaStyles/fs0%s.png"%vals_already[-8], vals_already[-9])
					hair = colorize_feats("FifaStyles/hs{:02}.png".format(f), vals_already[-10])
					f_hair = colorize_feats("FifaStyles/fh{:02}.png".format(vals_already[-7]), vals_already[-10])
					col_img.paste(hair,(0,0),hair)
					col_img.paste(f_hair,(0,0),f_hair)
					col_img = ImageTk.PhotoImage(image = col_img)
					photo.append(col_img)
					btn = tk.Button(image = photo[f], text = '%s'%f, width=50, height=46)
					if f == vals_already[-6]:
						btn['highlightthickness']=4
						btn['highlightcolor']="#37d3ff"
						btn['highlightbackground']="#37d3ff"
						btn['borderwidth']=4
					btn['command'] = lambda b=btn: callback(b)
					btn.pack()
				tk.mainloop()
				try:
					new_hair = c
				except:
					new_hair = vals_already[-6]
				print('Hairstyle selected: %s'%hairs[new_hair])
			new_hair = int(new_hair) << 4
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 6:
					temp_file += valori.read(1)
				if bit == 6:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 15)+new_hair
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'o':
			new_hc = args.get('value', None)
			if new_hc is None:
				while True:
					new_hc = int(input('\nEnter new hair colour [%s]: '%(', '.join(['%s: %s'%(e,f.lower()) for e,f in enumerate(hair_cl)]))))
					if new_hc in list(range(len(hair_cl))):
						break
			new_hc = int(new_hc) << 2
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 6:
					temp_file += valori.read(1)
				if bit == 6:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 243)+new_hc
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 's':
			new_sc = args.get('value', None)
			if new_sc is None:
				while True:
					new_sc = int(input('\nEnter new skin colour [%s]: '%(', '.join(['%s: %s'%(e,f) for e,f in enumerate(skin_cl)]))))
					if new_sc in list(range(len(skin_cl))):
						break
			new_sc = int(new_sc)
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 6:
					temp_file += valori.read(1)
				if bit == 6:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 252)+new_sc
					temp_file += bytes([temp_bit])
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == '*' or (ord(what_to_edit[0]) >= 48 and ord(what_to_edit[0]) <= 57):
			if what_to_edit != '*' and int(what_to_edit) < 17:
				new_vals = vals_already[:17]
				new_vals[int(what_to_edit)] = input('\nInput new value for %s (hit return to cancel): '%skill_fields[int(what_to_edit)])
				if len(new_vals[int(what_to_edit)]) == 0: return mod_offset
				print()
			else:
				new_vals = args.get('value', False)
				if new_vals == False:
					print('\033[30A\033[50C%s'%'\n\033[50C'.join([
						"                       ----- Special commands -----",
						"",
						"+[n]: increase average by n points through AI boost (features not editable in game)",
						"-[n]: decrease average by n points through AI lowering (features not editable in game)",
						"",
						"Example: +4 => raise average of player by 4 points, boosting",
						"only the AI skill points",
						"",
						"                       --- Skill average biases ---",
						"",
						"[s] = speedy player",
						"[f] = number 10",
						"[b] = physical player",
						"[n] = small and skillful",
						"[o] = finaliser",
						"[t] = master shooter",
						"[d] = defensive",
						"[a] = attacking",
						"[u] = low AI (weaker to play against; features not editable in game)",
						"",
						"Usage: [average].[bias]",
						"Example: 87.s ==> speedy player, average 87",
						"",
						"Biases alter the distribution of skill points.",
						"Biases may be combined and will be applied in order. The",
						"last bias prevails (e.g. 87.sa ==> speedy player + attacking",
						"player (attacking > speedy, average 87)"					
					]),end='\n\n\n\n')
					def handle_ai(difference,direction):
						vals = vals_already[0:17]
						oav = math.floor(sum(vals)/len(vals))
						range = [math.floor(sum((ov:=[y for e,y in enumerate(vals) if e not in ai_fields])+4*[99])/17),math.ceil(sum(ov+4*[39])/17)]
						nv = eval("math.floor(sum(vals)/len(vals)) %s %s"%(direction,difference))
						if nv < range[1]: difference = oav - range[1]
						if nv > range[0]: difference = range[0] - oav
						points = math.floor((abs(int(difference)) * 17)/4)*4
						while True:
							random.shuffle(ai_fields)
							if vals[ai_fields[0]] in [39,99]: continue
							exec("vals[ai_fields[0]] %s= 4"%direction)
							points -= 4
							if points <= 0:
								break
						return vals
					while True:
						new_vals = input('\nEnter new value sequence (17 vals., no spaces) or desired average (hit return to cancel): ')
						if '.' in new_vals:
							new_vals = gimme_values(new_vals, role=vals_already[-4])
						elif boost:=re.match('\+(\d+)', new_vals): new_vals = handle_ai(boost.group(1), '+')
						elif boost:=re.match('-(\d+)', new_vals): new_vals = handle_ai(boost.group(1), '-')
						elif len(new_vals) < 34 and new_vals[:2].isnumeric():
							if int(new_vals[:2]) > 38:
								new_vals = gimme_values(new_vals[:2].strip(),role=vals_already[-4])
							else: continue
						elif len(new_vals) >= 34 and new_vals.isnumeric():
							new_vals = [new_vals[i:i+2] for i in range(0, 34, 2)]
							if True in [int(_)<39 for _ in new_vals]: continue
						elif len(new_vals) == 0:
							return mod_offset
						else: continue
						break
				else:
					new_vals = gimme_values(new_vals, role=vals_already[-4])
			try:
				vals = [math.floor((int(x)-39)/4) for x in new_vals.split()]
			except:
				vals = [math.floor((int(x)-39)/4) for x in new_vals]
			else:
				print('New average: ', math.floor(sum([int(vals) for vals in new_vals.split()])/len(vals)))
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset-1)
			ind_inp = 0
			temp_bit = 0
			for bit in range(20):
				if bit < 9:
					temp_file += valori.read(1)
				if (bit >= 9 and bit <= 16):
					temp_bit = vals[ind_inp] << 4
					ind_inp +=1
					temp_bit = temp_bit + vals[ind_inp]
					ind_inp +=1
					temp_file += bytes([temp_bit])
					valori.seek(1,1)
				if bit == 17:
					temp_bit = (int.from_bytes(valori.read(1), 'big') & 240) + vals[ind_inp]
					temp_file += bytes([temp_bit])
					ind_inp +=1
				if bit > 17:
					temp_file += valori.read(1)
				temp_bit = 0
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		else:
			what_to_edit = None
			valid = False
		if valid: break
	try:
		p = args['value']
	except:
		if input('Continue editing? [yn] ') == 'y': edit_player(modify)
	else:
		del p
	valori.close()
	return mod_offset
	
def show_teams(*index):
	p = {}
	for pos,pl in enumerate(players):
		p.setdefault(pl['id'],pos)
	a = index[0] if index else input('Team name (hit return to cancel): ')
	if len(str(a)) == 0:
		return
	results = 0
	for idx,t in enumerate(teams):
		field = t['index_fcdb'] if index else t['names'][-1]
		if not case_sensitive:
			field = str(field).upper()
			a = str(a).upper()
		if re.search(a, field):
			os.system(clear_screen)
			results += 1
			print('%s'%('#'*80))
			print('Name', t['names'][-1], sep="\t\t\t")
			print('%s'%('-'*80))
			if len(t['names']) == 3: print('Short Name', t['names'][1], sep="\t\t")
			print('Abbreviation', t['names'][0], sep="\t\t")
			print('%s'%('-'*80))
			print('Index FCDB', t['index_fcdb'], sep="\t\t")
			print('Index FCDBPENG', t['index_fcdbpeng'], sep="\t\t")
			print('Id', t['id'], sep="\t\t\t")
			print('%s'%('-'*80))
			print('League', league_list[t['league']], sep="\t\t\t")
			print('Bankroll', t['bank'], sep="\t\t")
			print('Stadium', t['stadium'], sep="\t\t\t")
			print('%s'%('-'*80))
			firstkit, secondkit = '', ''
			firstkit+="\033[10C".join(['1st shirt type', t['first shirt']])
			firstkit+="\n1st shirt colours\033[7C%s%s%s\033[0m "%(cesc[t['first shirt - colour 1']],cesc[t['first shirt - colour 2']],cesc[t['first shirt - colour 3']])
			if jerseys: firstkit+=display_jersey(jersey_types.index(t['first shirt']),t['first shirt - colour 1'],t['first shirt - colour 2'],t['first shirt - colour 3'])
			firstkit+='\n'+"\033[9C".join(['1st shorts type', t['first shorts']])
			firstkit+='\n1st shorts colours\033[6C%s%s\033[0m'%(cesc[t['first shorts - colour 1']],cesc[t['first shorts - colour 2']])
			firstkit+='\n'+"\033[10C".join(['1st socks type', t['first socks']])
			firstkit+='\n1st socks colours\033[7C%s%s\033[0m'%(cesc[t['first socks - colour 1']],cesc[t['first socks - colour 2']])
			secondkit+="\033[10C".join(['2nd shirt type', t['second shirt']])
			secondkit+='\n2nd shirt colours\033[7C%s%s%s\033[0m'%(cesc[t['second shirt - colour 1']],cesc[t['second shirt - colour 2']],cesc[t['second shirt - colour 3']])
			if jerseys: secondkit+=display_jersey(jersey_types.index(t['second shirt']),t['second shirt - colour 1'],t['second shirt - colour 2'],t['second shirt - colour 3'])
			secondkit+='\n'+"\033[9C".join(['2nd shorts type', t['second shorts']])
			secondkit+='\n2nd shorts colours\033[6C%s%s\033[0m'%(cesc[t['second shorts - colour 1']],cesc[t['second shorts - colour 2']])
			secondkit+='\n'+"\033[10C".join(['2nd socks type', t['second socks']])
			secondkit+='\n2nd socks colours\033[7C%s%s\033[0m'%(cesc[t['second socks - colour 1']],cesc[t['second socks - colour 2']])
			fk=firstkit.split('\n')
			sk=secondkit.split('\n')
			for _ in range(len(fk)):
				print('%s\r\033[50C%s'%(fk[_],sk[_]))
			print('%s'%('-'*80))
			print('Strategy', t['strategy'], sep="\t\t")
			print('Tactics', t['tactics'], sep="\t\t\t")
			rt = recommended_tactics(t['squad'])
			current = rt['starting']
			lineup = ''
			reparti = list(numpy.cumsum([int(r) for r in t['tactics'].split('-')]))
			for lpl, p in enumerate(current):
				lineup += p[0]
				lineup += '; ' if lpl == 0 or lpl in reparti[:-1] else ', '
			lineup = lineup[:-2]
			sq_lines = textwrap.wrap(lineup, 64)	
			print('Current Lineup', sq_lines[0], sep="\t\t")
			print('\t\t\t','\n\t\t\t'.join(sq_lines[1:]))
			print('%s'%('-'*80))
			fine = '' if t['roster size']==len(pl_list := rt['pl_list']) else ' (%s)'%len(pl_list)
			print('Roster Size', str(t['roster size'])+fine, sep="\t\t")
			print('Average\t\t\t%s'%str(int(sum(values := rt['values'])/len(values))))
			sq_lines = textwrap.wrap(', ' .join(pl_list), 64)
			print('Squad', sq_lines[0], sep="\t\t\t")
			print('\t\t\t','\n\t\t\t'.join(sq_lines[1:]))
			if len(dpls:=rt['duplicate roles']) or rt['rec'] > 0:
				print('%s'%('-'*80))
				if len(dpls) > 0:
					print('Duplicate Roles', ', '.join(dpls), sep="\t\t")
				if rt['rec'] :
					print('Recommended Tactics', rt['rec_tactics'], sep="\t")
					sq_lines = textwrap.wrap('; '.join([', '.join([y[0] for y in x]) for x in rt['lineup']]), 64)
					print('Recommended Lineup', sq_lines[0], sep="\t")
					print('\t\t\t','\n\t\t\t'.join(sq_lines[1:]))
					print('Roles to Improve for')
					print('  Current Tactics', rt['to improve'], sep="\t")
			print('%s'%('#'*80))
			if len(index) == 0:
				if (tsl:=input('\nEdit %s? [ync] '%t['names'][-1])) == 'y':
					if not show_teams(edit_team(t)): return
				elif tsl == 'c': return
	if results == 0: print('Not found')
	if input('\nSearch new team? [yn] ') == 'n': return False
	else: show_teams()

def recommended_tactics(squad):
	p = {}
	for pos,pl in enumerate(players):
		p.setdefault(pl['id'],pos)
	values = []
	pl_list = []
	for px in squad:
		pl_list.append((players[p[px]]['name'],players[p[px]]['role'],av:=players[p[px]]['average'],players[p[px]]['starting']))
		values.append(av)
	current = sorted(sorted(pl_list, key=lambda y: y[3], reverse=True)[:11], key=lambda w: dict(GK=0,CB=2,RB=1,LB=3,SW=2,CM=5,RM=4,LM=6,CF=8,RF=7,LF=9)[w[1]])
	pool=sorted(pl_list, key = lambda x: x[2], reverse = True)
	pl_list = ['%s (%s, %s)'%(y,z,q) for (y,z,q,k) in pool]
	starting = []
	for i,x in enumerate(pool):
		if x[1] == 'GK':
			starting.append(pool.pop(i))
			break
	for i,x in enumerate(pool):
		if x[1] != 'GK':
			starting.append(pool[i])
		if len(starting) == 11:
			break
	d,m,f = 0,0,0
	lineup = [[starting[0]],[],[],[]]
	for x in starting:
		if x[1] in roles[1:5]:
			d += 1
			lineup[1].append(x)
		if x[1] in roles[5:8]:
			m += 1
			lineup[2].append(x)
		if x[1] in roles[8:]:
			f += 1
			lineup[3].append(x)
	to_improve = ', '.join([x[1] for x in set(current).difference(set(starting))])
	nndplroles = dict(LB=0,RB=0,LM=0,RM=0)
	dpls = [y for y in list(nndplroles.keys()) if [p[1] for p in current].count(y) > 1]
	return {'rec_tactics': '%s-%s-%s'%(d,m,f), 'values': values, 'pl_list': pl_list, 'lineup': lineup, 'starting': current, 'rec':set(current) != set(starting), 'to improve':to_improve, 'duplicate roles': dpls}

def edit_team(modify, **args):
	global table
	vals_already = modify
	valori = open(f_valori, 'r+b')
	temp_file = b''
	mod_offset=int(modify['index_fcdb'])
	new_value = args.get('value', None)
	lineup ='\n\t| [l]ineup                |' if vals_already['league'] <= 10 else ''
	call_players = '\n\t| [c]all players          |\n\t| call [d]ual nationals   |' if vals_already['league'] > 10 else ''
	buy_players = "\n\t| [buy] player            |" if len(vals_already['squad']) < 20 else ''
	edit_players = '%s\n\t| [sell] player           |\n\t| e[x]change players      |\n\t| [rel]ease player        |'%buy_players if vals_already['league'] <= 10 else ''

	valori.seek(0, 0)
	temp_file = valori.read(mod_offset)
	temp_bytes = [valori.read(1) for x in range(23)]
	
	what_to_edit = args.get('field', None)
	valid = True
	while True:
		if what_to_edit is None: what_to_edit = input("""
Parameter to edit:
	+-------------------------+
	| [n]ames                 |
	| [b]ankroll              |
	| [s]tadium               |
	| [f]irst [s]hirt         |
	|     └ [c]olours         |
	| [f]irst s[h]orts        |
	|     └ [c]olours         |
	| [f]irst soc[k]s         |
	|     └ [c]olours         |
	| [s]econd [s]hirt        |
	|     └ [c]olours         |
	| [s]econd s[h]orts       |
	|     └ [c]olours         |
	| [s]econd soc[k]s        |
	|     └ [c]olours         |
	| strateg[y]              |
	| [t]actics               |%s
	| [p]layers               |%s%s	
	+-------------------------+
(hit return to cancel): """%(lineup,edit_players,call_players))
		if len(what_to_edit) == 0:
			return mod_offset
		if what_to_edit == 'l':
			roster = [(p['name'],p['role'],p['index_fcdb'],p['average']) for p in players if (p['team_id'] == vals_already['db_position']) or (vals_already.get('nation','') in p['international_id'])]
			reparti = vals_already['tactics']
			if reparti == '5-4-1': reparti = ['GK','RB','CB','SW','CB','LB','RM','CM','CM','LM','F']
			if reparti == '5-3-2': reparti = ['GK','RB','CB','SW','CB','LB','CM','CM','CM','F','F']
			if reparti == '4-5-1': reparti = ['GK','RB','CB','CB','LB','RM','CM','CM','CM','LM','F']
			if reparti == '1-3-4-2': reparti = ['GK','SW','RB','CB','LB','RM','CM','CM','LM','F','F']
			if reparti == '1-3-3-3': reparti = ['GK','SW','RB','CB','LB','CM','CM','CM','F','F','F']
			if reparti == '4-4-2': reparti = ['GK','RB','CB','CB','LB','RM','CM','CM','LM','F','F']
			if reparti == '4-3-3': reparti = ['GK','RB','CB','CB','LB','CM','CM','CM','F','F','F']
			if reparti == '5-3-2': reparti = ['GK','CB','CB','CB','RM','CM','CM','CM','LM','F','F']
			if reparti == '5-3-2': reparti = ['GK','CB','CB','CB','RM','CM','CM','LM','F','F','F']
			lineup = set()
			def b(r):
				try:
					lineup.add(roster.pop(roster.index((tp:=[x for x in roster if x[1].find(r) > -1])[int(input('   '+'\n   '.join(['[%s]: %s (%s)'%(t,d[0],d[3]) for (t,d) in enumerate(tp)]) + '\n: '))]))[2])
				except:
					print('No player input, or not enough %s for the selected tactics'%r)
					if input('Try again? [yn] ') == 'n': return None
					else: b(r)
				else: return True
			for r in reparti:
				print('\nSelect %s:'%r)
				if b(r) is None: break
			if len(lineup) == 11:
				for x in roster:
					edit_player(x[2], field='st', value=None)
				for x in lineup:
					edit_player(x[2], field='st', value=180)
				load_database()
		elif what_to_edit in ['buy', 'sell', 'x', 'rel']:
			source_pl, dest_tm, dest_lg = None, None, None
			def edit_squad(xl_squad, index):
				if index == None: return True
				new_value = int((len(xl_squad)+1)/2)-7
				xl_squad += (20-len(xl_squad))*['0000']
				xl_squad = ''.join(xl_squad)
				xl_squad = [int(xl_squad[i:i+2],16) for i in range(0, len(xl_squad), 2)]
				xl_squad = bytes(xl_squad)
				valori = open(f_valori, 'r+b')
				valori.seek(0,0)
				temp_file = valori.read(index)
				temp_bytes = [valori.read(1) for x in range(24)]
				temp_bytes[19] = bytes([(int.from_bytes(temp_bytes[19], 'big') & 63)]) if new_value > 1 else bytes([(int.from_bytes(temp_bytes[19], 'big') & 63) + 64])
				temp_bytes[22] = bytes([(int.from_bytes(temp_bytes[22], 'big') & 240) + new_value+7])
				temp_file += b''.join(temp_bytes)
				temp_file += xl_squad
				valori.seek(len(xl_squad),1)
				temp_file += valori.read()
				save(f_valori, temp_file)
				return True
			if what_to_edit == 'buy':
				source_team = None
				a = input('\nSearch source team / Hit return to browse: ')
				if len(a) > 0:
					hits = 0
					for idx,t in enumerate(teams):
						field = t['names'][-1]
						if not case_sensitive:
							field = str(field).upper()
							a = str(a).upper()
						if re.search(a, field) and t['league'] < 11:
							hits += 1
							confirm = input('Selected team: %s. Confirm? [ync] '%t['names'][-1])
							if confirm == 'c': return
							elif confirm == 'y':
								source_team = t
								break
					if hits == 0: print('Not found')
				else:
					l = int(inputPlus('\nSelect league of source team:\n  $OPTIONLIST_d$$CANCEL$', {**leagues,**{len(league_list):None}}, dct=league_list+['free agent'], c=True, sep='\n  ')[0])
					if l < len(leagues):
						tms = [(team['names'][-1], e) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league'] == l]
						t = int(inputPlus('\nSelect source team:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
						if t < len(tms):
							t = tms[t][1]
							source_team = sorted(teams, key=lambda x: x['names'][-1])[t]
					elif l == len(league_list):
						source_team = {'squad':[p['id'] for p in players if p['team'] == '---'], 'index_fcdb':None,'names':['free agents']}
				if source_team:
					source_squad = source_team['squad']
					source_roster = [p for p in players if p['id'] in source_squad]
					destination_starting = [p for p in players if p['id'] in vals_already['squad'] if p['starting'] == 180]
					player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',source_roster, field="['name']+' ('+o['role']+', '+str(o['average'])+', '+o['country']+')'", c=True, sep='\n  ')[0])
					if player_to_transfer < len(source_roster):
						vals_already['squad'].append(source_roster[player_to_transfer]['id'])
						if source_roster[player_to_transfer]['starting'] == 180 and len(destination_starting) > 10:
							edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=None)
						elif source_roster[player_to_transfer]['starting'] != 180 and len(destination_starting) < 11:
							edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=180)
						source_squad.remove(source_roster[player_to_transfer]['id'])
						if edit_squad(vals_already['squad'],vals_already['index_fcdb']) and edit_squad(source_squad,source_team['index_fcdb']): print('\n%s succesfully transferred from %s to %s'%(source_roster[player_to_transfer]['name'], source_team['names'][-1], vals_already['names'][-1]))				
			elif what_to_edit == 'sell':
				destination_team = None
				source_roster = [p for p in players if p['id'] in vals_already['squad']]
				player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',source_roster, field="['name']+' ('+o['role']+', '+str(o['average'])+', '+o['country']+')'", c=True, sep='\n  ')[0])
				if player_to_transfer < len(source_roster):
					a = input('\nSearch destination team / Hit return to browse: ')
					if len(a) > 0:
						hits = 0
						for idx,t in enumerate(teams):
							field = t['names'][-1]
							if not case_sensitive:
								field = str(field).upper()
								a = str(a).upper()
							if re.search(a, field) and t['league'] < 11:
								hits += 1
								confirm = input('Selected team: %s. Confirm? [ync] '%t['names'][-1])
								if confirm == 'c': return
								elif confirm == 'y':
									destination_team = t
									break
						if hits == 0: print('Not found')
					else:						
						l = int(inputPlus('\nSelect league of destination team:\n  $OPTIONLIST_d$$CANCEL$', leagues, dct=league_list, c=True, sep='\n  ')[0])
						if l < len(leagues):
							tms = [(team['names'][-1], e) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league'] == l]
							t = int(inputPlus('\nSelect source team:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
							if t < len(tms):
								t = tms[t][1]
								destination_team = sorted(teams, key=lambda x: x['names'][-1])[t]
					if destination_team:
						if len(destination_team['squad']) < 20:
							destination_squad = destination_team['squad']
							vals_already['squad'].remove(source_roster[player_to_transfer]['id'])
							destination_starting = [p for p in players if p['id'] in destination_squad if p['starting'] == 180]
							destination_squad.append(source_roster[player_to_transfer]['id'])
							if source_roster[player_to_transfer]['starting'] == 180 and len(destination_starting) > 10:
								edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=None)
							elif source_roster[player_to_transfer]['starting'] != 180 and len(destination_starting) < 11:
								edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=180)
							if edit_squad(vals_already['squad'],vals_already['index_fcdb']) and edit_squad(destination_squad,destination_team['index_fcdb']): print('\n%s succesfully transferred from %s to %s'%(source_roster[player_to_transfer]['name'], vals_already['names'][-1], destination_team['names'][-1]))				
						elif input('Team full. Exchange players? [yn] ') == 'y':
							what_to_edit = 'x'
							source_pl = player_to_transfer
							dest_tm = t0
							dest_lg = l
			elif what_to_edit == 'x':
				destination_team = None
				source_roster = [p for p in players if p['id'] in vals_already['squad']]
				player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',source_roster, field="['name']+' ('+o['role']+', '+str(o['average'])+', '+o['country']+')'", c=True, sep='\n  ')[0])
				if player_to_transfer < len(source_roster):
					a = input('\nSearch destination team / Hit return to browse: ')
					if len(a) > 0:
						hits = 0
						for idx,t in enumerate(teams):
							field = t['names'][-1]
							if not case_sensitive:
								field = str(field).upper()
								a = str(a).upper()
							if re.search(a, field) and t['league'] < 11:
								hits += 1
								confirm = input('Selected team: %s. Confirm? [ync] '%t['names'][-1])
								if confirm == 'c': return
								elif confirm == 'y':
									destination_team = t
									break
						if hits == 0: print('Not found')
					else:			
						l = int(inputPlus('\nSelect league of destination team:\n  $OPTIONLIST_d$$CANCEL$', leagues, dct=league_list, c=True, sep='\n  ')[0])
						if l < len(leagues):
							tms = [(team['names'][-1], e) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league'] == l]
							t = int(inputPlus('\nSelect source team:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
							if t < len(tms):
								t = tms[t][1]
								destination_team = sorted(teams, key=lambda x: x['names'][-1])[t]
					if destination_team:
						destination_squad = destination_team['squad']
						destination_roster = [p for p in players if p['id'] in destination_squad]
						source_starting = [p for p in source_roster if p['starting'] == 180]
						destination_starting = [p for p in destination_roster if p['starting'] == 180]
						player_to_transfer_2 = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',destination_roster, field="['name']+' ('+o['role']+', '+str(o['average'])+', '+o['country']+')'", c=True, sep='\n  ')[0])
						if player_to_transfer_2 < len(destination_roster):
							if source_roster[player_to_transfer]['starting'] == 180 and len(destination_starting) > 10:
								edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=None)
							elif source_roster[player_to_transfer]['starting'] != 180 and len(destination_starting) < 11:
								edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=180)
							if source_roster[player_to_transfer_2]['starting'] == 180 and len(source_starting) > 10:
								edit_player(source_roster[player_to_transfer_2]['index_fcdb'], field='st', value=None)
							elif source_roster[player_to_transfer_2]['starting'] != 180 and len(source_starting) < 11:
								edit_player(source_roster[player_to_transfer_2]['index_fcdb'], field='st', value=180)
							vals_already['squad'].remove(source_roster[player_to_transfer]['id'])
							vals_already['squad'].append(destination_roster[player_to_transfer_2]['id'])
							destination_squad.append(source_roster[player_to_transfer]['id'])
							destination_squad.remove(destination_roster[player_to_transfer_2]['id'])
							if edit_squad(vals_already['squad'],vals_already['index_fcdb']) and edit_squad(destination_squad,destination_team['index_fcdb']): print('\n%s and %s succesfully exchanged %s and %s'%(vals_already['names'][-1], destination_team['names'][-1], source_roster[player_to_transfer]['name'], destination_roster[player_to_transfer_2]['name']))				
			elif what_to_edit == 'rel':
				source_roster = [p for p in players if p['id'] in vals_already['squad']]
				player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',source_roster, field="['name']+' ('+o['role']+', '+str(o['average'])+', '+o['country']+')'", c=True, sep='\n  ')[0])
				if player_to_transfer < len(source_roster):
					vals_already['squad'].remove(source_roster[player_to_transfer]['id'])
					if edit_squad(vals_already['squad'],vals_already['index_fcdb']): print('\n%s has been released by %s and is now a free agent'%(source_roster[player_to_transfer]['name'], vals_already['names'][-1]))				
			load_database()
			modify = [t for t in teams if t['index_fcdb'] == vals_already['index_fcdb']][0]
		elif what_to_edit == 'n':
			new_names = new_value if new_value else [
					(lambda x: x if len(y:=input('\nChange abbreviation (enter to confirm: "%s")?  '%x)) == 0 else y)(vals_already['names'][0]),
					(lambda x: x if len(y:=input('Change matchday name (enter to confirm: "%s")?  '%x)) == 0 else y)((vals_already['names'][1] if len( vals_already['names']) == 3 else vals_already['names'][0])),
					(lambda x: x if len(y:=input('Change full name (enter to confirm: "%s")?  '%x)) == 0 else y)(vals_already['names'][-1]),
				]
			while True:
				if len(new_names[0]) > 5: new_names[0] = input('\nChange abbreviation (max. 5 characters): ')
				else: break
			while True:
				if len(new_names[1]) > 10: new_names[1] = input('Change matchday name (max. 10 characters): ')
				else: break
			while True:
				if len(new_names[2]) > 18: new_names[2] = input('Change full name (max. 18 characters): ')
				else: break
		
			#fixing size of team names
			new_names = [bytes(new_name, 'iso-8859-1') for new_name in new_names]
			new_names[0] += (5-len(new_names[0])) * b'\x00'
			new_names[1] += (10-len(new_names[1])) * b'\x00'

			squadre = open(f_squadre, 'r+b')
			squadre.seek(12,0)
			init_byte = struct.unpack("<h", squadre.read(2))[0]
			end_prelim_byte = init_byte + 8
		
			#copy initial bit
			squadre.seek(0,0)
			temp_file = squadre.read(end_prelim_byte)
		
			#team count
			squadre.seek(init_byte,0)
			team_count = struct.unpack("<h", squadre.read(2))[0]
			#array of team indexes in file
			squadre.seek(end_prelim_byte,0)
			team_indexes = []
			for t in range(team_count):
				team_indexes.append(struct.unpack("<l", squadre.read(4))[0])
			temp_file_2 = []
			temp_file_3 = b''
			for w, team_index in enumerate(team_indexes):
				string = b''
				squadre.seek(team_index + init_byte, 0)
				temp_file_2.append(len(temp_file_3))
				if w == vals_already['db_position']:
					temp_file_3 += b'\x00'.join(new_names)+ b'\x00'
					continue
				temp_file_3 += squadre.read(17)
				while True:
					current_idx = squadre.tell()
					try:
						next_one = team_indexes[w+1] + init_byte
					except:
						next_one = 20000
					if current_idx < next_one:
						new_char = squadre.read(1)
						if not new_char:
							break
						elif new_char != b'\x00':
							string += new_char
						else:
							if len(string) > 0:	
								temp_file_3 += string + b'\x00'
								string = b''
					else:
						break
			temp_file_2 = b''.join([struct.pack("<l", x + team_indexes[0]) for x in temp_file_2])
			save(f_squadre, temp_file + temp_file_2 + temp_file_3)
			squadre.close()
			load_database()
		elif what_to_edit == 'b':
			if new_value is None: new_value = input('\nEnter new bankroll (hit return to cancel): ')
			if len(new_value) > 0:
				if not new_value.isdigit(): 
					new_value = None
					continue
				else: new_value = int(new_value)
				new_value = 131071 if new_value > (131071*bank) else int(new_value/bank)
				bankroll_bit = [0,0,0]
				bankroll_bit[2] = new_value >> 13
				bankroll_bit[1] = (new_value & 8160) >> 5
				bankroll_bit[0] = (new_value & 31) << 3
				temp_bytes[1] = bytes([(int.from_bytes(temp_bytes[1], 'big') & 7)+bankroll_bit[0]])
				temp_bytes[2] = bytes([bankroll_bit[1]])
				temp_bytes[3] = bytes([(int.from_bytes(temp_bytes[3], 'big') & 240)+bankroll_bit[2]])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 's':
			if new_value is None: new_value = int(inputPlus('\nEnter stadium ($OPTIONLIST_l$$CANCEL$)', stadiums, c=True)[0])
			if new_value < len(stadiums):
				temp_bytes[3] = bytes([(int.from_bytes(temp_bytes[3], 'big') & 15)+ (new_value << 4)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit in ['fs','ss']:
			kit = [0,'first'] if what_to_edit[0] == 'f' else [8,'second']
			select_jersey(vals_already[kit[1]+' shirt - colour 1'],vals_already[kit[1]+' shirt - colour 2'],vals_already[kit[1]+' shirt - colour 3'])
			addtypes = '' if len(jersey_types) == 32 else '\n\t--- custom jerseys ---\n\t%s'%'\n\t'.join([
				'[%s] %s'%(e,f) for e,f in enumerate(jersey_types) if e > 32
			])
			if new_value is None: new_value = int(inputPlus('\nEnter shirt type %s$CANCEL$'%addtypes,jersey_types,c=True,sep="\n\t")[0])
			if new_value < len(jersey_types):
				temp_bytes[5+kit[0]] = bytes([(int.from_bytes(temp_bytes[5+kit[0]], 'big') & 3)+ (new_value << 2)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit in ['fsc','ssc']:
			kit = [0,'first'] if what_to_edit[0] == 'f' else [8,'second']
			if new_value is None:
				print('\n%s\033[49m'%' '.join(['%s\033[0m [%s] %s'%(cesc[e],e,f) for e,f in enumerate(colours)]))
				print()
				new_value = [
					int((lambda x: x if (y:=int(inputPlus('Change first colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' shirt - colour 1'])),
					int((lambda x: x if (y:=int(inputPlus('Change second colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' shirt - colour 2'])),
					int((lambda x: x if (y:=int(inputPlus('Change third colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' shirt - colour 3']))
				]
			temp_bytes[4+kit[0]] = bytes([((new_value[1] & 7) << 5) + new_value[0]])
			temp_bytes[5+kit[0]] = bytes([(int.from_bytes(temp_bytes[5+kit[0]], 'big') & 252) + ((new_value[1] & 24) >> 3)])
			temp_bytes[6+kit[0]] = bytes([(int.from_bytes(temp_bytes[6+kit[0]], 'big') & 224) + new_value[2]])
			temp_file+=b''.join(temp_bytes)
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit in ['fh', 'sh']:
			kit = [0,'first'] if what_to_edit[0] == 'f' else [8,'second']
			if new_value is None: new_value = int(inputPlus('\nEnter shorts type\n\t$OPTIONLIST_l$$CANCEL$',shorts,c=True,sep='\n\t')[0])
			if new_value < len(shorts):
				temp_bytes[7+kit[0]] = bytes([(int.from_bytes(temp_bytes[7+kit[0]], 'big') & 63)+ (new_value << 6)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit in ['fhc','shc']:
			kit = [0,'first'] if what_to_edit[0] == 'f' else [8,'second']
			if new_value is None:
				print('\n%s'%' '.join(['%s\033[0m [%s] %s'%(cesc[e],e,f) for e,f in enumerate(colours)]))
				new_value = [
					int((lambda x: x if (y:=int(inputPlus('Change first colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' shorts - colour 1'])),
					int((lambda x: x if (y:=int(inputPlus('Change second colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' shorts - colour 2']))
				]
			temp_bytes[6+kit[0]] = bytes([(int.from_bytes(temp_bytes[6+kit[0]], 'big') & 31) + ((new_value[0] & 7) << 5)])
			temp_bytes[7+kit[0]] = bytes([(int.from_bytes(temp_bytes[7+kit[0]], 'big') & 252) + ((new_value[0] & 24) >> 3)])
			temp_bytes[8+kit[0]] = bytes([(int.from_bytes(temp_bytes[8+kit[0]], 'big') & 224) + new_value[1]])
			temp_file+=b''.join(temp_bytes)
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit in ['fk','sk']:
			if new_value is None: new_value = int(inputPlus('\nEnter socks type\n\t$OPTIONLIST_l$$CANCEL$',socks,c=True,sep='\n\t')[0])
			if new_value < len(socks):
				if what_to_edit[0] == 'f':
					temp_bytes[11] = bytes([(int.from_bytes(temp_bytes[11], 'big') & 63) + (new_value << 6)])
				else:
					temp_bytes[19] = bytes([(int.from_bytes(temp_bytes[19], 'big') & 207) + (new_value << 4)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit in ['fkc','skc']:
			kit = [0,'first'] if what_to_edit[0] == 'f' else [8,'second']
			if new_value is None:
				print('\n%s'%' '.join(['%s\033[0m [%s] %s'%(cesc[e],e,f) for e,f in enumerate(colours)]))
				new_value = [
					int((lambda x: x if (y:=int(inputPlus('Change first colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' socks - colour 1'])),
					int((lambda x: x if (y:=int(inputPlus('Change second colour (enter to confirm: "%s")?'%colours[x], colours, entC=True)[0])) == len(colours) else y)(vals_already[kit[1]+' socks - colour 2']))
				]
			temp_bytes[8+kit[0]] = bytes([(int.from_bytes(temp_bytes[8+kit[0]], 'big') & 31) + ((new_value[0] & 7) << 5)])
			temp_bytes[9+kit[0]] = bytes([(int.from_bytes(temp_bytes[9+kit[0]], 'big') & 252) + ((new_value[0] & 24) >> 3)])
			temp_bytes[10+kit[0]] = bytes([(int.from_bytes(temp_bytes[10+kit[0]], 'big') & 224) + new_value[1]])
			temp_file+=b''.join(temp_bytes)
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'y':
			if new_value is None: new_value = int(inputPlus('\nEnter strategy\n\t$OPTIONLIST_l$$CANCEL$',strategia,c=True,sep='\n\t')[0])
			if new_value < len(strategia):
				temp_bytes[17] = bytes([(int.from_bytes(temp_bytes[17], 'big') & 31) + (new_value << 5)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 't':
			if new_value is None: new_value = int(inputPlus('\nEnter tactics\n\t$OPTIONLIST_l$$CANCEL$',tactics,c=True,sep='\n\t')[0])
			if new_value < len(tactics):
				temp_bytes[21] = bytes([(int.from_bytes(temp_bytes[21], 'big') & 3) + (new_value << 2)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'r':
			if new_value is None: int(inputPlus('\nEnter roster size\n\t$OPTIONLIST_l$$CANCEL$',[14,16,18,20],c=True,sep='\n\t')[0])
			if new_value < 4:
				temp_bytes[19]=bytes([(int.from_bytes(temp_bytes[19], 'big') & 63)]) if new_value > 1 else bytes([(int.from_bytes(temp_bytes[19], 'big') & 63) + 64])
				temp_bytes[22] = bytes([(int.from_bytes(temp_bytes[22], 'big') & 240) + new_value+7])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == '#':
			if len(str(new_value)) > 0:
				temp_bytes[0] = bytes([new_value & 255])
				temp_bytes[1] = bytes([(int.from_bytes(temp_bytes[1], 'big') & 248) + (new_value >> 8)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'p':
			table = True
			roster = search_players(vals_already['db_position'], 'team_id', strict=True) if vals_already['league'] <= 10  else search_players(vals_already['nation'], 'international_id', strict = True)
			pmodify = input('Edit player?\n\t%s\n\t[c]ancel: '%('\n\t'.join(['[%s]: %s (%s)'%(i,x,y) for i,(x, y) in enumerate(roster)])))
			if pmodify != 'c':
				if pmodify == '*': pmodify = ','.join([str(x) for x in range(len(roster))])
				for x in pmodify.split(','):
					if x.isnumeric():
						if int(x) < len(roster):
							print('\nEditing %s'%roster[int(x)][0])
							search_players(edit_player(roster[int(x)][1]),'index_fcdb',strict=True)
					else:
						print('The value "%s" is not in the list'%x)
		elif what_to_edit == 'c':
			if (convocazioni := convoca(vals_already)) is not None:
				temp_file+=b''.join(temp_bytes)+valori.read(1)+convocazioni
				valori.seek(40,1)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
				modify = [t for t in teams if t['index_fcdb'] == vals_already['index_fcdb']][0]
		elif what_to_edit == 'd':
			if (convocazioni := convoca(vals_already, True)) is not None:
				temp_file+=b''.join(temp_bytes)+valori.read(1)+convocazioni
				valori.seek(40,1)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		else:
			what_to_edit = None
			valid = False
		if valid: break
	try:
		p = args['value']
	except:
		if input('Continue editing %s? [yn] '%vals_already['names'][-1]) == 'y': edit_team(modify)
	else:
		del p
	valori.close()
	return mod_offset

def convoca(team_data, *lax):
	nation = team_data['nation']
	goalies = []
	defs = []
	midf = []
	strikers = []
	directory = {}
	m_roles = dict(GK=goalies,CB=defs,RB=defs,LB=defs,SW=defs,CM=midf,RM=midf,LM=midf,CF=strikers,RF=strikers,LF=strikers)
	counter = 0
	refs = {}
	strict = "(x['nation'] == nation and x['team'] != '---') or nation in x['international_id']"
	if lax: strict = "True"
	for x in players:
		if eval(strict):
			counter += 1
			capped = '*' if x['id'] in team_data['squad'] else ''
			m_roles[x['role']].append({'id':x['id'],'name':x['name'],'team':x['team'],'role':x['role'],'average':x['average'],'c':counter, 'capped':capped})
			directory[counter] = x['name']
			refs[counter] = (x['id'],x['name'],x['role'])
	longest = sorted([len(goalies),len(defs),len(midf),len(strikers)])[3]
	goalies = sorted(goalies, key = lambda x: x['average'], reverse=True)
	midf = sorted(midf, key = lambda x: x['average'], reverse=True)
	defs = sorted(defs, key = lambda x: x['average'], reverse=True)
	strikers = sorted(strikers, key = lambda x: x['average'], reverse=True)
	already = []
	for w in goalies+defs+midf+strikers:
		if w['capped'] == '*':
			already.append(w['c'])
	table = 4*('+'+49*'-')+'+\n| Goalies'+41*' '+'| Defenders'+39*' '+'| Midfielders'+37*' '+'| Strikers'+40*' '+'|\n'+4*('+'+49*'-')+'+\n'
	for x in range(longest):
		try:
			table += '{:50}'.format('| [%s] %s (%s, %s)%s'%(goalies[x]['c'],goalies[x]['name'],goalies[x]['team'],goalies[x]['average'],goalies[x]['capped']))
		except:
			table +=  '|'+49*' '
		try:
			table += '{:50}'.format('| [%s] %s (%s, %s, %s)%s'%(defs[x]['c'],defs[x]['name'],defs[x]['role'],defs[x]['team'],defs[x]['average'],defs[x]['capped']))
		except:
			table +=  '|'+49*' '
		try:
			table += '{:50}'.format('| [%s] %s (%s, %s, %s)%s'%(midf[x]['c'],midf[x]['name'],midf[x]['role'],midf[x]['team'],midf[x]['average'],midf[x]['capped']))
		except:
			table +=  '|'+49*' '
		try:
			table += '{:50}|\n'.format('| [%s] %s (%s, %s)%s'%(strikers[x]['c'],strikers[x]['name'],strikers[x]['team'],strikers[x]['average'],strikers[x]['capped']))
		except:
			table +=  '|'+49*' '+'|\n'
	table +=  4*('+'+49*'-')+'+'
	print('\n'+table)
	new_squad = [None]*20
	x = 0
	cancelled = False
	print('\nEnter player numbers ([c]ancel, [auto] selection)\n')
	while True:
		try:
			new_squad[x] = int(input('Call player %s (current: %s, enter to confirm): '%(str(x+1), directory[already[x]])))
		except ValueError as e:
			if str(e)[-2] == 'c': 
				cancelled = True
				break
			elif str(e)[-5:-1] == 'auto':
				new_squad = []
				for g in goalies[:2]:
					new_squad.append(g['c'])
					goalies.remove(g)
				for d in defs[:6]:
					new_squad.append(d['c'])
					defs.remove(d)
				for m in midf[:7]:
					new_squad.append(m['c'])
					midf.remove(m)
				for s in strikers[:5]:
					new_squad.append(s['c'])
					strikers.remove(s)
				turn = 0
				while True:
					if len(new_squad) == 20 or len(goalies+defs+midf+strikers) == 0: break
					if turn == 0:
						if len(defs) > 0: new_squad.append(defs.pop(0)['c'])
						turn = 1
						continue
					if turn == 1:
						if len(strikers) > 0: new_squad.append(strikers.pop(0)['c'])
						turn = 2
						continue
					if turn == 2:
						if len(goalies) > 0: new_squad.append(goalies.pop(0)['c'])
						turn = 3
						continue
					if turn == 3:
						if len(midf) > 0: new_squad.append(midf.pop(0)['c'])
						turn = 0
						continue
				break
			elif str(e)[-2:] == "''": new_squad[x] = already[x]
			else: continue
		if new_squad[x] > counter:
			print('Player not in list')
			continue
		if len(set(filter(lambda u: u is not None, new_squad))) != len(list(filter(lambda u: u is not None, new_squad))):
			print('Duplicate player')
			continue
		if input('\tSelected player: %s. Confirm? [yn] '%refs[int(new_squad[x])][1]) != 'n':
			x += 1
		if x == 20: break
	while True:
		if not None in new_squad: break
		new_squad.remove(None)
	if cancelled: 
		print('Cancelled by user')
		return
	print('\n'+str(len(new_squad)), 'players selected\n')
	for x in new_squad:
		print('\t',refs[int(x)][1], '(%s)'%refs[int(x)][2])
	if input('\nConfirm? [yn] ') == 'y':
		new_squad = ''.join([refs[int(x)][0] for x in new_squad])
		new_squad = [int(new_squad[i:i+2],16) for i in range(0, len(new_squad), 2)]
		return bytes(new_squad)
	
def show_leagues(**kwargs):
	lines_side = [0,0]
	line_counter = 0
	left_space = ''
	for e,_ in enumerate([league_list.index(x) for x in sorted(league_list[:11])]):
		print(left_space+'{:#^40}'.format(' %s '%league_list[_].upper())); line_counter += 1
		print(left_space+'|%s|'%(38*" ")); line_counter += 1
		tnlist = sorted([teams[t]['names'][-1] for t in leagues[_]])
		for t in tnlist:
			print(left_space+'|{: ^38}|'.format(t)); line_counter += 1
		print(left_space+'|%s|'%(38*" ")); line_counter += 1
		print(left_space+'#'*40,'\n'); line_counter += 1
		if e % 2 == 0 and e < 10:
			lines_side[0] = line_counter
			line_counter = 0
			print('\033[%sA'%(lines_side[0]+1), end = '')
			left_space = '\033[42C'
		else:
			lines_side[1] = line_counter
			line_counter = 0
			left_space=''
			if (diff:=lines_side[0] - lines_side[1]) > 0: print('\n'*diff,end='')

	if not kwargs.get('transfers',False):
		if input('Rename league? [yn] ') == 'y':
			l = int(inputPlus('\nSelect league:\n  $OPTIONLIST_d$$CANCEL$', leagues, dct=league_list, c=True, sep='\n  ')[0])
			if l < len(leagues): edit_leagues(l)
	if kwargs.get('transfers',False) or input('Transfer team? [yn] ') == 'y':
		l = int(inputPlus('\nSelect source league:\n  $OPTIONLIST_d$$CANCEL$', leagues, dct=league_list, c=True, sep='\n  ')[0])
		if l < len(leagues):
			tms = [(team['names'][-1], team['index_fcdb']) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league'] == l]
			t = int(inputPlus('\nSelect team:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
			if t < len(tms):
				t = tms[t][1]
				dl = int(inputPlus('\nSelect destination league:\n  $OPTIONLIST_d$$CANCEL$', leagues, dct=league_list, c=True, sep='\n  ')[0])
				if dl < len(leagues):
					tms = [(team['names'][-1], team['index_fcdb']) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league'] == dl]
					dt = int(inputPlus('\nSelect team to swop:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
					if dt < len(tms):
						dt = tms[dt][1]
						swop = []
						sw_name = []
						for team in teams:
							if team['index_fcdb'] == t or team['index_fcdb'] == dt:								
								swop.append(team['index_fcdb'])
								sw_name.append(team)
						edit_team(sw_name[0], field="#", value = sw_name[1]['id'])
						edit_team(sw_name[1], field="#", value = sw_name[0]['id'])
						swop = sorted(swop)
						valori = open(f_valori, 'r+b')
						temp_file = valori.read(swop[0])
						valori.seek(swop[1],0)
						temp_file += valori.read(64)
						valori.seek(swop[0]+64,0)
						temp_file += valori.read(swop[1]-(swop[0]+64))
						valori.seek(swop[0],0)
						temp_file += valori.read(64)
						valori.seek(swop[1]+64,0)
						temp_file += valori.read()
						save(f_valori, temp_file)
						load_database()
						for _,n in enumerate(sw_name):	
							if len(nn:=n['names']) == 2: sw_name[_]['names'] = [nn[0][:5],nn[1][:10],nn[1]]
							elif len(nn) == 1: sw_name[_]['names'] = [nn[0][:5],nn[0][:10],nn[0]]
						edit_team(sw_name[0], field="n", value = sw_name[1]['names'])
						edit_team(sw_name[1], field="n", value = sw_name[0]['names'])
						print('\r\033[K\n%s transferred to %s, %s transferred to %s'%(sw_name[0]['names'][-1],league_list[dl],sw_name[1]['names'][-1],league_list[l]))
						if input('\nKeep working on leagues? [yn] ') == 'y': show_leagues(transfers=True)

def edit_leagues(target):
	tmpfl = b''
	new_char = b''
	lglist = b''
	squadre = open(f_squadre, 'r+b')
	interface = open(f_interfaccia, 'r+b')
	interface_content = interface.read()
	interface.close()
	groups = []
	n = []
	squadre.seek(8,0)
	init_size_list = struct.unpack("<h", squadre.read(2))[0]+8
	squadre.seek(12,0)
	init_size_list_teams = struct.unpack("<h", squadre.read(2))[0]+8
	squadre.seek(20,0)
	how_many = struct.unpack("<h", squadre.read(2))[0]
	squadre.seek(init_size_list,0)
	init_byte = struct.unpack("<h", squadre.read(2))[0]+20
	squadre.seek(init_byte,0)
	zerocount = 0
	league_list = []
	string = b''
	skip = False
	lgidx = 0
	while True:
		new_char = squadre.read(1)
		lglist += new_char
		if new_char == b'\x00':
			zerocount +=1
			if skip == False and lgidx == target:
				new_string = bytes(input('Change "%s" ?: '%string.decode('unicode-escape')), 'iso-8859-1')
				if len(new_string) > 0:
					if new_string == b'*':
						skip = True
					else:
						groups.append(string)
						n.append(new_string)
						upd_int = interface_content.replace(b'\x00%s\x00'%string,b'\x00%s\x00'%new_string)
						g = open('temp.bin', 'wb+').write(upd_int)
						os.remove(f_interfaccia)
						shutil.copyfile('temp.bin', f_interfaccia)
						os.remove('temp.bin')
						string = new_string
						del new_string
			league_list.append(string)
			string = b''
			lgidx += 1
		else:
			string += new_char
		if zerocount == how_many:
			break
	for e,g in enumerate(groups):
		lglist = lglist.replace(b'\x00%s\x00'%g,b'\x00%s\x00'%n[e])
	index_end_of_list = squadre.tell()
	how_many_teams = struct.unpack("<h", squadre.read(2))[0]
	squadre.seek(init_size_list_teams,0)
	cl_team_sizes = []
	for x in range(how_many_teams):
		cl_team_sizes.append(struct.unpack("<l", squadre.read(4))[0])
	#create league_list_sizes
	league_list_sizes = []
	for e,league in enumerate(league_list):
		if e == 0:
			start_index = init_byte-20
		else:
			start_index = len(league_list[e-1])+league_list_sizes[e-1]+1
		league_list_sizes.append(start_index)
	last_index_leagues = league_list_sizes[-1] + len(league_list[-1])+20
	new_init_size_list_teams = last_index_leagues + 1
	offset = new_init_size_list_teams + 8 - init_size_list_teams
	new_cl_team_sizes = []
	squadre.seek(0,0)
	tmpfl += squadre.read(12)
	tmpfl += struct.pack("<l", new_init_size_list_teams)
	squadre.seek(16,0)
	tmpfl += squadre.read(12)
	for i in league_list_sizes:
		tmpfl += struct.pack("<l", i)
	squadre.seek(4*len(league_list_sizes),1)
	tmpfl += lglist
	squadre.seek(index_end_of_list,0)
	tmpfl += squadre.read()
	output = open(f_squadre,'w+b')
	output.write(tmpfl)
	output.close()
	load_database()
	

def commit():
	print('Committing...')
	home = os.path.expanduser('~')
	shutil.copyfile(f_valori, f_valori.replace(Fifapath, gamepath))
	shutil.copyfile(f_nomi, f_nomi.replace(Fifapath, gamepath))
	shutil.copyfile(f_squadre, f_squadre.replace(Fifapath, gamepath))
	shutil.copyfile(f_interfaccia, f_interfaccia.replace(Fifapath, gamepath))
	input('Changes saved. Return to main menu. ')

def restore():
	print('Restoring...')
	home = os.path.expanduser('~')
	shutil.copyfile(f_valori.replace(Fifapath, gamepath), f_valori)
	shutil.copyfile(f_nomi.replace(Fifapath, gamepath), f_nomi)
	shutil.copyfile(f_squadre.replace(Fifapath, gamepath), f_squadre)
	shutil.copyfile(f_interfaccia.replace(Fifapath, gamepath), f_interfaccia)
	load_database()
	input('Database restored. Return to main menu. ')
	
def match_day():
	def nt_lineup(squad, tactics, player):
		reparti = tactics.split('-')
		if len(reparti) == 4: reparti = [int(reparti[0])+int(reparti[1]), reparti[2], reparti[3]]
		reparti = [int(_) for _ in reparti]
		lineup = [[],[],[],[]]
		rls = dict(GK=0,CB=1,RB=1,LB=1,SW=1,CM=2,RM=2,LM=2,CF=3,RF=3,LF=3)
		for _ in players:
			if _['id'] in squad:
				lineup[rls[_['role']]].append((_['id'],_['average']))
		final_lineup = [sorted(lineup[0], key = lambda r: r[1])[-1]]
		for l,_ in enumerate(lineup[1:]):
			final_lineup += sorted(_, reverse=True, key = lambda r: r[1])[:reparti[l]]
		final_lineup = [_[0] for _ in final_lineup]
		return 2 if player in final_lineup else 1
		
	import pandas as pd
	l1 = int(inputPlus('Select league of team 1:\n  $OPTIONLIST_l$$CANCEL$', league_list[:12], c=True, sep='\n  ')[0])
	if l1 < 12:
		tms = [(team['names'][-1],team['db_position'],team.get('nation',None),team['squad'],team['tactics']) for team in sorted(teams, key=lambda x: x['names'][-1]) if team['league'] == l1]
	else: return
	t = int(inputPlus('\nSelect team 1:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
	if t < len(tms):
		t1 = tms[t][0]
		t1id = tms[t][1]
		t1nat = tms[t][2]
		t1sq = tms[t][3]
		t1ta = tms[t][4]
	else: return
	l2 = int(inputPlus('\nSelect league of team 2:\n  $OPTIONLIST_l$$CANCEL$', league_list[:12], c=True, sep='\n  ')[0])
	if l2 < 12:
		tms = [(team['names'][-1],team['db_position'],team.get('nation',None),team['squad'],team['tactics']) for team in sorted(teams, key=lambda x: x['names'][-1]) if team['league'] == l2]
	else: return
	t = int(inputPlus('\nSelect team 2:\n  $OPTIONLIST_l$$CANCEL$', tms, idx='0', c=True, sep='\n  ')[0])
	if t < len(tms):
		t2 = tms[t][0]
		t2id = tms[t][1]
		t2nat = tms[t][2]
		t2sq = tms[t][3]
		t2ta = tms[t][4]
	else: return
	teams0 = {'N':[],'Name':[],'P':[],'Nat':[],'AV':[],'St':[],'Role':[]}
	teams1 = {'N':[],'Name':[],'P':[],'Nat':[],'AV':[],'St':[],'Role':[]}
	in1 = "x['country']"
	in2 = "x['country']"
	what1 = "x['team_id'] == t1id"
	what2 = "x['team_id'] == t2id"
	
	if t1id not in league_teams:
		what1 = "t1nat in x['international_id']"
		in1='x["team"]'
	if t2id not in league_teams:
		what2 = "t2nat in x['international_id']"
		in2='x["team"]'
	
	for x in players:
		if eval(what1):
			teams0['N'].append(x['jersey'])
			teams0['Name'].append(x['name'])
			teams0['P'].append(x['role'])
			teams0['Nat'].append(eval(in1))
			teams0['AV'].append(x['average'])
			teams0['Role'].append(dict(GK=0,CB=2,RB=1,LB=3,SW=2,CM=5,RM=4,LM=6,CF=8,RF=7,LF=9)[x['role']])
			if l1 < 11: teams0['St'].append(x['starting'])
			else: teams0['St'].append(nt_lineup(t1sq, t1ta, x['id']))
		if eval(what2):
			teams1['N'].append(x['jersey'])
			teams1['Name'].append(x['name'])
			teams1['P'].append(x['role'])
			teams1['Nat'].append(eval(in2))
			teams1['AV'].append(x['average'])
			teams1['Role'].append(dict(GK=0,CB=2,RB=1,LB=3,SW=2,CM=5,RM=4,LM=6,CF=8,RF=7,LF=9)[x['role']])
			if l2 < 11: teams1['St'].append(x['starting'])
			else: teams1['St'].append(nt_lineup(t2sq, t2ta, x['id']))
	table = pd.DataFrame(data = teams0)
	table = table.sort_values(by=['St','Role'])
	table = table[['N', 'Name','P','Nat','AV']]
	table1 = pd.DataFrame(data = teams1)
	table1 = table1.sort_values(by=['St','Role'])
	table1 = table1[['N', 'Name','P','Nat','AV']]
	rows = []
	table = list(table.iterrows())
	table = table[-11:]+table[:-11]
	table1 = list(table1.iterrows())
	table1 = table1[-11:]+table1[:-11]
	for e,i in enumerate(table):
		row = []
		if e == 11:
			row.append('-'*53+'|'+'-'*53)
			rows.append(row)
			row = []
		row.append('{:>3}'.format(i[1][0]))
		row.append(align(i[1][1],'Name'))
		row.append(align(i[1][2],'Role'))
		row.append(align(i[1][3],'Nation'))
		row.append('{:<4}'.format(i[1][4]))
		row.append('|')
		try:
			row.append('{:>2}'.format(table1[e][1][0]))
			row.append(align(table1[e][1][1],'Name'))
			row.append(align(table1[e][1][2],'Role'))
			row.append(align(table1[e][1][3],'Nation'))
			row.append('{:<5}'.format(table1[e][1][4]))
		except:
			row.append('   ')
			row.append(align('','Name'))
			row.append(align('','Role'))
			row.append(align('','Nation'))
			row.append('    ')
		rows.append(row)
	for e,i in enumerate(table1):
		if e < len(rows)-1:
			continue 
		else:
			row = []
			row.append('   ')
			row.append(align('','Name'))
			row.append(align('','Role'))
			row.append(align('','Nation'))
			row.append('    ')
			row.append('|')
			row.append('{:>2}'.format(i[1][0]))
			row.append(align(i[1][1],'Name'))
			row.append(align(i[1][2],'Role'))
			row.append(align(i[1][3],'Nation'))
			row.append('{:<5}'.format(i[1][4]))
		rows.append(row)
	os.system(clear_screen)
	print('+{0}+{0}+'.format('—'*(3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5)))
	print('|{0}{1}{2}|{3}{4}{5}|'.format(
			math.floor((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t1))/2)*' ',
			t1.upper(),
			math.ceil((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t1))/2)*' ',
			math.floor((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t2))/2)*' ',
			t2.upper(),
			math.ceil((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t2))/2)*' ',
		)
	)
	print('+{0}+{0}+'.format('—'*(3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5)))
	for r in rows:
		print('|%s|'%' '.join(r))
	print('+{0}+{0}+'.format('—'*(3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5)))
	input('\nReturn to main menu ')

def general_list():
	tpos = {}
	for tm in teams:
		tpos.setdefault(tm['db_position'],tm)
	tpos[-1] = {'names':['---']}
	by_role = {}
	for p in sorted(players, key=lambda x: x['average'], reverse = True):
		by_role.setdefault((m_roles:=dict(GK='Goalkeepers',CB='Defenders',RB='Defenders',LB='Defenders',SW='Defenders',CM='Midfielders',RM='Midfielders',LM='Midfielders',CF='Forwards',RF='Forwards',LF='Forwards'))[p['role']], []).append('{0:<17}{1:<13}{2:<16}{3:>3}'.format(p['name'],tn[1] if len(tn:=tpos[p['team_id']]['names']) > 1 else tn[0] ,p['country'][:15]+('*' if len(p['international']) > 0 else ''),p['average']))
	lines = {}
	for role in set(m_roles.values()):
		lines.setdefault(role,[]).append("—"*49)
		lines[role].append("{:^49}".format(role))
		lines[role].append("—"*49)
		lines[role]+=by_role[role]
		lines[role].append("—"*49)
	x = sorted([len(_) for _ in lines.values()])[-1]
	for _ in range(x):
		line = [g[_] if _ < len(g:=lines['Goalkeepers']) else ' '*49,d[_] if _ < len(d:=lines['Defenders']) else ' '*49,m[_] if _ < len(m:=lines['Midfielders']) else ' '*49,f[_] if _ < len(f:=lines['Forwards']) else ' '*49]
		print('|'.join(line).replace('{0}|{0}'.format(' '*49),' '*99).replace('—|—','—+—').replace('|—','+—').replace('—|','—+'))
	input('Return to main menu ')
	
def initialize():
	def start_search():
		global sf
		a = input('Player name (hit return to cancel): ')
		if len(a) == 0: return 'n'
		if a[0] == '@':
			command = a.split('@')[1]
			a = a.split('@')[2]
		else:
			command = 'name'
		results = search_players(a, command)
		if len(results) > 0:
			while True:
				modify = input('Edit player?\n\n  %s\n  ----------\n  [*] all \n  [c]ancel: '%('\n  '.join(['[%s]: %s (%s)'%(i,x,y) for i,(x, y) in enumerate(results)])))
				if modify != 'c':
					if modify == '*': modify = ','.join([str(x) for x in range(len(results))])
					for x in modify.split(','):
						if x.isnumeric():
							if int(x) < len(results):
								print('\nEditing %s'%results[int(x)][0])
								search_players(edit_player(results[int(x)][1]),'index_fcdb',strict=True)
							else: print('The value "%s" is not in the list'%x)
						else: print('The value "%s" is not in the list'%x)
					break
				else: break
		return input("\nNew search? [yn] ")
	while True:
		if start_search() == 'n':
			break

def inputPlus(message, valid_options, **params):
	dct = valid_options
	n_vals = len(valid_options)
	idx = ''
	field = ''
	separator = ', '
	delimiter = None
	valid_params = None
	c = False
	entC = False
	if params:
		separator = params.get('sep',separator)
		delimiter = params.get('dlt',None)
		valid_params = params.get('par',None)
		dct = params.get('dct', dct)
		if (i:= params.get('idx', None)): idx = '[%s]'%i
		if (i:= params.get('field', None)): field = '%s'%i
		c = params.get('c', False)
		entC = params.get('entC', False)
	c_separator = '{0}-----------{0}'.format(separator) if '\n' in separator else separator
	if '$OPTIONLIST_d$' in message: message = message.replace('$OPTIONLIST_d$', separator.join(['[%s] %s'%(e,dct[e]) for e in valid_options.keys()]))
	elif '$OPTIONLIST_l$' in message: message = message.replace('$OPTIONLIST_l$', eval("separator.join(['[%s] %s'%(e,o"+idx+field+") for (e,o) in enumerate(valid_options)])"))
	valid_options = [str(_) for _ in list(valid_options.keys())] if type(valid_options) == dict else [str(_) for _ in range(n_vals)]
	if c: message = message.replace('$CANCEL$', '%s[%s] cancel'%(c_separator,n_vals)); valid_options += [str(n_vals)]
	if entC == True: valid_options += ['']
	while True:
		option = input('%s: '%message)
		param = None
		if delimiter and delimiter in option:
			option = (args:=option.split(delimiter))[0]
			if len(param := args[1]) == 0: continue
		if option in valid_options: 
			if not param is None:
				if param in valid_params: break
				else: continue
			if option == '': option = len(valid_options)-1
			break
	return [option,param]

def ch_game_path(**kwargs):
	os.system(clear_screen)
	if not kwargs.get('wait',False): print('Current path:', gamepath[:-7])
	while True:
		nf = input('Enter path to the main folder of FIFA RTWC 98 (hit return to cancel): ')
		if len(nf) == 0: return False
		if os.path.isdir(pth:=nf+'/common'):
			custom_vals['gamepath'] = [pth]
			json.dump(custom_vals, open('fifa_config.json', 'w'), indent=2)
			break
		else: print('Not a valid FIFA RTWC 98 folder')
	print('New game folder: %s.'%nf)
	if not kwargs.get('wait',False): restore()
	else: return pth

def ch_lang(**kwargs):
	os.system(clear_screen)
	lval = ['DUT','ENG','FRE','GER','ITA','SPA','SWE']
	llist = ['Dutch','English','French','German','Italian','Spanish','Swedish']
	if not kwargs.get('wait',False): print('Current language:', (llist)[(lval).index(lang)])
	while True:
		nf = int(inputPlus('Select game language\n $OPTIONLIST_d$$CANCEL$', lval:={x:y for x,y in enumerate(lval)}, dct=llist, c=True, sep="\n ")[0])
		if nf == len(llist): return False
		else:
			custom_vals['lang'] = [lval[nf]]
			json.dump(custom_vals, open('fifa_config.json', 'w'), indent=2)
			break
	print('New game language: %s'%llist[nf])
	if not kwargs.get('wait',False): restore()
	else: return lval[nf]

def main_menu():
	os.system(clear_screen)
	global case_sensitive
	commands = [
		('Show/edit leagues','os.system(clear_screen);show_leagues()'),
		('Search/edit team(s)','os.system(clear_screen);global debug, jerseys; jerseys = False; debug = False; show_teams()'),
		('Search/edit team(s), display jerseys','os.system(clear_screen);global jerseys, debug; jerseys = True; debug = False; show_teams()'),
		('Search/edit player(s), list view','os.system(clear_screen);global table, debug; table = False; debug = False; initialize()'),
		('Search/edit player(s), table view','os.system(clear_screen);global table, debug; table = True; debug = False; initialize()'),
		('Matchday','os.system(clear_screen); match_day()'),
		('List all players','os.system(clear_screen);general_list()'),
		('Debug mode','os.system(clear_screen);global debug; print("#### Debug mode ####\\n"); debug = True; load_database(); initialize()'),
		('Select game folder','ch_game_path()'),
		('Select language','ch_lang()'),
		('Save to game','commit()'),
		('Restore previous database version','restore()'),
		('Exit','sys.exit()')
	]
	while True:
		os.system(clear_screen)
		print('+{:—^44}+'.format(' MAIN MENU '))
		print('|%s|'%(' '*44))
		print('\n'.join(['| {:<42} |'.format('[%s] %s'%(index,command[0])) for (index,command) in enumerate(commands)]))
		print('|%s|'%(' '*44))
		print('+%s+'%('—'*44))
		print('Add [.c] for case-sensitive searches (0.c, etc.)')
		print('Add [.h] for help on an option (0.h, etc.)\n')
		option, param = inputPlus('Select option', commands, dlt='.',par=['c','h'])
		if param == 'c': case_sensitive = True
		if param == 'h': help(option)
		else: exec(commands[int(option)][1])
		print()

def help(item):
	os.system(clear_screen)
	print("""
               FIFA RTWC 98 Python Editor, by megas_alexandros@hotmail.com.
               (c) 2020. This software is distributed under the MIT License.

The editor needs at least a 201-column terminal window to display correctly. Please resize 
window/font accordingly (this will be done automatically in Mac OS).

The editor works on a copy of the game database files and creates a backup copy whenever 
saves are copied into the game files.

In the interface, all commands are indicated in square brackets. Enter values without the 
brackets. [ync] means: 'enter y for yes, enter n for no, enter c to cancel'.

""")
	entries = [
"""                 
                            ------ SHOW/EDIT LEAGUES ------

Displays lists of teams in each national league in a 2-column layout.
 (1) Rename league: select league name to edit. The edit affects the stadium name, too,
     which is what is shown in the league selection screen whens starting a league compe-
     tition.
     Cancelling returns to main menu.
 (2) Transfer team: swop teams between leagues

""",
"""
                            ------ SEARCH/EDIT TEAMS ------

Search for a team by its name. If more than one team is found, each team is displayed se-
quentially, and users are asked whether they wish to edit the currently displayed team.
[N]o moves on to the next team, while [c]ancel returns to the main menu.

*NB: THE CORRECT LINEUP IS ONLY SHOWN FOR TEAMS FOR WHICH IT HAS BEEN EDITED THROUGH THE
EDITOR, AND NEVER FOR NATIONAL TEAMS*.

Notes:

(1) In the squad list, players are ordered by average (which is displayed together 
with their role).
(2) If the number of players in the team is smaller than the size of the 
roster for that team in the database, the current number of players is displayed in bra-
ckets next to the value for 'Roster Size'. If this happens, the last player in the team 
list will be repeated in the Player Transfer lists in the game. The problem can be fixed 
by buying or selling players to match a legal roster size (12, 14, 16, 18, or 20 players).
(3) Recommended Tactics shows the tactics that would employ the best 11 players in the
team (sometimes these tactics are impossible, if the roster is unbalanced). Roles to Im-
prove for Current Tactics indicates which roles should be strengthened in order to have a 
balanced roster to play with the currently active tactics.

Notes on editing commands:

- [fs] --> first kit shirt, [fsc] --> first kit shirt colours, [fh] --> first kit shorts,
  [fhc] --> first kit shorts colour, etc.
- Jersey type names can be customized by populating the jersey_types array in
  fifa_config.json
- Custom jerseys (JERSxx.fsh with xx > 32 in the game folder ingame/PLAYER/TEXTURES/PLYRKITS)
  can be added by listing them in the custom_jerseys property in fifa_config.json (in the 
  nested array).
- [l]ineup (for clubs only): select the starting eleven, role by role, for the current tac-
  tics, as required by the game algorithm. The lineup will be applied if team management
  is reset in the game. Selectable players are listed for each role, together with their
  skill average. Lineups of national teams may not be edited (due to potential conflicts
  with the status of players in clubs) and should be adjusted in the game.
- [rel]ease player (clubs only): remove players from team roster and add to free agents.
- [c]all players (national teams only): select players from the players of the correct na-
  tionality. Players are selected from lists where they are divided by position and are
  sorted by skill average. The automatic selection option picks the best 2 goalkeepers, 6 
  defenders, 7 midfielders and 5 strikers.
- call [d]ual nationals: allows users to select any player for the active national team,
  regardless of their nationality. It is recommended to split the terminal window to scroll
  up and down the list while inputting values.

""",
"""
                     ------ SEARCH/EDIT TEAMS, DISPLAY JERSEYS ------

Same as search/edit teams, but a text-mode rendition of jerseys is displayed.

""",
"""
                       ------ SEARCH/EDIT PLAYERS, LIST VIEW ------

Search players by name. To search for multiple names, separate them with a slash (e.g.
Name1/Name2). It is also possible to search other fields than the name. Field names must
be enclosed in a pair of @ signs and the searched value must follow immediately (e.g.
@field@value).

The following fields can be searched: country, jersey, role, team, international, speed,
acceleration, agility, aggression, attack bias, ball, awareness, fitness, creativity,
passing, passing bias, heading, reaction, tackle, shot bias, shot power, shot accuracy,
average.
International selects players in the squad of the desired national team (e.g.
@international@Spain).

Values are displayed in a list. Users can select players for editing. When prompted, users
can select a player at a time, or select multiple players separating their list indexes
with commas. When multiple players are selected, the editing menu is presented sequentially
for each player at a time.

The descriptors for skin colour, face type, facial hair, and hair styles can be customized
by populating properties in fifa_config.json (skin_cl, faces, beards, hairs).

When the option [*] all is selected for editing, users may input either the desired average
skill for the player or a sequence of 17 values (from 39 to 99), one for each of the skills
in the same order as they appear in the menu.

For example, the sequence 8791797571758375877967876767868667 means:

  aggression:              87
  acceleration:            91
  attack bias:             79
  agility:                 75
  ball:                    71
  awareness:               75
  fitness:                 83
  creativity:              75
  passing:                 87
  heading:                 79
  reaction:                67
  pass bias:               87
  shot power:              67
  shot bias:               87
  speed:                   87
  shot accuracy:           67
  tackle:                  87

If only the average is input (e.g. 75), the user will be asked how wide the range of skill
values should be. A large standard deviation means that the player may have very high skill
at the same time as very low ones, while a limited one makes for players that don't have
features in which they are very good and others in which they are very bad.
The distribution of skill values averaging to the desired value is based on the player's
role. For a striker, higher points will be assigned primarily to attacking and goalscoring
skills and lower points will be assigned to defensive and playmaking skills. For a centre
back, heading, focusing and tackling skills will be prioritized.
The distribution can be biased manually by attaching special flags to the desired average
(details and instructions are provided contextually).

""","""
                 ------ SEARCH/EDIT PLAYERS, TABLE VIEW ------

Same as search/edit players, list view, but player values are displayed as a table, with a
row for each player. This option is recommended if comparing players or editing more than 
one player at a time and is default when players are edited in team editing mode.

Fields:

 H	hair type (hex digit)
 HC	hair colour (colour)
 SC	skin colour (colour)
 F	face type (digit)
 B	facial hair
 $$$	price
 Jers	jersey number
 Aggr	aggression
 Accl	acceleration
 AttB	attack bias
 Agil	agility
 Ball	ball control
 Awar	awareness
 Fitn	fitness
 Crea	creativity
 Reac	reaction
 PBia	passing bias
 SPow	shot power
 SBia	shot bias
 Spee	speed
 SAcc	shot accuracy
 Tack	tackle
 AV		average
 InFPE	index in name database
 InFCDB	index in skill database
 Team	club team (if any)

In the final row, a count of nations represented in the table is provided in the Nation
column. Other columns show the average for the respective field. If the Jersey column has
value '!!' in the last row, this means that some jersey numbers are repeated in the table.
This is only relevant when one and only one whole team is listed and is a way to check for
duplicated jersey numbers (the game will change one to an available jersey number if this
is not fixed).

Particulars: (1) In 'Nation' column, an asterisk following the country name indicates
that the player is capped for the national team. If a player is a dual national, the 
national team for which he was capped is added between brackets.

""","""
                                  ------ MATCHDAY ------

Select two teams and display their lineup and substitutes. For national teams, the lineup
is automatically selected by the game (see help on team editing) and this option does not
display the correct one. *NB: THE CORRECT LINEUP IS ONLY SHOWN FOR TEAMS FOR WHICH IT HAS
BEEN EDITED THROUGH THE EDITOR*.

If clubs are selected, players are listed according to their position. The displayed data
includes their number, role, average, and nationality. If national teams are selected, the
lineup order is simply a selection of the strongest players in each role; instead of the
players' nationality, their club team (if any) is displayed.

""","""
                              ------ LIST ALL PLAYERS ------

Prints a table listing all players divided by position (Goalkeepers, Defenders, Midfield-
ers, Forwards) and sorted by the average of their skill points. The table also shows their
club team (if any) and nationality. If players are capped for a national team, an asterisk
is displayed next to their nation.

""","""
                                 ------ DEBUG MODE ------

Automatic checks for:
- Unacceptable roster sizes (see help on team editing).
- Duplicate jersey numbers in club teams. Users are prompted if they wish to change one of
  the player's number to an automatically selected available one.
- Duplicate player names in the database.

Users may also select a player and display the binary code of the corresponding database
record in a tabular view (as in search/edit players, table view). All bits for each byte
are displayed.

""","""
                             ------ SELECT GAME FOLDER ------

Select location of FIFA RTWC 98. Enter absolute path.                             
                             
""","""
                              ------ SELECT LANGUAGE ------

Select the language used in the game in order to edit the corresponding name databases.

""","""
                                ------ SAVE TO GAME ------

Save the changes made in the editor to the game database files. If changes are not saved to
game, they will only be stored in the files the editor works on.

""","""
                     ------ RESTORE PREVIOUS DATABASE VERSION ------

Discard all unsaved changes and restore the database currently used in the game.

"""
	]
	view = True
	if item.isnumeric():
		if int(item) < len(entries):
			print(entries[int(item)])
		else: view = False
	else: view = False
	if not view: print('\nNo help entry for the selected option')
	input('Return to main menu ')
	
#start
os.system(clear_screen)
if platform.system() == 'Darwin':
	os.system('''/usr/bin/osascript -e 'tell app "System Events" to keystroke "0" using command down' ''')
	os.system('''/usr/bin/osascript -e 'tell app "System Events" to keystroke "-" using command down' ''')
	print("\x1b[8;46;201t", end = '')

#load settings
custom_vals = json.loads(open('fifa_config.json', 'r').read())
for custom_field in custom_vals.keys():
	exec('{0} = a if len(a:=custom_vals["{0}"]) == len({0}) else {0}'.format(custom_field))

gamepath = gamepath[0]
lang = lang[0]
jersey_types += custom_jerseys[0]

gamepath = ch_game_path(wait=True) if gamepath == '' else gamepath
if not gamepath: sys.exit()

lang = ch_lang(wait=True) if lang == '' else lang
if not lang: sys.exit()
	
filenames = ["FCDBPENG.DBI","FCDB.DBI","FCDB_%s.DBI"%lang,"FC%s.BIN"%lang]

Fifapath = os.path.dirname(os.path.realpath(__file__))+'/FifaDb'
if not os.path.isdir(Fifapath):
	print('Initializing...')
	os.mkdir(Fifapath)
	restore()
	
f_nomi, f_valori, f_squadre, f_interfaccia = ["%s/%s"%(Fifapath,fn) for fn in filenames]
if sum([fn in os.listdir(Fifapath) for fn in filenames]) < len(filenames): restore()
else:
	try: load_database()
	except:
		print('The database files are corrupt. Restoring from last saved version.')
		restore()

main_menu()