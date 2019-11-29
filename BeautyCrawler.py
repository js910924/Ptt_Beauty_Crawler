from bs4 import BeautifulSoup as bs
import requests
import os
import sys
import threading
from datetime import datetime, timedelta

class BeautyCrawler:
	def __init__(self, input_date):
		self.url = 'https://www.ptt.cc/bbs/Beauty/index.html'
		self.soup = self.getSoup(self.url)
		self.date = ''
		self.input_date = input_date.split('/')

		# Set path where you want to store your pictures
		# default is your current path
		self.path = os.getcwd() + '\\' + '.'.join(self.input_date)
		if not os.path.exists(self.path):
			os.mkdir(self.path)
 
	def getSoup(self, url):
		payload = {
			"from": "https://www.ptt.cc/bbs/Beauty/index.html",
			"yes": "yes"
		}
		rs = requests.session()
		res = rs.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FBeauty%2Findex.html", data=payload)
		res = rs.get(url)
		soup = bs(res.text, 'html.parser')
		
		return soup

	def previousPage(self, current_url):
	    previous = self.soup.findAll('a', 'btn wide')[1].get('href')
	    current_url = 'https://www.ptt.cc' + previous

	    return current_url

	def getArticles(self, input_date):
		articles = self.soup.findAll('div', 'r-ent')
		NOT_EXIST = bs('<a href= "">本文已被刪除</a>', 'html.parser').a
		tmp = [article for article in articles]
		tmp.reverse()
		
		for article in tmp:
			meta = article.find('div', 'title').find('a') or NOT_EXIST
			title = meta.get_text()
			link = meta.get('href')
			self.date = article.find('div', 'date').get_text().strip().split('/')
			if link != '' and self.date == input_date:
				path = self.path + ('\\' + title)
				if not os.path.isdir(path):
					try:
						os.mkdir(path)
					except NotADirectoryError:
						return
				
				t = threading.Thread(target = self.getPic, args = (link, path))
				t.start()

	def getPic(self, link, path):
	    name = 0   # 圖檔取名用
	    picture_url = 'https://www.ptt.cc' + link
	    pic_links = self.getSoup(picture_url).findAll('a')

	    print('-----------------Downloading pictures....-----------------')
	    for i in range(5, len(pic_links)-1):
	        tmp = pic_links[i].get('href')
	        if ('.jpg' in tmp) or ('.png' in tmp):
	            pic_link = tmp
	            print(pic_link)
	            response = requests.get(pic_link)
	            response_content = response.content
	            pic_name = path + ('/%s.jpg' % name)
	            f = open(pic_name, "wb")
	            f.write(response_content)
	            f.close()
	            name += 1
	    print('-----------Current page all pictures downloaded-----------')

	def run(self):
		page = 1
		now = datetime.now()
		input_time = datetime.strptime("{0}-{1}-{2}".format(now.year, int(self.input_date[0]), int(self.input_date[1])), "%Y-%m-%d")

		while True:
			print('Page [%d]' % page)
			page += 1
			self.soup = self.getSoup(self.url)
			self.getArticles(self.input_date)
			current_time = datetime.strptime("{0}-{1}-{2}".format(now.year, int(self.date[0]), int(self.date[1])), "%Y-%m-%d")
			if input_time > current_time:
				print('---------------------Mission Complete---------------------')
				break
			self.url = self.previousPage(self.url)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		now = datetime.now()
		input_date = now.strftime("%m/%d")
		print("Download all image today: %s" % input_date)
	else:
		print("Download all image on %s" % sys.argv[1])
		input_date = sys.argv[1]

	Crawler = BeautyCrawler(input_date)
	Crawler.run()