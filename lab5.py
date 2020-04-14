import re

def gost705(art):
    ls =['Author','Title', 'Journal','Year','Pages', 'Numpages', 'Volume', 'Language']
    prefx_eng = {
        'Pages':'.-P. ',
        'Volume':'.-Vol. ',
        'Year': '.-',
    }
    prefx_rus = {
        'Pages':'-С, ',
        'Volume':',-Вып ',
        'Year':'.-'
    }
    art_temp = {}
    if art.get('Language') == 'russian':
        prefx = prefx_rus
    else:
        prefx = prefx_eng
    for x in ls:
        if x in art:
            art_temp[x]= prefx.get(x,'') + art.get(x,'')
        else:
            art_temp[x] = ''
    art_temp['Author'] = art_temp['Author'].replace(' and ', ', ')
    temp_dict = {
        'Article': '{Author} {Title} // {Journal}{Year}{Pages}',
        'Book': '{Author} {Title}{Year} {Numpages}'}
    if art['type'] in temp_dict.keys():
        return temp_dict[art['type']].format(**art_temp)
    else:
        return temp_dict['Article'].format(**art_temp)

file = open(r'c:\pyt\biblio.bib', mode = 'r', encoding = 'utf-8')
data = file.read()
reg1 = re.compile(r'@(?P<type>\w+){(?P<tag>.+?),(?P<body>.+?)}\s*}', re.DOTALL)
reg2 = re.compile(r'(\w+)\s*=\s*{(.+?)}')
iterat = reg1.finditer(data)
d_list = []
for i in iterat:
	body_orig = i.group('body')+'}'
	body_list = reg2.findall(body_orig)
	d = {
	'type': i.group('type'),
	'tag' : i.group('tag')
	}
	for i in body_list:
		d[i[0]] = i[1]
	d_list.append(d)
for d in d_list:
    print(gost705(d)) #вывод научных публикаций