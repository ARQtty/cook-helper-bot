import json
import sqlite3
from time import sleep

from parser import EdaPageParser
from network import Request

# Возможные категории
# osnovnye-blyuda, zavtraki, salaty, pasta-picca
category = 'osnovnye-blyuda'

# Создаём базу
conn = sqlite3.connect("mydatabase.sqlite")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Recipes
				  (recipeID    INTEGER PRIMARY KEY AUTOINCREMENT,
				   category    TEXT NOT NULL,
				   name 	   TEXT NOT NULL,
				   cookTime    INTEGER,
				   source 	   TEXT NOT NULL,
				   ingredients TEXT NOT NULL)""")


req = ' '
reqCounter = 0
trueReqCounter = 232
# Парсер остановит выполнение программы, когда закончатся рецепты в указанной категории
while req != '':
	# Получаем страницу
	req = Request(category)
	page = req.getPage(trueReqCounter)


	# Парсим её
	parser = EdaPageParser()
	obj = parser.parse(page)
	obj = json.loads(obj)

	# Кладём данные в базу
	for recipe in obj:
		cursor.execute("""INSERT INTO Recipes
		                  (category, name, cookTime, source, ingredients)
		                  VALUES (?, ?, ?, ?, ?)""",
		                (category, recipe['name'].replace('\xa0', ' '), recipe['time'], recipe['ref'], ','.join(recipe['ings']))
		               )

	conn.commit()
	trueReqCounter += 1
	
	# Не создаём большую нагрузку на сайт
	if reqCounter > 8:
		#sleep(1)
		reqCounter = 0
		print("Просмотрено %d страниц" % trueReqCounter)
	else:
		reqCounter += 1