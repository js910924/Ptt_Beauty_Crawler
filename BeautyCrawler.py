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
		self.date = datetime.now()
		self.input_date = input_date

		# Set path where you want to store your pictures
		# default is your current path
		self.path = os.getcwd() + '/' + '.'.join([str(self.input_date.month), str(self.input_date.day)])
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
			date = article.find('div', 'date').get_text().strip().split('/')
			self.date = datetime(self.date.year, int(date[0]), int(date[1]))
			if link != '' and self.date.strftime("%x") == input_date.strftime("%x"):
				path = self.path + ('/' + title)
				if not os.path.isdir(path):
					try:
						os.mkdir(path)
					except:
						print("Can't make article file: ", path)
						break
				
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
				try:
					f = open(pic_name, "wb")
					f.write(response_content)
					f.close()
					name += 1
				except:
					continue
		print('-----------Current page all pictures downloaded-----------')

	def run(self):
		page = 1

		while True:
			print('Page [%d]' % page)
			page += 1
			self.soup = self.getSoup(self.url)
			self.getArticles(self.input_date)
			current_time = datetime(now.year, self.date.month, self.date.day)
			print("Input: ", self.input_date.strftime("%x"), "Current: ", current_time.strftime("%x"))
			if self.input_date > current_time:
				print('---------------------Mission Complete---------------------')
				break
			self.url = self.previousPage(self.url)

if __name__ == '__main__':
	now = datetime.now()
	if len(sys.argv) != 2:
		print("Download all image today: %s" % now.strftime("%m/%d"))
		input_date = now
	else:
		print("Download all image on %s" % sys.argv[1])
		date = sys.argv[1].split("/")
		input_date = datetime(now.year, int(date[0]), int(date[1]))

	Crawler = BeautyCrawler(input_date)
	Crawler.run()
