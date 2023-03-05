import requests
import os
import tkinter
import re
from tkinter import messagebox


def get_page(num3, num4, url2):
    page_list2 = []
    for i in range(num3, num4 + 1):
        page_list2.append(url2 + '%d' % i + '/')
    return page_list2


def get_html(url3):
    response = requests.get(url3)
    html2 = response.text
    print(html2)
    return html2


def parse_html(html1):
    pattern = re.compile(r'img class="BDE_Image" src="(.*?)" size=')
    pattern2 = re.compile(r'img class="BDE_Image" src=".*?sign=.*?/(.*?).jpg')
    img_list2 = re.findall(pattern, html1)
    title_list2 = re.findall(pattern2, html1)
    return img_list2, title_list2


def parse_txt(html2):
    pattern3 = re.compile(r"'threadTitle': '(.*?)'}")
    name_list1 = re.findall(pattern3, html2)
    return name_list1


def download(path2, img_list1, title_list1):
    for i in range(len(img_list1)):
        r = requests.get(img_list1[i])
        with open(path2 + title_list1[i] + '.jpg', 'wb') as f:
            f.write(r.content)
            f.close()


def mkdir(path1, film1):
    folder = os.path.exists(path1)
    if not folder:
        os.makedirs(path1)
        print(film1 + '创建中')
        print(film1 + '已创建')
    else:
        print(film1 + '已存在')


root = tkinter.Tk()
root.title('贴吧爬虫')
root.geometry('500x200+888+400')
tkinter.Label(root, text='帖子号：', font=('楷体', 15)).grid()
entry = tkinter.Entry(root)
entry.grid(row=0, column=1)
tkinter.Label(root, text='起始页：', font=('楷体', 15)).grid(row=1, column=0)
entryPage1 = tkinter.Entry(root)
entryPage1.grid(row=1, column=1)
tkinter.Label(root, text='终止页：', font=('楷体', 15)).grid(row=2, column=0)
entryPage2 = tkinter.Entry(root)
entryPage2.grid(row=2, column=1)
tkinter.Label(root, text='文件夹：', font=('楷体', 15)).grid(row=3, column=0)
entryFilm = tkinter.Entry(root)
entryFilm.grid(row=3, column=1)


def act():
    y = entry.get().strip()
    x = 'https://tieba.baidu.com/p/' + y + '?pn='
    num1 = entryPage1.get()
    num1 = int(num1)
    num2 = entryPage2.get()
    num2 = int(num2)
    film = entryFilm.get()
    return x, film, num1, num2


def action(x, film, num1, num2):
    if __name__ == '__main__':
        page_list = get_page(num1, num2, x)
        count = num1
        url4 = page_list[0]
        html = get_html(url4)
        name_list = parse_txt(html)
        path = film + '//' + name_list[0] + '//'
        mkdir(path, name_list[0])
        for url in page_list:
            html = get_html(url)
            img_list, title_list = parse_html(html)
            print(' 第 %s 页图片下载中' % count)
            download(path, img_list, title_list)
            count = count + 1


def action2():
    x, film, num1, num2 = act()
    action(x, film, num1, num2)
    tkinter.messagebox.showinfo(message='下载完成')


button = tkinter.Button(root, text='运行', width='10', command=action2)
button.grid(row=4, column=1)
button1 = tkinter.Button(root, text='载入', width='10', command=act)
button1.grid(row=4, column=0)
root.mainloop()
