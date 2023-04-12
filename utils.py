import requests
import re
import os
from time import sleep

class Spieder():
    def __init__(self): 
        self.id = ''
        self.num = 0
    def get_page(self, num_start, num_end):#生成每页地址
        self.url = 'https://tieba.baidu.com/p/'+self.id+'?pn='
        page_list=[]
        for i in range(num_start, num_end+1):
            page_list.append(self.url+'%d' %i+'/')
        return page_list
    def get_html(self, url):#获取当页网址源代码
        response=requests.get(url)
        self.html=response.text
    def parse_html(self):#解析获取图片地址和名称
        pattern = re.compile(r'img class="BDE_Image".*?"(.*?)"')
        pattern2 = re.compile(r'img class="BDE_Image".*?sign=.*?/(.*?).jpg')
        self.img_list=re.findall(pattern, self.html)
        self.name_list=re.findall(pattern2, self.html)
    def parse_title(self, film):#获取帖子标题
        pattern3 = re.compile(r"'threadTitle': '(.*?)'}")
        self.title_list = re.findall(pattern3, self.html)
        self.path = film + '//' + self.title_list[0] + '//'
        return self.path
    def mkdir(self):#找到存储位置
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            print(self.title_list[0]+'创建中')
            print(self.title_list[0]+'已创建')
        else:
            print(self.title_list[0]+'已存在')
    def download(self):#下载图片
        for i in range(len(self.img_list)):
            r=requests.get(self.img_list[i])
            with open(self.path+self.name_list[i]+'.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
                self.num = self.num + 1
                print(' 第 %s 张图片下载完成' % self.num)
            sleep(1)
