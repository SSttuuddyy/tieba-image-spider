import requests
import re
import os
from time import sleep

class Spieder():
    def __init__(self): 
        self.num = 0
        self.gui = ''
        self.sum = 0
    def select_brow(self, brow_id): # to select a headers
        if brow_id == 0:
            self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'
                }
        else:
            self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
                }
    def get_html(self, url): # get the html of inputed page
        response=requests.get(url,headers=self.headers)
        self.html = response.text
        pattern = re.compile(r'<span class="red">(.*?)</span>')
        self.sum = re.findall(pattern, self.html)
        self.sum = int(self.sum[0])
    def parse_html(self): # get the image url and the name of the image from the html
        pattern1 = re.compile(r'img class="BDE_Image".*?src="(.*?)"')
        pattern2 = re.compile(r'img class="BDE_Image".*?sign=.*?/(.*?).jpg')
        self.img_list = re.findall(pattern1, self.html)
        self.name_list = re.findall(pattern2, self.html)
    def parse_title(self, film): # get the title of the post
        pattern3 = re.compile(r"'threadTitle': '(.*?)'}]")
        self.title_list = re.findall(pattern3, self.html)
        self.title_list = self.title_list[0]
        if '回复：' in self.title_list:
            self.title_list = self.title_list[3:]
        sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in self.title_list:
            if char in sets:
                self.title_list = self.title_list.replace(char, '')
        self.path = film + '/' + self.title_list + '/'
        return self.path
    def mkdir(self): # create a folder with the name of the post to store the images
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            self.gui.tinsert(1, '\n'+self.title_list+' 创建中')
            self.gui.tinsert(1, '\n'+self.title_list+' 创建成功')
        else:
            self.gui.tinsert(1, '\n'+self.title_list+' 已存在')
    def download(self): # download the image
        for i in range(len(self.img_list)):
            r=requests.get(self.img_list[i])
            with open(self.path+self.name_list[i]+'.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
                self.num = self.num + 1
                # self.gui.tinsert(2, '\n第 '+ str(self.num) +' 张图片下载完成')
                self.gui.tinsert(2, '\n' + '下载进度 ' + str(self.num) + '/' + str(len(self.img_list)) + '张')
            sleep(1)
