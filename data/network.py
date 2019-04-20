import requests
import bs4 as BS


class Request():
	# Предоставляет уровень абстракции для получения страниц с сайта eda.ru
	# 
	def __init__(self, category):
		self.category = category


	def getPage(self, pageN):
		headers = {
	        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
	        			   Chrome/72.0.3626.121 YaBrowser/19.3.1.777 (beta) Yowser/2.5 Safari/537.36'
	    }
		url = 'https://eda.ru/recepty/%s?page=%d' % (self.category, pageN)
		r = requests.get(url, headers=headers)
		
		if not r.ok:
			print("Unexpected status %d" % r.status_code)
			print("on request to page %d in category %s" % (pageN, self.category))
			return ""
		else:
			return BS.BeautifulSoup(r.text, features="lxml")
