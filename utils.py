import requests
import re
import os
from time import sleep

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
    def parse_txt(self, html2):
        self.pattern3 = re.compile(r"'threadTitle': '(.*?)'}")
        self.name_list1 = re.findall(self.pattern3, html2)
        return self.name_list1
    def mkdir(self, path1, film1):
        self.folder = os.path.exists(path1)
        if not self.folder:
            os.makedirs(path1)
            print(film1+'创建中')
            print(film1+'已创建')
        else:
            print(film1+'已存在')
    def download(self, path, img_list, title_list):
        for i in range(len(img_list)):
            self.r=requests.get(img_list[i])
            with open(path+title_list[i]+'.jpg', 'wb') as f:
                f.write(self.r.content)
                f.close()
            sleep(1)
