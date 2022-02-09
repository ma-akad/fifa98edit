import os
import platform
import json
jerseys = [
            """
            
            ░░░░░░░▙▃▟░░░░░░░
            ░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░░░░╚╩╝░░░░░░░
            ░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ββββ░░░▙▃▟░░░ββββ
            ░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            β░░░░░░▙▃▟░░░░░░β
            β░░░░░░░░░░░░░░░β
            β░░░░░░░░░░░░░░░β
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            β░░░░░░▙▃▟░░░░░░β
            β░░░░░░░░░░░░░░░β
            β░░░░░░░░░░░░░░░β
                ░γ░░░░░γ░
                βγ░░░░░γβ
                βγ░░░░░γβ
                βγ░░░░░γβ
                βγ░░░░░γβ
""","""

            ββββ░░░▙▃▟░░░ββββ
            ββββ░░░░░░░░░ββββ
            ββββ░░░░░░░░░ββββ
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░░░β╚╩╝β░░░░░░
            ░░░░░░βββββ░░░░░░
            ░░░░░░βββββ░░░░░░
                ░░βββββ░░
                ░░βββββ░░
                ░░βββββ░░
                ░░βββββ░░
                ░░βββββ░░
""","""

            ░░░░░░░╚╩╝░░░░░░░
            ░░░░░░░βββ░░░░░░░
            ░░░░░░░βββ░░░░░░░
                ░░░βββ░░░
                ░░░βββ░░░
                ░░░βββ░░░
                ░░░βββ░░░
                ░░░βββ░░░
""","""

            ░░░░░░░╚╩╝░░░░░░░
            ░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░░░░░░░░
                βββββββββ
                βββββββββ
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            βββββββ╚╩╝βββββββ
            ░░░░βββββββββ░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░β░░▙▃▟░░β░░░░
            ░░░░β░░░░░░░β░░░░
            ░░░░β░░░░░░░β░░░░
                β░░░░░░░β
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░β░β╚╩╝β░β░░░░
            ░░░░β░β░░░β░β░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░β░░╚╩╝░░β░░░░
            ░░░░β░░░░░░░β░░░░
            ░░░░β░░░░░░░β░░░░
                β░░░░░░░β
                β░░░░░░░β
                β░░░░░░░β
                β░░░░░░░β
                β░░░░░░░β
""","""

            ░░░░β░░╚╩╝βββ░░░░
            ░░░░β░░░░ββββ░░░░
            ░░░░β░░░░ββββ░░░░
                β░░░░ββββ
                β░░░░ββββ
                β░░░░ββββ
                β░░░░ββββ
                β░░░░ββββ
""","""

            βββββββ▙▃▟βββββββ
            ░░░░░βββββββ░░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░░░░╚╩╝░░░░░░░
            ░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░░░░░░░░
                βββββββββ
                γγγγγγγγγ
                βββββββββ
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            βββββββ╚╩╝βββββββ
            ░░░βββββββββββ░░░
            ░░░░░░░βββ░░░░░░░
                ░░░βββ░░░
                ░░░βββ░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ββββ░░β╚╩╝░░░ββββ
            ░░░░░░ββ░░░░░░░░░
            ░░░░░░ββ░░░░░░░░░
                ░░ββ░░░░░
                βββββββββ
                βββββββββ
                ░░ββ░░░░░
                ░░ββ░░░░░
""","""

            ββββ░░░▙▃▟░░░ββββ
            ░░░░░░░░░░░░░░░░░
            ░░░░βββββββββ░░░░
                ░░░░░░░░░
                βββββββββ
                ░░░░░░░░░
                βββββββββ
                ░░░░░░░░░
""","""

            ░░░░░░░╚╩╝░░░░░░░
            βββββββββββββββββ
            βββββββββββββββββ
                —————————
                βββββββββ
                βββββββββ
                —————————
                βββββββββ
""","""

            ░░░░░░░└─┘░░░░░░░
            βββββ░░░░░░░βββββ
            ββββββ░░░░░ββββββ
                ββ░β░β░ββ
                ββ░β░β░ββ
                ββ░β░β░ββ
                ββ░β░β░ββ
                ββ░β░β░ββ  
""","""

            ββββ░β░╚╩╝░β░ββββ
            ░░░░░β░░β░░β░░░░░
            ░░░░░β░░β░░β░░░░░
                ░β░░β░░β░
                ░β░░β░░β░
                ░β░░β░░β░
                ░β░░β░░β░
                ░β░░β░░β░
""","""

            γ░░░ββ░▙▃▟░ββ░░░γ
            γ░░░ββ|░░░|ββ░░░γ
            γ░░░ββ|░░░|ββ░░░γ
                ββ|░░░|ββ
                ββ|░░░|ββ
                ββ|░░░|ββ
                ββ|░░░|ββ
                ββ|░░░|ββ
""","""

            ░░░░β░β╚╩╝β░β░░░░
            ░░░░β░β░░░β░β░░░░
            ░░░░β░β░░░β░β░░░░
                β░β░░░β░β
                β░β░░░β░β
                β░β░░░β░β
                β░β░░░β░β
                β░β░░░β░β
""","""

            ░░░░βγβ▙▃▟βγβ░░░░
            ░░░░░βγβγβγβ░░░░░
            ░░░░░░βγβγβ░░░░░░
                ░░░βγβ░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ░░░░β░β▙▃▟β░β░░░░
            ░░░░░β░β░β░β░░░░░
            ░░░░β░β░β░β░β░░░░
                ░β░β░β░β░
                β░β░β░β░β
                ░β░β░β░β░
                β░β░β░β░β
                ░β░β░β░β░
""","""

            ░░░░░░░▙▃▟βββ░░░░
            ░░░░░░░░βββββ░░░░
            ░░░░░░░░βββββ░░░░
                ░░░░βββββ
                ββββ░░░░░
                ββββ░░░░░
                ββββ░░░░░
                ββββ░░░░░
""","""

            ░░░░β░β▙▃▟β░β░░░░
            ░░░░β░β░░░β░β░░░░
            ░░░░β░β░░░β░β░░░░
                ░░β░░░β░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
""","""

            ββββ░░░└─┘░βγββββ
            ββββ░░░░░░░βγββββ
            ββββ░░░░░░░βγββββ
                ░░░░░░░βγ
                ░░░░░░░βγ
                ░░░░░░░βγ
                ░░░░░░░βγ
                ░░░░░░░βγ
""","""

            ░░░░ββ░╚╩╝░░░░░░░
            ░░░░░ββ░░░░░░░░░░
            ░░░░░░ββ░░░░░░░░░
                ░░░ββ░░░░
                ░░░░ββ░░░
                ░░░░░ββ░░
                ░░░░░░ββ░
                ░░░░░░░ββ
""","""

            ░░░░░░░╚╩╝░ββ░░░░
            ░░░░░░░░░░ββ░░░░░
            ░░░░░░░░░ββ░░░░░░
                ░░░░ββ░░░
                ░░░ββ░░░░
                ░░ββ░░░░░
                ░ββ░░░░░░
                ββ░░░░░░░
""","""

            ░░░░░░░╚╩╝░░░░░░░
            ░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░βββββ░░
                ░ββ░░░░░░
                ░ββ░░░░░░
""","""

            ░░░βββ░╚╩╝░░░░░░░
            ░░░░░░ββββββ░░░░░
            ░░░░░ββ░β░░░░░░░░
                βββ░░β░░░
                βββ░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
                ░░░░░░░░░
"""
]

custom_vals = json.loads(open('fifa_config.json', 'r').read())
		
gamepath = custom_vals['gamepath'][0]

for f in os.listdir(j_dir:=os.path.join(gamepath.replace('common','ingame'),'PLAYER','TEXTURES','PLYRKITS')):
	if f[-3:].lower() == 'fsh':
		if (jt:=int(f[4:6])) > len(jerseys): jerseys.append([10*"\n"])

def colorize(colour, *args):
	symbol = args[0] if args else " "
	colours = [
		'\033[48;5;204m',
		'\033[48;5;124m',
		'\033[48;5;52m',
		'\033[48;5;208m',
		'\033[48;5;202m' ,
		'\033[48;5;1m',
		'\033[48;5;220m',
		'\033[48;5;214m',
		'\033[48;5;136m',
		'\033[48;5;76m',
		'\033[48;5;28m',
		'\033[48;5;22m',
		'\033[48;5;32m',
		'\033[48;5;25m',
		'\033[48;5;19m',
		'\033[48;5;18m',
		'\033[48;5;134m',
		'\033[48;5;91m',
		'\033[48;5;56m',
		'\033[48;5;15m',
		'\033[48;5;249m',
		'\033[48;5;241m',
		'\033[48;5;237m',
		'\033[0m'
	]
	output = colours[colour]+symbol+'\033[0m'
	if args: output = output.replace(symbol, colours[args[1]].replace('48','38')+symbol)
	if platform.system() == 'Windows':
		colours = [
			'\033[95;47m▒',
			'\033[41m ',
			'\033[91;40m▒',
			'\033[91;43m▒',
			'\033[31;43m▒',
			'\033[33;41m▒',
			'\033[33;103m▒',
			'\033[97;43m▒',
			'\033[43m ',
			'\033[102m ',
			'\033[42m ',
			'\033[34;42m▒',
			'\033[104m ',
			'\033[44m ',
			'\033[30;44m▒',
			'\033[34;40m▒',
			'\033[105;97m▒',
			'\033[105m ',
			'\033[45m ',
			'\033[107m ',
			'\033[100m ',
			'\033[30;100m▒',
			'\033[0;90m▒'
			'\033[0m'
		]
		colours_fg = [
			'\033[95m',
			'\033[31m',
			'\033[91m',
			'\033[33m',
			'\033[33m',
			'\033[33m',
			'\033[93m',
			'\033[97m',
			'\033[33m',
			'\033[92m',
			'\033[32m',
			'\033[34m',
			'\033[96m',
			'\033[94m',
			'\033[34m',
			'\033[34m',
			'\033[97m',
			'\033[95m',
			'\033[35m',
			'\033[97m',
			'\033[90m',
			'\033[90m',
			'\033[90m',
			'\033[0m'
		]
		symbol = symbol.replace("▃", "\u2584").replace("▙", "\u2588").replace("▟", "\u2588")
		if args: output = colours[colour][:-1]+colours_fg[args[1]]+symbol+'\033[0m'
		else: output = colours[colour]+'\033[0m'
	return output
def display_jersey(type, col1, col2, col3):
	return('%s'%jerseys[type]\
		.replace("░",colorize(col1))\
		.replace("β",colorize(col2))\
		.replace("γ",colorize(col3))\
		.replace("▃", colorize(22, "▃", col2))\
		.replace("▙", colorize(22, "▙", col2))\
		.replace("▟", colorize(22, "▟", col2))\
		.replace("╩", colorize(22, "▃", col1))\
		.replace("╚", colorize(22, "▙", col1))\
		.replace("╝", colorize(22, "▟", col1))\
		.replace("─", colorize(22, "▃", col3))\
		.replace("└", colorize(22, "▙", col3))\
		.replace("┘", colorize(22, "▟", col3))\
		.replace("—", colorize(col1, "—", col2))\
		.replace("|", colorize(col1, "|", col2))
	)

def select_jersey(col1, col2, col3):
	lines = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
	final_table = []
	for _ in range(33):
		x = jerseys[_].split('\n')
		for j,line in enumerate(x):
			lines[j].append('{:^19}'.format(line.strip()))
	for i in [0,4,8,12,16,20,24,28]:
		final_table.append(('+'+'-'*21)*4+'+')
		final_table.append(': %s :'%' : '.join(['{:^19}'.format(i+z) for z in range(4)]))
		final_table.append(('+'+'-'*21)*4+'+')
		for l in lines[1:-2]:
			final_table.append(': %s :'%' : '.join(l[i:i+4]))
		final_table.append(('+'+'-'*21)*4+'+')
		final_table.append('')
	final_table.append('+'+'-'*21+'+')
	final_table.append(': {:^19} :'.format('32'))
	final_table.append('+'+'-'*21+'+')
	for l in lines[1:-2]:
		final_table.append(': %s :'%''.join(l[32]))
	final_table.append('+'+'-'*21+'+')
	for e,l in enumerate(final_table):
		final_table[e] = l.replace("░",colorize(col1)).replace("β",colorize(col2)).replace("γ",colorize(col3)).replace("▃", colorize(22, "▃", col2)).replace("▙", colorize(22, "▙", col2)).replace("▟", colorize(22, "▟", col2)).replace("╩", colorize(22, "▃", col1)).replace("╚", colorize(22, "▙", col1)).replace("╝", colorize(22, "▟", col1)).replace("─", colorize(22, "▃", col3)).replace("└", colorize(22, "▙", col3)).replace("┘", colorize(22, "▟", col3)).replace("—", colorize(col1, "—", col2)).replace("|", colorize(col1, "|", col2)).replace(':', '|')
	print('\n'.join(final_table))