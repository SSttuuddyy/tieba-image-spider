import tkinter as tk
from tkinter import messagebox
import os, re
from tkinter.filedialog import askdirectory
from tkinter import StringVar
from tkinter import Text
from tkinter import INSERT, END, ttk

class Gui():
    def __init__(self):
        self.sp = None
    def gene(self):
        if True:
            self.root = tk.Tk()
            width = 380
            height = 260
            sw = self.root.winfo_screenwidth()  # width
            sh = self.root.winfo_screenheight() - 80  # higth
            x = (sw-width) / 2
            y = (sh-height) / 2
            self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
            # select a browser
            tk.Label(self.root, text='浏览器：', font=('楷体', 15)).grid(row=0, column=0)
            self.brow = ttk.Combobox(self.root)
            self.brow = ttk.Combobox(self.root)
            self.brow.grid(row=0, column=1, ipadx=25)
            self.brow['value'] = ('Edge', 'Google')
            self.brow.current(0)
            # id number of post
            tk.Label(self.root, text='帖子号：', font=('楷体', 15)).grid(row=1, column=0)
            self.entry = tk.Entry(self.root)
            self.entry.grid(row=1, column=1, ipadx=25)
            self.entry.bind("<Button-3>", self.paste)
            # start page
            tk.Label(self.root, text='起始页：', font=('楷体', 15)).grid(row=2, column=0)
            self.entryPage1 = ttk.Combobox(self.root)
            self.entryPage1.grid(row=2, column=1, ipadx=25)
            self.entryPage1['value'] = tuple([i for i in range(1,11)])
            self.entryPage1.current(0)
            # sum page
            tk.Label(self.root, text='合计页：', font=('楷体', 15)).grid(row=3, column=0)
            tk.Label(self.root, text='可以超过实', font=('楷体', 10)).grid(row=2, column=2)
            tk.Label(self.root, text='际最大页数', font=('楷体', 10)).grid(row=3, column=2)
            self.entryPage2 = ttk.Combobox(self.root)
            self.entryPage2.grid(row=3, column=1, ipadx=25)
            self.entryPage2['value'] = tuple([i for i in range(1,11)])
            self.entryPage2.current(0)
            # a button to select path to create a folder
            self.select_path = StringVar()
            self.select_path.set('D:/')
            tk.Label(self.root, text='文件夹：', font=('楷体', 15)).grid(row=4, column=0)
            self.entryFilm = tk.Entry(self.root, textvariable=self.select_path)
            self.entryFilm.grid(row=4, column=1, ipadx=25)
            # a square frame to show the information
            self.text1 = tk.Text(self.root, width=28, height=2)
            self.text1.grid(row=7, column=1)
            self.text1.insert(END, ' ')
            self.text2 = tk.Text(self.root, width=28, height=1)
            self.text2.grid(row=8, column=1)
            self.text2.insert(END, ' ')
        # some button
        button1 = tk.Button(self.root, text='运行', width='10', command=lambda: self.action())
        button1.grid(row=5, column=1)
        button2 = tk.Button(self.root, text='打开文件夹', width='15', command=lambda: self.open_folder())
        button2.grid(row=6, column=1)
        button3 = tk.Button(self.root, text="选择文件夹", width='10', command=lambda: self.select_folder())
        button3.grid(row=4, column=2)
        self.root.mainloop()
    def act(self): # get the post id, start page, sum of page and store path
        if str(self.brow.get()) == 'Edge':
            self.sp.select_brow(0)
        else:
            self.sp.select_brow(1)
        self.id = self.entry.get()
        self.num_start = int(self.entryPage1.get())
        self.num_sum = int(self.entryPage2.get())
        self.film = self.select_path.get()
    def action(self): # get info, create folder and download
        self.text1.delete('1.0', 'end')
        self.text2.delete('1.0', 'end')
        self.root.update()
        self.act()
        url = 'https://tieba.baidu.com/p/'+self.id+'?pn='
        self.sp.get_html(url + '1')
        page_list = []
        for i in range(min(self.num_start, self.sp.sum), min(self.num_start + self.num_sum, self.sp.sum + 1)):
            page_list.append(url+'%d' %i+'/')
        for i in range(self.num_sum - min(self.num_start + self.num_sum, self.sp.sum + 1) + min(self.num_start, self.sp.sum)):
            page_list.append('0')
        count = self.num_start
        self.path = self.sp.parse_title(self.film)
        self.sp.mkdir()
        for url in page_list:
            if url != '0':
                if self.num_start > self.sp.sum:
                    self.tinsert(1, '\n第 '+ str(count) +' 页不存在\n正在下载第 '+str(self.sp.sum)+' 页图片')
                else:
                    self.tinsert(1, '\n第 '+ str(count) +' 页图片下载中')
                self.sp.get_html(url)
                self.sp.parse_html()
                self.sp.download()
            else:
                self.tinsert(1, '\n第 '+ str(count) +' 页不存在')
            count = count + 1
            self.sp.num = 0
        self.tinsert(1, '下载完成')
        messagebox.showinfo(message='下载完成')
    def open_folder(self): # open the folder created
        os.startfile(self.path)
    def select_folder(self): # select a path to create
        path_ = askdirectory()
        self.select_path.set(path_)
    def tinsert(self, id, text): # show the infomation about download
        if id == 1:
            self.text1.insert(END, text)
            self.text1.see(END)
        else:
            self.text2.insert(END, text)
            self.text2.see(END)
        self.root.update()
    def paste(self, event=None): # paste the post id from the pasteboard of user's computer by the right key of mouse
        self.entry.event_generate('<<Paste>>')