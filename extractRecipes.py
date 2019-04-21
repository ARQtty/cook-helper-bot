import sqlite3
import random


def getFastNRecipes(category, n):
	conn = sqlite3.connect("./data/mydatabase.sqlite")
	cursor = conn.cursor()
	
	recs = cursor.execute("SELECT * FROM Recipes \
						   WHERE category='%s'\
							     AND cookTime IS NOT NULL\
						   ORDER BY cookTime\
						   LIMIT %d" % (category, n*3))
	recs = recs.fetchall()
	randomRecs = []
	for i in range(n):
		randNum = random.randint(0, len(recs))
		randRecipe = recs[randNum]
		randomRecs.append([x for x in randRecipe])
		randomRecs[-1][4] = "https://eda.ru/recepty/" + category + "/" + randRecipe[4]
		recs.pop(randNum)

	conn.close()

	return randomRecs


def menu():
	categoriesRu = ["Основные", "Завтраки", "Салаты", "Пицца-паста"]
	categoriesEn = ["osnovnye-blyuda", "zavtraki", "salaty", "pasta-picca"]

	print("\n".join(["%d %s" % (i+1, categoriesRu[i]) for i in range(len(categoriesRu))]))
	cat = categoriesEn[int(input())-1]
	view(getFastNRecipes(cat, 5))


def view(recipes):
	print("\n\n".join(["%s\n%d\n%s\n%s" % (x[2], x[3], x[4], ', '.join(x[5].split(','))) for x in recipes]))



if __name__ == '__main__':
	menu()