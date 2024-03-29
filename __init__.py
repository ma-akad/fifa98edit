#imports
print('Loading libraries...')
import os
import sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import struct
import textwrap
import re
import math
import shutil
import platform
import random
import numpy
import io
import copy
from average_fifa import *
from functools import reduce
import functools
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import colorsys
import json
import unidecode

compress_command = ""
decompress_command = ""
custom_jerseys = [[]]
WorldCupFaces = False

if platform.system() != 'Windows':
	import termios, tty
else:
	import msvcrt
def capture():
	if platform.system() != 'Windows':
		fd = sys.stdin.fileno()
		attr = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			return sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd,termios.TCSADRAIN,attr)
	else:
		return msvcrt.getch()

def getter():
	while(1):
		k = capture()
		if k != '': break
	return ord(k)

def find_key():
	command = False
	while True:
		k = getter()
		if platform.system() != 'Windows':
			if k == 27:
				command = True
				continue
			else:
				if command == True:
					if k == 91: continue
					if k == 65: return('up')
					if k == 66: return('down')
					if k == 67: return('right')
					if k == 68: return('left')
					break
				else:
					return(chr(k))
					command = False
					break
		else:
			if k == 224:
				command = True
				continue
			else:
				if command == True:
					if k == 72: return('up')
					if k == 80: return('down')
					if k == 77: return('right')
					if k == 75: return('left')
					break
				else:
					return(chr(k))
					command = False
					break

hslCols = [(242,165,237),(2,206,170),(7,216,107),(19,201,239),(17,234,224),(12,242,163),(34,237,239),(28,219,232),(24,224,170),(83,175,196),(85,226,142),(97,214,99),(145,181,196),(156,178,165),(166,170,147),(174,201,114),(197,160,209),(211,188,140),(188,168,142),(0,2,244),(0,2,226),(127,7,160),(0,0,40)]
color_selector = []
for color in hslCols:
	img = Image.new('HSV', (20,20), color)
	color_selector.append(img)
def showJersey(jersey,side,shorts_type,sock_type,je1,je2,je3,sh1,sh2,so1,so2):
	global socks, shorts
	sock_type = socks.index(sock_type)
	shorts_type = shorts.index(shorts_type)
	paletteCols = [
		(0,0,0),
		(0,0,0),
		hslCols[je1],
		hslCols[je2],
		hslCols[je3],
		hslCols[sh1],
		hslCols[sh2],
		hslCols[so1],
		hslCols[so2],
		(0,0,0),
		(0,0,0),
		(0,0,0),
		(0,0,255)
	]
	if not os.path.isfile(jersey_file:=os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS',f'JERS{jersey+1:0>2}.FSH')): return Image.open("jersey_mask.png")
	data = open(jersey_file, "rb")
	data.seek(72)
	bkhi = data.read(128**2)
	data.seek(22665)
	frhi = data.read(128**2)
	side = frhi if side=='front' else bkhi
	sideMonochrome = [b & 15 for b in side]
	sideColour = [(b & 240) >> 4 for b in side]
	flatColside = [paletteCols[c] for c in sideColour]
	deepColside = [(a,b,int(c*sideMonochrome[e]/15)) for e,(a,b,c) in enumerate(flatColside)]
	sleeves = os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','COMMON','3DTEXHI.FSH')
	sleeve_data = open(sleeves, "rb")
	sleeve_data.seek(136)
	horizontal_sleeve = sleeve_data.read(64*46)
	sleeve_data.seek(4136)
	vertical_sleeve = sleeve_data.read(64*46)
	sleeve = horizontal_sleeve if jersey in [3,4,22] else vertical_sleeve
	sleeve = [b''.join(sleeve[i:i+9] for i in range(35,2944,64)), b''.join(sleeve[i:i+20] for i in range(44,2944,64))]
	if jersey in [2,3,4,9,14,16,17,18,21]:
		paletteCols[9] = paletteCols[2]
		paletteCols[10] = paletteCols[3]
	elif jersey in [19,20,39,49]:
		paletteCols[9] = paletteCols[3]
		paletteCols[10] = paletteCols[2]
	elif jersey == 22:
		paletteCols[9] = paletteCols[2]
		paletteCols[10] = paletteCols[4]
	elif jersey in [0,1,6,7,8,10,11,12,13,15,23,24,25,26,27,29,30,31,32] or jersey > 32:
		paletteCols[9] = paletteCols[2]
		paletteCols[10] = paletteCols[2]
	elif jersey in [5,28]:
		paletteCols[9] = paletteCols[3]
		paletteCols[10] = paletteCols[3]
	sleeve_Monochrome =  [[b & 15 for b in sleeve[0]],[b & 15 for b in sleeve[1]]]
	sleeve_Colour = [[(b & 240) >> 4 for b in sleeve[0]], [(b & 240) >> 4 for b in sleeve[1]]]
	flatColSleeve = [[paletteCols[c] for c in sleeve_Colour[0]],[paletteCols[c] for c in sleeve_Colour[1]]]
	deepColSleeve = [[(a,b,int(c*sleeve_Monochrome[0][e]/15)) for e,(a,b,c) in enumerate(flatColSleeve[0])],[(a,b,int(c*sleeve_Monochrome[1][e]/15)) for e,(a,b,c) in enumerate(flatColSleeve[1])]]
	sleeveTopImg = Image.new('HSV', (9,46), "white")
	sleeveTopImg.putdata(deepColSleeve[0])
	sleeveTopImg = sleeveTopImg.resize((32,46),resample=Image.NEAREST)
	sleeveBottomImg = Image.new('HSV', (20,46), "white")
	sleeveBottomImg.putdata(deepColSleeve[1])
	sleeveBottomImg = sleeveBottomImg.resize((14,46),resample=Image.NEAREST)
	sleeveImg = Image.new('HSV', (46,46), "white")
	sleeveImg.paste(sleeveTopImg,(0,0))
	sleeveImg.paste(sleeveBottomImg,(32,0))
	leftSleeve = sleeveImg.rotate(285,expand=1,fillcolor=(0,0,209))
	rightSleeve = sleeveImg.rotate(105,expand=1,fillcolor=(0,0,209)).transpose(method=Image.FLIP_TOP_BOTTOM)
	chest = Image.new('HSV', (128,128), "white")
	chest.putdata(deepColside)
	if sock_type > 1:
		sleeve_data.seek(78120) #socks, stripes
	else:
		sleeve_data.seek(60696) #socks, trim
		if sock_type == 0:
			paletteCols[8] = paletteCols[7]
	socks_data = sleeve_data.read(128**2)
	socks_data = b''.join(socks_data[i:i+50] for i in range(5760,128**2,128))
	socksMonochrome = [b & 15 for b in socks_data]
	socksColour = [(b & 240) >> 4 for b in socks_data]
	flatColSocks = [paletteCols[c] for c in socksColour]
	deepColSocks = [(a,b,int(c*socksMonochrome[e]/15)) for e,(a,b,c) in enumerate(flatColSocks)]
	socksImg = Image.new('HSV', (50,83), "white")
	socksImg.putdata(deepColSocks)
	socksImg = socksImg.convert('RGBA').transpose(method=Image.FLIP_LEFT_RIGHT)
	rightSock = socksImg.rotate(5,expand=1)
	leftSock = socksImg.rotate(5,expand=1).transpose(method=Image.FLIP_LEFT_RIGHT)
	if shorts_type > 1:
		sleeve_data.seek(25816) #shorts, vertical
	else:
		sleeve_data.seek(43256) #shorts, horizontal
		if shorts_type == 0:
			paletteCols[6] = paletteCols[5]
	shorts_data = sleeve_data.read(128**2)
	shorts_data = b''.join(shorts_data[i:i+64] for i in range(45,10240,128))
	shortsMonochrome = [b & 15 for b in shorts_data]
	shortsColour = [(b & 240) >> 4 for b in shorts_data]
	flatColShorts = [paletteCols[c] for c in shortsColour]
	deepColShorts = [(a,b,int(c*shortsMonochrome[e]/15)) for e,(a,b,c) in enumerate(flatColShorts)]
	fullShorts = []
	for _ in range(0,5120,64):
		fullShorts += deepColShorts[_:_+64] + deepColShorts[_:_+64][::-1]
	shortsImg = Image.new('HSV', (128,80), "white")
	shortsImg.putdata(fullShorts)
	shortsImg = shortsImg.convert('RGBA')
	def find_coeffs(pa, pb):
		matrix = []
		for p1, p2 in zip(pa, pb):
			matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
			matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

		A = numpy.matrix(matrix, dtype=numpy.float64)
		B = numpy.array(pb).reshape(8)

		res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
		return numpy.array(res).reshape(8)
	coeffs = find_coeffs(
        [(8, 0), (120, 0), (128, 80), (0, 80)],
        [(0, 0), (128, 0), (128, 80), (0, 80)])
	shortsImg=shortsImg.transform((128,80),Image.PERSPECTIVE,coeffs,Image.BICUBIC)
	img = Image.new('RGBA', (218,208), (209,209,209))
	img.paste(leftSleeve, (0,0))
	img.paste(rightSleeve, (160,0))
	img.paste(chest,(45,0))
	img.paste(shortsImg,(45,128))
	img.paste(leftSock,(-30,128),leftSock)
	img.paste(rightSock,(183,128),rightSock)
	mask = Image.open("jersey_mask.png")
	img.paste(mask, (0,0), mask=mask)
	return img

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
tableSort = 'Name'
case_sensitive = False
lang = [None]
gamepath = ['']
what_to_edit = None
decomp_path = [""]

#platform-specific settings
if platform.system() == 'Windows':
	import colored
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
roles = ['GK','SW','LB','CB','RB','LM','CM','RM','LF','CF','RF','RCB','LCB','RCM','LCM'] 
hair_cl = ['blond','brown','red','BLack']
skin_cl = ['fairer','fair','dark','darker']
faces = ['African 1','African 2','Asian 1','European 1','European 2','European 3','Asian 2','African 3','Middle Eastern']
beards = ['Beard','Mouche','Moustache','Evening Shadow','Full','Goatee','Shaven']
hairs = ['Afro','Balding','Tidy','Marine','Curly','Long','Parted','Curtain','Bangs','Brazilian Crop','Shaven','Wavy']
league_sizes = list(range(1,51))
league_interface = [688,929,340,790,1647,1142,1834,1014,818,1489,1714] 
setpiece = ['CKL','CKR','FK','PK','PK1','PK2','PK3','PK4','PK5'] 

#ND
preset_looks = {
	  "Esp": [["asian","white"],["BLack","brown"],["middle eastern","cool kid"],["clean","full","full","full","goatee","three-day","three-day","three-day","three-day","three-day"],["tidy","tidy","tidy","tidy","bald/shaven","high fade","high fade","high fade","beckham"]],
	  "Gre": [["white"],["BLack"],["middle eastern","middle eastern", "skinny", "cool kid"],["clean","full","goatee","three-day","three-day","three-day","three-day"],["tidy","tidy","tidy","tidy","bald/shaven","high fade","high fade","high fade"]],
	  "Ita": [["asian","white"],["BLack","brown"],["middle eastern","cool kid","cool kid"],["clean","full","full","goatee","three-day","three-day","three-day","three-day"],["tidy","tidy","tidy","tidy","bald/shaven","high fade","high fade","terence-hill","terence-hill","terence-hill","curly"]],
	  "Fre": [["white"],["brown"],["drunkard","skinny","middle eastern","cool kid","cool kid","cool kid","cool kid"],["clean","full","goatee","three-day"],["tidy","terence-hill","curly","beckham"]],
	  "Ger": [["white"],["brown","brown","blond"],["worker","worker","drunkard","drunkard","cool kid"],["clean","full","goatee","three-day","three-day"],["machine-cut","machine-cut","machine-cut","tidy","tidy","tidy","tidy","tidy","tidy","bald/shaven"]],
	  "Sca": [["white"],["blond","blond","red"],["worker","drunkard","cool kid"],["clean","full","three-day"],["tidy","tidy","tidy","tidy","long","terence-hill","high fade","high fade"]],
	  "Sla": [["white"],["blond","blond","brown"],["drunkard","drunkard","worker","worker","worker","cool kid"],["clean","three-day","goatee"],["terence-hill","terence-hill","beckham","beckham","beckham","bald/shaven","long","long","machine-cut","high fade","high fade","high fade","high fade","high fade","curly"]],
	  "Bal": [["asian"],["BLack","BLack","BLack","blond"],["skinny","drunkard","middle eastern","drunkard","cool kid"],["clean","goatee","full","three-day","three-day","three-day","three-day"],["tidy","tidy","tidy","tidy","long","long","long","bald/shaven","high fade","high fade","receding"]],
	  "Bra": [["brown","brown","brown","brown","black"],["BLack"],["afro","afro","afro","afro","skinny","skinny","indian","chinese"],["clean","goatee","full","three-day","moustache"],["receding","curly","curly","high fade","high fade","machine-cut","bald/shaven","bald/shaven","bald/shaven"]],
	  "Afr": [["black"],["BLack"],["afro","chinese","indian"],["clean","goatee","full","three-day","arab","moustache"],["receding","curly","curly","high fade","machine-cut","machine-cut","bald/shaven","bald/shaven","bald/shaven","bald/shaven"]],
	  "Lat": [["brown","brown","brown","brown","white"],["BLack"],["skinny","middle eastern","middle eastern","cool kid","cool kid","cool kid","chinese"],["clean","goatee","three-day","full"],["curly","bald/shaven","tidy","terence-hill","machine-cut"]],
	  "Ara": [["brown","brown","white","asian"],["BLack"],["skinny","skinny","skinny","afro","middle eastern","middle eastern","middle eastern", "middle eastern"],["clean","moustache","arab","full","full","full","three-day"],["receding","tidy","high fade","high fade","high fade","bald/shaven"]],
	  "Asi": [["asian"],["BLack"],["chinese"],["clean","clean","clean","clean","goatee","mouche"],["tidy","tidy","high fade","beckham","monk","bald/shaven"]]
	}

league_sizes = list(range(1,31)) 
league_interface = [688,929,340,790,1647,1142,1834,1014,818,1489,1714] 
setpiece = ['CKL','CKR','FK','PK','PK1','PK2','PK3','PK4','PK5']

nations = {0: 'n/a', 22: 'Yugoslavia', 65: 'Mali'}
nat_groups = {17: [45, 330, 311, 305, 317, 306, 26, 318, 307, 327, 31, 312, 328, 322, 308, 323, 314, 202, 309, 315, 316, 329, 331, 332, 18, 196, 21, 333, 310, 324, 321, 325, 313, 319, 326, 320], 42: [42, 30, 49, 20, 63, 263, 265, 267, 269, 281, 270, 272, 193, 275, 276, 262, 273, 277, 279, 266, 280, 34, 282, 283, 37, 284, 285, 268, 287, 271, 274, 286, 199, 264, 192, 278], 38: [43, 33, 345, 241, 243, 237, 248, 256, 249, 250, 195, 251, 242, 244, 260, 239, 258, 240, 247, 261, 252, 245, 259, 257, 255, 238, 246, 254, 253, 201], 12: [64, 39, 40, 44, 46, 342, 343, 12, 8, 344], 13: [65, 36, 337, 341, 334, 335, 340, 338, 336, 339], 28: [303, 304, 66, 291, 292, 38, 288, 41, 191, 295, 47, 48, 50, 293, 296, 51, 52, 289, 53, 25, 27, 194, 28, 15, 29, 294, 301, 200, 32, 302, 297, 290, 35, 10, 11, 13, 14, 16, 17, 300, 19, 298, 208, 22, 23, 24, 6, 7, 9, 299]}

FCDB = []
FCDB_ENG = []
FCDBPENG = []
non_league_teams = set()

tactics = [
	'5d-4-1',
	'5d-3-2',
	'4d-5-1',
	'4d-4-2',
	'4d-3-3',
	'4-4-2',
	'4-3-3',
	'3-5-2',
	'3-4-3'
]

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
	'trim',
	'stripes'
]
socks = [
	'plain',
	'trim',
	'stripes'
]
jersey_types = {}

strategia = [
	'+2 att',
	'+1 att',
	'bal',
	'+1 def',
	'+2 def'
]

original_league_sizes = {37: 20, 38: 18, 39: 18, 40: 18, 41: 20, 42: 18, 43: 20, 46: 15, 48: 18, 50: 10, 52: 14, 32841: 10, 32842: 3, 41035: 3, 41036: 3, 41037: 4, 32846: 10, 57423: 4, 57424: 4, 57425: 4, 57426: 4, 57427: 4, 57428: 3, 57429: 3, 57430: 4, 57431: 3, 57432: 4, 32857: 10, 36954: 5, 36955: 5, 36956: 6, 36957: 6, 36958: 6, 36959: 6, 36960: 5, 36961: 6, 36962: 6, 32867: 3, 12388: 20, 12389: 4, 12390: 6, 32871: 36, 104: 6, 36993: 1, 130: 2, 131: 2, 132: 8, 133: 12, 134: 4, 135: 2, 136: 2, 137: 2, 138: 1, 139: 2, 140: 2, 141: 2, 142: 2, 143: 2, 144: 2, 145: 2, 146: 2, 147: 1, 148: 1, 149: 1, 150: 1, 151: 2, 152: 2, 153: 2, 154: 2, 155: 2, 156: 2, 157: 2, 158: 2, 159: 2, 160: 2, 161: 3, 162: 2, 163: 2, 164: 2, 165: 2, 166: 2, 167: 2, 168: 2, 169: 4, 170: 3, 171: 3, 172: 1, 173: 1, 174: 4, 175: 4, 176: 10, 177: 8, 178: 9, 179: 9, 180: 8, 181: 21, 182: 10, 183: 11, 184: 2, 185: 4, 186: 6, 187: 18, 188: 5, 189: 8, 190: 10, 191: 13, 192: 1, 193: 1, 194: 1}

fieldopedia = {
	'Name': {'short': 'Name', 'width': 16, 'db': 'name', 'align':'l'},
	'ID': {'short': 'ID', 'width': 4, 'db': 'id', 'align':'c'}, 
	'Nation': {'short': 'Nation', 'width': 21, 'db': 'country', 'align':'l'},
	'Hair Type': {'short': 'H', 'width': 1, 'db': 'hair type', 'align':'c'},
	'Hair Colour': {'short': 'HC', 'width': 2, 'db': 'hair colour', 'align':'c'},
	'Skin Colour': {'short': 'SC', 'width': 2, 'db': 'skin colour', 'align':'c'},
	'Face': {'short': 'F', 'width': 1, 'db': 'face', 'align':'c'},
	'Beard': {'short': 'B', 'width': 1, 'db': 'beard', 'align':'c'},
	'Price': {'short': '$$$', 'width': 7, 'db': 'price', 'align':'r'},
	'Jersey': {'short': 'Jers', 'width': 4, 'db': 'jersey', 'align':'r'},
	'Role': {'short': 'Role', 'width': 5, 'db': 'role', 'align':'c'},
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
	'Team': {'short': 'Team', 'width': 14, 'db': 'team', 'align':'l'}, 
	'International': {'short': '', 'width': 0, 'db': 'international', 'align':'l'}
}

field_order = ['Name','ID','Nation','Hair Type','Hair Colour','Skin Colour','Face','Beard','Price','Jersey','Role','Aggression','Acceleration','Attack Bias','Agility','Ball Control','Awareness','Fitness','Creativity','Passing','Heading','Reaction','Pass Bias','Shot Power','Shot Bias','Speed','Shot Accuracy','Tackle','Average','Index FCDBPENG','Index FCDB','Team','International']

leagueNations = [
	'0069',
	'0047',
	'0059',
	'0071',
	'0038',
	'0054',
	'0815',
	'0641',
	'0072',
	'0035',
	'0039'
]

skill_fields = field_order[11:28]
ai_fields =[x-11 for x in [11,13,22,24]]

fs_left = ['{0}{1}'.format(fieldopedia[k]['short'],(fieldopedia[k]['width']-len(fieldopedia[k]['short']))*' ') for k in fieldopedia.keys() if len(fieldopedia[k]['short'])>0]
fs_right = ['{1}{0}'.format(fieldopedia[k]['short'],(fieldopedia[k]['width']-len(fieldopedia[k]['short']))*' ') for k in fieldopedia.keys() if len(fieldopedia[k]['short'])>0]
fs_center = ['{1}{0}{2}'.format(fieldopedia[k]['short'],math.floor((fieldopedia[k]['width']-len(fieldopedia[k]['short']))/2)*' ',math.ceil((fieldopedia[k]['width']-len(fieldopedia[k]['short']))/2)*' ') for k in fieldopedia.keys() if len(fieldopedia[k]['short'])>0]

#graphics
border='╒%s╕'%'╤'.join(['═'*fieldopedia[x]['width'] for x in field_order[:-1]])
inner_line='├%s┤'%'┼'.join(['─'*fieldopedia[x]['width'] for x in field_order[:-1]])
end_border ='╘%s╛'%'╧'.join(['═'*fieldopedia[x]['width'] for x in field_order[:-1]])

custom_vals = json.loads(open(f'{os.getcwd()}/fifa_config.json', 'r').read())
for custom_field in custom_vals.keys():
	exec('{0} = a if len(a:=custom_vals["{0}"]) == len({0}) else {0}'.format(custom_field))

players_db = {}
tmmng_db = {}

#functions
def bank(s):
	if lang == 'ENG': return s
	if lang == 'GER': return round(s*2.8335)*1000
	if lang == 'ITA': return round(s*2.7813)
	if lang == 'DUT': return round(s*10.7866)*1000
	if lang == 'ESP': return round(s*239.3311)
	if lang == 'FRE': return round(s*9.5554)
	if lang == 'SWE': return round(s*12.725)

def unbank(s):
	if lang == 'ENG': return s
	if lang == 'GER': return round(round(s/1000)/2.8335)
	if lang == 'ITA': return round(s/2.7813)
	if lang == 'DUT': return round(round(s/1000)/10.7866)
	if lang == 'ESP': return round(s/239.3311)
	if lang == 'FRE': return round(s/9.5554)
	if lang == 'SWE': return round(s/12.725)

def _fgRoles(role,starting):
	if starting == 196:
		if role == 'CB': return 'LCB'
		elif role == 'CM': return 'LCM'
	elif starting == 195:
		if role == 'CB': return 'RCB'
		elif role == 'CM': return 'RCM'
	else: return role
	
def save(where, what):
	what_to_edit = None
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
	global players, teams, leagues, nations, league_list, sorted_leagues, sorted_leagues_names, non_league_teams, players_db, FCDB, FCDB_ENG, FCDBPENG, globalDB, debug
	globalDB = {} 
	FCDB, FCDB_ENG, FCDBPENG = [],[],[] 
	non_league_teams = set() 
	interface = open(f_interfaccia, 'r+b')
	interface_content = interface.read().split(b'\x00')
	interface.close()
	#load player names
	print('\033[KLoading names...', end ='')
	players = []
	nomi = open(f_nomi, 'r+b')
	while True:
		if nomi.tell() == 20:
			FCDBPENG.append(nPlayers:=struct.unpack("<l", nomi.read(4))[0])
			globalDB.setdefault('FCDBPENG',{})['number of players'] = len(FCDBPENG)-1
		if nomi.tell() == 28: break
		FCDBPENG.append(struct.unpack("<l", nomi.read(4))[0])
	n_indexes = []
	for pl in range(nPlayers):
		n_indexes.append(struct.unpack("<l", nomi.read(4))[0])
	FCDBPENG.append(n_indexes)
	globalDB['FCDBPENG']['indexes'] = len(FCDBPENG)-1
	pl_names = []
	for _ in n_indexes:
		nomi.seek(_+20,0)
		plnIndex = nomi.tell()
		string = b''
		while True:
			new_char = nomi.read(1)
			if new_char != b'\x00':
				string += new_char
			else:
				if len(string) > 0:
					players.append({'name':string.decode('unicode_escape'), 'index_fcdbpeng': plnIndex, 'search_name':unidecode.unidecode(string.decode('unicode_escape'))})
					pl_names.append(string)
				break
	FCDBPENG.append(pl_names)
	globalDB['FCDBPENG']['names'] = len(FCDBPENG)-1
	nomi.close()

	#load league names
	squadre = open(f_squadre, 'r+b')
	while True:
		if squadre.tell() == 12:
			FCDB_ENG.append(tnIndex:=struct.unpack("<l", squadre.read(4))[0])
			globalDB.setdefault('FCDB_ENG',{})['start index of team names'] = len(FCDB_ENG)-1
		if squadre.tell() == 20:
			FCDB_ENG.append(nLeagues:=struct.unpack("<l", squadre.read(4))[0])
			globalDB['FCDB_ENG']['number of leagues'] = len(FCDB_ENG)-1
		if squadre.tell() == 28: break
		FCDB_ENG.append(struct.unpack("<l", squadre.read(4))[0])
	ln_indexes = []
	for lg in range(nLeagues):
		ln_indexes.append(struct.unpack("<l", squadre.read(4))[0])
	FCDB_ENG.append(ln_indexes)
	globalDB['FCDB_ENG']['league name indexes'] = len(FCDB_ENG)-1
	leagues = []
	league_list = []
	for e,_ in enumerate(ln_indexes):
		squadre.seek(_+20,0)
		string = b''
		while True:
			new_char = squadre.read(1)
			if new_char != b'\x00':
				string += new_char
			else:
				if len(string) > 0:
					league_list.append(string.decode('unicode-escape'))
					leagues.append({'name': string.decode('unicode-escape'), 'index_fcdbpeng': _+20, 'db_position': e})
					if e<11:
						interface_content[league_interface[e]] = string
						upd_int = b'\x00'.join(interface_content)
						g = open(f_interfaccia, 'wb+').write(upd_int)
				break
	FCDB_ENG.append(league_list)
	globalDB['FCDB_ENG']['league names'] = len(FCDB_ENG)-1
	league_list = league_list[:len(leagues)] + ['National Teams'] + league_list[len(leagues):]
	sorted_leagues = {sorted(league_list[:11]).index(k):e for e,k in enumerate(league_list[:11])}
	sorted_leagues_names = [league_list[v] for k,v in sorted(sorted_leagues.items(), key=lambda x:x[0])]
	for i in range(FCDB_ENG[globalDB['FCDB_ENG']['start index of team names']]-squadre.tell()):
		FCDB_ENG.append(squadre.read(1))
	#load team names
	teams = []
	print('\r\033[KLoading team names...', end = '')
	FCDB_ENG.append(nTeams:=struct.unpack("<l", squadre.read(4))[0])
	globalDB['FCDB_ENG']['number of teams'] = len(FCDB_ENG)-1
	FCDB_ENG.append(struct.unpack("<l", squadre.read(4))[0])
	team_indexes = []
	for tm in range(nTeams):
		team_indexes.append(struct.unpack("<l", squadre.read(4))[0])
	FCDB_ENG.append(team_indexes)
	globalDB['FCDB_ENG']['team name indexes'] = len(FCDB_ENG)-1
	tm_names = []
	for e,_ in enumerate(team_indexes):
		squadre.seek(_+tnIndex,0)
		string = b''
		while True:
			new_char = squadre.read(1)
			if (squadre.tell() < team_indexes[min(e+1,len(team_indexes)-1)]+tnIndex or e == len(team_indexes)-1) and new_char:
				string += new_char
			else:
				if len(string) > 0:
					tm_names.append(temp_list:=[n for n in string.decode('unicode-escape').split('\x00') if n!=''])
					teams.append({'names': temp_list, 'index_fcdbpeng': _+tnIndex, 'db_position': e, 'search_name': unidecode.unidecode(temp_list[-1])})
				break
	FCDB_ENG.append(tm_names)
	globalDB['FCDB_ENG']['team names'] = len(FCDB_ENG)-1
	squadre.close()
	#loading database
	print('\r\033[KLoading parameters...\r', end = '')
	valori = open(f_valori, 'r+b')
	while True:
		if valori.tell() == 12:
			FCDB.append(init_teams:=struct.unpack("<l", valori.read(4))[0])
			globalDB.setdefault('FCDB',{})['start index of team data'] = len(FCDB)-1
		if valori.tell() == 16:
			FCDB.append(init_byte:=struct.unpack("<l", valori.read(4))[0])
			globalDB['FCDB']['start index of player data'] = len(FCDB)-1
		if valori.tell() == 20:
			FCDB.append(nLeagues:=struct.unpack("<l", valori.read(4))[0])
			globalDB['FCDB']['number of leagues'] = len(FCDB)-1
		if valori.tell() == 28: break
		FCDB.append(struct.unpack("<l", valori.read(4))[0])
	l_indexes = []
	for lg in range(nLeagues):
		l_indexes.append(struct.unpack("<l", valori.read(4))[0])
	FCDB.append(l_indexes)
	globalDB['FCDB']['league indexes'] = len(FCDB)-1
	for e,_ in enumerate(l_indexes):
		valori.seek(_+20,0)
		leagues[e]['id'] = (tmpLid:=struct.unpack("<H", valori.read(2))[0])
		leagues[e]['index_fcdb'] = valori.tell()
		tmpLg = [tmpLid]
		tmpLgDB = {'league id':len(tmpLg)-1}
		tmpLg.append(tmpLSize:=struct.unpack("<H", valori.read(2))[0])
		tmpLgDB['league size'] = len(tmpLg)-1
		leagues[e]['size'] = tmpLSize >> 10
		tmpLgTms = []
		tmRange = math.ceil((tmpLSize >> 10)/2)*2
		for u in range(tmRange):
			tmpLgTms.append(struct.unpack("<H", valori.read(2))[0])
		tmpLg.append(tmpLgTms)
		tmpLgDB['teams in league'] = len(tmpLg)-1
		leagues[e]['teams'] = tmpLgTms
		FCDB.append(tmpLg)
		tmpLgDB['position'] = len(FCDB)-1
		globalDB['FCDB'][f'league {e}'] = tmpLgDB
		if e < len(l_indexes)-1:
			for i in range(l_indexes[e+1]+20-valori.tell()):
				FCDB.append(valori.read(1))
	for i in range(init_teams-valori.tell()):
		FCDB.append(valori.read(1))
	FCDB.append(nTeams:=struct.unpack("<l", valori.read(4))[0])
	globalDB['FCDB']['number of teams'] = len(FCDB)-1
	FCDB.append(tSize:=struct.unpack("<l", valori.read(4))[0])
	globalDB['FCDB']['team record length'] = len(FCDB)-1
	FCDB.append([])
	globalDB['FCDB']['teams'] = len(FCDB)-1

	#retrieve team data
	sq_itr = 0

	for _ in range(nTeams):
		sq_idx = valori.tell()
		squad = valori.read(tSize)
		FCDB[-1].append([
			squad[:24],
			[squad[i:i+2] for i in range(24,64,2)]
		])
		teams[sq_itr]['index_fcdb'] = sq_idx
		teams[sq_itr]['squad'] = list(set(["{:04X}".format(int.from_bytes(squad[i:i+2] , 'big')) for i in range(24,64,2) if int.from_bytes(squad[i:i+2] , 'big') != 0]))
		teams[sq_itr]['id'] = ((int.from_bytes(squad[1:2], 'big') & 7) << 8) + int.from_bytes(squad[0:1], 'big')
		teams[sq_itr]['bank'] = ((int.from_bytes(squad[1:2], 'big') & 248) >> 3) + (int.from_bytes(squad[2:3], 'big') << 5) + ((int.from_bytes(squad[3:4], 'big') & 15) << 13)
		teams[sq_itr]['stadium'] = stadiums[int.from_bytes(squad[3:4], 'big') >> 4]
		teams[sq_itr]['first shirt'] = int.from_bytes(squad[5:6], 'big') >> 2
		teams[sq_itr]['first shirt - colour 1'] = int.from_bytes(squad[4:5], 'big') & 31
		teams[sq_itr]['first shirt - colour 2'] = ((int.from_bytes(squad[5:6], 'big') & 3) << 3) + (int.from_bytes(squad[4:5], 'big') >> 5)
		teams[sq_itr]['first shirt - colour 3'] = int.from_bytes(squad[6:7], 'big') & 31
		teams[sq_itr]['first shorts'] = shorts[int.from_bytes(squad[7:8], 'big') >> 6]
		teams[sq_itr]['first shorts - colour 1'] = (int.from_bytes(squad[6:7], 'big') >> 5) + ((int.from_bytes(squad[7:8], 'big') & 3) << 3)
		teams[sq_itr]['first shorts - colour 2'] = int.from_bytes(squad[8:9], 'big') & 31
		teams[sq_itr]['first socks'] = socks[int.from_bytes(squad[11:12], 'big') >> 6]
		teams[sq_itr]['first socks - colour 1'] = (int.from_bytes(squad[8:9], 'big') >> 5) + ((int.from_bytes(squad[9:10], 'big') & 3) << 3)
		teams[sq_itr]['first socks - colour 2'] = int.from_bytes(squad[10:11], 'big') & 31
		teams[sq_itr]['second shirt']  = int.from_bytes(squad[13:14], 'big') >> 2
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
		teams[sq_itr]['nation'] = (squad[23] & 15) << 4 | (squad[22] & 240) >> 4
		nations.setdefault(teams[sq_itr]['nation'],teams[sq_itr]['names'][-1])
		teams[sq_itr]['league'] = 'Non-League'
		teams[sq_itr]['league_id'] = len(leagues)
		for l in leagues:
			if teams[sq_itr]['id'] in l['teams'] and (bool(teams[sq_itr].get('nation',False)) == (l['db_position'] > 11)):
				teams[sq_itr]['league'] = [l['name'] for l in leagues if teams[sq_itr]['id'] in l['teams']][0]
				teams[sq_itr]['league_id'] = min([l['db_position'] for l in leagues if teams[sq_itr]['id'] in l['teams']][0], 11)
		if teams[sq_itr]['league'] == 'Non-League': non_league_teams.add(teams[sq_itr]['id'])
		sq_itr+=1
	#retrieve player data
	FCDB.append(nPlayers:=struct.unpack("<l", valori.read(4))[0])
	globalDB['FCDB']['number of players'] = len(FCDB)-1
	FCDB.append(plSize:=struct.unpack("<l", valori.read(4))[0])
	globalDB['FCDB']['player record length'] = len(FCDB)-1
	FCDB.append([])
	globalDB['FCDB']['players'] = len(FCDB)-1
	for iterations in range(nPlayers):
		players[iterations]['db_pos'] = iterations
		current_idx = valori.tell()
		string = valori.read(plSize)
		FCDB[-1].append(string)
		#bit 0
		players[iterations]['index_fcdb']=current_idx
		players[iterations]['id'] = string[0]
		#bit 1
		players[iterations]['id'] = ((string[1] & 63) << 8) + players[iterations]['id']
		players[iterations]['id'] = "{:04X}".format(int.from_bytes(players[iterations]['id'].to_bytes(2, 'little'), 'big'))
		players[iterations]['team'] = '---'
		players[iterations]['search_team'] = '---'
		players[iterations]['team_id'] = -1
		players[iterations]['international'] = []
		players[iterations]['international_id'] = []
		for t in teams:
			if players[iterations]['id'] in t['squad']:
				if t.get('nation',False):
					players[iterations]['international'].append(t['names'][-1])
					players[iterations]['international_id'].append(t['nation'])
				else:
					players[iterations]['team'] = t['names'][-1]
					players[iterations]['search_team'] = unidecode.unidecode(t['names'][-1])
					players[iterations]['team_id'] = t['id']
					players[iterations]['league_id'] = t['league_id']

		players[iterations]['nation'] = (string[1] & 192) >> 6
		#bit 2
		players[iterations]['nation'] = (string[2] << 2) + players[iterations]['nation']
		players[iterations]['country'] = nations[players[iterations]['nation']]
		#bit 3
		players[iterations]['starting'] = string[3]
		#bit 4
		players[iterations]['price'] = string[4]
		#bit 5
		players[iterations]['price'] = (string[5] << 8) + players[iterations]['price']
		#bit 6:
		hair = string[6] >> 4
		hair_c = hair_cl[(string[6] & 12) >> 2]
		skin_c = string[6] & 3
		players[iterations]['hair type'] = hair
		players[iterations]['hair colour'] = hair_c
		players[iterations]['skin colour'] = skin_c
		#bit 7
		face = string[7] >> 3
		beard = string[7] & 7
		players[iterations]['face'] = face
		players[iterations]['beard'] = beard
		#bit 8
		players[iterations]['aggression'] = ((string[8] & 240) >> 4)*4+39
		players[iterations]['acceleration'] = (string[8] & 15)*4+39
		#bit 9
		players[iterations]['attack bias'] = ((string[9] & 240) >> 4)*4+39
		players[iterations]['agility'] = (string[9] & 15)*4+39
		#bit 10
		players[iterations]['ball'] = ((string[10] & 240)>>4)*4+39
		players[iterations]['awareness'] = (string[10] & 15)*4+39
		#bit 11:
		players[iterations]['fitness'] = ((string[11] & 240)>>4)*4+39
		players[iterations]['creativity'] = (string[11] & 15)*4+39
		#bit 12:
		players[iterations]['passing'] = ((string[12] & 240)>>4)*4+39
		players[iterations]['heading'] = (string[12] & 15)*4+39
		#bit 13:
		players[iterations]['reaction'] = ((string[13] & 240)>>4)*4+39
		players[iterations]['pass bias'] = (string[13] & 15)*4+39
		#bit 14:
		players[iterations]['shot power'] = ((string[14] & 240)>>4)*4+39
		players[iterations]['shot bias'] = (string[14] & 15)*4+39
		#bit 15:
		players[iterations]['speed'] = ((string[15] & 240)>>4)*4+39
		players[iterations]['shot accuracy'] = (string[15] & 15)*4+39
		#bit 16:
		players[iterations]['jersey'] = ((string[16] & 240)>>4)
		players[iterations]['tackle'] = (string[16] & 15)*4+39
		#bit 17:
		players[iterations]['role'] = roles[((string[17] & 240)>>4)]
		players[iterations]['jersey'] = (string[17] & 15)*16 + players[iterations]['jersey']
		#bit 18:
		players[iterations]['average']  = math.floor(sum([players[iterations][fieldopedia[r]['db']] for r in skill_fields])/len(skill_fields))

		if debug:
			binary = []
			for bit in string:
				binary.append("{0:08b}".format(bit).upper())
			players[iterations]['binary'] = binary
	if debug:
		print('Detecting problems...\n')
		tmsvls = {}
		for _ in teams:
			tmsvls.setdefault(_['db_position'], {'tactics':_['tactics']})
		team_db = {}
		name_db = {}
		values_db = {}
		positions = [_*2 for _ in range(17)]
		for x in players:
			team_db.setdefault(x['team_id'], []).append((x['team'],x['jersey'],x['name'],x['index_fcdb'],x['role'],tmsvls.get(x['team_id'], {}).get('tactics',None)))
			name_db.setdefault(x['name'],set()).add(x['id'])
			cur_val = str(x['aggression']) + str(x['acceleration']) + str(x['attack bias']) + str(x['agility']) + str(x['ball']) + str(x['awareness']) + str(x['fitness']) + str(x['creativity']) + str(x['passing']) + str(x['heading']) + str(x['reaction']) + str(x['pass bias']) + str(x['shot power']) + str(x['shot bias']) + str(x['speed']) + str(x['shot accuracy']) + str(x['tackle'])
			if cur_val in values_db.keys():
				if x['name'] == 'New Player': continue
				print(x['name'],'has the same values as', ', '.join([w for w in values_db[cur_val]]))
		for team,values in team_db.items():
			if team == -1: continue
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
				dupl_teams = [y['team'] for y in players if y['id'] in howmany and y.get('league_id',11) > 10]
				dupl_purged = list(filter(lambda b: b!= '---', dupl_teams))
				if len(dupl_purged) > 1:
					print('There are %s players named %s, in %s'%(len(howmany),dupl_name, ', '.join(dupl_purged)))
		firstkits = []
		secondkits = []
		kitteam = []
		for t in teams:                                                                                                                                                                                
			k =(t['first shirt'], t['first shirt - colour 1'], t['first shirt - colour 2'], t['first shirt - colour 3'], t['first shorts'], t['first shorts - colour 1'], t['first shorts - colour 2'], t['first socks'], t['first socks - colour 1'], t['first socks - colour 2'])
			s =(t['second shirt'], t['second shirt - colour 1'], t['second shirt - colour 2'], t['second shirt - colour 3'], t['second shorts'], t['second shorts - colour 1'], t['second shorts - colour 2'], t['second socks'], t['second socks - colour 1'], t['second socks - colour 2'])
			kitteam.append(t['names'][-1])
			if k in firstkits:
				print('Duplicate kits:',t['names'][-1],'&',kitteam[firstkits.index(k)])
			if s in secondkits:
				print('Duplicate kits:',t['names'][-1],'(away) &',kitteam[secondkits.index(k)],'(away)')
			firstkits.append(k)
		print()
	debug = False
	players_db = cpdb()

def add_player(*from_menu, **kwargs): 
	ids = [int(p['id'][2:]+p['id'][:2],16) for p in players]
	new_id = sorted(ids)[-1] + 1
	new_player = new_id.to_bytes(2,'little') + bytes(18)
	if (data:=kwargs.get('data',None)):
		new_player = new_id.to_bytes(2,'little')[0].to_bytes(1,'little') + ((data[1] & 192) + new_id.to_bytes(2,'little')[1]).to_bytes(1,'little') + data[2:]
	#INCREASE NUMBER OF PLAYERS
	FCDB[globalDB['FCDB']['number of players']] += 1
	FCDBPENG[globalDB['FCDBPENG']['number of players']] += 1
	#ADD PLAYER RECORD
	FCDB[globalDB['FCDB']['players']].append(new_player)
	#RESTRUCTURE NAME DB
	FCDBPENG[globalDB['FCDBPENG']['indexes']].append(FCDBPENG[globalDB['FCDBPENG']['indexes']][-1]+len(FCDBPENG[globalDB['FCDBPENG']['names']][-1])+1)
	for e,i in enumerate(FCDBPENG[globalDB['FCDBPENG']['indexes']]):
		FCDBPENG[globalDB['FCDBPENG']['indexes']][e] += 4
	#ADD NAME TO DB
	new_name = bytes(kwargs.get('name','New Player'),'iso-8859-1') + b'\x00'
	FCDBPENG[globalDB['FCDBPENG']['names']].append(new_name)
	rebuildDbFiles()
	if from_menu:
		table = False
		idFormat = "{:04X}".format(int.from_bytes(new_id.to_bytes(2, 'little'), 'big'))
		search = search_players(idFormat,'id')
		for _ in next(iter(search['files'].values())): exec(_)
		toEdit = list(search['files'])[0]
		for _ in search_players(edit_player(search['results'][0]['index_fcdb']),'index_fcdb',strict=True)['files'][toEdit]: exec(_)
		input('\nReturn to main menu')
	else: return "{:04X}".format(int.from_bytes(new_id.to_bytes(2, 'little'), 'big'))

def duplicate_player(): 
	while True:
		a = input('Enter name of player to duplicate (hit return to cancel): ')
		if len(a) == 0: return 'n'
		if a[0] == '@':
			command = a.split('@')[1]
			a = a.split('@')[2]
		else:
			command = 'search_name'
		if command == 'team': command = 'search_team'
		search = search_players(unidecode.unidecode(a), command)
		results = search['results']
		if len(results) == 0:
			if input('No matches. New search? [yn] ') == 'n': return
		else: break
	while True:
		view = input(f'Select player to duplicate:\n\n  %s\n  ----------\n  [c]ancel: '%('\n  '.join(['[%s]: %s (%s, %s)'%(i,x['name'],x['index_fcdb'],x['team']) for i,x in enumerate(results)])))
		print()
		if view != 'c':
			if view.isnumeric():
				if int(view) < len(results):
					name = results[int(view)]['name']
					db_position = players.index(results[int(view)])
					add_player(data=FCDB[globalDB['FCDB']['players']][db_position],name=name)
					break
				else: print('The value "%s" is not in the list'%view)
			else: print('The value "%s" is not in the list'%view)
		else:
			break
		print('\033[%sA'%(7+len(results)))

def delete_player(): 
	def _perform_deletion(toDelete, **kwargs):
		id = int(toDelete['id'],16).to_bytes(2,'big')
		#SEARCH FOR ID IN TEAMS AND REMOVE IT
		for e,team in enumerate(FCDB[globalDB['FCDB']['teams']]):
			if id in team[1]:
				team[1].remove(id)
				team[1] += [b'\x00\x00']
		#REDUCE NUMBER OF PLAYERS
		FCDB[globalDB['FCDB']['number of players']] -= 1
		FCDBPENG[globalDB['FCDBPENG']['number of players']] -= 1
		#REMOVE PLAYER RECORD
		db_position = players.index(toDelete)
		del FCDB[globalDB['FCDB']['players']][db_position]
		#REMOVE FROM NAME DB
		del FCDBPENG[globalDB['FCDBPENG']['names']][db_position]
		#RESTRUCTURE NAME DB
		name_len = len(toDelete['name']) + 1
		del FCDBPENG[globalDB['FCDBPENG']['indexes']][db_position]
		for e,i in enumerate(FCDBPENG[globalDB['FCDBPENG']['indexes']]):
			FCDBPENG[globalDB['FCDBPENG']['indexes']][e] -= 4
			if e>=db_position: FCDBPENG[globalDB['FCDBPENG']['indexes']][e] -= name_len
		rebuildDbFiles(batch=kwargs.get('batch',False))

	while True:
		a = input('Enter name of player to delete (hit return to cancel): ')
		if len(a) == 0: return 'n'
		if a[0] == '@':
			command = a.split('@')[1]
			a = a.split('@')[2]
		else:
			command = 'search_name'
		if command == 'team': command = 'search_team'
		search = search_players(unidecode.unidecode(a), command)
		results = search['results']
		if len(results) == 0:
			if input('No matches. New search? [yn] ') == 'n': return
		else: break
	while True:
		view = input(f'Select player to delete:\n\n  %s\n  ----------\n  [*] all listed players\n  [c]ancel: '%('\n  '.join(['[%s]: %s (%s, %s)'%(i,x['name'],x['index_fcdb'],x['team']) for i,x in enumerate(results)])))
		print()
		if view == '*':
			if input(f'Permanently delete all listed players? Are you sure? [yn] ') != 'y': return
			for q,pl2d in enumerate(results[::-1]):
				pl2d['index_fcdbpeng'] -= 4*q
				_perform_deletion(pl2d, batch=True)
				print('\r\033[K',q+1,' of ',len(results),sep='',end='')
			load_database()
			input('\n\nReturn to main menu')
			break
		elif view != 'c':
			if view.isnumeric():
				if int(view) < len(results):
					if input(f'Permanently delete {results[int(view)]["name"]}? Are you sure? [yn] ') != 'y': return
					_perform_deletion(results[int(view)])
					input('\nPlayer deleted')
					break
				else: print('The value "%s" is not in the list'%view)
			else: print('The value "%s" is not in the list'%view)
		else:
			break
		print('\033[%sA'%(8+len(results)))

def add_team(**kwargs):
	nat = input('National team [yn]? ') == 'y'
	ids = [t['id'] for t in teams if type(t['id']) == int]
	new_id = sorted(ids)[-1] + 1
	new_team = new_id.to_bytes(2,'little') + bytes(22)
	if nat:
		nation_n = len(nations)
		new_team = new_id.to_bytes(2,'little') + bytes(20) + (((nation_n & 15) << 4) + 10).to_bytes(1,'big') + (nation_n >> 4).to_bytes(1,'big')
		createNatTeamFlag(str(f'{new_id:04}'))
	if (data:=kwargs.get('data',None)):
		new_team = new_id.to_bytes(2,'little')[0].to_bytes(1,'little') + ((data[0][1] & 248) + new_id.to_bytes(2,'little')[1]).to_bytes(1,'little') + data[0][2:]
	#INCREASE NUMBER OF TEAMS
	FCDB[globalDB['FCDB']['number of teams']] += 1
	FCDB_ENG[globalDB['FCDB_ENG']['number of teams']] += 1
	#ADD TEAM RECORD
	empty_squad = 20*[b'\x00\x00']
	if (data:=kwargs.get('data',None)): empty_squad = data[1]
	FCDB[globalDB['FCDB']['teams']].append([new_team, empty_squad])
	#UPDATE VALUE DB
	FCDB[globalDB['FCDB']['start index of player data']] += 64
	#RESTRUCTURE NAME DB
	FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']].append(FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']][-1]+18+len(FCDB_ENG[globalDB['FCDB_ENG']['team names']][-1][-1]))
	for e,i in enumerate(FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']]):
		FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']][e] += 4
	#ADD NAME TO DB
	new_names = kwargs.get('names',['NTeam','New Team',f'New Team {new_id}'])
	FCDB_ENG[globalDB['FCDB_ENG']['team names']].append(new_names)
	rebuildDbFiles()
	show_teams(new_names[-1])

def duplicate_team(): 
	l1 = int(inputPlus('\nSelect league:\n  $OPTIONLIST_l$$CANCEL$', sorted_leagues_names+['National Teams'], c=True, sep='\n  ')[0])
	if l1 < 12:
		l1 = sorted_leagues.get(l1,l1)
		tms = [(team['names'][-1],team['db_position']) for team in sorted(teams, key=lambda x: x['names'][-1]) if team['league_id'] == l1]
	else: return
	t = int(inputPlus('\nSelect team:\n  $OPTIONLIST_l$$CANCEL$', [t[0] for t in tms], idx='0', c=True, sep='\n  ')[0])
	if t < len(tms):
		t = tms[t][1]
	else: return
	add_team(data=FCDB[globalDB['FCDB']['teams']][t],names=FCDB_ENG[globalDB['FCDB_ENG']['team names']][t])

def delete_team(): 
	print('Only non-league teams can be deleted. If you wish to delete a team, release it from its league.')
	if len(non_league_teams) == 0:
		input()
		return
	tms = [t for t in teams if t['id'] in non_league_teams]
	t = int(inputPlus('\nSelect team to delete:\n  $OPTIONLIST_l$$CANCEL$', [t['names'][-1] for t in tms], c=True, sep='\n  ')[0])
	if t < len(tms):
		toDelete = tms[t]
		db_position = teams.index(toDelete)
		#REDUCE NUMBER OF TEAMS
		FCDB[globalDB['FCDB']['number of teams']] -= 1
		FCDB_ENG[globalDB['FCDB_ENG']['number of teams']] -= 1
		#REMOVE TEAM RECORD
		del FCDB[globalDB['FCDB']['teams']][db_position]
		#UPDATE VALUE DB
		FCDB[globalDB['FCDB']['start index of player data']] -= 64
		#REMOVE FROM NAME DB
		del FCDB_ENG[globalDB['FCDB_ENG']['team names']][db_position]
		#RESTRUCTURE NAME DB
		name_len = 18+len(toDelete['names'][-1])
		print()
		if input(f'Are you sure that you want to delete {toDelete["names"][-1]}? [yn] ') != 'y': return
		del FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']][db_position]
		for e,i in enumerate(FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']]):
			FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']][e] -= 4
			if e>=db_position: FCDB_ENG[globalDB['FCDB_ENG']['team name indexes']][e] -= name_len
		rebuildDbFiles()

def rebuildDbFiles(**kwargs): 
	temp_file = b''
	list_tracker = 0
	for e,_ in enumerate(FCDB):
		if type(_) == int: temp_file += _.to_bytes(4,'little')
		if type(_) == list:
			list_tracker += 1
			for __ in _:
				if list_tracker == 1: #league indexes
					temp_file += __.to_bytes(4,'little')
				elif list_tracker <= 110: #leagues
					if type(__) == int: temp_file += __.to_bytes(2,'little')
					elif type(__) == list:
						for ___ in __:
							temp_file += ___.to_bytes(2,'little')
				elif list_tracker == 111: #teams
					for ___ in __:
						if type(___) == bytes: temp_file += ___
						else: temp_file += b''.join(___)
			if list_tracker == 112: #players_db
				temp_file += b''.join(_)
		if type(_) == bytes: temp_file += _

	rbdb = open(f_valori,'wb+')
	rbdb.write(temp_file)

	temp_file = b''
	for e,_ in enumerate(FCDBPENG):
		if type(_) == int: temp_file += _.to_bytes(4,'little')
		if type(_) == list:
			for __ in _:
				if type(__) == bytes: temp_file += __  + b'\x00'
				else: temp_file += __.to_bytes(4,'little')
		if type(_) == bytes: temp_file += _

	rbdb = open(f_nomi,'wb+')
	rbdb.write(temp_file)

	def _fixb(s,tni):
		if tni == 0:
			return s + (5-len(s))*b'\x00'
		if tni == 1:
			return s + (10-len(s))*b'\x00'
		if tni == 2:
			return s

	temp_file = b''
	list_tracker = 0
	for e,_ in enumerate(FCDB_ENG):
		if type(_) == int: temp_file += _.to_bytes(4,'little')
		if type(_) == bytes: temp_file += _
		if type(_) == list:
			list_tracker += 1
			for __ in _:
				if type(__) == int: temp_file += __.to_bytes(4,'little')
				if type(__) == str: temp_file += bytes(__, 'iso-8859-1') + b'\x00'
				if type(__) == list:
					temp_file += b'\x00'.join(_fixb(bytes(___, 'iso-8859-1'), tni) for tni,___ in enumerate(__)) + b'\x00'

	rbdb = open(f_squadre,'wb+')
	rbdb.write(temp_file)
	if not kwargs.get('batch',False): load_database()

def search_players(a,field,*laconic, **kwargs):
	results = []
	player_files = {}
	tableBuilder = []
	if not laconic:
		if debug == True:
			print()
			print(f'╒════╤{30*"═"}{20*"╤════"}╕')
			print(f'│    │{"Name":^30}│{"│".join(["{:4d}".format(x) for x in range(20)])}│')
		if table == True:
			tableBuilder.append('')
			tableBuilder.append(border)
			tableBuilder.append('│%s│'%'│'.join(fs_center))
			fields = [set(),[],set(),[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	fc = 0
	if field == 'nation': field == 'country'
	for b in str(a).split('/'):
		for x in players:
			what = b.strip()
			where = str(x.get(field, ''))
			if field == 'league': where = lg[0] if len (lg:=[l['name'] for l in leagues if l['db_position'] == x.get('league_id', '')]) > 0 else ''
			if field.upper() == 'INTERNATIONAL' and len(where) > 2: where = where[1:-1]
			if case_sensitive == False:
				what = what.upper().split(',')
				where = where.upper()
			for operator in ['>=','<=','>','<']:
				if operator in what[0]:
					mv = int(what[0].split(operator)[1])
					if '>' in operator:
						what = [str(_) for _ in range((((mv-39)//4) + ('=' not in operator))*4+39,100,4)]
						break
					if '<' in operator:
						what = [str(_) for _ in range(39, (((mv-39)//4) + ('=' not in operator))*4+40,4)]
						break
			found = what[0] == where if kwargs.get('strict', False) else any([w in where for w in what])
			if re.search('[\[\]\|\(\)\*\+\$\^]', what[0]):
				found = re.search(what[0],where)
			if (refine:=kwargs.get('refine',None)): 
				for extraField in refine:
					extraCommand = extraField.split('@')[1]
					extraQuery = extraField.split('@')[2].split(',')
					for operator in ['>=','<=','>','<']:
						if operator in extraQuery[0]:
							mv = int(extraQuery[0].split(operator)[1])
							if '>' in operator:
								extraQuery = [str(_) for _ in range((((mv-39)//4) + ('=' not in operator))*4+39,100,4)]
								break
							if '<' in operator:
								extraQuery = [str(_) for _ in range(39, (((mv-39)//4) + ('=' not in operator))*4+40,4)]
								break
					if not any([re.search(w.upper(), str(x.get(extraCommand,'')).upper()) for w in extraQuery]): found = False
			if found:
				index = kwargs.get('index', x['index_fcdb'])
				role = _fgRoles(x['role'], x['starting'])
				if not laconic:
					fields_off = ['Name','ID','Hair Type','Hair Colour','Skin Colour','Face','Beard','Role','Index FCDBPENG','Index FCDB','Team','International']
					if debug == True:
						print(f'├────┼{30*"─"}{20*"┼────"}┤')
						print(f'│{fc:^4}│{x["name"]:<30}│{"│".join([w[:4] for w in x["binary"]])}│')
						print(f'│    │{" "*30}│{"│".join([w[4:] for w in x["binary"]])}│')
						fc += 1
					else:
						if table == False:
							player_files[index] = ['os.system(clear_screen)']
							int_string = ', '.join(x['international'])
							player_files[index].append("print('\\n%s'%('━'*83))")
							fullname = x['name']
							player_files[index].append(f'print("{fullname:^80}")')
							player_files[index].append("print(83*'━')")
							player_files[index].append(f"print('ID:','{x['id']}', sep='\t\t\t')")
							player_files[index].append(f"print('Index FCDBPENG:','{x['index_fcdbpeng']}', sep='\t\t')")
							player_files[index].append(f"print('Index FCDB:','{x['index_fcdb']}', sep='\t\t')")
							player_files[index].append("print(40*'━')")
							player_files[index].append(f'print("Nation:","{x["country"]}", sep="\t\t\t")')
							player_files[index].append(f'print("Team:", "{x["team"]}", sep ="\t\t\t")')
							player_files[index].append(f'print("International:", "{int_string}", sep ="\t\t")')
							player_files[index].append("print(40*'━')")
							player_files[index].append(f"print('Position:','{dict(GK='Goalkeeper',CB='Defender',RB='Defender',LB='Defender',SW='Defender',CM='Midfielder',RM='Midfielder',LM='Midfielder',CF='Forward',RF='Forward',LF='Forward',RCB='Defender',LCB='Defender',RCM='Midfielder',LCM='Midfielder')[role]}', sep='\t\t')")
							player_files[index].append(f"print('Role:','{role}', sep='\t\t\t')")
							player_files[index].append(f"print('Jersey:','{x['jersey']}', sep='\t\t\t')")
							player_files[index].append(f"print('Price:','{bank(x['price'])}', sep='\t\t\t')")
							player_files[index].append(f"print('Starting:','{'Yes' if x['starting'] > 128 else 'No'}', sep='\t\t')")
							player_files[index].append("print(40*'━')")
							player_files[index].append(f"print('Skin Colour:','{skin_cl[x['skin colour']]}', sep='\t\t')")
							player_files[index].append(f"print('Face:','{faces[x['face']]}', sep='\t\t\t')")
							player_files[index].append(f"print('Hair Type:','{hairs[x['hair type']]}', sep='\t\t')")
							player_files[index].append(f"print('Hair Colour:','{x['hair colour'].lower()}', sep='\t\t')")
							player_files[index].append(f"print('Beard:','{beards[x['beard']]}', sep='\t\t\t')")
							player_files[index].append("print(83*'━')")
							player_files[index].append("print('\033[20A', end='')")
							player_files[index].append(f"print('\033[43CSpeed:','{x['speed']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CAcceleration:','{x['acceleration']}', sep='\t\t')")
							player_files[index].append(f"print('\033[43CAgility:','{x['agility']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CAggression:','{x['aggression']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CAttack Bias:','{x['attack bias']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CBall Control:','{x['ball']}', sep='\t\t')")
							player_files[index].append(f"print('\033[43CAwareness:','{x['awareness']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CFitness:','{x['fitness']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CCreativity:','{x['creativity']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CPassing:','{x['passing']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CPass Bias:','{x['pass bias']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CHeading:','{x['heading']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CReaction:','{x['reaction']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CTackle:','{x['tackle']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CShot Bias:','{x['shot bias']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CShot Power:','{x['shot power']}', sep='\t\t\t')")
							player_files[index].append(f"print('\033[43CShot Accuracy:','{x['shot accuracy']}', sep='\t\t')")
							player_files[index].append("print('\033[43C',40*'─',sep = '')")
							player_files[index].append(f"print('\033[43CAVERAGE:', '{x['average']}', sep ='\t\t\t')")
							player_files[index].append("print()")
						else:
							player_files[index] = ['']
							titolare = '*' if x['starting'] > 128 else '' 
							team_string = x['team']+titolare 
							if len(team_string) > fieldopedia['Team']['width']: team_string = team_string [:fieldopedia['Team']['width']-3] + ('.' if team_string[fieldopedia['Team']['width']-4] != ' ' else team_string[fieldopedia['Team']['width']-3])+'.' + ('.' if titolare == '' else titolare)
							
							international = ['','']
							for n in x['international_id']:
								if n != x['nation']:
									international[1] = ' (%s*)'%nations[n]
								if n == x['nation']:
									international[0] = '*'
							international = ''.join(international)

							tbl_row ='│'
							for g in field_order[:-1]:
								cell_content = x[fieldopedia[g]['db']]
								if g == 'Hair Colour' :cell_content = hair_cl_d[cell_content]
								if g == 'Skin Colour' :cell_content = skin_cl_d[cell_content]
								if g == 'Nation': cell_content += international
								if g == 'Price': cell_content = bank(cell_content)
								if g == 'Team': cell_content = team_string
								tbl_row += align(cell_content,g)
								tbl_row += '│'
							tableBuilder.append(tbl_row)

							cy = 0
							for f in field_order:
								if f not in fields_off:
									try:
										fields[cy].add(x[fieldopedia[f]['db']])
									except:
										fields[cy].append(x[fieldopedia[f]['db']])
									cy+=1
					results.append(x)
				else:
					results = [x[fieldopedia[g]['db']] for g in skill_fields]
					results += [x['starting'],x['hair colour'],x['skin colour'],x['face'],x['beard'],x['hair type'],x['jersey'],role,x['name'],x['index_fcdbpeng'],players.index(x)] 
	if table:
		sortField = [_.strip() for _ in fs_center].index(tableSort)+1
		sortRev = (sortField > 11 and sortField < 30) or sortField == 9
		sortedRows = sorted([_ for _ in tableBuilder[3:]], key=lambda x: x.split('│')[sortField], reverse = sortRev)
		tableBuilder = tableBuilder[:3]
		for _ in sortedRows:
			tableBuilder.append(inner_line)
			tableBuilder.append(_)
	if not laconic:
		if debug == True:
			print(f"╘════╧{30*'═'}{20*'╧════'}╛")
			print()
			print('Legend: 0.1 = ID; 1.1.1 = Nation, 1.1.2 = ID, 1.2 = ID; 2 = Nation; 3 = In starting lineup; 4 and 5 = Price; 6.1 = Hair, 6.2.1 = Hair Colour 6.2.2 = Skin Colour; 7.1 = Face, 7.2 = Beard; 8.1 = Aggression, 8.2 = Acceleration; 9.1 = Attack Bias, 9.2 = Agility; 10.1 = Ball, 10.2 = Awareness; 11.1 = Fitness, 11.2 = Creativity; 12.1 = Passing, 12.2 = Heading; 13.1 = Reaction, 13.2 = Pass Bias; 14.1 = Shot Power, 14.2 = Shot Bias; 15.1 = Speed, 15.2 = Shot Accuracy; 16.1 = Jersey (low), 16.2 = Tackle; 17.1 = Role, 17.2 = Jersey (high); 18 and 19 = ?')
			print()
		if table == True:
			if len(results) == 0:
				global end_border
				tableBuilder.append(inner_line.replace('┼','┴'))
				tableBuilder.append('│ No results%s│'%((sum([fieldopedia[c]['width'] for c in fieldopedia.keys()])+len(fieldopedia.keys())-13)*' '))
				tableBuilder.append(end_border.replace('╧','═').replace('╪','═'))
				print('\n'.join(_ for _ in tableBuilder))
				return {'results':results}
			conflict = 'ok'
			if len(fields[2]) != len(fields[1]): conflict = '!!'

			if not debug:
				for e,data in enumerate(fields):
					if e == 0: fields[e] = "{:>{width}}".format("%s nations"%len(fields[0]),width=fieldopedia['Nation']['width'])
					if e == 1: fields[e] = align(bank(math.floor(sum(fields[e])/len(fields[e]))),'Price')
					if e == 2: fields[e] = align(conflict, 'Average')
					if e > 2:  fields[e] = align(math.floor(sum(fields[e])/len(fields[e])),'Average')

			frag_border = ' '
			summary = ' '
			cy = 0
			end_border = '╘'
			for e,f in enumerate(field_order):
				if f in fields_off:
					if len(end_border)>1:
						if e > 0 and field_order[e-1] not in fields_off: end_border += '╪'
						else: end_border += '╧' if e < len(field_order)-1 else '╛'
					if frag_border[:-1] == ' ':
						frag_border = frag_border[:-1]+' '*(fieldopedia[f]['width']+2)
						summary = summary[:-1]+' '*(fieldopedia[f]['width']+2)
					else:
						frag_border += ' '*(fieldopedia[f]['width']+1)
						summary += ' '*(fieldopedia[f]['width']+1)
				else:
					end_border += '╪'
					summary = summary[:-1]+'│'
					summary += fields[cy]
					summary	+= '│'
					cy += 1
					frag_border = frag_border[:-1]+'╧' if e > 0 and field_order[e-1] not in fields_off else frag_border[:-1]+'╘'
					frag_border += '═'*fieldopedia[f]['width']
					frag_border += '╛'
				end_border += '═'*(fieldopedia[f]['width'])
			tableBuilder.append(end_border)
			tableBuilder.append(summary)
			tableBuilder.append(frag_border)
			tableBuilder.append('')
			print('\n'.join(_ for _ in tableBuilder))
	return {'results':results,'files':player_files}

def edit_player(modify,**args):
	global f_valori, f_nomi, roles, nations
	vals_already = search_players(modify, 'index_fcdb', True, strict=True)['results']
	ttmng = tmmng_db.get(players[vals_already[-1]]['team_id'], None)
	valori = open(f_valori, 'r+b')
	temp_file = b''
	mod_offset=int(modify)
	what_to_edit = args.get('field', None)
	valid = True
	edit_menu = [ 
		[
			f" [0] aggression ({vals_already[0]})",
			f" [1] acceleration ({vals_already[1]})",
			f" [2] attack bias ({vals_already[2]})",
			f" [3] agility ({vals_already[3]}) ",
			f" [4] ball ({vals_already[4]})",
			f" [5] awareness ({vals_already[5]})",
			f" [6] fitness ({vals_already[6]})",
			f" [7] creativity ({vals_already[7]})",
			f" [8] passing ({vals_already[8]})",
			f" [9] heading ({vals_already[9]})",
			f" [10] reaction ({vals_already[10]})",
			f" [11] pass bias ({vals_already[11]})",
			f" [12] shot power ({vals_already[12]})",
			f" [13] shot bias ({vals_already[13]})",
			f" [14] speed ({vals_already[14]})",
			f" [15] shot accuracy ({vals_already[15]})",
			f" [16] tackle ({vals_already[16]})",
			f" [*] all "
		],
		[
			" [n]ame",
			f" [j]ersey ({vals_already[23]})",
			f" [r]ole ({vals_already[24]})",
			f" countr[y]",
			f" [p]rice"		
		],
		[
			f" [f]ace",
			f" [s]kin colour",
			f" [h]air",
			f" hair c[o]lour",
			f" [b]eard"
		]
	]
	menu = '	╔═════════════════════════╗\n'+\
		  '\n	╟─────────────────────────╢\n'.join(['\n'.join([f"	║{t:<25}║" for t in submenu]) for submenu in edit_menu])+\
	   """\n	╚═════════════════════════╝
(hit return to go back):\033[J """	  
	while True:
		if what_to_edit is None: what_to_edit = input(f"Parameter to edit:\n{menu}")
		if len(what_to_edit) == 0:
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
		elif what_to_edit == 'p': 
			new_price = int(args.get('value', None))
			if new_price is None:
				new_price = input('\nEnter new price (\'c\' to cancel): ')
				while True:
					try:
						new_price = int(new_price)
						break
					except:
						if new_price == 'c': break
						print('Enter a number or \'c\' to cancel.')
						return 
			new_price = min(unbank(new_price), 65535)
			price_bit = [new_price & 255,new_price>>8]
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			for bit in range(20):
				if bit < 4:
					temp_file += valori.read(1)
				if bit == 4:
					valori.read(1)
					temp_file += bytes([price_bit[0]])
				if bit == 5:
					valori.read(1)
					temp_file += bytes([price_bit[1]])
			temp_file+=valori.read()
			save(f_valori, temp_file)
			load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'r':
			if (new_role := args.get('value', None)) is None:
				new_role = int(inputPlus('\nEnter new role ($OPTIONLIST_l$$CANCEL$)', roles, sep=', ', c=True)[0])
				if new_role == len(roles): return mod_offset
			else:
				new_role=roles.index(new_role)
			starting = args.get('starting', False) or vals_already[-11]
			if starting > 128:
				if new_role in [roles.index(_) for _ in ['GK','SW','RB','RM','RF']]: starting = 180
				elif new_role in [roles.index(_) for _ in ['CB','CM','CF']]: starting = 198
				elif new_role in [roles.index(_) for _ in ['RCB','RCM']]: starting = 195
				elif new_role in [roles.index(_) for _ in ['LCB','LCM']]: starting = 196
				elif new_role in [roles.index(_) for _ in ['LB','LM','LF']]: starting = 192
			else: starting = 128
			if new_role == 11: new_role = 3
			elif new_role == 12: new_role = 3
			elif new_role == 13: new_role = 6
			elif new_role == 14: new_role = 6
			new_role = new_role << 4
			valori.seek(0, 0)
			temp_file = valori.read(mod_offset)
			temp_bit = 0
			for bit in range(20):
				if bit < 3:
					temp_file += valori.read(1)
				elif bit == 3:
					temp_file += bytes([starting])
					valori.seek(1,1)
				elif bit < 17:
					temp_file += valori.read(1)
				elif bit == 17:
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
				del countries['N/A']
			new_country= args.get('value', '')
			if new_country.upper() not in countries.keys():
				print('\n')
				nl  = '\n' if platform.system() == 'Windows' else ''
				while True:
					new_country = input('\033[1A\033[K'+f'Enter new country {("for "+vals_already[-3]+" ")*(not args.get("value",None) is None)}(hit return to cancel; [l]ist countries): ')
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
			nc_b2 = new_country >> 2
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
			current_role = args.get('role', vals_already[-4])
			if starting is None: starting = 128
			elif current_role in ['GK','SW','RB','RM','RF']: starting = 180
			elif current_role in ['CB','CM','CF']: starting = 198
			elif current_role in ['RCB','RCM']: starting = 195
			elif current_role in ['LCB','LCM']: starting = 196
			elif current_role in ['LB','LM','LF']: starting = 192
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
			return (starting, current_role)
		elif what_to_edit == 'f':
			new_face = args.get('value', None)
			if new_face is None:
				print('\nSelect new face')
				face_sel = tk.Tk()
				face_sel.geometry('+0+0')
				face_sel.attributes("-topmost", True)
				global c
				c = None
				def on_closing(event):
					if event.widget == face_sel:
						if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				face_sel.bind("<Destroy>", on_closing)
				photo = []
				def callback(n):
					global c
					c = int(n['text'])
					face_sel.destroy()
					if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				for f in range(0,7+WorldCupFaces):
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
					btn.grid(row=int(f/4), column=f%4, padx=2, pady=2)
				face_sel.title(f'{vals_already[-3]}: face')
				face_sel.mainloop()
				if new_face is None:
					new_face = c or vals_already[-8]
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
				face_sel.attributes("-topmost", True)
				c = None
				def on_closing(event):
					if event.widget == face_sel:
						if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				face_sel.bind("<Destroy>", on_closing)
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
					btn.grid(row=int(f/4), column=f%4, padx=2, pady=2)
				face_sel.title(f'{vals_already[-3]}: facial hair')
				face_sel.mainloop()
				if new_beard is None: new_beard = c or vals_already[-7]
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
				face_sel.attributes("-topmost", True)
				c = None
				def on_closing(event):
					if event.widget == face_sel:
						if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				face_sel.bind("<Destroy>", on_closing)
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
					btn.grid(row=int(f/4), column=f%4, padx=2, pady=2)
				face_sel.title(f'{vals_already[-3]}: hair')
				face_sel.mainloop()
				if new_hair is None:
					new_hair = c or vals_already[-6]
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
				value = args.get('value', False)
				if not value:
					new_vals[int(what_to_edit)] = input('\nInput new value for %s (hit return to cancel): '%skill_fields[int(what_to_edit)])
					if len(new_vals[int(what_to_edit)]) == 0: return mod_offset
					print()
				else: new_vals[int(what_to_edit)] = value
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
						elif new_vals == '=':
							full_ave = math.floor(sum(vals_already[0:17])/len(vals_already[0:17]))
							old_ave = math.floor(sum(no_ai:=[y for e,y in enumerate(vals_already[0:17]) if e not in ai_fields])/len(no_ai))
							if full_ave == old_ave:
								print('The averages correspond')
								return mod_offset
							else:
								print('Equalizing current average (%s) to average without AI fields (%s)'%(full_ave, old_ave))
								new_vals = handle_ai(difference := old_ave - full_ave, '+' if difference > 0 else '-')
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
					if len(new_vals) >= 34 and new_vals.isnumeric():
						new_vals = [new_vals[i:i+2] for i in range(0, 34, 2)]
					else: new_vals = gimme_values(new_vals, role=vals_already[-4], verbose=args.get('verbose', True))
			try:
				vals = [math.floor((int(x)-39)/4) for x in new_vals.split()]
			except:
				vals = [math.floor((int(x)-39)/4) for x in new_vals]
			else:
				print('New average: ', math.floor(sum([int(vals) for vals in new_vals.split()])/len(vals)))
			if ttmng:
				pl_team = [t for t in teams if t['id'] == players[vals_already[-1]]['team_id']][0]
				if players[vals_already[-1]]['id'] in ttmng['lineup']:
					pos = ttmng['lineup'].index(players[vals_already[-1]]['id'])
					if vals[0] != (vals_already[0]-39)//4:
						ttmng['aggression'][pos] = vals[0]
						_refresh_tmmng(pl_team,'aggression',ttmng['aggression'])
					if vals[2] != (vals_already[2]-39)//4:
						ttmng['attack'][pos] = vals[2]
						_refresh_tmmng(pl_team,'attack',ttmng['attack'])
					write_tmmng()
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
			print('\033[34A',end="")
		if valid: break
	try:
		p = args['value']
	except:
		if input('Continue editing? [yn] ') == 'y':
			os.system(clear_screen)
			for _ in search_players(mod_offset,'index_fcdb',strict=True)['files'][modify]: exec(_)
			edit_player(modify)
	else:
		del p
	valori.close()
	if args.get('returnValues'):
		return {field:new_vals[e] for e,field in enumerate(list(fieldopedia.keys())[11:28])}
	return mod_offset

def show_teams(*index):
	p = {}
	for pos,pl in enumerate(players):
		p.setdefault(pl['id'],pos)
	a = index[0] if index else input('Team name (hit return to cancel): ')
	if len(str(a)) == 0:
		return
	results = 0
	field = a.split('@')[1] if a[0] == '@' else 'names'
	a = a.split('@')[-1]
	for idx,t in enumerate(teams):
		params = (idx, t, index)
		sf = unidecode.unidecode(str(t[field]))
		if not case_sensitive:
			a = unidecode.unidecode(str(a).upper())
			sf = sf.upper()
		if a in sf:
			results += 1
			if _display_team(params) == 'cancelled': return
	if results == 0: print('Not found')
	if (ntSearch:=input('\nSearch new team? [yn] ')) == 'n': return False
	else: show_teams(ntSearch) if ntSearch != 'y' else show_teams()

def _display_team(params, **kwargs):
	os.system(clear_screen)
	refresh = kwargs.get('refresh',None)
	(idx, t, index) = params
	if refresh: t = teams[idx]
	ttmng = tmmng_db.get(t['id'],{}) 
	print('%s'%('━'*81))
	print('Name', t['names'][-1], sep="\t\t\t")
	print('%s'%('─'*81))
	if len(t['names']) == 3: print('Short Name', t['names'][1], sep="\t\t")
	print('Abbreviation', t['names'][0], sep="\t\t")
	print('%s'%('─'*81))
	print('Index FCDB', t['index_fcdb'], sep="\t\t")
	print('Index FCDBPENG', t['index_fcdbpeng'], sep="\t\t")
	print('Id', t['id'], sep="\t\t\t")
	if (ttnn:=t['nation']) != 0: print('Nation ID',ttnn,sep = '\t\t') #NEW
	print('%s'%('─'*81))
	print('League', t['league'], sep="\t\t\t") 
	print('Bankroll', bank(t['bank']), sep="\t\t")
	print('Stadium', t['stadium'], sep="\t\t\t")
	print('%s'%('─'*81))
	firstkit, secondkit = '', ''
	firstkit+="\033[10C".join(['1st shirt type', jersey_types.get(t['first shirt'],f"jers{t['first shirt']+1}.fsh")])
	firstkit+="\n1st shirt colours\033[7C%s%s%s\033[0m "%(cesc[t['first shirt - colour 1']],cesc[t['first shirt - colour 2']],cesc[t['first shirt - colour 3']])
	firstkit+='\n'+"\033[9C".join(['1st shorts type', t['first shorts']])
	firstkit+='\n1st shorts colours\033[6C%s%s\033[0m'%(cesc[t['first shorts - colour 1']],cesc[t['first shorts - colour 2']])
	firstkit+='\n'+"\033[10C".join(['1st socks type', t['first socks']])
	firstkit+='\n1st socks colours\033[7C%s%s\033[0m'%(cesc[t['first socks - colour 1']],cesc[t['first socks - colour 2']])
	secondkit+="\033[10C".join(['2nd shirt type', jersey_types.get(t['second shirt'],f"jers{t['second shirt']+1}.fsh")])
	secondkit+='\n2nd shirt colours\033[7C%s%s%s\033[0m'%(cesc[t['second shirt - colour 1']],cesc[t['second shirt - colour 2']],cesc[t['second shirt - colour 3']])
	secondkit+='\n'+"\033[9C".join(['2nd shorts type', t['second shorts']])
	secondkit+='\n2nd shorts colours\033[6C%s%s\033[0m'%(cesc[t['second shorts - colour 1']],cesc[t['second shorts - colour 2']])
	secondkit+='\n'+"\033[10C".join(['2nd socks type', t['second socks']])
	secondkit+='\n2nd socks colours\033[7C%s%s\033[0m'%(cesc[t['second socks - colour 1']],cesc[t['second socks - colour 2']])
	fk=firstkit.split('\n')
	sk=secondkit.split('\n')
	for _ in range(len(fk)):
		print('%s\r\033[50C%s'%(fk[_],sk[_]))
	print('%s'%('─'*81))
	rt = recommended_tactics(t['squad'])
	if t["league_id"] >= 11:
		rt = recommended_tactics(t['squad'], tactics=t['tactics'])
	print('Strategy', t['strategy'], sep="\t\t")
	n_tactics = ttmng.get('formation',[]) if not ttmng.get('formation',None) is None else t['tactics'].split('-')
	print('Tactics', '-'.join(n_tactics), sep="\t\t\t")
	current = [(players_db[p]['name'],_fgRoles(players_db[p]['role'],players_db[p]['starting']),players_db[p]['average'],players_db[p]['starting'],players_db[p]['country'],players_db[p][f'jersey'],p,players_db[p]['index_fcdb'],players_db[p]['team']) for p in ttmng.get('lineup',[])] if not ttmng.get('lineup',None) is None else rt['starting']
	if (rls:=[_[1] for _ in current]).count('CB') > 1 and rls.count('SW') > 0 and rls[::-1].index('SW') < rls[::-1].index('CB'):
		current = current[:rls.index('CB')+1] + [current[rls.index('SW')]] + [current[rls.index('SW')-1]] + current[len(current)-rls[::-1].index('SW'):]
	fine = '' if t['roster size']==len(pl_list := rt['pl_list']) else ' (%s)'%len(pl_list)
	print('Roster Size', str(t['roster size'])+fine, sep="\t\t")
	print('Average\t\t\t%s'%str(int(sum(values := rt['values'])/max(1,len(values)))))
	spt = [f'{setpiece[e]+":":<4} {players_db[i]["name"]}' for e,i in enumerate(ttmng.get("set_piece",[]) if not ttmng.get("set_piece",None) is None else _find_set_piece(t))]  if len(t['squad']) >= 11 else []
	if len(t['squad']) >= 11:
		spt = [spt[x] for x in [0,4,1,5,2,6,3,7]]+['']+[spt[8]]
		spt = [f'{spt[a]:<23}{spt[a+1]:<23}' for a in range(0,9,2)]
	print('Set piece takers',"\n                \t".join(spt),sep='\t')
	print('%s'%('─'*80))
	lineup = ''
	if 'd' in n_tactics[0]: n_tactics = ['1',str(int(n_tactics[0].replace('d',''))-1),n_tactics[1],n_tactics[2]]
	reparti = list(numpy.cumsum([int(r.replace('d','')) for r in n_tactics]))
	for lpl, p in enumerate(current):
		p = list(p)
		lineup += f'{p[5]:>6} {p[0]:<40.39} {p[1]:>3} {p[4] if t["league_id"] < 11  or t["league"] == "Non-League" else p[8] :<20} {p[2]}'
		lineup += '\n{:>79}\n'.format('─'*77) if lpl == 0 or lpl in reparti[:-1] else '\n'
	print('Squad\n',lineup[:-1],'{:^80}'.format('━'*72),sep='\n')
	bench = sorted([_ for _ in rt['pl_list'] if _ not in current], key = lambda x: x[6])
	subs = ''
	for lpl, p in enumerate(bench):
		p = list(p)
		subs += f'{p[5]:>6} {p[0]:<40.39} {p[1]:>3} {p[4] if t["league_id"] < 11  or t["league"] == "Non-League" else p[8] :<20} {p[2]}\n'
	print(subs)
	lineup = lineup[:-2]
	sq_lines = textwrap.wrap(lineup, 64)
	if len(dpls:=rt['duplicate roles']) or rt['rec'] > 0:
		print('%s'%('─'*81))
		if len(dpls) > 0:
			print('Duplicate Roles', ', '.join(dpls), sep="\t\t")
		if rt['rec'] :
			print('Recommended Tactics', rt['rec_tactics'], sep="\t")
			sq_lines = textwrap.wrap(rt['lineup'], 64)
			print('Recommended Lineup', sq_lines[0], sep="\t")
			print('\t\t\t','\n\t\t\t'.join(sq_lines[1:]))
			print('Roles to Improve for')
			print('  Current Tactics', rt['to improve'], sep="\t")
			if len(rt['problems']) > 0:
				print('Problems with')
				print('  Current Roster:', f"Missing positions: {', '.join(rt['problems'])}", sep="\t")
	print('%s'%('━'*81))
	print()
	if not refresh:
		team_data_query = ''
		standard_query = f"[e]dit team {t['names'][-1]} / show [k]its / [s]how player info {'/ reset team [m]anagement ' if ttmng else ''}/ [n]ext team / [c]ancel" 

		while True:
			print('\033[J\033[1A\033[41;37m\n',standard_query,"\033[0m", sep="",end = "\r")
			k = chr(getter())
			if k == 'e':
				print('\033[2K\033[1A')
				edit_team(teams[idx])
				if _display_team(params, refresh=True) == 'cancelled': return 'cancelled'
			elif k == 'm' and ttmng:
				del ttmng[t['id']]
				write_tmmng()
				if _display_team(params, refresh=True) == 'cancelled': return 'cancelled'
			elif k == 'k':
				def on_closing(event):
					if event.widget == kitWindow:
						if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				kitWindow = tk.Tk()
				kitWindow.geometry('+0+0')
				kitWindow.title(f'{t["names"][-1]}: home/away jerseys')
				kitWindow.bind("<Destroy>", on_closing)
				kitWindow.attributes("-topmost", True)
				homeKit = showJersey(teams[idx]['first shirt'],'front',teams[idx]['first shorts'],teams[idx]['first socks'],teams[idx]['first shirt - colour 1'],teams[idx]['first shirt - colour 2'],teams[idx]['first shirt - colour 3'],teams[idx]['first shorts - colour 1'],teams[idx]['first shorts - colour 2'],teams[idx]['first socks - colour 1'],teams[idx]['first socks - colour 2'])
				awayKit = showJersey(teams[idx]['second shirt'],'front',teams[idx]['second shorts'],teams[idx]['second socks'],teams[idx]['second shirt - colour 1'],teams[idx]['second shirt - colour 2'],teams[idx]['second shirt - colour 3'],teams[idx]['second shorts - colour 1'],teams[idx]['second shorts - colour 2'],teams[idx]['second socks - colour 1'],teams[idx]['second socks - colour 2'])
				hkimg = ImageTk.PhotoImage(homeKit)
				akimg = ImageTk.PhotoImage(awayKit)
				homeKitDisplay = Label(kitWindow,image = hkimg)
				homeKitDisplay.pack(side = "left", fill = "none", expand = "yes")
				awayKitDisplay = Label(kitWindow,image = akimg)
				awayKitDisplay.pack(side = "right", fill = "none", expand = "yes")
				kitWindow.mainloop()
			elif k == 's':
				print('\033[2K\033[2A')
				global table
				table = False
				team_data_query = '[r]eturn to team info / [s]how other player info / [c]ancel'
				standard_query = team_data_query
				plnames = [_[0] for _ in sorted(rt['pl_list'], key=lambda w:w[0])]
				plindexes = [_[-2] for _ in sorted(rt['pl_list'], key=lambda w:w[0])] + ['cancel']
				plindex = plindexes[int(inputPlus('\nSelect Player:\n  $OPTIONLIST_l$$CANCEL$', plnames, c=True, sep='\n  ')[0])]
				if plindex == 'cancel':
					team_data_query = 'return'
					break
				os.system(clear_screen)
				for _ in search_players(plindex, 'index_fcdb')['files'][plindex]: exec(_)
			elif k == 'n':
				print('\033[2A')
				print('\033[J', end="")
				break
			elif k =='c':
				return 'cancelled'
			elif k == 'r':
				team_data_query = 'return'
				break
		if team_data_query == 'return':
			if _display_team(params) == 'cancelled': return 'cancelled'

def recommended_tactics(squad, **kwargs):
	p = {}
	for pos,pl in enumerate(players):
		p.setdefault(pl['id'],pos)
	values = []
	pl_list = []
	takers = {}
	takers_ids = {}
	for px in squad:
		if players[p[px]]['role'] != 'GK':
			takers.setdefault(players[p[px]]['shot power'], []).append(players[p[px]]['name'])
			takers_ids.setdefault(players[p[px]]['shot power'],[]).append(players[p[px]]['id'])
		px_role = _fgRoles(players[p[px]]['role'],players[p[px]]['starting'])		
		pl_list.append((
			players[p[px]]['name'],
			px_role,av:=players[p[px]]['average'],
			players[p[px]][f'starting'],
			players[p[px]]['country'],
			players[p[px]][f'jersey'],
			players[p[px]]['id'],
			players[p[px]]['index_fcdb'],
			players[p[px]]['team']))
		values.append(av)
	current = sorted(sorted(pl_list, key=lambda y: y[3], reverse=True)[:11], key=lambda w: dict(GK=0,RB=1,RCB=2,SW=0.5,CB=3,LCB=4,LB=5,RM=6,RCM=7,CM=8,LCM=9,LM=10,RF=11,CF=12,LF=13)[w[1]]) 
	pool=sorted(pl_list, key = lambda x: x[2], reverse = True)
	role_order = dict(GK=0,RB=1,RCB=2,SW=0.5,CB=3,LCB=4,LB=5,RM=6,RCM=7,CM=8,LCM=9,LM=10,RF=11,RCF=11.5, CF=12,LCF=12.5,LF=13)
	pl_list = ['%s (%s, %s)'%(y,z,q) for (y,z,q,k,w,j,h,u,x) in pool]
	possible_lineups = {
			'5d-4-1': [['GK','SW','RB','RCB','LCB','LB','RM','RCM','LCM','LM','CF']],
			'5d-3-2':[['GK','SW','RB','RCB','LCB','LB','RCM','CM','LCM','CF','CF']],
			'4d-5-1':[['GK','SW','RCB','CB','LCB','RM','RCM','CM','LCM','LM','CF']],
			'4-4-2':[['GK','RB','RCB','LCB','LB','RM','RCM','LCM','LM','CF','CF']],
			'4-3-3':[['GK','RB','RCB','LCB','LB','RCM','CM','LCM','RF','CF','LF']],
			'4d-4-2':[['GK','SW','RB','CB','LB','RM','RCM','LCM','LM','CF','CF']],
			'4d-3-3':[['GK','SW','RB','CB','LB','RCM','CM','LCM','RF','CF','LF']],
			'3-4-3':[['GK','RCB','CB','LCB','RM','RCM','LCM','LM','RF','CF','LF']],
			'3-5-2':[['GK','RCB','CB','LCB','RM','RCM','CM','LCM','LM','CF','CF']]
	}
	missing_positions = {}
	for lineup,roles in possible_lineups.items():
		starting = []
		score = 0
		tmpPool = copy.deepcopy(pool)
		for _role in roles[0]:
			selected=[_ for _ in tmpPool if _[1] == _role or ('F' in _role and 'F' in _[1]) or ('CM' in _role and 'CM' in _[1]) or ('CB' in _role and 'CB' in _[1]) or (_role == 'SW' and _[1]=='CB')]
			if len(selected) == 0:
				starting = []
				missing_positions.setdefault(lineup,[]).append('/'.join(_role) if type(_role) is tuple else str(_role))
				score = 0
				break
			selected = selected[0]
			starting.append(selected)
			score += selected[2]
			tmpPool.remove(selected)
		possible_lineups[lineup].append(starting)
		possible_lineups[lineup].append(score)
	problems = []
	cTacProblems = ''
	best_lineup = sorted([[l,s[1],s[2]] for l, s in possible_lineups.items()], key=lambda sc: sc[2], reverse=True)[0]
	rec = set(best_lineup[1])!=set(current)
	if ntt:=kwargs.get('tactics',None):
		rec = True
		(current,power) = (possible_lineups[ntt][1],possible_lineups[ntt][2])
		if power == 0: cTacProblems = f"{', '.join(missing_positions[ntt])} missing"
	if best_lineup[2] == 0:
			rec = True
			lroles = {
				'GK':len([pl for pl in pool if pl[1] == 'GK']),
				'LB':len([pl for pl in pool if pl[1] == 'LB']),
				'CB':len([pl for pl in pool if 'CB' in pl[1]]),
				'RB':len([pl for pl in pool if pl[1] == 'RB']),
				'RM':len([pl for pl in pool if pl[1] == 'RM']),
				'LM':len([pl for pl in pool if pl[1] == 'LM']),
				'CM':len([pl for pl in pool if 'CM' in pl[1]]),
				'F':len([pl for pl in pool if 'F' in pl[1]])
			}
			for n in ['GK','CB','CM','F']:
				if lroles[n] == 0: problems.append(n)
			for n in ['LB','RB']:
				if lroles[n] == 0 and any([lroles[m] == 0 for m in ['RM','LM']]): problems.append(n)
			for n in ['LM','RM']:
				if lroles[n] == 0 and any([lroles[m] == 0 for m in ['RB','LB']]): problems.append(n)
	best_reparti = [1] + [int(_.replace('d','')) for _ in best_lineup[0].split('-')]
	lineup = []
	c = 0
	for s in best_reparti:
		lineup.append(', '.join([_[0] for _ in best_lineup[1][c:c+s]]))
		c += s
	lineup = '; '.join(lineup) if all([len(b)>0 for b in lineup]) > 0 else 'n/a'
	to_improve = ', '.join([x[1] for x in set(current).difference(set(best_lineup[1]))])
	if len(to_improve) == 0: to_improve = cTacProblems
	nndplroles = dict(LB=0,RB=0,LM=0,RM=0)
	dpls = [y for y in list(nndplroles.keys()) if [p[1] for p in current].count(y) > 1]
	if len(squad) > 0:
		takers = takers[sorted(takers)[-1]]
		takers_ids = takers_ids[sorted(takers_ids)[-1]]
	return {'rec_tactics': best_lineup[0] if best_lineup[2] > 0 else 'n/a', 'values': values, 'pl_list': pool, 'lineup': lineup, 'lineup_ids': [o[-3] for o in best_lineup[1]], 'starting': current, 'rec':rec, 'to improve':to_improve, 'duplicate roles': dpls,'problems':problems,'shot takers':takers,'takers_ids':takers_ids}

fields_tmmng = {
	'formation':lambda x:x['tactics'].split('-'),
	'strategy':lambda x:strategia.index(x['strategy']),
	'lineup':lambda x:[p[6] for p in recommended_tactics(x['squad'])['starting']],
	'set_piece':lambda x:_find_set_piece(x),
	'positions':lambda x:[(8,8)]*11,
	'aggression':lambda x:[int((players_db[p[6]]['aggression']-39)/4) for p in recommended_tactics(x['squad'])['starting']],
	'attack':lambda x:[int((players_db[p[6]]['attack bias']-39)/4) for p in recommended_tactics(x['squad'])['starting']]
	} 

def _find_set_piece(team):
	if len(team['squad']) == 0: return []
	set_piece = []
	tactics = [int(r.replace('d','')) for r in team['tactics'].split('-')]
	if len(tactics) == 4: tactics = [tactics[0]+tactics[1],tactics[2],tactics[3]]
	current = [c[6] for c in recommended_tactics(team['squad'])['starting']]
	reparti = list(numpy.cumsum([0,1] + tactics))
	by_pos = []
	for e,c in enumerate(reparti[:-1]):
		by_pos.append(current[c:reparti[e+1]])
	set_piece.append(by_pos[2][-1])
	set_piece.append(by_pos[2][0])
	other = sorted([p for p in players if p['id'] in current], key=lambda w:w['shot power'])[-1]['id']
	set_piece += [other, other]
	set_piece += current[6:]
	return set_piece

def _refresh_tmmng(team,field,value):
	global tmmng_db
	t = tmmng_db.setdefault(team['id'],{})
	for f,corr in fields_tmmng.items():
		if f == field:
			t[f] = value
		else:
			t.setdefault(f,corr(team))
			
def _tmmng_roles(formation):
	sweeper = False
	reparti = ['1'] + formation
	if 'd' in reparti[1]:
		sweeper = True
		reparti.insert(1,'1')
	reparti = [int(v.replace('d','')) for v in reparti]
	if len(reparti) == 5: reparti[2] -= 1
	role_plantilla = []
	rroles = ['B','F','M']
	for e,r in enumerate(reparti):
		if e == 0: role_plantilla.append('GK')
		if e == 1 and sweeper: role_plantilla.append('SW')
		if e >= len(reparti)-3:
			if r == 1: role_plantilla.append(f'C{rroles[len(reparti)-3-e]}')
			if r == 2:
				role_plantilla.append(f'RC{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'LC{rroles[len(reparti)-3-e]}')
			if r == 3:
				role_plantilla.append(f'RC{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'C{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'LC{rroles[len(reparti)-3-e]}')
			if r == 4:
				role_plantilla.append(f'R{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'RC{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'LC{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'L{rroles[len(reparti)-3-e]}')
			if r == 5:
				role_plantilla.append(f'R{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'RC{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'C{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'LC{rroles[len(reparti)-3-e]}')
				role_plantilla.append(f'L{rroles[len(reparti)-3-e]}')
	return role_plantilla

def edit_team(modify, **args):
	global table, players
	vals_already = modify
	ttmng = tmmng_db.get(vals_already['id'],{})
	valori = open(f_valori, 'r+b')
	temp_file = b''
	mod_offset=int(modify['index_fcdb'])
	new_value = args.get('value', None)
	lineup ='\n\t║ [l]ineup                ║\n\t║ s[e]t piece taker       ║' #ND
	pos = '\n\t║ [pos]itions of players  ║' if ttmng != {} else ''
	call_players = '\n\t║ [c]all players          ║\n\t║ call [d]ual nationals   ║' if vals_already['nation'] > 0 else '' 
	buy_players = "\n\t║ [buy] player            ║" if len(vals_already['squad']) < 20 and vals_already['nation'] == 0 else '' 
	fill_team = "\n\t║ [fill] roster           ║" if len(vals_already['squad']) == 0 else '' 
	edit_players = '%s\n\t║ [sell] player           ║\n\t║ e[x]change players      ║\n\t║ [rel]ease player        ║\n\t║ [rec]ommend player      ║'%buy_players if vals_already['nation'] == 0 else '' #ND recommend
	valori.seek(0, 0)
	temp_file = valori.read(mod_offset)
	temp_bytes = [valori.read(1) for x in range(23)]

	what_to_edit = args.get('field', None)
	valid = True
	while True:
		if what_to_edit is None:
			what_to_edit = input(cmlst:="""
Parameter to edit:
	╔═════════════════════════╗
	║ [n]ames                 ║
	║ [b]ankroll              ║
	║ [s]tadium               ║
	║ [f]irst [k]it           ║
	║ [s]econd [k]it          ║
	║ strateg[y]              ║
	║ forma[t]ion             ║%s%s
	║ [p]layers               ║%s%s%s
	╚═════════════════════════╝
(hit return to go back): """%(lineup,pos,fill_team,edit_players,call_players))
			cmlst = re.sub('(.*?) +║\n\t║     └ ',r'\1\n\1',cmlst)
			cmlst = re.sub('\].*?\[','',cmlst)
			legit_commands = re.findall('\[([a-z]+)\]',cmlst)
			if what_to_edit not in legit_commands:
				what_to_edit = None
				valid = False
		if what_to_edit is None:
			return mod_offset
		if what_to_edit == 'l':
			roster = [(p['name'],p['role'],p['index_fcdb'],p['average'],p['id']) for p in players if (p['team_id'] == vals_already['id']) or (vals_already.get('nation','') in p['international_id'])]
			if ttmng:
				role_plantilla = _tmmng_roles(ttmng['formation'])
				lineup = []
				role_order = dict(GK=0,RB=1,RCB=2,SW=0.5,CB=3,LCB=4,LB=5,RM=6,RCM=7,CM=8,LCM=9,LM=10,RF=11,RCF=11.5, CF=12,LCF=12.5,LF=13)
				def b():
					try:
						lineup.append(roster.pop(roster.index((tp:=sorted(roster, key = lambda x: role_order[x[1]]))[int(input('   '+'\n   '.join(['[%s]: %s (%s, %s)'%(t+1,d[0],d[1],d[3]) for (t,d) in enumerate(tp)]) + '\n: '))-1]))[-1])
					except:
						print(f'No player input')
						if input('Try again? [yn] ') != 'y': return None
						else: b()
					else: return True
				for role in role_plantilla:
					print('\nSelect %s:'%role)
					if b() is None: return
				_refresh_tmmng(vals_already,'lineup',lineup)
				write_tmmng()
			else:
				reparti = vals_already['tactics']
				if reparti == '5d-4-1': reparti = ['GK','SW','RB',('CB','RCB'),('CB','LCB'),'LB','RM',('CM','RCM'),('CM','LCM'),'LM','F']
				if reparti == '5d-3-2': reparti = ['GK','SW','RB',('CB','RCB'),('CB','LCB'),'LB',('CM','RCM'),'CM',('CM','LCM'),'F','F']
				if reparti == '4d-5-1': reparti = ['GK','SW',('CB','RCB'),'CB',('CB','LCB'),'RM',('CM','RCM'),'CM',('CM','LCM'),'LM','F']
				if reparti == '4d-4-2': reparti = ['GK','SW','RB','CB','LB','RM',('CM','RCM'),('CM','LCM'),'LM','F','F']
				if reparti == '4d-3-3': reparti = ['GK','SW','RB','CB','LB',('CM','RCM'),'CM',('CM','LCM'),('F','RF'),('F','CF'),('F','LF')]
				if reparti == '4-4-2': reparti = ['GK','RB',('CB','RCB'),('CB','LCB'),'LB','RM',('CM','RCM'),('CM','LCM'),'LM','F','F']
				if reparti == '4-3-3': reparti = ['GK','RB',('CB','RCB'),('CB','LCB'),'LB',('CM','RCM'),'CM',('CM','LCM'),('F','RF'),('F','CF'),('F','LF')]
				if reparti == '3-4-3': reparti = ['GK',('CB','RCB'),'CB',('CB','LCB'),'RM',('CM','RCM'),('CM','LCM'),'LM',('F','RF'),('F','CF'),('F','LF')]
				if reparti == '3-5-2': reparti = ['GK',('CB','RCB'),'CB',('CB','LCB'),'RM',('CM','RCM'),'CM',('CM','LCM'),'LM','F','F']
				reparti = [(r, r) if isinstance(r,str) else r for r in reparti]
				lineup = {}
				def b(r):
					try:
						lineup.setdefault(roster.pop(roster.index((tp:=sorted([x for x in roster if x[1].find(r[0]) > -1], key = lambda x: x[3], reverse=True))[int(input('   '+'\n   '.join(['[%s]: %s (%s)'%(t+1,d[0],d[3]) for (t,d) in enumerate(tp)]) + '\n: '))-1]))[2], r[1])
					except:
						print(f'No player input, or not enough {r[0]} for the selected tactics')
						if input('Try again? [yn] ') == 'n': return None
						else: b(r)
					else: return True
				for r in reparti:
					print('\nSelect %s:'%r[1])
					if b(r) is None: break
				if len(lineup) == 11:
					for x in roster:
						edit_player(x[2], field='st', value=None)
					for x,r in lineup.items():
						edit_player(x, field='st', value=180, role=r if isinstance(r,str) else r[-1])
					load_database()
		elif what_to_edit == 'pos':
			positions = list(zip(_tmmng_roles(ttmng['formation']),ttmng['positions']))
			pitch_pos = {
				'GK': (3,24),
				'SW': (9,24),
				'RB': (15,39),
				'RCB': (12,32),
				'CB': (15,24),
				'LCB': (12,16),
				'LB': (15,9),
				'RM': (28,39) if 'd' in ttmng['formation'][2] else (26,39),
				'RCM': (21,32) if 'd' in ttmng['formation'][2] else (23,32),
				'CM': (28,24) if 'd' in ttmng['formation'][2] else (26,24),
				'LCM': (21,16) if 'd' in ttmng['formation'][2] else (23,16),
				'LM': (28,9) if 'd' in ttmng['formation'][2] else (26, 9),
				'RCF': (30,24) if ttmng['formation'][2] == '2d' else (33,32),
				'CF': (30,24) if 'd' in ttmng['formation'][2] else (35,24),
				'LCF': (35,24) if ttmng['formation'][2] == '2d' else (33,16)
			}
			current = positions[1]
			while True:
				pitch = [[]]
				pitch.append(['\033[48;5;15m   ']*55+['\033[0m'])
				for i in range(47):
					pitch.append(['\033[48;5;15m   ']+['\033[48;5;22m   ']*26+[' \033[48;5;15m \033[48;5;22m ']+['\033[48;5;22m   ']*26+['\033[48;5;15m   ']+['\033[0m'])
				pitch.append(['\033[48;5;15m   ']*55+['\033[0m'])
				for pos,alter in positions:
					coordinates = pitch_pos[pos]
					latitude = coordinates[1] + alter[1] - 8
					longitude = coordinates[0] + alter[0] - 8
					pitch[latitude][longitude] = '\033[48;5;22m'+pos.ljust(3)
				for r in pitch:
					print('\033[97m\033[1m',''.join(r),sep=' ')
				print('\033[42;44m\n',f'Move the {current[0]} using the arrow keys; [c]hange player, [r]eset, [q]uit ','\033[0m', sep='', end='\r')
				k = find_key()
				if k == 'q': break
				if k == 'r': positions = [[p[0],[8,8]] for p in positions]
				if k == 'c':
						while True:
							print(f'\033[2KSelect player {", ".join([p[0] for p in positions])} or [c]ancel', end='')
							current = input(': ').upper()
							if current == 'C':
								current=positions[1]
								print('\033[1A\033[2K\033[1A')
								break
							if current in [p[0] for p in positions]:
								current = [p for p in positions if p[0] == current][0]
								current = positions[positions.index(current)]
								print('\033[1A\033[2K\033[1A')
								break
							else: print('\r\033[2A\033[2K')
				if k in 'left':
					current[1][0] = max(current[1][0]-1,0)
				if k == 'right':
					current[1][0] = min(current[1][0]+1,15)
				if k == 'up':
					current[1][1] = max(current[1][1]-1,0)
				if k == 'down':
					current[1][1] = min(current[1][1]+1,15)
				print('\033[52A')
			new_positions = [p[1] for p in positions]
			if input('\033[2KSave changes? ') == 'y':
				_refresh_tmmng(vals_already,'positions',new_positions)
				write_tmmng()
		elif what_to_edit in ['buy', 'sell', 'x', 'rel','fill']: 
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
				load_database()
				return True
			if what_to_edit == 'fill':
				free_agents = [p for p in players if p['team'] == '---']
				quotas = {'GK':[2,0],'CB':[3,0],'LB':[2,0],'RB':[2,0],'RM':[2,0],'CM':[3,0],'LM':[2,0],'CF':[4,0]}
				squad = []
				while True:
					random.shuffle(free_agents)
					pl = free_agents.pop()
					if quotas.get(pl['role'],[0,0])[1] < quotas.get(pl['role'],[0,0])[0]:
						squad.append(pl['id'])
					if len(squad)==20: break
				edit_squad(squad,vals_already['index_fcdb'])
			elif what_to_edit == 'buy':
				source_team = None
				a = input('\nSearch source team / Hit return to browse: ')
				if len(a) > 0:
					hits = 0
					for idx,t in enumerate(teams):
						field = t['names'][-1]
						if not case_sensitive:
							field = str(field).upper()
							a = str(a).upper()
						if re.search(a, field) and t['league_id'] < 11:
							hits += 1
							confirm = input('Selected team: %s. Confirm? [ync] '%t['names'][-1])
							if confirm == 'c': return
							elif confirm == 'y':
								source_team = t
								break
							return
					if hits == 0:
						print('Not found')
						return
				else:
					l = int(inputPlus('\nSelect league of source team:\n  $OPTIONLIST_l$$CANCEL$',	sorted_leagues_names+['free agent'], c=True, sep='\n  ')[0])
					if l < 11:
						l = sorted_leagues[l]
						tms = [(team['names'][-1], e) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league_id'] == l]
						t = int(inputPlus('\nSelect source team:\n  $OPTIONLIST_l$$CANCEL$', [t[0] for t in tms], idx='0', c=True, sep='\n  ')[0])
						if t < len(tms):
							t = tms[t][1]
							source_team = sorted(teams, key=lambda x: x['names'][-1])[t]
						else: return
					elif l == 11:
						source_team = {'squad':[p['id'] for p in players if p['team'] == '---'], 'index_fcdb':None,'names':['free agents']}
					else: return
				if source_team:
					source_squad = source_team['squad']
					source_roster = sorted([p for p in players if p['id'] in source_squad], key=lambda w:w['name'])
					menu_entries = [f"{_['name']} ({_['role']}, {_['average']}, {_['country']})" for _ in source_roster] 
					destination_starting = [p for p in players if p['id'] in vals_already['squad'] if p['starting'] == 180]
					player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',menu_entries, c=True, sep='\n  ')[0])
					if player_to_transfer < len(source_roster):
						vals_already['squad'].append(source_roster[player_to_transfer]['id'])
						if source_roster[player_to_transfer]['starting'] == 180 and len(destination_starting) > 10:
							edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=None)
						elif source_roster[player_to_transfer]['starting'] != 180 and len(destination_starting) < 11:
							edit_player(source_roster[player_to_transfer]['index_fcdb'], field='st', value=180)
						source_squad.remove(source_roster[player_to_transfer]['id'])
						if edit_squad(vals_already['squad'],vals_already['index_fcdb']) and edit_squad(source_squad,source_team['index_fcdb']): print('\n%s succesfully transferred from %s to %s'%(source_roster[player_to_transfer]['name'], source_team['names'][-1], vals_already['names'][-1]))
					else: return 
			elif what_to_edit == 'sell':
				destination_team = None
				source_roster = sorted([p for p in players if p['id'] in vals_already['squad']], key=lambda w:w['name'])
				menu_entries = [f"{_['name']} ({_['role']}, {_['average']}, {_['country']})" for _ in source_roster]
				player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',menu_entries, c=True, sep='\n  ')[0])
				if player_to_transfer < len(source_roster):
					a = input('\nSearch destination team / Hit return to browse: ')
					if len(a) > 0:
						hits = 0
						for idx,t in enumerate(teams):
							field = t['names'][-1]
							if not case_sensitive:
								field = str(field).upper()
								a = str(a).upper()
							if re.search(a, field) and t['league_id'] < 11:
								hits += 1
								confirm = input('Selected team: %s. Confirm? [ync] '%t['names'][-1])
								if confirm == 'c': return
								elif confirm == 'y':
									destination_team = t
									break
								return
						if hits == 0:
							print('Not found')
							return
					else:
						l = int(inputPlus('\nSelect league of destination team:\n  $OPTIONLIST_l$$CANCEL$',	sorted_leagues_names, c=True, sep='\n  ')[0])
						if l < 11:
							l = sorted_leagues[l]
							tms = [(team['names'][-1], e) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league_id'] == l]
							t = int(inputPlus('\nSelect destination team:\n  $OPTIONLIST_l$$CANCEL$', [t[0] for t in tms], idx='0', c=True, sep='\n  ')[0])
							if t < len(tms):
								t = tms[t][1]
								destination_team = sorted(teams, key=lambda x: x['names'][-1])[t]
							else: return
						else: return
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
						else:
							input('Team full. Hit return to continue.')
							return
			elif what_to_edit == 'x':
				destination_team = None
				source_roster = sorted([p for p in players if p['id'] in vals_already['squad']], key=lambda w:w['name'])
				menu_entries = [f"{_['name']} ({_['role']}, {_['average']}, {_['country']})" for _ in source_roster]
				player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',menu_entries, c=True, sep='\n  ')[0])
				if player_to_transfer < len(source_roster):
					a = input('\nSearch destination team / Hit return to browse: ')
					if len(a) > 0:
						hits = 0
						for idx,t in enumerate(teams):
							field = t['names'][-1]
							if not case_sensitive:
								field = str(field).upper()
								a = str(a).upper()
							if re.search(a, field) and t['league_id'] < 11:
								hits += 1
								confirm = input('Selected team: %s. Confirm? [ync] '%t['names'][-1])
								if confirm == 'c': return
								elif confirm == 'y':
									destination_team = t
									break
								return
						if hits == 0: print('Not found')
					else:
						l = int(inputPlus('\nSelect league of destination team:\n  $OPTIONLIST_l$$CANCEL$',	sorted_leagues_names, c=True, sep='\n  ')[0])
						if l < 11:
							l = sorted_leagues[l]
							tms = [(team['names'][-1], e) for (e,team) in enumerate(sorted(teams, key=lambda x: x['names'][-1])) if team['league_id'] == l]
							t = int(inputPlus('\nSelect destination team:\n  $OPTIONLIST_l$$CANCEL$', [t[0] for t in tms], idx='0', c=True, sep='\n  ')[0])
							if t < len(tms):
								t = tms[t][1]
								destination_team = sorted(teams, key=lambda x: x['names'][-1])[t]
							else: return
					if destination_team:
						destination_squad = destination_team['squad']
						destination_roster = sorted([p for p in players if p['id'] in destination_squad], key=lambda w:w['name'])
						menu_entries = [f"{_['name']} ({_['role']}, {_['average']}, {_['country']})" for _ in destination_roster] 
						source_starting = [p for p in source_roster if p['starting'] == 180]
						destination_starting = [p for p in destination_roster if p['starting'] == 180]
						player_to_transfer_2 = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',menu_entries, c=True, sep='\n  ')[0])
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
						else: return
			elif what_to_edit == 'rel':
				source_roster = sorted([p for p in players if p['id'] in vals_already['squad']], key=lambda w:w['name'])
				menu_entries = [f"{_['name']} ({_['role']}, {_['average']}, {_['country']})" for _ in source_roster]
				player_to_transfer = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',menu_entries, c=True, sep='\n  ')[0])
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
			vals_already['names'] = [new_name.decode('iso-8859-1') for new_name in new_names]
		elif what_to_edit == 'b':
			if new_value is None: new_value = input('\n'+f'Enter new bankroll{"for" if args.get("field",None) else ""} {(vals_already["names"][-1]+" ") if args.get("field",None) else ""}(hit return to cancel): ')
			if len(new_value) > 0:
				if not new_value.isdigit():
					new_value = None
					continue
				else: new_value = int(new_value)
				new_value = min(131071,unbank(new_value))
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
		elif what_to_edit in ['fs','ss','fk','sk']:
			global alreadyEdited
			try:
				alreadyEdited
			except:
				alreadyEdited = {}
			def _doEdits(new_value, cols, kit, vals_already,*reload):
				valori.seek(0,0)
				temp_file = valori.read(vals_already['index_fcdb'])
				temp_bytes = [valori.read(1) for x in range(24)]
				if new_value < len(jersey_types):
					temp_bytes[5+kit[0]] = bytes([(int.from_bytes(temp_bytes[5+kit[0]], 'big') & 3)+ (new_value << 2)])

					#jec
					temp_bytes[4+kit[0]] = bytes([((cols[1] & 7) << 5) + cols[0]])
					temp_bytes[5+kit[0]] = bytes([(int.from_bytes(temp_bytes[5+kit[0]], 'big') & 252) + ((cols[1] & 24) >> 3)])
					temp_bytes[6+kit[0]] = bytes([(int.from_bytes(temp_bytes[6+kit[0]], 'big') & 224) + cols[2]])
					#shc
					temp_bytes[6+kit[0]] = bytes([(int.from_bytes(temp_bytes[6+kit[0]], 'big') & 31) + ((cols[3] & 7) << 5)])
					temp_bytes[7+kit[0]] = bytes([(int.from_bytes(temp_bytes[7+kit[0]], 'big') & 63)+ (shorts.index(vals_already[f'{kit[1]} shorts']) << 6)])
					temp_bytes[7+kit[0]] = bytes([(int.from_bytes(temp_bytes[7+kit[0]], 'big') & 252) + ((cols[3] & 24) >> 3)])
					temp_bytes[8+kit[0]] = bytes([(int.from_bytes(temp_bytes[8+kit[0]], 'big') & 224) + cols[4]])
					#soc
					temp_bytes[8+kit[0]] = bytes([(int.from_bytes(temp_bytes[8+kit[0]], 'big') & 31) + ((cols[5] & 7) << 5)])
					temp_bytes[9+kit[0]] = bytes([(int.from_bytes(temp_bytes[9+kit[0]], 'big') & 252) + ((cols[5] & 24) >> 3)])
					temp_bytes[10+kit[0]] = bytes([(int.from_bytes(temp_bytes[10+kit[0]], 'big') & 224) + cols[6]])
					temp_bytes[11+kit[0]] = bytes([(int.from_bytes(temp_bytes[7+kit[0]], 'big') & (63 + kit[0]*18))+ (shorts.index(vals_already[f'{kit[1]} socks']) << (6-int(kit[0]/4)))])
					temp_file+=b''.join(temp_bytes)
					temp_file+=valori.read()
					save(f_valori, temp_file)
					if not reload:
						load_database(load=len(args.get('field', '')))
					else:
						load_database()
			if (v:=alreadyEdited.get(vals_already['id'],False)): vals_already = v
			kit = [0,'first'] if what_to_edit[0] == 'f' else [8,'second']
			cols = [
				vals_already[f'{kit[1]} shirt - colour 1'],
				vals_already[f'{kit[1]} shirt - colour 2'],
				vals_already[f'{kit[1]} shirt - colour 3'],
				vals_already[f'{kit[1]} shorts - colour 1'],
				vals_already[f'{kit[1]} shorts - colour 2'],
				vals_already[f'{kit[1]} socks - colour 1'],
				vals_already[f'{kit[1]} socks - colour 2']
			]

			if os.path.isdir(os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS')):
				jerseys = [_ for _ in os.listdir(os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS')) if re.match('jers\d\d.fsh',_.lower())]
				root = tk.Tk() if not (parentW:=args.get('asChild', False)) else tk.Toplevel(parentW) #NEW
				root.title(f'Edit {kit[1]} kit of {vals_already["names"][-1]}')
				root.geometry("800x600+0+0")
				#Code from Codemy
				# Create A Main Frame
				main_frame = tk.Frame(root, bg="white")
				main_frame.pack(fill="both", expand=1)

				top_frame = Frame(main_frame)
				top_frame.pack(side="top",fill="both")

				# Create A Canvas
				my_canvas = tk.Canvas(main_frame)
				my_canvas.pack(side="left", fill="both", expand=1)

				# Add A Scrollbar To The Canvas
				my_scrollbar = Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
				my_scrollbar.pack(side="right", fill="y")

				# Configure The Canvas
				my_canvas.configure(yscrollcommand=my_scrollbar.set)
				my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

				# Create ANOTHER Frame INSIDE the Canvas
				second_frame = tk.Frame(my_canvas, bg="white")

				# Add that New frame To a Window In The Canvas
				my_canvas.create_window((0,0), window=second_frame, anchor="nw")

				def chCol(x,y):
					nonlocal cols
					try:
						cIndex=y
						if cIndex != cols[x]:
							cols[x] = cIndex
							kcMenu[x][0].config(text=colours[y].ljust(12))
							for e,button in enumerate(buttons):
								images[e] = ImageTk.PhotoImage(image = showJersey(e,'front',vals_already[f'{kit[1]} shorts'],vals_already[f'{kit[1]} socks'],*cols))
								button.config(image = images[e])
					except:
						pass
				def chShortsSocks(x,y):
					nonlocal vals_already
					oiMenu[y][0].config(text=eval(ois[y])[x])
					for e,button in enumerate(buttons):
						if y == 0:
							images[e] = ImageTk.PhotoImage(image = showJersey(e,'front',shorts[x],vals_already[f'{kit[1]} socks'],*cols))
							vals_already[f'{kit[1]} shorts'] = shorts[x]
						if  y == 1:
							images[e] = ImageTk.PhotoImage(image = showJersey(e,'front',vals_already[f'{kit[1]} shorts'],socks[x],*cols))
							vals_already[f'{kit[1]} socks'] = socks[x]
						button.config(image = images[e])

				kit_colours = ["Jersey: 1","Jersey: 2","Jersey: 3","Shorts: 1","Shorts: 2","Socks: 1","Socks: 2"]
				kcMenu = []
				for kcn, kc in enumerate(kit_colours):
					kcMenu.append([])
					kcMenu[-1].append(tk.Menubutton(top_frame, text=colours[cols[kcn]].ljust(12)))
					kcMenu[-1].append(tk.Menu(kcMenu[-1][0]))
					for cid, color in enumerate(colours):
						kcMenu[-1][1].add_command(label = color, compound="left", command = lambda x=cid,y=kcn: chCol(y,x), image = ImageTk.PhotoImage(image = color_selector[cid]))
					kcMenu[-1][0]["menu"]=kcMenu[-1][1]
					kcMenu[-1][0].grid(row=1,column=kcn,padx=5,pady=3)
					kcMenu[-1].append(Label(top_frame,text = kc))
					kcMenu[-1][2].grid(row=0,column=kcn, pady=3)
				oi_types = ['plain', 'trim',' stripes']
				ois = ['shorts','socks']
				oiMenu = []
				for ioi, oi in enumerate(ois):
					menuShortsB = tk.Menubutton(top_frame, text=vals_already[f'{kit[1]} {oi}'].ljust(12))
					menuShorts = tk.Menu(menuShortsB)
					for it,t in enumerate(oi_types):
						menuShorts.add_command(label = t, command = lambda x = it, y=ioi: chShortsSocks(x, y))
					menuShortsB["menu"] = menuShorts
					menuShortsB.grid(row=3,column = 3+2*ioi, padx=5,pady=3)
					menuShortsL = Label(top_frame,text = f'{oi.title()} Type')
					menuShortsL.grid(row=2,column = 3+2*ioi, pady=3)
					oiMenu.append([menuShortsB,menuShorts,menuShortsL])
				images = []
				global c
				c = None
				def on_closing(event, pWbuttons):
					nonlocal new_value, cols, kit, temp_file, temp_bytes, parentW, vals_already
					global alreadyEdited
					global c
					if event.widget == root:
						if new_value is None: new_value = c or vals_already[f'{kit[1]} shirt']
						if parentW:
							pWbuttons.config(image = (nImg:=ImageTk.PhotoImage(showJersey(new_value,'front',vals_already[f'{kit[1]} shorts'],vals_already[f'{kit[1]} socks'],*cols))))
							pWbuttons.image = nImg
							vals_already[f'{kit[1]} shirt'] = new_value
							vals_already[f'{kit[1]} shirt - colour 1'] = cols[0]
							vals_already[f'{kit[1]} shirt - colour 2'] = cols[1]
							vals_already[f'{kit[1]} shirt - colour 3'] = cols[2]
							vals_already[f'{kit[1]} shorts - colour 1'] = cols[3]
							vals_already[f'{kit[1]} shorts - colour 2'] = cols[4]
							vals_already[f'{kit[1]} socks - colour 1'] = cols[5]
							vals_already[f'{kit[1]} socks - colour 2'] = cols[6]
							alreadyEdited[vals_already['id']] = vals_already

						else: _doEdits(new_value,cols, kit, vals_already)

						if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				root.bind("<Destroy>", lambda e,pWbuttons=args.get('buttons',False): on_closing(e,pWbuttons))
				def callback(n):
					global c
					c = int(n['text'])
					root.destroy()
					if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
				buttons = []
				for e,j in enumerate(jerseys):
					images.append(ImageTk.PhotoImage(image = showJersey(e,'front',vals_already[f'{kit[1]} shorts'],vals_already[f'{kit[1]} socks'],*cols)))
					btn = tk.Button(second_frame, text = e, image = images[-1])
					buttons.append(btn)
					if e == vals_already[f'{kit[1]} shirt']:
						btn['highlightthickness']=4
						btn['highlightcolor']="#37d3ff"
						btn['highlightbackground']="#37d3ff"
						btn['borderwidth']=4
					btn['command'] = lambda b=btn: callback(b)
					btn.grid(row=int(e/3)+3, column=e%3, padx=10, pady=10)
				root.attributes("-topmost", True)
				root.mainloop()
				if parentW: return functools.partial(_doEdits,new_value, cols, kit, vals_already,True)
			else:
				select_jersey(vals_already[kit[1]+' shirt - colour 1'],vals_already[kit[1]+' shirt - colour 2'],vals_already[kit[1]+' shirt - colour 3'])
				addtypes = '' if len(jersey_types) == 32 else '\n\t--- custom jerseys ---\n\t%s'%'\n\t'.join([
					'[%s] %s'%(e,f) for e,f in enumerate(jersey_types) if e > 32
				])
				if new_value is None: new_value = int(inputPlus('\nEnter shirt type %s$CANCEL$'%addtypes,jersey_types,c=True,sep="\n\t")[0])
				_doEdits(new_value, cols, kit, vals_already)
		elif what_to_edit == 'y':
			if new_value is None: new_value = int(inputPlus('\nEnter strategy\n\t$OPTIONLIST_l$$CANCEL$',strategia,c=True,sep='\n\t')[0])
			if new_value < len(strategia):
				if ttmng:
					_refresh_tmmng(vals_already,'strategy',2 * new_value)
					write_tmmng()
				temp_bytes[17] = bytes([(int.from_bytes(temp_bytes[17], 'big') & 31) + (new_value << 5)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 't':
			if new_value is None: new_value = int(inputPlus('\nEnter tactics\n\t$OPTIONLIST_l$$CANCEL$',tactics+['Custom'],c=True,sep='\n\t')[0])
			if new_value == len(tactics) or ttmng or type(new_value) == str:
				block = False
				if type(new_value) == int:
					if new_value < len(tactics): new_value = tactics[new_value]
					else:
						while True:
							new_value = input('Enter formation (e.g. 4d-4-2; d for diamond), [c] to cancel): ')
							if len(new_value.split('-')) == 3: break
							if new_value == 'c': 
								block = True
								break
				if not block:
					new_value = new_value.split('-')
					diamonds = [''+('d' in v)*'d' for v in new_value]
					new_value = [min(int(v.replace('d','')),5) for v in new_value]
					e = 0
					while True:
						if e == 3: e = 0
						if sum(new_value) == 10: break
						if sum(new_value) > 10:
							new_value[e] = max(new_value[e]-1,0)
						if sum(new_value) < 10:
							new_value[e] = min(new_value[e]+1,5)
						e+=1
					formation = [f'{v}{diamonds[e]}' for e,v in enumerate(new_value)]
					_refresh_tmmng(vals_already,'formation',formation)
					write_tmmng()
			elif new_value < len(tactics):
				temp_bytes[21] = bytes([(int.from_bytes(temp_bytes[21], 'big') & 3) + (new_value << 2)])
				temp_file+=b''.join(temp_bytes)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'r':
			if new_value is None: new_value = int(inputPlus('\nEnter roster size\n\t$OPTIONLIST_l$$CANCEL$',[14,16,18,20],c=True,sep='\n\t')[0])
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
			roster = search_players(vals_already['id'], 'team_id', strict=True)['results'] if vals_already['league_id'] <= 10  else search_players(vals_already['nation'], 'international_id', strict = True)['results']
			pmodify = input('Edit player?\n  %s\n  ----------\n  [c]ancel: '%('\n  '.join(['[%s]: %s  (%s)'%(i,x['name'],x['index_fcdb']) for i,x in enumerate(sorted(roster,key=lambda x:x['name']))])))
			if pmodify != 'c':
				if pmodify == '*': pmodify = ','.join([str(x) for x in range(len(roster))])
				for x in pmodify.split(','):
					if x.isnumeric():
						if int(x) < len(roster):
							print('\nEditing %s'%sorted(roster,key=lambda x:x['name'])[int(x)]['name'])
							for _ in search_players(edit_player(sorted(roster,key=lambda x:x['name'])[int(x)]['index_fcdb']),'index_fcdb',strict=True)['files'][sorted(roster,key=lambda x:x['name'])[int(x)]['index_fcdb']]: exec(_)
					else:
						print('The value "%s" is not in the list'%x)
		elif what_to_edit == 'c':
			if (convocazioni := convoca(vals_already,t=modify)) is not None:
				temp_file+=b''.join(temp_bytes)+valori.read(1)+convocazioni
				valori.seek(40,1)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
				modify = [t for t in teams if t['index_fcdb'] == vals_already['index_fcdb']][0]
		elif what_to_edit == 'd':
			if (convocazioni := convoca(vals_already, True,t=modify)) is not None:
				temp_file+=b''.join(temp_bytes)+valori.read(1)+convocazioni
				valori.seek(40,1)
				temp_file+=valori.read()
				save(f_valori, temp_file)
				load_database(load=len(args.get('field', '')))
		elif what_to_edit == 'e':
			roster = sorted([p for p in players if p['id'] in vals_already['squad'] and p['starting'] > 128], key=lambda w:w['name'])
			menu_entries = [f"{_['name']} ({_['role']}, {_['average']})" for _ in roster]
			if new_value is None:
				if ttmng or input('Select a piece taker for each set piece [yn]? ') == 'y':
					roster = ttmng.get('lineup', [p['id'] for p in roster])
					menu_entries = [f"{players_db[_]['name']} ({players_db[_]['role']}, {players_db[_]['average']})" for _ in roster]
					spt = []
					for piece in setpiece:
						spt.append(int(inputPlus('\nSelect taker of {}:\n  $OPTIONLIST_l$$CANCEL$'.format(piece),menu_entries, c=True, sep='\n  ')[0]))
						if spt[-1] == len(roster): return
					spt = [roster[_] for _ in spt]
					_refresh_tmmng(vals_already,'set_piece',spt)
					write_tmmng()
					return
				new_taker = int(inputPlus('\nSelect player:\n  $OPTIONLIST_l$$CANCEL$',menu_entries, c=True, sep='\n  ')[0])
				if new_taker < 11:
					new_value = roster[new_taker]
				else: return

			old_score = new_value['shot power']
			old_score1 = new_value['shot accuracy']
			old_score2 = new_value['passing']
			old_average = new_value['average']

			current_max = sorted(roster, key = lambda w: w['shot power'])[-1]['shot power']
			players_hitting_max = [x for x in roster if x['shot power'] == current_max]
			for p in players_hitting_max:
				edit_player(p['index_fcdb'],field='12',value=max(current_max-4,39))
				edit_player(p['index_fcdb'],field='13',value=min(p['shot bias']+4,99))
			changedPlayers = {target_player['id']: {field:target_player[fieldopedia[field]['db']] for field in skill_fields} for target_player in players_hitting_max}
			edit_player(new_value['index_fcdb'],field='13',value=max(new_value['shot bias']-(current_max-new_value['shot power']),39))
			edit_player(new_value['index_fcdb'],field='12',value=min(current_max+4,99))
			newSPT = sorted([p for p in players if p['id'] in vals_already['squad'] and p['starting'] > 128], key=lambda w:w['shot power'])[-1]['name']
			strtpr = f"{newSPT} is the new set piece taker of {vals_already['names'][-1]}"
			if args.get('returnValues', None):
				changedPlayers[new_value['id']] = {field:new_value[fieldopedia[field]['db']] for field in skill_fields}
				return changedPlayers
			print(strtpr)
		else:
			what_to_edit = None
			valid = False
		if valid: break
	try:
		p = args['value']
	except:
		if input('Continue editing %s? [yn] '%vals_already['names'][-1]) == 'y':
			load_database()
			edit_team(teams[modify['db_position']])
	else:
		del p
	valori.close()
	return mod_offset

def convoca(team_data, *lax, **kwargs):
	global players
	nation = team_data['nation']
	lists = {'goalies':[],'defs':[],'midf':[],'strikers':[]}
	directory = {}
	m_roles = dict(GK=lists['goalies'],CB=lists['defs'],RB=lists['defs'],LB=lists['defs'],SW=lists['defs'],CM=lists['midf'],RM=lists['midf'],LM=lists['midf'],CF=lists['strikers'],RF=lists['strikers'],LF=lists['strikers'])
	counter = 0
	refs = {}
	strict = "x['nation'] == nation or nation in x['international_id']"
	if lax: strict = "True"
	working_players = copy.deepcopy(players)
	for x in working_players:
		if eval(strict):
			counter += 1
			capped = '*' if x['id'] in team_data['squad'] else ''
			tn = [t['names'][1] for t in teams if t['id'] == x['team_id']] + ['---']
			tn = tn[0]
			m_roles[x['role']].append({'id':x['id'],'name':x['name'],'team':tn,'role':x['role'],'average':x['average'],'c':counter, 'capped':capped,'starting':'*' if x['starting']>128 and tn != '---' else ''})
			directory[counter] = x['name']
			refs[counter] = (x['id'],x['name'],x['role'])
	longest = sorted([len(lists[_]) for _ in lists])[3]
	for _ in lists:
			lists[_] = sorted(lists[_], key = lambda x: x['average'], reverse=True)
	already = []
	for w in [p for r in lists.values() for p in r]:
		if w['capped'] == '*':
			already.append(w['c'])
	cdr_table = '┌'+49*'─'+\
			3*('┬'+49*'─')+\
			'┐\n│ Goalies'+41*' '+'│ Defenders'+39*' '+'│ Midfielders'+37*' '+'│ Strikers'+40*' '+'│\n'+'├'+49*'─'+3*('┼'+49*'─')+'┤\n'
	for x in range(longest):
		for position in ['goalies','defs','midf','strikers']:
			if x < len(lists[position]):
				innerString = f"[{lists[position][x]['c']}] {lists[position][x]['name']} ({lists[position][x]['role']}, {lists[position][x]['team']}{lists[position][x]['starting']}, {lists[position][x]['average']})"
				if (tl:=len(innerString)) > 48:
					innerString = f"[{lists[position][x]['c']}] {lists[position][x]['name']} ({lists[position][x]['role']}, {lists[position][x]['team'][:len(lists[position][x]['team'])-tl+48]}{lists[position][x]['starting']}, {lists[position][x]['average']})"
				new_line = '{:54}'.format('%s %s'%('\033[41m' if lists[position][x]['capped']=='*' else '\033[0m', innerString))
				cdr_table += f"|{new_line}%s"%('\033[0m' if lists[position][x]['capped']=='*' else '\033[1D')
			else:
				cdr_table +=  '│'+49*' '
		cdr_table += '│\n'
	cdr_table +=  '└'+49*'─'+\
			3*('┴'+49*'─')+\
			'┘'
	print('\n'+cdr_table)
	new_squad = [None]*20
	x = 0
	cancelled = False
	print('\nEnter player numbers ([c]ancel, [auto] selection)\n')
	auto_tactics = False
	while True:
		try:
			tmpC = f" (current: {directory[already[x]]}, enter to confirm)"
			new_squad[x] = int(input(f'Call player {str(x+1)}{tmpC if len(already)>0 else ""}: ')) 
		except ValueError as e:
			if str(e)[-2] == 'c':
				cancelled = True
				break
			elif str(e)[-5:-1] == 'auto':
				squad = [_[0] for _ in refs.values()]
				rt = recommended_tactics(squad)
				print()
				print(f'Recommended Tactics: {rt["rec_tactics"]}')
				top_11 = rt['lineup_ids']
				auto_tactics = rt['rec_tactics']
				new_squad = []
				count = [0] * 4
				for p in top_11:
					search_in = dict(GK='goalies',CB='defs',RB='defs',LB='defs',SW='defs',CM='midf',RM='midf',LM='midf',CF='strikers',RF='strikers',LF='strikers')[players_db[p]['role']]
					g = [item for item in lists[search_in] if item['id'] == p][0]
					new_squad.append(g['c'])
					lists[search_in].remove(g)
					count[['goalies','defs','midf','strikers'].index(search_in)] += 1
				tactics_caps = {
					'5d-4-1':[2,8,7,3],
					'5d-3-2':[2,8,6,4],
					'4d-5-1':[2,7,8,3],
					'4d-4-2':[2,7,7,4],
					'4d-3-3':[2,7,5,6],
					'4-4-2':[2,6,7,5],
					'4-3-3':[2,7,5,6],
					'3-5-2':[2,6,8,4],
					'3-4-3':[2,6,7,5]
				}
				caps = tactics_caps.get(rt['rec_tactics'],[2,6,7,5])

				for e,cap in enumerate(caps):
					pos_cap = cap - count[e]
					for _ in range(pos_cap):
						if len(lists[['goalies','defs','midf','strikers'][e]]) < 1: break
						new_squad.append(lists[['goalies','defs','midf','strikers'][e]].pop(0)['c'])

				turn = 0
				while True:
					if len(new_squad) == 20 or len([p for r in lists.values() for p in r]) == 0: break
					if turn == 0:
						if len(lists['defs']) > 0: new_squad.append(lists['defs'].pop(0)['c'])
						turn = 1
						continue
					if turn == 1:
						if len(lists['strikers']) > 0: new_squad.append(lists['strikers'].pop(0)['c'])
						turn = 2
						continue
					if turn == 2:
						if len(lists['goalies']) > 0: new_squad.append(lists['goalies'].pop(0)['c'])
						turn = 3
						continue
					if turn == 3:
						if len(lists['midf']) > 0: new_squad.append(lists['midf'].pop(0)['c'])
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
		if auto_tactics:
			edit_team(kwargs['t'], value=tactics.index(auto_tactics), field='t')
		return bytes(new_squad)

def show_leagues(**kwargs): 
	def _edit_league(league_source, l):
		os.system(clear_screen)
		print('%s'%('━'*80))
		print(l['name'].center(80))
		print('%s'%('─'*80))
		print('Index FCDB', l['index_fcdb'], sep="\033[20C")
		print('Index FCDBPENG', l['index_fcdbpeng'], sep="\033[16C")
		print('Id', l['id'], sep="\033[28C")
		print('%s'%('─'*80))
		print('Size', l['size'], sep="\033[26C")
		print('%s'%('─'*80))
		print('Teams\033[1A')
		for t in tnlist[l['id']]:
			print('\033[29C',t['names'][-1])
		print('%s'%('━'*80))
		print()
		menu_items = ["[r]ename league","[t]ransfer teams","restore [o]riginal","change [s]ize"]
		supernumerary = l['size']-original_league_sizes[l['id']]
		if supernumerary > 0: menu_items += ["choose super[n]umerary"]
		menu_items += ["[c]ancel"]
		while True:
			standard_query = ' / '.join(menu_items)
			print('\033[J\033[1A\033[41;37m\n',standard_query,"\033[0m", sep="",end = "\r")
			k = chr(getter())
			if k == 'r':
				old_name = FCDB_ENG[globalDB['FCDB_ENG']['league names']][l['db_position']]
				FCDB_ENG[globalDB['FCDB_ENG']['league names']][l['db_position']] = input('\033[JEnter new name for "%s": [press enter to cancel] '%l['name']) #NEW
				length_diff = len(FCDB_ENG[globalDB['FCDB_ENG']['league names']][l['db_position']]) - len(old_name)
				for e,h in enumerate(FCDB_ENG[globalDB['FCDB_ENG']['league name indexes']]):
					if e > l['db_position']:
						FCDB_ENG[globalDB['FCDB_ENG']['league name indexes']][e] += length_diff
				FCDB_ENG[globalDB['FCDB_ENG']['start index of team names']] += length_diff
				rebuildDbFiles()
				return
			elif k =='t':
				tms = sorted([t for t in teams if t['id'] in l['teams']], key=lambda x:x['names'][-1])
				t = int(inputPlus('\033[J\nSelect team:\n  $OPTIONLIST_l$$CANCEL$', [t['names'][-1] for t in tms], c=True, sep='\n  ')[0])
				if t < len(tms):
					swap1 = tms[t]
					if 'Group' in l['name']: league_source = sorted(leagues, key=lambda x: x['name'])+[{'name':'National Teams','teams':sorted([t['id'] for t in teams if t['league_id']==11])}]
					ls=[s for s in league_source if s['name'] != l['name']]
					l2i = int(inputPlus('\nSelect destination league:\n  $OPTIONLIST_l$$CANCEL$', [y['name'] for y in ls]+['Non-League'], c=True, sep='\n  ')[0])
					
					if l2i < len(league_source)-1:
						l2 = ls[l2i]
						tms = sorted([t for t in teams if t['id'] in l2['teams']], key=lambda x:x['names'][-1])
					else:
						tms = [t for t in teams if t['id'] in non_league_teams]
					t = int(inputPlus('\nSelect team to swop:\n  $OPTIONLIST_l$$CANCEL$', [t['names'][-1] for t in tms], c=True, sep='\n  ')[0])
					if t < len(tms):
						swap2 = tms[t]
						if input(f'\nSwapping {swap1["names"][-1]} with {swap2["names"][-1]}. Proceed? [yn] ') == 'y':
							l['teams'][l['teams'].index(swap1['id'])]=swap2['id']
							FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']] = l['teams']
							if l2i < 10 and not 'Group' in l['name']:
								l2['teams'][l2['teams'].index(swap2['id'])]=swap1['id']
								FCDB[globalDB['FCDB'][f'league {l2["db_position"]}']['position']][globalDB['FCDB'][f'league {l2["db_position"]}']['teams in league']] = l2['teams']
							rebuildDbFiles()
							t_fsh = f'{tms[t]["id"]:0>4}'
							if tms[t]['league_id'] != 11 and not os.path.isfile('/'.join([gamepath.replace('common','fepack'),'IGFLAGS',f'{t_fsh}.pak'])): feflags(tms[t]['id'])
				return
			elif k =='s':
				while True:
					new_size = input(f'\r\033[KEnter new size ({", ".join(str(ls) for ls in league_sizes)}, or [c]ancel): ')
					if new_size == 'c': return
					if new_size in (str(ls) for ls in league_sizes): break
					print('\033[1A', end="")
				new_size_value = int(((new_size:=int(new_size)) + .5)*1024)
				compensate = new_size % 2
				offset = 2*(math.ceil(new_size/2)*2-math.ceil(l['size']/2)*2)
				tms = sorted([t for t in teams if t['id'] in l['teams']], key=lambda x:x['names'][-1])
				diff = l['size'] - new_size
				if diff == 0: return
				if diff > 0:
					tmsToRem = []
					print(f'Select {diff} teams to remove from league')
					for i in range(diff):
						while True:
							t = int(inputPlus(f'\033[J\nSelect team {i+1}:\n  $OPTIONLIST_l$$CANCEL$', [t['names'][-1] for t in tms], c=True, sep='\n  ')[0])
							if t < len(tms):
								tmsToRem.append(tms[t]['id'])
								del tms[t]
								break
							if t == len(tms): return
					for i in tmsToRem:
						FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']].remove(i)
					if not all(FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']]):FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']].remove(0)
				if diff < 0:
					missing = -diff-len(non_league_teams)
					if missing > 0:
						input(f'There are not enough available non-league teams to expand the league to the chosen size. Create {-diff-len(non_league_teams)} teams or release them from other leagues and try again.')
						return
					tmsToAdd = []
					tms = [t for t in teams if t['id'] in non_league_teams]
					if l['db_position'] > 10: tms = [t for t in teams if t['nation'] != 0]
					for m in range(-diff):
						while True:
							t = int(inputPlus('\nSelect team to add:\n  $OPTIONLIST_l$$CANCEL$', [t['names'][-1] for t in tms], c=True, sep='\n  ')[0])
							if t < len(tms):
								tmsToAdd.append(tms[t]['id'])
								del tms[t]
								break
							if t == len(tms): return
					for i in tmsToAdd:
						FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']].append(i)
					if not all(FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']]):FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']].remove(0)
				if compensate: FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']].append(0)
				FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['league size']] = new_size_value
				for i in range(FCDB[globalDB['FCDB']['number of leagues']]):
					if i <= l["db_position"]: continue
					FCDB[globalDB['FCDB']['league indexes']][i]+=offset
				FCDB[globalDB['FCDB']['start index of team data']]+=offset
				FCDB[globalDB['FCDB']['start index of player data']]+=offset
				rebuildDbFiles()
				return
			elif k == 'n' and supernumerary > 0:
				teams_db = {x['id']:{i:x[i] for i in x if i != 'id'} for x in teams}
				pool = l['teams']
				zeros = pool.count(0)
				pool = [p for p in pool if p != 0]
				print('\r\033[KSelect team to make supernumerary\n')
				for s in range(supernumerary):
					for e,t in enumerate(pool):
						print(f"[{e}]".rjust(4),teams_db[t]['names'][-1])
					while True:
						ch = input('\n [c]ancel: ')
						if ch == 'c': return
						if not ch.isnumeric(): continue
						if int(ch) < len(pool): break
					ch = pool[int(ch)]
					pool.remove(ch)
					pool.append(ch)
				pool += zeros * [0]
				FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']] = pool
				rebuildDbFiles()
			elif k == 'o':
				if not os.path.isfile(os.path.join(Fifapath,'original.json')):
					saveIntLeagues()
					return
				original = json.load(open(Fifapath+'/original.json', 'r'))
				new_size = original[str(l['db_position'])]['size']
				new_teams = original[str(l['db_position'])]['teams'] 
				if new_size != l['size']:
					new_size_value = int(((new_size:=int(new_size)) + .5)*1024)
					offset = 2*(math.ceil(new_size/2)*2-math.ceil(l['size']/2)*2)
					FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['league size']] = new_size_value
					for i in range(FCDB[globalDB['FCDB']['number of leagues']]):
						if i <= l["db_position"]: continue
						FCDB[globalDB['FCDB']['league indexes']][i]+=offset
					FCDB[globalDB['FCDB']['start index of team data']]+=offset
					FCDB[globalDB['FCDB']['start index of player data']]+=offset
				if new_teams != l['teams']:
					FCDB[globalDB['FCDB'][f'league {l["db_position"]}']['position']][globalDB['FCDB'][f'league {l["db_position"]}']['teams in league']] = new_teams
					rebuildDbFiles()
				return
			elif k =='c':
				return
	while True:
		current = 'c'
		currLeague = 0
		while True:
			os.system(clear_screen)
			if current == 'c': league_source = sorted(leagues[:11], key=lambda x: x['name'])
			if current == 'n': league_source = sorted(leagues[11:], key=lambda x: x['name'])
			standard_query = f"Use arrow keys to select league / switch to {'[c]lubs' if current == 'n' else '[n]ational teams'} / [e]dit league / back to [m]ain menu"
			league_boxes = []
			tnlist = {}
			for e,l in enumerate(league_source):
				sthi = '\033[93m' if e == currLeague else ''
				endhi = '\033[0m' if e == currLeague else ''
				tmplg = []
				tnlist[l['id']] = sorted([t for t in teams if t['id'] in l['teams']], key=lambda x:x['names'][-1])
				tmplg.append(f'{sthi}╒{"◉ "+l["name"].upper()+" ◉":═^38}╕{endhi}')
				tmplg.append(f'{sthi}│{38*" "}│{endhi}')
				for t in tnlist[l['id']]:
					tmplg.append(f'{sthi}│{t["names"][-1] + ("*" if l["teams"].index(t["id"])>=original_league_sizes[l["id"]] else ""): ^38}│{endhi}')
				tmplg.append(f'{sthi}│{38*" "}│{endhi}')
				tmplg.append(f'{sthi}╘{38*"═"}╛{endhi}')
				league_boxes.append(tmplg)
			maxHeight = sorted([len(l) for l in league_boxes])[-1]
			for line in range(maxHeight+1):
				print((crp:=(ltp:=(' '*4).join([box[line] if line < len(box) else ' '*40 for box in [league_boxes[currLeague-1 if currLeague > 0 else 10]]+league_boxes[currLeague:]+league_boxes[:currLeague]]))[:204 if '\033[0m' in ltp else 195]),f'{".." if crp[-2:] != "  " else ""}')

			print('\033[1A\033[41;37m\n',standard_query,"\033[0m", sep="")

			k = find_key()
			if k == 'm': return
			if k in ['c','n']:
				current = k
				currLeague = 0
			if k == 'e':
				if current == 'n':
					if input('\033[2A\033[31mWARNING: editing of national team groups is completely untested. Proceed at your own risk? [yn]\033[0m ') != 'y': continue
				_edit_league(league_source,league_source[currLeague])
			if k == 'right': currLeague = currLeague + 1 if currLeague < len(league_boxes)-1 else 0
			if k == 'left': currLeague = currLeague - 1 if currLeague > 0 else len(league_boxes)-1
			if k == 'l' and current == 'c':
				list_file = {l['db_position']:{k:l[k] for k in ['name','index_fcdbpeng','id','index_fcdb','size','teams']} for l in leagues if l['db_position'] < 11}
				ncols = 7
				sorted_teams = sorted(teams,key=lambda x:x['names'][-1])
				team_names = [t['names'][-1] for t in sorted_teams]
				teams_per_col = math.ceil(len(team_names)/ncols)
				team_name_cols = [[y for y in team_names[i:i+teams_per_col]] for i in range(0,len(team_names),teams_per_col)]
				team_name_cols = [t+(teams_per_col-len(t))*[''] for t in team_name_cols]
				for id,l in list_file.items():
					print('League',f'{id}; current name: {l["name"]}. Rename? ',end='')
					if input('[yn] ') == 'y':
						old_name = FCDB_ENG[globalDB['FCDB_ENG']['league names']][id]
						FCDB_ENG[globalDB['FCDB_ENG']['league names']][id] = input('\033[JEnter new name for "%s": [press enter to cancel] '%l['name']) #NEW
						length_diff = len(FCDB_ENG[globalDB['FCDB_ENG']['league names']][id]) - len(old_name)
						for e,h in enumerate(FCDB_ENG[globalDB['FCDB_ENG']['league name indexes']]):
							if e > id:
								FCDB_ENG[globalDB['FCDB_ENG']['league name indexes']][e] += length_diff
						FCDB_ENG[globalDB['FCDB_ENG']['start index of team names']] += length_diff
					print(f'Current size: {l["size"]}. Enter new size (return to confirm current size): ', end='')
					new_size = int(new_size) if (new_size:=input()).isnumeric() else l["size"]
					new_teams = set()
					while True:
						for row in range(teams_per_col):
							print(''.join([(f'[{row+f*teams_per_col}] '+team_name_cols[f][row]).ljust(201//ncols) for f in range(ncols) if team_name_cols[f][row] != '']))
						if (ntid:=input('\nEnter team to add: ')).isnumeric() and int(ntid) <= len(team_names): new_teams.add(sorted_teams[int(ntid)]['id'])
						elif ',' in ntid:
							ntid = ntid.split(',')
							if all([r.isnumeric() for r in ntid]): new_teams = {sorted_teams[int(r)]['id'] for r in ntid}
						if len(new_teams) == new_size: break
					new_teams = [t for t in new_teams] + [0] * (len(new_teams) % 2)
					if new_size != l['size']:
						new_size_value = int(((new_size:=int(new_size)) + .5)*1024)
						offset = 2*(math.ceil(new_size/2)*2-math.ceil(l['size']/2)*2)
						FCDB[globalDB['FCDB'][f'league {id}']['position']][globalDB['FCDB'][f'league {id}']['league size']] = new_size_value
						for i in range(FCDB[globalDB['FCDB']['number of leagues']]):
							if i <= id: continue
							FCDB[globalDB['FCDB']['league indexes']][i]+=offset
						FCDB[globalDB['FCDB']['start index of team data']]+=offset
						FCDB[globalDB['FCDB']['start index of player data']]+=offset
					if new_teams != l['teams']:
						FCDB[globalDB['FCDB'][f'league {id}']['position']][globalDB['FCDB'][f'league {id}']['teams in league']] = new_teams
					print(FCDB_ENG[globalDB['FCDB_ENG']['league names']][id], [[tz for tz in teams if tz['id']==tid][0]['names'][-1] for tid in new_teams])
				rebuildDbFiles()
				return

def rename_league(target): 
	tmpfl = b''
	new_char = b''
	lglist = b''
	squadre = open(f_squadre, 'r+b')
	groups = []
	n = []
	squadre.seek(8,0)
	init_size_list = struct.unpack("<h", squadre.read(2))[0]+8
	squadre.seek(12,0)
	how_many_teams = struct.unpack("<h", squadre.read(2))[0]
	init_size_list_teams = how_many_teams+8
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
				new_string = bytes(input('\033[JEnter new name for "%s": [press enter to cancel] '%string.decode('unicode-escape')), 'iso-8859-1')
				if len(new_string) > 0:
					if new_string == b'*':
						skip = True
					else:
						groups.append(string)
						n.append(new_string)
						string = new_string
						del new_string
				else: return
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
	garbage_bytes = squadre.read(how_many_teams-index_end_of_list)
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
	new_init_size_list_teams = last_index_leagues + 1 #!!!!!
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
	squadre.seek(index_end_of_list+len(garbage_bytes),0)
	tmpfl += squadre.read()
	output = open(f_squadre,'w+b')
	output.write(tmpfl)
	output.close()
	load_database()

def commit():
	global decomp_path
	print('Committing...')
	home = os.path.expanduser('~')
	shutil.copyfile(f_valori, f_valori.replace(Fifapath, gamepath))
	shutil.copyfile(f_nomi, f_nomi.replace(Fifapath, gamepath))
	shutil.copyfile(f_squadre, f_squadre.replace(Fifapath, gamepath))
	shutil.copyfile(f_interfaccia, f_interfaccia.replace(Fifapath, gamepath))
	currdir = os.getcwd()
	if len(compress_command) == 0: return #NEW
	os.chdir(decomp_path[0])
	os.system(f'{compress_command} "{Fifapath}/tmmng.dec" "{gamepath.replace("common","user")}/tmmng.db"')
	os.chdir(currdir)
	input('Changes saved. Return to main menu. ')

def restore(*args):
	if not args:
		if input('Confirm restoring [yn]? ') != 'y': return
	print('Copying database...' if args else 'Restoring...')
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
	l1 = int(inputPlus('Select league of team 1:\n  $OPTIONLIST_l$$CANCEL$',	sorted_leagues_names+['National Teams'], c=True, sep='\n  ', top=True)[0])
	if l1 < 12:
		l1 = sorted_leagues.get(l1,l1)
		tms = [(team['names'][-1],team['id'],team.get('nation',None),team['squad'],team['tactics']) for team in sorted(teams, key=lambda x: x['names'][-1]) if team['league_id'] == l1]
	else: return
	print()
	t = int(inputPlus('Select team 1:\n  $OPTIONLIST_l$$CANCEL$', [t[0] for t in tms], idx='0', c=True, sep='\n  ')[0])
	if t < len(tms):
		t1 = tms[t][0]
		t1id = tms[t][1]
		t1nat = tms[t][2]
		t1sq = tms[t][3]
		t1ta = tms[t][4]
	else: return
	print()
	l2 = int(inputPlus('Select league of team 2:\n  $OPTIONLIST_l$$CANCEL$',	sorted_leagues_names+['National Teams'], c=True, sep='\n  ')[0])
	if l2 < 12:
		l2 = sorted_leagues.get(l2, l2)
		tms = [(team['names'][-1],team['id'],team.get('nation',None),team['squad'],team['tactics']) for team in sorted(teams, key=lambda x: x['names'][-1]) if team['league_id'] == l2]
	else: return
	print()
	t = int(inputPlus('Select team 2:\n  $OPTIONLIST_l$$CANCEL$', [t[0] for t in tms], idx='0', c=True, sep='\n  ')[0])
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

	if l1 > 10:
		what1 = "t1nat in x['international_id']"
		in1='x["team"]'
	if l2 > 10:
		what2 = "t2nat in x['international_id']"
		in2='x["team"]'

	rls = dict(GK=0,RB=2,RCB=3,SW=1,CB=3,LCB=4,LB=5,RM=6,RCM=7,CM=8,LCM=9,LM=10,RF=11,CF=12,LF=13)
	for x in players:
		px_role = _fgRoles(x['role'],x['starting']) 
		if eval(what1):
			teams0['N'].append(x['jersey'])
			teams0['Name'].append(x['name'])
			teams0['P'].append(px_role)
			teams0['Nat'].append(eval(in1))
			teams0['AV'].append(x['average'])
			teams0['Role'].append(rls[px_role])
			if l1 < 12:
				if x['starting'] > 128: teams0['St'].append(2)
				else: teams0['St'].append(1)
			else: teams0['St'].append(nt_lineup(t1sq, t1ta, x['id']))
		if eval(what2):
			teams1['N'].append(x['jersey'])
			teams1['Name'].append(x['name'])
			teams1['P'].append(px_role)
			teams1['Nat'].append(eval(in2))
			teams1['AV'].append(x['average'])
			teams1['Role'].append(rls[px_role])
			if l2 < 12:
				if x['starting'] > 128: teams1['St'].append(2)
				else: teams1['St'].append(1)
			else: teams1['St'].append(nt_lineup(t2sq, t2ta, x['id']))
	table0 = pd.DataFrame(data = teams0)
	table0 = table0.sort_values(by=['St','Role'])
	table0 = table0[['N', 'Name','P','Nat','AV']]
	table1 = pd.DataFrame(data = teams1)
	table1 = table1.sort_values(by=['St','Role'])
	table1 = table1[['N', 'Name','P','Nat','AV']]
	rows = []
	table0 = list(table0.iterrows())
	table0 = table0[-11:]+table0[:-11]
	table1 = list(table1.iterrows())
	table1 = table1[-11:]+table1[:-11]
	for e,i in enumerate(table0):
		row = []
		if e == 11:
			row.append('─'*54+'┼'+'─'*54)
			rows.append(row)
			row = []
		row.append('{:>3}'.format(i[1][0]))
		row.append(align(i[1][1],'Name'))
		row.append(align(i[1][2],'Role'))
		row.append(align(i[1][3],'Nation'))
		row.append('{:<4}'.format(i[1][4]))
		row.append('│')
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
			row.append('│')
			row.append('{:>2}'.format(i[1][0]))
			row.append(align(i[1][1],'Name'))
			row.append(align(i[1][2],'Role'))
			row.append(align(i[1][3],'Nation'))
			row.append('{:<5}'.format(i[1][4]))
		rows.append(row)
	os.system(clear_screen)
	print('┌{0}┬{0}┐'.format('─'*(3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5)))
	print('│{0}{1}{2}│{3}{4}{5}│'.format(
			math.floor((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t1))/2)*' ',
			t1.upper(),
			math.ceil((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t1))/2)*' ',
			math.floor((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t2))/2)*' ',
			t2.upper(),
			math.ceil((3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5-len(t2))/2)*' ',
		)
	)
	print('├{0}┼{0}┤'.format('─'*(3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5)))
	for e,r in enumerate(rows):
		if e == 11: print('├%s┤'%' '.join(r))
		else: print('│%s│'%' '.join(r))
	print('└{0}┴{0}┘'.format('─'*(3+fieldopedia['Name']['width']+fieldopedia['Role']['width']+fieldopedia['Nation']['width']+fieldopedia['Average']['width']+5)))
	input('\nReturn to main menu ')

def list_by_role():
	maxL = os.get_terminal_size().lines
	maxW = 80
	if platform.system() != 'Windows':
		import termios, tty
	else:
		import msvcrt
	tpos = {}
	for tm in teams:
		tpos.setdefault(tm['id'],tm)
	tpos[-1] = {'names':['---']}
	by_role = {}
	for p in sorted(players, key=lambda x: x['average'], reverse = True):
		if p['name'] == 'New Player': continue
		by_role.setdefault(p['role'],[]).append('{0:<17}{1:<24}{2:<24}{3:>3}'.format(p['name'],tpos[p['team_id']]['names'][-1]+('*' if p['starting'] > 128 else ''),p['country']+('*' if len(p['international']) > 0 else ''),p['average']).center(maxW))
	role_carousel = ['GK','RB','CB','SW','LB','RM','CM','LM','RF','CF','LF']
	starting_pos = 0
	starting_page = 0

	by_role_pages = {}
	for role,pls in by_role.items():
		tmp = [' ']
		for e,p in enumerate(pls):
			if e % (maxL - 6) == 0 and e > (maxL - 7): tmp.append('...'.center(maxW))
			tmp.append(p)
			if e % (maxL - 6) == maxL-7 and e != len(pls) - 1: tmp.append('...'.center(maxW))
			if e % (maxL - 6) == maxL-7 or e == len(pls) - 1:
				if e == len(pls) - 1: tmp.append(maxW*'━')
				by_role_pages.setdefault(role,[]).append(tmp)
				tmp = []

	def print_list(role,page):
		os.system(clear_screen)

		print(f' {dict(GK="Goalkeepers", LB="Left Backs", CB="Centre Backs", SW="Sweepers", RB="Right Backs",LM="Left Midfielders", CM="Central Midfielders", RM="Right Midfielders",LF="Left Forwards", CF="Central Forwards", RF="Right Forwards")[role]} ({page+1}/{len(by_role_pages[role])}) '.center(maxW,'━'))
		print('\n'.join(by_role_pages[role][page]))

	while True:
		print_list(role_carousel[starting_pos],starting_page)
		print('\n',f'Left for {role_carousel[len(role_carousel) -1 if starting_pos - 1 < 0 else starting_pos -1]}, right for {role_carousel[0 if starting_pos + 1 == len(role_carousel) else starting_pos + 1]}, up/down to scroll the list, type "q" to quit', end='\r')
		k = find_key()
		if k == 'q': break
		if k == 'left':
			if starting_pos - 1 < 0: starting_pos = len(role_carousel) -1
			else: starting_pos -= 1
			starting_page = 0
		if k == 'right':
			if starting_pos + 1 == len(role_carousel): starting_pos = 0
			else: starting_pos += 1
			starting_page = 0
		if k == 'up':
			if starting_page > 0:
				starting_page -= 1
		if k == 'down':
			if starting_page < len(by_role_pages[role_carousel[starting_pos]])-1:
				starting_page += 1
	return
def general_list():
	tpos = {}
	for tm in teams:
		tpos.setdefault(tm['id'],tm)
	tpos[-1] = {'names':['---']}
	by_role = {}
	for p in sorted(players, key=lambda x: x['average'], reverse = True):
		by_role.setdefault((m_roles:=dict(GK='Goalkeepers', CB='Defenders',RB='Defenders',LB='Defenders',SW='Defenders',CM='Midfielders',RM='Midfielders',LM='Midfielders',CF='Forwards',RF='Forwards',LF='Forwards'))[p['role']],[]).append('{0:<17}{1:<13}{2:<16}{3:>3}'.format(p['name'],tn[1] if len(tn:=tpos[p['team_id']]['names']) > 1 else tn[0] ,p['country'][:15]+('*' if len(p['international']) > 0 else ''),p['average']))
	lines = {}
	for role in set(m_roles.values()):
		lines.setdefault(role,[]).append("━"*49)
		lines[role].append("{:^49}".format(role))
		lines[role].append("━"*49)
		lines[role]+=by_role[role]
		lines[role].append("━"*49)
	x = sorted([len(_) for _ in lines.values()])[-1]
	for _ in range(x):
		line = [g[_] if _ < len(g:=lines['Goalkeepers']) else ' '*49,d[_] if _ < len(d:=lines['Defenders']) else ' '*49,m[_] if _ < len(m:=lines['Midfielders']) else ' '*49,f[_] if _ < len(f:=lines['Forwards']) else ' '*49]
		if _ == 0:
			print('┳'.join(line))
		elif _ == 2:
			print('╋'.join(line))
		elif "━"*49 in line:
			toprint = ['','','','','','','','']
			if any(tr:=[line[y] == "━"*49 and line[min(len(line)-1, y+1)] != "━"*49 for y in range(len(line))]):
				for y,le in enumerate(tr):
					if le:
						toprint[y*2] = line[y]
						toprint[y*2+1] = '┫'
			if any(tr:=[line[y] != "━"*49 and line[min(len(line)-1, y+1)] == "━"*49 for y in range(len(line))]):
				for y,le in enumerate(tr):
					if le:
						toprint[y*2] = line[y]
						toprint[y*2+1] = '┣'
			if any(tr:=[line[y].strip() == '' and line[min(len(line)-1, y+1)] == "━"*49 for y in range(len(line))]):
				for y,le in enumerate(tr):
					if le:
						toprint[y*2] = line[y]
						toprint[y*2+1] = '┗'
			if any(tr:=[line[y]== "━"*49 and line[min(len(line)-1, y+1)].strip() == '' for y in range(len(line))]):
				for y,le in enumerate(tr):
					if le:
						toprint[y*2] = line[y]
						toprint[y*2+1] = '┛'
			if any(tr:=[line[y]== "━"*49 and line[min(len(line)-1, y+1)]== "━"*49 for y in range(len(line))]):
				for y,le in enumerate(tr):
					if le:
						toprint[y*2] = line[y]
						toprint[y*2+1] = '┻'
			for y,le in enumerate(toprint):
				if y % 2 == 0 and le == '':
					toprint[y] = line[int(y/2)]
				if y % 2 == 1 and le == '':
					toprint[y] = '┃' if line[int((y-1)/2)].strip() != '' or line[min(int((y-1)/2+1),3)].strip() != '' else ' '
			toprint[-1] = '\n'
			print(''.join(toprint), end='')
		else:
			print('┃'.join(line).replace('{0}┃{0}'.format(' '*49),' '*99))
	input('Return to main menu ')

def initialize(*db):
	global debug
	if db: debug = True
	def start_search():
		global sf, tableSort
		a = input('Player name (hit return to cancel): ')
		if len(a) == 0: return 'n'
		if table:
			llist = sorted(list(fieldopedia.keys()))
			lval = [fieldopedia[_]['short'] for _ in sorted(fieldopedia)]
			tableSort = lval[int(fc) if (fc:=inputPlus('\n$OPTIONLIST_d$', lval:={x:y for x,y in enumerate(lval)}, dct=llist, c=True, sep="@grid", cancelNull=True, additional_message="Sort table by (default = Name)")[0]).isnumeric() else 19]
		b = None
		if ';' in a or '|':
			b = a.split(';')[1:]
			a = a.split(';')[0]
		if a[0] == '@':
			command = a.split('@')[1]
			a = a.split('@')[2]
		else:
			command = 'search_name'
		if command == 'team': command = 'search_team'
		os.system(clear_screen)
		search = search_players(unidecode.unidecode(a), command, refine=b)
		results = search['results']
		if len(results) == 0:
			if not table: print('No matches')
		else:
			toEdit = False
			if len(results) == 1 and not table and not debug:
				for _ in next(iter(search['files'].values())): exec(_)
				toEdit = list(search['files'])[0]
				name = results[0]['name']
			elif len(results) > 1 or table or debug:
				results = sorted(results, key=lambda x:x['name'])
				action = 'Select' if not table else 'Edit'
				while True:
					view = input(f'{action} player:\n\n  %s\n  ----------\n  [c]ancel: '%('\n  '.join(['[%s]: %s (%s, %s)'%(i,x['name'],x['index_fcdb'],x['team']) for i,x in enumerate(results)])))
					if view != 'c':
						if view.isnumeric():
							if int(view) < len(results):
								if not debug:
									for _ in search['files'][results[int(view)]['index_fcdb']]: exec(_)
								toEdit = results[int(view)]['index_fcdb']
								name = results[int(view)]['name']
							else: print('The value "%s" is not in the list'%view)
						else: print('The value "%s" is not in the list'%view)
						break
					else:
						toEdit = False
						break
			if toEdit:
				if table or input(f'Edit {name} [yn]? ') == 'y':
					print(f'\nEditing {name}')
					for _ in search_players(edit_player(toEdit),'index_fcdb',strict=True)['files'][toEdit]: exec(_)

		return input("\nNew search? [yn] ")
	while True:
		if start_search() == 'n':
			break

def export_database():
	def _export_to(dir):
		if not dir: return
		print('Preparing data...')
		complete_db = {'leagues':[],'non-league teams':[],'teamless players':[]}
		for l in leagues:
			complete_db['leagues'].append(l)
		leagueTeams = []
		teamPlayers = []
		for l in complete_db['leagues']:
			tmptms = []
			for t in teams:
				if t['id'] in l['teams']:
					tmptms.append({**t})
					leagueTeams.append(t['id'])
			l['teams'] = tmptms
			for t in l['teams']:
				tmpsq = []
				for p in players:
					if p['id'] in t['squad']:
						tmpsq.append({**p})
						teamPlayers.append(p['id'])
				t['squad'] = tmpsq
		for t in teams:
			if t['id'] not in leagueTeams:
				complete_db['non-league teams'].append(t)
				tmpsq = []
				for p in players:
					if p['id'] in complete_db['non-league teams'][-1]['squad']:
						tmpsq.append(p)
						teamPlayers.append(p['id'])
				complete_db['non-league teams'][-1]['squad'] = tmpsq
		for p in players:
			if p['id'] not in teamPlayers:
				complete_db['teamless players'].append(p)
		print(json.dumps(complete_db,indent=2),file=open(os.path.join(dir,'complete_db.json'),'w+'))
		input('The data has been saved. Hit enter to return to the main menu.')
		load_database()
		
	dir = input('Enter destination folder ([c]ancel): ').strip()
	if len(dir) > 0 and os.path.isdir(dir) and dir != 'c': _export_to(dir)

def inputPlus(message, valid_options, **params):
	dct = valid_options
	n_vals = len(valid_options)
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
		c = params.get('c', False)
		entC = params.get('entC', False)
	c_separator = '{0}{1}{0}'.format(separator, 11*'━') if '\n' in separator else separator
	width, width_l, grid_sp = 0, 1, 0
	msg = ''
	if separator == '@grid':
		width = max([len(_) for _ in dct]) if '$OPTIONLIST_d$' in message else max([len(_) for _ in valid_options])
		width_l = len(str(len(dct))) if '$OPTIONLIST_d$' in message else len(str(len(valid_options)))
		separator = ''
		grid_sp = 4
	if '$OPTIONLIST_d$' in message: msg = separator.join([f'[{e}] {dct[e]:{width+width_l-(len(str(e))-grid_sp)*(width>0)}}' for e in valid_options.keys()])
	elif '$OPTIONLIST_l$' in message: msg = separator.join([f'[{e}] {o:{width+width_l-(len(str(e))-grid_sp)*(width>0)}}' for (e,o) in enumerate(valid_options)])
	if width > 0:
		winWidth = os.get_terminal_size().columns-2
		itemWidth = width+width_l+3+grid_sp
		perLine = winWidth // itemWidth
		totLines = math.ceil(n_vals / perLine)
		msgbits = []
		for _ in range(totLines):
			msgbits.append((fl:=msg[_*itemWidth*perLine:(_+1)*perLine*itemWidth])+' '*(itemWidth*perLine-len(fl)))
			fl=msg[_*itemWidth*perLine:(_+1)*perLine*itemWidth]
		msg = '┌'+'─'*(perLine*itemWidth)+'┐\n│'+'│\n│'.join(msgbits)+'│\n└'+'─'*(perLine*itemWidth)+'┘\n'

	message = message.replace('$OPTIONLIST_d$', msg).replace('$OPTIONLIST_l$', msg)
	valid_options = [str(_) for _ in list(valid_options.keys())] if type(valid_options) == dict else [str(_) for _ in range(n_vals)]
	if c: message = message.replace('$CANCEL$', '%s[%s] cancel'%(c_separator,n_vals)); valid_options += [str(n_vals)]
	if entC == True: valid_options += ['']
	while True:
		option = input(f'{message}{(" "+(addm:=params.get("additional_message", "")))*(len(addm)>0)}:\033[J ')
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
		if option == '' and params.get('cancelNull',None):
			option = ''
			break
		print('\033[%sA'%(2+message.count('\n')))
		if params.get('top',False): os.system(clear_screen)
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
	global f_nomi, f_valori, f_squadre, f_interfaccia, filenames, lang
	os.system(clear_screen)
	lval = ['DUT','ENG','FRE','GER','ITA','SPA','SWE']
	llist = ['Dutch','English','French','German','Italian','Spanish','Swedish']
	unavailable = []
	for li,llang in enumerate(lval):
		if not (os.path.isfile("%s/FCDB_%s.DBI"%(gamepath,llang)) and os.path.isfile("%s/FC%s.BIN"%(gamepath,llang))):
			unavailable.append(li)
	for u in unavailable[::-1]:
		del lval[u]
		del llist[u]
	if not kwargs.get('wait',False): print('Current language:', llist[lval.index(lang)])
	while True:
		nf = int(inputPlus('Select *game* (not editor!) language\n $OPTIONLIST_d$$CANCEL$', lval:={x:y for x,y in enumerate(lval)}, dct=llist, c=True, sep="\n ")[0])
		if nf == len(llist): return False
		else:
			custom_vals['lang'] = [lval[nf]]
			json.dump(custom_vals, open('fifa_config.json', 'w'), indent=2)
			break
	print('New game language: %s'%llist[nf])
	lang = lval[nf]
	if not kwargs.get('wait',False):
		filenames = ["FCDBPENG.DBI","FCDB.DBI","FCDB_%s.DBI"%lval[nf],"FC%s.BIN"%lval[nf]]
		f_nomi, f_valori, f_squadre, f_interfaccia = ["%s/%s"%(Fifapath,fn) for fn in filenames]
		restore()
	else: return lval[nf]

def show_all_kits(*args):
	if os.path.isdir(os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS')):
		wh = 'first'
		print('\033[1A\033[KLoading jerseys...')
		jerseys = [_ for _ in os.listdir(os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS')) if re.match('jers\d\d.fsh',_.lower())]
		mainRoot = tk.Tk()
		mainRoot.title('Select jersey')
		mainRoot.geometry("726x580+300+0")
		mainRoot.configure(background='#EAEAEA')
		queue = {}
		def callback(n,h,tm):
			n = int(n['text'])
			e = n
			n = sorted(teams, key=lambda x: x['names'][-1])[n]
			f = edit_team(n,field='fs' if wh == 'first' else 'ss',asChild=mainRoot,buttons = buttons[e%6])
			queue.setdefault(n['id'],{}).setdefault(f.args[2][1], []).append(f)
			print('\033[2A\033[J')
		def on_closing(event):
			if event.widget == mainRoot:
				if platform.system() == 'Darwin': os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Terminal" to true' ''')
		mainRoot.bind("<Destroy>", on_closing)
		buttons = {}
		visibleButtons = []

		startTeam = 0

		for e in range(6):
			kd = tk.Button(mainRoot)
			kn = Label(mainRoot)
			visibleButtons.append({'label':kn,'button':kd})

		def _move(evt):
			direction = int(w.get())*6
			nonlocal fired, startTeam
			fired = False
			startTeam = direction
			_updateButtons(False)
			if startTeam == int(len(teams) / 6) *6:
				for e in range(len(teams),(int(len(teams)/6)+1)*6):
					visibleButtons[e % 6]['button'].grid_forget()
					visibleButtons[e % 6]['label'].grid_forget()

		def _swopHA():
			nonlocal wh, fired
			fired = False
			z.config(text = 'Away' if wh == 'first' else 'Home')
			wh = 'second' if wh == 'first' else 'first'
			_updateButtons(False)

		fired = False
		def _updateButtons(event):
			nonlocal fired
			if fired: return
			fired = True
			for e,t in enumerate(sorted(teams, key=lambda x: x['names'][-1])):
				if e <= startTeam-1: continue
				if e == startTeam + 6: break
				j = t[f'{wh} shirt']
				k = showJersey(j,'front',t[f'{wh} shorts'],t[f'{wh} socks'],t[f'{wh} shirt - colour 1'],t[f'{wh} shirt - colour 2'],t[f'{wh} shirt - colour 3'],t[f'{wh} shorts - colour 1'],t[f'{wh} shorts - colour 2'],t[f'{wh} socks - colour 1'],t[f'{wh} socks - colour 2'])
				n = t['names'][-1]
				jersey = ImageTk.PhotoImage(image = k)
				visibleButtons[e % 6]['button'].config(text = e, image = jersey)
				visibleButtons[e % 6]['button'].image = jersey
				visibleButtons[e % 6]['button']['command'] = lambda b=visibleButtons[e % 6]['button']: callback(b,wh,t)
				visibleButtons[e % 6]['label']['text'] = n
				buttons[e % 6] = visibleButtons[e % 6]['button']
				visibleButtons[e % 6]['button'].grid(row=int((e%6)*2/6)*2, column=(e%6)%3, padx=10, pady=10)
				visibleButtons[e % 6]['label'].grid(row=int((e%6)*2/6)*2+1, column=(e%6)%3, padx=10, pady=0)

		w = Scale(mainRoot, from_=0, to=int(len(teams)/6), orient="horizontal", length="500")
		w.bind("<ButtonRelease-1>", lambda x: _move(x))
		w.place(x=113,y=540)

		z = tk.Button(mainRoot, text='Home', command=_swopHA)
		z.place(x=650,y=540)

		mainRoot.bind('<Visibility>', _updateButtons)
		mainRoot.attributes("-topmost", True)
		mainRoot.mainloop()

		valori = open(f_valori, 'r+b')
		for tid, ql in queue.items():
			for ha, q in ql.items():
				q[0]()

def createNatTeamFlag(id):
	global decomp_path
	while True:
		path = input('Enter path of flag image ([c]ancel): ')
		if os.path.isfile(path): break
		if path == 'c': return
		
	currdir = os.getcwd()
	dp = decomp_path[0]
	if len(compress_command) == 0: return
	os.chdir(dp)
	
	flag_original = Image.open(path)
	flag_resize_big = flag_original.resize((60,39))
	
	flag_big_256 = flag_resize_big.convert("P", palette=Image.ADAPTIVE, colors=256)
	
	flag_big_bytes = io.BytesIO()
	flag_big_256.save(flag_big_bytes, format='BMP')
	flag_big_bytes = flag_big_bytes.getvalue()
	flag_fsh = b''
	fsh_header = b'SHPI\\\r\x00\x00\x01\x00\x00\x00GIMX'+id.encode('ascii')+b'\x18\x00\x00\x00{4\t\x00<\x00\'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	flag_fsh += fsh_header
	bmp_body = flag_big_bytes[1078:1078+60*39]
	bmp_body = [bmp_body[i:i+60] for i in range(0, len(bmp_body), 60)]
	bmp_body = b''.join(bmp_body[::-1])
	flag_fsh += bmp_body
	flag_fsh += b'\x2a' + 15*b'\x00'
	bmp_palette = [flag_big_bytes[54+i:54+i+3]+b'\xff' for i in range(0, 256*4, 4)]
	flag_fsh += b''.join(bmp_palette)
	o = open('tmp.fsh','wb')
	o.write(flag_fsh)
	o.close()
	os.system(f'{compress_command} "tmp.fsh" "{"/".join([gamepath.replace("common","fepack"),"igflags",id])}.pak"')
	
	flag_resize_sma = flag_original.resize((28,20))
	flag_sma_256 = flag_resize_sma.convert("P", palette=Image.ADAPTIVE, colors=256)
	flag_sma_bytes = io.BytesIO()
	flag_sma_256.save(flag_sma_bytes, format='BMP')
	flag_sma_bytes = flag_sma_bytes.getvalue()
	flag_fsh = b''
	fsh_header = b'\x7b\x40\x02\x00\x1c\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	flag_fsh += fsh_header
	bmp_body = flag_sma_bytes[1078:1078+28*20]
	bmp_body = [bmp_body[i:i+28] for i in range(0, len(bmp_body), 28)]
	bmp_body = b''.join(bmp_body[::-1])
	flag_fsh += bmp_body
	flag_fsh += b'\x24\x10\x03\x00\x00\x01\x01\x00\x00\x01' + 6*b'\x00'
	bmp_palette = [b''.join([flag_sma_bytes[54+i+2:57+i],flag_sma_bytes[54+i+1:56+i],flag_sma_bytes[54+i:55+i]]) for i in range(0, 256*4, 4)]
	flag_fsh += b''.join(bmp_palette)
	flag_fsh += b'\x006F\x00\x00\x00\x4C\x00\x00\x00\x76\x70\x61\x74\x68\x3D\x43\x3A\x5C\x46\x49\x46\x41\x27\x39\x38\x5C\x66\x65\x62\x69\x74\x73\x5C\x66\x6C\x61\x67\x73\x5C\x32\x30\x58\x32\x38\x5C\x66\x69\x6E\x61\x6C\x5C\x74\x67\x61\x73\x5C\x0D\x0A\x66\x6E\x61\x6D\x65\x3D'+id.encode('ascii')+b'x2E\x74\x67\x61\x0D\x0A\x73\x6E\x61\x6D\x65\x3D'+id.encode('ascii')+b'\x00'	
	os.chdir(currdir)
	feflags(add=id,data=flag_fsh)

def feflags(*spTeam,**kwargs):
	global decomp_path
	feflags_file = '/'.join([gamepath.replace('common','fepack'),'global','feflags.pak'])
	currdir = os.getcwd()
	dp = decomp_path[0]
	if len(compress_command) == 0: return
	os.chdir(dp)
	if not os.path.isfile('n_feflags.pak'):
		os.system(f'{decompress_command} feflags_original.pak n_feflags.pak') #NEW
	feflags = open('n_feflags.pak','rb')
	feflags.seek(0,0)
	feflags_parts = []
	feflags_parts.append(feflags.read(16))
	while True:
		if len(feflags_parts) > 1 and feflags.tell() == feflags_parts[1]['index']: break
		name = feflags.read(4)
		index = feflags.read(4)
		feflags_parts.append({'name':name.decode('iso-8859-1'), 'index':int.from_bytes(index, byteorder='little')})
	for e,_ in enumerate(feflags_parts):
		if e == 0: continue
		if e < len(feflags_parts)-1:
			_['image'] = feflags.read(feflags_parts[e+1]['index']-_['index'])
		else:
			_['image'] = feflags.read()
	if (teamToAdd:=kwargs.get('add',None)):
		data = kwargs['data']
		if teamToAdd not in [f['name'] for f in feflags_parts[1:]]:
			for image in feflags_parts[1:]:
				image['index'] += 8
			feflags_parts.append({'name':teamToAdd,'index':os.path.getsize('n_feflags.pak') + 8,'image':data})
		else:
			position = [f['name'] for f in feflags_parts[1:]].index(teamToAdd) + 1
			start_index = feflags_parts[position]['index']
			end_index = start_index + len(data)
			difference = end_index - (feflags_parts[position+1]['index'] if position < len(feflags_parts) -1 else os.path.getsize('n_feflags.pak'))
			for f in feflags_parts[position+1:]:
				f['index'] += difference
			feflags_parts[position] = ({'name':teamToAdd,'index':start_index,'image':data})
	else:
		tmn_flags = {}
		for t in teams:
			if t['league_id'] < 11: continue
			t_fsh = f'{t["id"]:0>4}'
			t_fsh_data = [f for f in feflags_parts[1:] if f['name'] == t_fsh]
			if len(t_fsh_data) == 0: continue
			tmn_flags[t['names'][-1]] = dict(t_fsh_data[0])
		for t in teams:
			if t['league_id'] >= 11: continue
			if spTeam and spTeam[0] != t['id']: continue
			t_fsh = f'{t["id"]:0>4}'
			t_nation = leagueNations[t['league_id']]
			t_fsh_data = dict(tmn_flags[t_nation])
			t_fsh_data['image'] = t_fsh_data['image'].replace(t_fsh_data['name'].encode('ascii'),t_fsh.encode('ascii'))
			shutil.copyfile('/'.join([gamepath.replace('common','fepack'),'IGFLAGS',f'{t_fsh_data["name"]}.pak']), '/'.join([gamepath.replace('common','fepack'),'IGFLAGS',f'{t_fsh}.pak']))
			bigFlagFile = open('/'.join([gamepath.replace('common','fepack'),'IGFLAGS',f'{t_fsh}.pak']),'rb')
			bigFlag = bigFlagFile.read().replace(t_fsh_data['name'].encode('ascii'),t_fsh.encode('ascii'))
			bigFlagFile.close()
			bigFlagFile = open('/'.join([gamepath.replace('common','fepack'),'IGFLAGS',f'{t_fsh}.pak']),'wb')
			bigFlagFile.write(bigFlag)
			bigFlagFile.close()
			t_fsh_data['name'] = t_fsh
			t_fsh_data['index'] = feflags_parts[-1]['index']+len(feflags_parts[-1]['image'])
			feflags_parts.append(t_fsh_data)
			for f in feflags_parts[1:]:
				f['index'] += 8
	
	new_file = feflags_parts[0][:8]+struct.pack('<h',len(feflags_parts[1:]))+feflags_parts[0][10:]
	for f in feflags_parts[1:]:
		new_file += f['name'].encode('ascii')
		new_file += struct.pack('<l',f['index'])
	for f in feflags_parts[1:]:
		new_file += f['image']
	nff = open('n_feflags.pak','wb+')
	nff.write(new_file)
	nff.close()
	os.system(f'{compress_command} n_feflags.pak "{feflags_file}"') #NEW
	os.chdir(currdir)
	return True

def write_tmmng():
	global tmmng_db
	startByte = 32
	n_teams = len(tmmng_db)
	tempFile = []
	tempFile.append(b'FCDB')
	tempFile.append(b'\x00\x00\x01\x00')
	tempFile.append(b'\x00\x00')
	tempFile.append(b'\x00\x00')
	tempFile.append(startByte.to_bytes(1,'big'))
	tempFile.append(b'\x00'*7)
	tempFile.append(b'\x00\x00')
	tempFile.append(b'\x00'*(startByte-len(b''.join(tempFile))))
	tempFile.append(n_teams.to_bytes(3,'little'))
	tempFile.append(b'\x06')
	for id in sorted(list(tmmng_db.keys())):
		t = tmmng_db[id]
		tactics = t['formation']
		tmp_bytes = id.to_bytes(2,'little')
		tmp_bytes = int.from_bytes(tmp_bytes, 'big') << 8
		defenders = int(tactics[0].split('d')[0])
		midfielders = int(tactics[1].split('d')[0])
		forwards = int(tactics[2].split('d')[0])
		d_def = 'd' in tactics[0]
		d_mid = 'd' in tactics[1]
		d_for = 'd' in tactics[2]
		tmp_bytes += (midfielders & 3) << 14
		tmp_bytes += (midfielders & 4) >> 2
		tmp_bytes += defenders-d_def << 11
		tmp_bytes += forwards << 1
		tmp_bytes += d_for << 7
		tmp_bytes += d_mid << 6
		tmp_bytes += d_def << 5
		tmp_bytes += 16
		tempFile.append(tmp_bytes.to_bytes(3,'big'))
		tempFile.append(b'\x00')
		for i in range(5):
			pos1 = _conv_position(*t['positions'][i*2])
			pos2 = _conv_position(*t['positions'][i*2+1])
			posBytes = [0,0,0]
			posBytes[0] = ((pos1&15) << 4) | ((pos1 >> 8) & 15)
			posBytes[1] = ((pos2 >> 8) << 4) | ((pos1 & 240) >> 4)
			posBytes[2] = pos2 & 255
			tempFile.append(bytes(posBytes))
			abByte = (t['attack'][i*2] | t['attack'][i*2+1] << 4).to_bytes(1,'big')
			tempFile.append(abByte)
		stratAnd11 = [0,0]
		pos11 =  _conv_position(*t['positions'][-1])
		stratAnd11[0] = ((pos11&15) << 4) | ((pos11 >> 8) & 15)
		stratAnd11[1] = (t['strategy'] << 4) | ((pos11 & 240) >> 4)
		tempFile.append(bytes(stratAnd11))
		tempFile.append(b'\x00\x00\x00\x00\x00')
		tempFile.append((t['attack'][-1] << 4).to_bytes(1,'big'))
		tempFile.append(3*b'\x00')
		tempFile.append((t['aggression'][-1] << 4).to_bytes(1,'big'))
		tmppl = b''
		for i,p in enumerate(t['lineup']):
			pl_id = int(p, base=16)
			if i % 2 == 0:
				tmppl = pl_id.to_bytes(2,'big')
			else:
				tmppl = int.from_bytes(tmppl, 'big') << 16
				tmppl += (pl_id & 64512) >> 2
				tmppl += (pl_id & 768) << 14
				tmppl += (pl_id & 60) >> 2
				tmppl += (pl_id & 3) << 14
				if i > 2: tmppl += t['aggression'][i//2] << 4
				tmppl = tmppl.to_bytes(4,'big')
				tempFile.append(tmppl)
				tmppl = b''
		for i,p in enumerate(t['set_piece']):
			pl_id = int(p, base=16)
			if i % 2 == 1:
				tmppl = pl_id.to_bytes(2,'big')
				if i == 9: tempFile.append(tmppl)
			else:
				tmppl = int.from_bytes(tmppl, 'big') << 16
				tmppl += (pl_id & 64512) >> 2
				tmppl += (pl_id & 768) << 14
				tmppl += (pl_id & 60) >> 2
				tmppl += (pl_id & 3) << 14
				tmppl += t['aggression'][i//2+5] << 4
				tmppl = tmppl.to_bytes(4,'big')
				tempFile.append(tmppl)
				tmppl = b''
	tempFile[2] = len(b''.join(tempFile)).to_bytes(2,'little')
	tempFile[6] = (len(b''.join(tempFile))-startByte).to_bytes(2,'little')
	o = open(f'{Fifapath}/tmmng.dec','wb')
	o.write(b''.join(tempFile))
	o.close()
	data = io.BytesIO()
	data.write(b''.join(tempFile))
	read_tmmng(data)		

def _conv_position(latitude,longitude):
	pos = ((longitude & 3) << 8) + (latitude << 4) + ((longitude & 12) >> 2)
	return pos

def _read_position(pos):
	latitude = (pos & 240) >> 4
	longitude = ((pos >> 8) & 3) + ((pos & 3) << 2)
	return [latitude, longitude] 

def read_tmmng(*arg,**kwargs):
	global decomp_path, tmmng_db
	t_verbose = kwargs.get('verbose',False)
	tmmng = gamepath.replace("common","user")+"/tmmng.db"
	currdir = os.getcwd()
	if kwargs.get('refresh',None) or not os.path.isfile(f'{Fifapath}/tmmng.dec'):
		if len(compress_command) == 0: return
		os.chdir(decomp_path[0])
		if os.path.isfile(tmmng): os.system(f'{decompress_command} "{tmmng}" "{Fifapath}/tmmng.dec"')
		else: return
	tmmng = open(f'{Fifapath}/tmmng.dec', 'rb')
	if arg: tmmng = arg[0]
	if t_verbose:
		tmmng.seek(8,0)
		print ('file size:', int.from_bytes(tmmng.read(2),'little'))
	tmmng.seek(12,0)
	init_byte=int.from_bytes(tmmng.read(1),'little')
	if t_verbose:
		print ('init byte:', init_byte)
		tmmng.seek(20,0)
		print ('whole team-data length:', team_data_length:=int.from_bytes(tmmng.read(2),'little'))
	tmmng.seek(init_byte,0)
	n_teams = int.from_bytes(tmmng.read(2),'little')
	if t_verbose:
		print('number of teams:', n_teams)
	tmmng.seek(2,1)
	for i in range(n_teams):
		teamBytes = tmmng.read(2)
		teamBytes = struct.unpack('<h', (teamBytes[0].to_bytes(1, 'little') + (teamBytes[1]&3).to_bytes(1, 'little')))[0]
		if t_verbose:
			team = None
			for t in teams:
				if t['id'] == teamBytes:
					team = t
					break
			print(team['names'][-1])
		db_entry = tmmng_db.setdefault(teamBytes,{})
		tmmng.seek(-1,1)
		tactics_bits = tmmng.read(2)
		midfield = (tactics_bits[0] & 192) >> 6
		def_l1 = (tactics_bits[0] & 56) >> 3
		def_l2 = (tactics_bits[0] & 12) >> 2
		mid_bit = tactics_bits[1] & 1
		strikers = (tactics_bits[1] & 14) >> 1
		att_line = (tactics_bits[1] & 128) >> 7
		mid_line = (tactics_bits[1] & 64) >> 6
		def_line = (tactics_bits[1] & 32) >> 5
		if t_verbose: print(midfield,def_l1,def_l2,strikers,sep='\n')
		formation = [int(def_l1)+int(def_line),int(midfield+4*mid_bit),int(strikers)]
		if t_verbose: print(formation, ['diamond'*y for y in [int(att_line),int(mid_line),int(def_line)]])
		diamond = ['d'*y for y in [int(def_line),int(mid_line),int(att_line)]]
		db_entry['formation'] = [f'{f}{diamond[e]}' for e,f in enumerate(formation)]
		db_entry['positions'] = []
		db_entry['aggression'] = [0] * 11
		db_entry['attack'] = []
		tmmng.seek(1,1)
		for i in range(5):
			posBytes = tmmng.read(3)
			pos1 = ((posBytes[1] & 15) << 4 | (posBytes[0] & 240) >> 4) | ((posBytes[0] & 15) << 8)
			pos2 = posBytes[2] | ((posBytes[1] & 240) << 4)
			db_entry['positions'].append(pos1)
			db_entry['positions'].append(pos2)
			abByte = tmmng.read(1)
			abByte1 = abByte[0] & 15
			abByte2 = (abByte[0] & 240) >> 4
			db_entry['attack'].append(abByte1)
			db_entry['attack'].append(abByte2)
		stratAnd11 = tmmng.read(2)
		db_entry['positions'].append(((stratAnd11[1] & 15) << 4 | (stratAnd11[0] & 240) >> 4) | ((stratAnd11[0] & 15) << 8))
		db_entry['strategy'] = (stratAnd11[1] & 240) >> 4
		db_entry['positions'] = [_read_position(p) for p in db_entry['positions']]
		if t_verbose: print('Strategy: ',db_entry['strategy'])
		tmmng.seek(5,1)
		db_entry['attack'].append((tmmng.read(1)[0] & 240) >> 4)
		tmmng.seek(3,1)
		db_entry['aggression'][-1] = (tmmng.read(1)[0] & 240) >> 4
		init_players = tmmng.tell()
		db_entry['lineup'] = []
		for i in range(11):
			if i % 2 == 0:
				pl_bytes = tmmng.read(2)
				pl_id = pl_bytes[0].to_bytes(1, 'little') + (pl_bytes[1]&63).to_bytes(1, 'little')
			else:
				tmmng.seek(-1,1)
				pl_bytes = tmmng.read(3)
				pl_id = (((pl_bytes[1] & 63) << 2) + ((pl_bytes[0]&192) >>6)).to_bytes(1, 'little') + (((pl_bytes[2]
				& 15)  << 2) + ((pl_bytes[1] & 192) >> 6)).to_bytes(1, 'little')
			db_entry['lineup'].append("{:04X}".format(int.from_bytes(pl_id, 'big')))
		init_setpiece = tmmng.tell()
		db_entry['set_piece'] = []
		for e in range(1,10):
			if e % 2 == 0:
				pl_bytes = tmmng.read(2)
				pl_id = pl_bytes[0].to_bytes(1, 'little') + (pl_bytes[1]&63).to_bytes(1, 'little')
			else:
				tmmng.seek(-1,1)
				pl_bytes = tmmng.read(3)
				pl_id = (((pl_bytes[1] & 63) << 2) + ((pl_bytes[0]&192) >>6)).to_bytes(1, 'little') + (((pl_bytes[2]
				& 15)  << 2) + ((pl_bytes[1] & 192) >> 6)).to_bytes(1, 'little')
			db_entry['set_piece'].append("{:04X}".format(int.from_bytes(pl_id, 'big')))
		tmmng.seek(init_players+4,0)
		for e in range(9):
			tmmng.seek(3,1)
			db_entry['aggression'][e+1] = (tmmng.read(1)[0] & 240) >> 4
		if t_verbose:
			for i in range(11):
				print(players_db.get(db_entry['lineup'][i], {}).get('name','?'), db_entry['aggression'][i], db_entry['attack'][i],db_entry['positions'][i])
			for i in range(9):
				print(setpiece[i], players_db.get(db_entry['set_piece'][i], {}).get('name','?'),sep='\t')
	os.chdir(currdir)

def saveIntLeagues():
	print(json.dumps({l['db_position']:{k:l[k] for k in ['name','index_fcdbpeng','id','index_fcdb','size','teams']} for l in leagues}), file = open(os.path.join(Fifapath,'original.json'), 'w+'))

def main_menu():
	os.system(clear_screen)
	global case_sensitive
	commands = [
		('Show/edit leagues','os.system(clear_screen);show_leagues()'),
		('Search/edit team(s)','os.system(clear_screen);global debug, jerseys; jerseys = False; debug = False; show_teams()'),
		('Show/edit all jerseys','show_all_kits()'),
		('Search/edit player(s), list view','os.system(clear_screen);global table, debug; table = False; debug = False; initialize()'),
		('Search/edit player(s), table view','os.system(clear_screen);global table, debug; table = True; debug = False; initialize()'),
		('Add player to database','os.system(clear_screen);add_player(True)'),
		('Duplicate player','os.system(clear_screen);duplicate_player()'),
		('Delete player','os.system(clear_screen);delete_player()'), 
		('Add team to database','os.system(clear_screen);add_team()'),
		('Duplicate team','os.system(clear_screen);duplicate_team()'),
		('Delete team','os.system(clear_screen);delete_team()'), 
		('Matchday','os.system(clear_screen); match_day()'),
		('List all players','os.system(clear_screen);general_list()'),
		('List all players by role','list_by_role()'),
		('Export database as JSON file','export_database()'),
		('Debug mode','os.system(clear_screen);global table, debug; print("#### Debug mode ####\\n"); debug = True; table=False; load_database(); initialize(True)'),
		('Select game folder','ch_game_path()'),
		('Select language','ch_lang()'),
		('Save to game','commit()'),
		('Reload tmmng.db','read_tmmng(refresh=True)'),
		('Backup current leagues','saveIntLeagues()'),
		('Restore previous database version','restore()'),
		('Exit','sys.exit()')
	]
	while True:
		os.system(clear_screen)
		print('┏{:━^44}┓'.format(' MAIN MENU '))
		print('┃%s┃'%(' '*44))
		print('\n'.join(['┃ {:<42} ┃'.format('[%s] %s'%(index,command[0])) for (index,command) in enumerate(commands)]))
		print('┃%s┃'%(' '*44))
		print('┗%s┛'%('━'*44))
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
\033[16CFIFA RTWC 98 Python Editor, by megas_alexandros@hotmail.com.
\033[18C(c) 2022. This code is distributed on the MIT License.

The editor needs at least a 201-column terminal window to display correctly. Please resize
window/font accordingly.

The editor works on a copy of the game database files and creates a backup copy whenever
saves are copied into the game files.

In the interface, all commands are indicated in square brackets. For instance: [buy] means
that the command to be entered is "buy". [e] means that the command is just the letter "e".
Enter values without the brackets or quotes. [ync] means: 'enter "y" for yes, enter "n" for
no, enter "c" to cancel'.

""")
	entries = [
"""
\033[30C------ SHOW/EDIT LEAGUES ------

Displays lists of teams of all leagues in a carousel (use arrow keys to navigate). The ac-
tive league is printed in yellow.

Commands:
[n] switches the view to national teams
[c] switches the view to clubs
[e] opens the editing window.

Leagues can be edited ([e]) in the following ways:
- They can be renamed.
- They can exchange teams.
- Their size of leagues can be expanded or reduced to any size between 2 and 30. WARNING:
  CHANGING LEAGUE SIZES MAKES THEM UNPLAYABLE AS LEAGUES IN THE GAME. Teams can be used in 
  friendlies etc. 
  Expansion is only possible if there are league-less teams to be added; reduction releases
  teams from the league.
- League teams can replace national teams. Doing so requires adding a flag for the team to
  the game graphics. One can select any flag from the national team ones. This operation
  requires decompressing/compressing the EA graphics files, for which the MS-DOS utility 
  RefPack Tool is needed (https://github.com/MicaelJarniac/RefPack-Tool), and can only be
  performed on a Windows/PC machine. The replaced national team is not removed from the 
  database and can be restored in place using the same procedure.
- Restore original ([o]) restores the selected league to the latest backup point.

""",
"""
\033[30C------ SEARCH/EDIT TEAMS ------

Search for a team by its name. If more than one team is found, each team is displayed se-
quentially. The command [n] moves on to the next team, while [c]ancel returns to the main
menu. The command [e] lets the user edit the team. [k] shows a rendering of the team's ho-
me and away kits in a new window. [r] resets the edits to the team done in Team Management
in the game and stored in tmmng.db. [s] loads the list of all players in the team from which
data for each player can be accessed (displayed as in FORM VIEW). When a player's file is
loaded, [r] returns to the team file, while [s] reloads the list of players and [c] returns
to the main menu.

Notes:

(1) In the squad list, players are ordered by average (which is displayed together with
their role) unless a proper lineup is created in the editor. If a lineup was selected,
players are listed by role (Goalkeeper, Sweeper if any, Defenders right to left, Midfielders
r->l, Forwards r->l).
(2) If the number of players in the team is smaller than the size of the
roster for that team in the database, the current number of players is displayed in bra-
ckets next to the value for 'Roster Size'. If this happens, the last player in the team
list will appear twice in the Player Transfer lists in the game. The problem can be fixed
by buying or selling players to match a legal roster size (12, 14, 16, 18, or 20 players).
(3) Recommended Tactics shows the tactics that would employ the best 11 players in the
team (sometimes these tactics are impossible, if the roster is unbalanced). Roles to Im-
prove for Current Tactics indicates which roles should be strengthened in order to have a
balanced roster to play with the currently active tactics.

Notes on editing commands:

- [fk] --> first kit, [sk] --> second kit. Jersey type names can be customized by populat-
  ing the jersey_types array in fifa_config.json. Custom jerseys (JERSxx.fsh with xx > 32 
  in the game folder ingame/PLAYER/TEXTURES/PLYRKITS) can be added by listing them in the
  custom_jerseys property in fifa_config.json (in the nested array).
- forma[t]ion: custom formations may be added in the same way as in Team Management. Three
  divisions may be selected (defense, midfield, attack) with min. 2 and max. 5 players each.
  Custom lineups are stored in tmmng.db in the USER folder (unlike the standard ones, which
  are stored in the database files in the COMMON folder).
- [l]ineup (for clubs only): select the starting eleven, role by role, for the current tac-
  tics, as required by the game algorithm. The lineup will be applied if team management
  is reset in the game. Selectable players are listed for each role, together with their
  skill average. Lineups of national teams may not be edited (due to potential conflicts
  with the status of players in clubs) and should be adjusted in the game.
  If a custom formation is selected, any player may be selected for any position (like in
  Team Management). If this is the case, lineups are stored in tmmng.db in the USER folder
  (not in the database files in the COMMON folder).
- s[e]t piece taker: selects the player (from the starting eleven) that should have the
  highest 'Shot Power' score and that the game will automatically pick as the free kick
  and penalty taker. NB: it might be necessary to select the starting lineup in the editor
  before selecting the set piece taker.
  If 'Select a piece taker for each set piece' is chosen, it will be possible to select
  takers for each set piece like in Team Management from the starting lineup. CKL = left
  corner kick, CKR = right corner kick, FK = free kick, PK = penalty kick, PK1–5 = penalty
  kicks in knockout games. Custom set piece takers are stored in tmmng.db in the USER folder
  (not in the database files in the COMMON folder).
- [p]layers: loads all players in TABLE VIEW for further editing.
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
\033[30C------ SHOW/EDIT ALL JERSEYS ------

Displays a window with the jerseys of all the teams. Clicking each jersey opens a new
window that enables the user to choose a different jersey for the corresponding team.

""",
"""
\033[23C------ SEARCH/EDIT PLAYERS, FORM VIEW ------

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

Found players are listed in a menu and can be selected for viewing and editing. Values are
displayed in a 2-column form. Users can select players for editing.

The descriptors for skin colour, face type, facial hair, and hair styles can be customized
by populating properties in fifa_config.json (skin_cl, faces, beards, hairs). This file is
contained in the Python module (Mac: /Library/Frameworks/Python.framework/Versions/[version
number]/lib/python[version number]/site-packages/fifa98edit; Win: /lib/site-packages in your
Python folder).

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

When editing the role of a player, it will be possible to select roles that are not there
in the in-game editor: LCB, RCB, LCM, RCM. These roles specify if a player must be the left
or right centre back if team tactics have an odd number of defenders (3-5-2, 5-3-2, 3-4-3,
5-4-1). LCM and RCM do the same job for tactics where midfielders are in odd number (4-3-3,
5-3-2, 3-5-2). For 3-5-2, 5-3-2 and 5-4-1, CB (not SW!) selects the sweeper.
NB: These roles only apply to players in the starting lineup.

""","""
\033[23C------ SEARCH/EDIT PLAYERS, TABLE VIEW ------

Search players by name, with player values are displayed as a table, with a row for each
player. This option is recommended if comparing players or editing more than one player at
a time and is default when players are edited in team editing mode. To search for multiple
names, separate them with a slash (e.g. Name1/Name2). It is also possible to search other
fields than the name. Field names must be enclosed in a pair of @ signs and the searched
value must follow immediately (e.g. @field@value).

The following fields can be searched: country, jersey, role, team, international, speed,
acceleration, agility, aggression, attack bias, ball, awareness, fitness, creativity,
passing, passing bias, heading, reaction, tackle, shot bias, shot power, shot accuracy,
average. 'International' selects players in the squad of the desired national team (e.g.
@international@Spain).

Multiple fields can be searched and must be separated by a semicolon (e.g. @speed@91;@role@CB).
The following comparison operators can be used for numeric fields: >, >=, <, <= (e.g.
@speed@>91).

The table can be sorted by each field (default is by name); the user will be prompted to
select one after entering the value to be searched.

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
\033[27C------ ADD PLAYER TO DATABASE ------

Creates a new player and loads it up for editing. New players will be listed as 'free agents'
when buying a player (in SEARCH/EDIT TEAMS) or will be callable to a national team.

""","""
\033[34C---- DUPLICATE PLAYER ----

Duplicates a player and loads it up for editing. The duplicate will be listed as a 'free agent'
when buying a player (in SEARCH/EDIT TEAMS) or will be callable to a national team.

""","""

\033[27C---- DELETE PLAYER FROM DATABASE ----

*Permanently* deletes a player and removes him from all teams.

""","""
\033[27C------ ADD TEAM TO DATABASE ------

Creates a new team and loads it up for editing. New teams will be available for adding to
leagues if leagues are expanded or in exchange for an existing team, which will be released
from the league. New teams are empty and can be populated by buying players from existing
teams or by adding free-agent players (new players, players of national teams).
If the team is a National Team, the user is prompted to add a flag (the path to a PNG or
BMP file should be provided).
This operation requires decompressing/compressing the EA graphics files, for which the 
MS-DOS utility RefPack Tool is needed (https://github.com/MicaelJarniac/RefPack-Tool), and 
can only be performed on a Windows/PC machine.
Once it is created, the new national team may be added to a national team group by swopping
it with an existing one (see SHOW/EDIT LEAGUES). The new nationality may be selected for
players to be callable into the national team.

""","""
\033[34C---- DUPLICATE TEAM ----

Duplicates a team. Duplicate teams will be available for adding to leagues if leagues
are expanded or in exchange for an existing team, which will be released from the league.

""","""
\033[27C---- DELETE TEAM FROM DATABASE ----

*Permanently* deletes a team. This option is only available for league-less teams. Release
any teams you may wish to delete. Team players will be released as free-agents.

""","""
\033[34C------ MATCHDAY ------

Select two teams and display their lineup and substitutes. For national teams, the lineup
is automatically selected by the game (see help on team editing) and this option does not
display the correct one.

If clubs are selected, players are listed according to their position. The displayed data
includes their number, role, average, and nationality. If national teams are selected, the
lineup order is simply a selection of the strongest players in each role; instead of the
players' nationality, their club team (if any) is displayed.

""","""
\033[30C------ LIST ALL PLAYERS ------

Prints a table listing all players divided by position (Goalkeepers, Defenders, Midfield-
ers, Forwards) and sorted by the average of their skill points. The table also shows their
club team (if any) and nationality. If players are capped for a national team, an asterisk
is displayed next to their nation.

""","""
\033[30C------ LIST ALL PLAYERS BY ROLE ------

Prints a table listing all players divided for each role (GK, LB, CB, etc.) sorted by the
average of their skill points. The table also shows their club team (if any) and nationa-
lity. If players are capped for a national team, an asterisk is displayed next to their
nation. If they are in the starting XI of a club, an asterisk is displayed next to their
team name.

""","""
\033[31C------ EXPORT DATABASE AS JSON FILE------

Dumps the whole database to the JSON file "complete_db.json" in the script folder.

""","""
\033[38C------ DEBUG MODE ------

Automatic checks for:
- Unacceptable roster sizes (see help on team editing).
- Duplicate jersey numbers in club teams. Users are prompted if they wish to change one of
  the player's number to an automatically selected available one.
- Duplicate player names in the database.

Users may also select a player and display the binary code of the corresponding database
record in a tabular view (as in search/edit players, table view). All bits for each byte
are displayed.

""","""
\033[29C------ SELECT GAME FOLDER ------

Select location of FIFA RTWC 98. Enter absolute path.

""","""
\033[31C------ SELECT LANGUAGE ------

Select the language used in the game in order to edit the corresponding name databases.

""","""
\033[32C------ SAVE TO GAME ------

Save the changes made in the editor to the game database files. If changes are not saved to
game, they will only be stored in the files the editor works on.

""","""
\033[22C------ RELOAD TMMNG.DB ------

Load or reload the changes made in the game using Team Management into the editor.
""","""
\033[22C---- BACKUP CURRENT LEAGUES & NATIONAL TEAM GROUPS ----

Creates a new restore point for leagues and national team groups.

""","""

\033[22C------ RESTORE PREVIOUS DATABASE VERSION ------

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
	print("\x1b[8;53;201t", end = '')

#load settings		
gamepath = gamepath[0]
lang = lang[0]

gamepath = ch_game_path(wait=True) if gamepath == '' else gamepath
if not gamepath: sys.exit()

for f in os.listdir(j_dir:=os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS')):
	if f[-3:].lower() == 'fsh':
		fsh = open(os.path.join(j_dir,f),'rb')
		fsh.seek(46512,0)
		jersey_types[(jt:=int(f[4:6]))-1] = jname if (jname:=fsh.read().split(b'\x00')[0].decode('utf-8')) else f
lang = ch_lang(wait=True) if lang == '' else lang
if not lang: sys.exit()

try:
	heads = open(os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','COMMON','HIHEAD.FSH'), 'rb')
	heads.seek(74,0)
	if heads.read(2).decode('ascii') == '07': WorldCupFaces = True
except:
	pass

filenames = ["FCDBPENG.DBI","FCDB.DBI","FCDB_%s.DBI"%lang,"FC%s.BIN"%lang]

Fifapath = os.path.dirname(os.path.realpath(__file__))+'/FifaDb'
f_nomi, f_valori, f_squadre, f_interfaccia = ["%s/%s"%(Fifapath,fn) for fn in filenames]

if not os.path.isdir(Fifapath):
	print('Initializing...')
	os.mkdir(Fifapath)
	restore(True)

#establish compress/decompress command #NEW
if len(decomp_path[0]) == 0:
	while True:
		nf = input('Enter folder of Refpack compressor/decompressor executables: ')
		if os.path.isdir(nf) and os.path.isfile(os.path.join(nf,'compressd.exe')) and os.path.isfile(os.path.join(nf,'decompressd.exe')):
			custom_vals['decomp_path'] = [nf]
			json.dump(custom_vals, open('fifa_config.json', 'w'), indent=2)
			decomp_path, dp = [nf], nf
			break
		else:
			print('Utilities not found.')
if len(decomp_path[0]) > 0:
	if platform.system() == "Windows":
		compress_command = 'compressd'
		decompress_command = 'decompressd'
	else:
		if os.system('wine --version') == 0:
			compress_command = 'wine compressd.exe'
			decompress_command = 'wine decompressd.exe'
		else:
			input('Warning: If you wish to edit flags and team management load the Wine environment first.')

if sum([fn in os.listdir(Fifapath) for fn in filenames]) < len(filenames): restore()
else:
	try: load_database()
	except KeyboardInterrupt:
		sys.exit()
	except:
		print('The database files are corrupt. Restoring from last saved version.')
		restore()
read_tmmng()
from display_jerseys import *
main_menu()
