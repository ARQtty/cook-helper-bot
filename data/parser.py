import json

class EdaPageParser():
	# Предоставляет статический метод для парсинга страницы сайта
	# eda.ru вида https://eda.ru/recepty/%category%/*
	#
	# Возвращает json объект с полями 
	# name - Название блюда
	# time - Время приготовления
	# ings - Список ингредиентов
	# ref  - Ссылка на страницу с рецептом


	def __init__(self):
		pass


	def parse(self, page):
		sections = self._getSections(page)
		if len(sections) < 5:
			print("[ERROR] Слишком мало рецептов в выдаче. Возможно закончились страницы рецептов")
			raise Exception

		serialized = []
		
		for section in sections:
			serialized.append(dict())
			serialized[-1]["name"] = self._getName(section)
			serialized[-1]["time"] = self._getTime(section)
			serialized[-1]["ings"] = self._getIngridients(section)
			serialized[-1]["ref"]  = self._getRef(section)

		return json.dumps(serialized)


	def _getSections(self, page):
		# Возвращает код всех плашек рецептов по отдельности
		sections = page.findAll('div', {'class': 'clearfix'})
		return sections


	def _getRef(self, section):
		# Парсит ссылку на страницу с рецептом
		# Отрезает префикс https://eda.ru/recepty/%category/
		# Пример категории - osnovnye-blyuda
		ref = section.find('h3', {'class': 'horizontal-tile__item-title'})
		ref = ref.find('a').get('href')
		ref = ref.split('/')[-1]
		return ref


	def _getTime(self, section):
		# Парсит время приготовления блюда. Возвращает время в минутах
		
		def measure(string, index):
			# Находит число справа от указанного индекса
			string = string[:index-1]
			i = -1
			while string[i] != ' ':
				i-=1
			return string[i+1:]

		mins = section.text.lower().find('мин')
		hours = section.text.lower().find('час')

		# Перевод в минуты
		totalTime = 0
		if hours != -1:
			try:
				hours = int(measure(section.text, hours))
				totalTime += hours * 60
			except Exception as e:
				pass
		if mins != -1:
			try:
				mins = int(measure(section.text, mins))
				totalTime += mins
			except Exception as e:
				pass
			

		if totalTime == 0:
			totalTime = None

		return totalTime


	def _getName(self, section):
		# Парсит название блюда на русском
		name = section.find('h3', {'class': 'horizontal-tile__item-title'})
		name = name.find('span').getText().rstrip().lstrip()
		return name


	def _getIngridients(self, section):
		# Парсит список ингредиентов
		ings = section.find('div', {'class': 'ingredients-list__content'})
		ings = [x.getText().lstrip() for x in ings.findAll('p')]
		# Справа написано количество ингредиента. Не отрезается через .rstrip()
		ings = [x.split('  ')[0].rstrip() for x in ings]
		return ings

