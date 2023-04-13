import tkinter as tk
from tkinter import messagebox
import os
from tkinter.filedialog import askdirectory
from tkinter import StringVar
from tkinter import Text
from tkinter import INSERT, END

class Gui():
    def __init__(self):
        self.sp = None
    def gene(self):
        if True:
            self.root = tk.Tk()
            width = 370
            height = 380
            sw = self.root.winfo_screenwidth()  # 得到屏幕宽度
            sh = self.root.winfo_screenheight() - 80  # 得到屏幕高度
            x = (sw-width) / 2
            y = (sh-height) / 2
            #路径变量
            self.select_path = StringVar()
                # self.select_path.set(os.path.abspath("."))
            self.select_path.set('D:/')
            #贴号
            self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
            tk.Label(self.root, text='帖子号：', font=('楷体', 15)).grid()
            self.entry = tk.Entry(self.root)
            self.entry.grid(row=0, column=1, ipadx=25)
            self.entry.bind("<Button-3>", self.paste)
            #起始
            tk.Label(self.root, text='起始页：', font=('楷体', 15)).grid(row=1, column=0)
            self.entryPage1 = tk.Entry(self.root)
            self.entryPage1.grid(row=1, column=1, ipadx=25)
            self.entryPage1.insert(END, '1')
            #终止
            tk.Label(self.root, text='终止页：', font=('楷体', 15)).grid(row=2, column=0)
            tk.Label(self.root, text='可以超过实', font=('楷体', 10)).grid(row=1, column=2)
            tk.Label(self.root, text='际最大页数', font=('楷体', 10)).grid(row=2, column=2)
            self.entryPage2 = tk.Entry(self.root)
            self.entryPage2.grid(row=2, column=1, ipadx=25)
            self.entryPage2.insert(END, '1')
            #路径
            tk.Label(self.root, text='文件夹：', font=('楷体', 15)).grid(row=3, column=0)
            self.entryFilm = tk.Entry(self.root, textvariable=self.select_path)
            self.entryFilm.grid(row=3, column=1, ipadx=25)
            #消息提示框
            self.text1 = tk.Text(self.root, width=28, height=5)
            self.text1.grid(row=6, column=1)
            self.text1.insert(END, ' ')
            self.text2 = tk.Text(self.root, width=28, height=10)
            self.text2.grid(row=7, column=1)
            self.text2.insert(END, ' ')
        #按钮
        button1 = tk.Button(self.root, text='运行', width='10', command=lambda: self.action())
        button1.grid(row=4, column=1)
        button2 = tk.Button(self.root, text='打开文件夹', width='15', command=lambda: self.open_file())
        button2.grid(row=5, column=1)
        button3 = tk.Button(self.root, text="选择文件夹", width='10', command=lambda: self.select_folder())
        button3.grid(row=3, column=2)
        self.root.mainloop()
    def act(self):#获取贴号，起始页，存储位置
        self.id = self.entry.get().strip()
        self.num_start = self.entryPage1.get()
        self.num_start = int(self.num_start)
        self.num_end = self.entryPage2.get()
        self.num_end = int(self.num_end)
        self.film = self.select_path.get()
    def action(self):#执行操作
        self.text1.delete('1.0', 'end')
        self.text2.delete('1.0', 'end')
        self.root.update()
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
            self.tinsert(1, '\n第 '+ str(count) +' 页图片下载中')
            self.sp.download()
            count = count + 1
        messagebox.showinfo(message='下载完成')#提示完成
        self.sp.num = 0
    def open_file(self): #打开下载的文件夹
        os.startfile(self.path)
    def select_folder(self): #文件夹选择
        path_ = askdirectory()
        self.select_path.set(path_)
    def tinsert(self, id, text): #消息提醒
        if id == 1:
            self.text1.insert(END, text)
            self.text1.see(END)
        else:
            self.text2.insert(END, text)
            self.text2.see(END)
        self.root.update()
    def paste(self, event=None): #右键粘贴
        self.entry.event_generate('<<Paste>>')