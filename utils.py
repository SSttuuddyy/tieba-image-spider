import requests
import re
import os
from time import sleep

class Spieder():
    def __init__(self): 
        self.id = ''
        self.num = 0
        self.gui = ''
        self.brow_id = 0
        if self.brow_id == 0:
            self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'
                }
        else:
            self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
                }
    def get_page(self, num_start, num_end): # get the url of required pages of post
        self.url = 'https://tieba.baidu.com/p/'+self.id+'?pn='
        page_list = []
        for i in range(num_start, num_end+1):
            page_list.append(self.url+'%d' %i+'/')
        return page_list
    def get_html(self, url): # get the html of inputed page
        response=requests.get(url,headers=self.headers)
        self.html = response.text
    def parse_html(self): # get the image url and the name of the image from the html
        pattern = re.compile(r'img class="BDE_Image".*?src="(.*?)"')
        pattern2 = re.compile(r'img class="BDE_Image".*?sign=.*?/(.*?).jpg')
        self.img_list = re.findall(pattern, self.html)
        self.name_list = re.findall(pattern2, self.html)
    def parse_title(self, film): # get the title of the post
        pattern3 = re.compile(r"'threadTitle': '(.*?)'}]")
        self.title_list = re.findall(pattern3, self.html)
        if self.gui.num_start > 1:
            self.title_list[0] = self.title_list[0][3:]
        sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in self.title_list[0]:
            if char in sets:
                self.title_list[0] = self.title_list[0].replace(char, '')
        self.path = film + '/' + self.title_list[0] + '/'
        return self.path
    def mkdir(self): # create a folder with the name of the post to store the images
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            self.gui.tinsert(1, '\n'+self.title_list[0]+'创建中')
            self.gui.tinsert(1, '\n'+self.title_list[0]+'创建成功')
        else:
            self.gui.tinsert(1, '\n'+self.title_list[0]+'已存在')
    def download(self): # download the image
        for i in range(len(self.img_list)):
            r=requests.get(self.img_list[i], headers = self.headers)
            with open(self.path+self.name_list[i]+'.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
                self.num = self.num + 1
                self.gui.tinsert(2, '\n第 '+ str(self.num) +' 张图片下载完成')
            sleep(1)
