import requests
import re

class Spieder():
    def __init__(self, y):
        self.y = y
        self.x = 'https://tieba.baidu.com/p/'+self.y+'?pn='
    def get_page(self, num, num1):
        self.page_list=[]
        self.url=self.x
        for i in range(num1, num+1):
            self.page_list.append(self.url+'%d' %i+'/')
        return self.page_list
    def get_html(self, url):
        self.response=requests.get(url)
        self.html=self.response.text
        return self.html
    def parse_html(self, html):
        self.pattern = re.compile(r'img class="BDE_Image".*?src="(.*?)" size=')
        self.pattern2 = re.compile(r'img class="BDE_Image".*?src=".*?sign=.*?/(.*?).jpg')
        self.img_list=re.findall(self.pattern, html)
        self.title_list=re.findall(self.pattern2, html)
        return self.img_list, self.title_list
    def download(self, path, img_list, title_list):
        for i in range(len(img_list)):
            self.r=requests.get(img_list[i])
            with open(path+title_list[i]+'.jpg', 'wb') as f:
                f.write(self.r.content)
                f.close()
