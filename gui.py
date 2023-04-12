import tkinter as tk
from tkinter import messagebox
import os

class Gui():
    def __init__(self):
        self.sp = None
    def gene(self):
        if True:
            root = tk.Tk()
            width = 280
            height = 180
            sw = root.winfo_screenwidth()  # 得到屏幕宽度
            sh = root.winfo_screenheight() - 80  # 得到屏幕高度
            x = (sw-width) / 2
            y = (sh-height) / 2
            root.geometry("%dx%d+%d+%d" % (width, height, x, y))
            tk.Label(root, text='帖子号：', font=('楷体', 15)).grid()
            #输入框
            self.entry = tk.Entry(root)
            self.entry.grid(row=0, column=1)
            tk.Label(root, text='起始页：', font=('楷体', 15)).grid(row=1, column=0)
            self.entryPage1 = tk.Entry(root)
            self.entryPage1.grid(row=1, column=1)
            tk.Label(root, text='终止页：', font=('楷体', 15)).grid(row=2, column=0)
            self.entryPage2 = tk.Entry(root)
            self.entryPage2.grid(row=2, column=1)
            tk.Label(root, text='文件夹：', font=('楷体', 15)).grid(row=3, column=0)
            self.entryFilm = tk.Entry(root)
            self.entryFilm.grid(row=3, column=1)
        #按钮
        button1 = tk.Button(root, text='运行', width='10', command=lambda: self.action())
        button1.grid(row=4, column=1)
        button2 = tk.Button(root, text='打开文件夹', width='15', command=lambda: self.open_file())
        button2.grid(row=5, column=1)
        root.mainloop()
    def act(self):#获取贴号，起始页，存储位置
        self.id = self.entry.get().strip()
        self.num_start = self.entryPage1.get()
        self.num_start = int(self.num_start)
        self.num_end = self.entryPage2.get()
        self.num_end = int(self.num_end)
        self.film = self.entryFilm.get()
    def action(self):#执行操作
        self.act()
        self.sp.id = self.id
        page_list = self.sp.get_page(self.num_start, self.num_end)
        count = self.num_start
        self.sp.get_html(page_list[0])
        self.path = self.sp.parse_title(self.film)#返回类型为列表
        self.sp.mkdir()
        for url in page_list:#遍历页码
            self.sp.get_html(url)
            self.sp.parse_html()
            print(' 第 %s 页图片下载中' % count)
            self.sp.download()
            count = count + 1
        messagebox.showinfo(message='下载完成')#提示完成
    def open_file(self):
        os.startfile(self.path)
