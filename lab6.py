import re
import sqlite3

def output_table(name):
	"""Функция для вывода статей определенного автора"""
	con = sqlite3.connect(r'c:\pyt\test.db')
	c = con.cursor()
	author = ["%"+name+"%",]
	c.execute("SELECT * FROM articles WHERE Autor LIKE ?", author)
	print(c.fetchall())
	con.close()

con = sqlite3.connect(r'c:\pyt\test.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS articles (Autor,Journal,Title, Year)""")
file = open(r'c:\pyt\biblio.bib', mode = 'r', encoding = 'utf-8')
data = file.read()
reg1 = re.compile(r'@(?P<type>\w+){(?P<tag>.+?),(?P<body>.+?)}\s*}', re.DOTALL)
reg2 = re.compile(r'(\w+)\s*=\s*{(.+?)}')
iterat = reg1.finditer(data)
d_list = []
for i in iterat:
	body_orig = i.group('body')+'}' # находим "тело"
	body_list = reg2.findall(body_orig) # записываем тело в список
	d = {
	'type': i.group('type'),
	'tag' : i.group('tag')
	}
	for i in body_list:
		d[i[0]] = i[1]
	d_list.append(d) #создаем список словарей
stolb = ['Author', 'Journal','Title', 'Year']
tmp = {}
for i in d_list:
	for j in stolb:
		if j in i:
			tmp[j] = i.get(j)
		else:
			tmp[j] = ''
	tmp['Author'] = tmp['Author'].replace(' and ', ',')
	purchases = [(tmp.get('Author'),tmp.get('Journal'),tmp.get('Title'),tmp.get('Year'))]
	cur.executemany("INSERT INTO articles VALUES(?,?,?,?)",purchases)
	con.commit()
con.close()
print ('Введите имя автора')
name = input()
output_table(name)