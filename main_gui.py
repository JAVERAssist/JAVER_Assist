#! /usr/lib/python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) [year] [fullname]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext

import javer_Assist


class MainGUI:
    __WHITE = '#FFFFFF'
    __BG_GREY = '#DDDDDD'
    __FG_GREY = '#EEEEEE'
    __FONT = ("Microsoft YaHei", 12)

    def __init__(self):
        self.__main_frame_creator()
        self.__tabs_creator()

    def __main_frame_creator(self):
        self.root = tk.Tk()
        # 1440x900
        self.root.geometry("900x550+240+150")
        self.root.resizable(width=False, height=False)
        self.root.title('a fun work')  # JAVER Assist: A fan work
        self.root.iconbitmap('material\\JIcon.ico')

    def __tabs_creator(self):
        style = ttk.Style()
        style.theme_create('st', settings={
            ".": {
                "configure": {
                    "background": self.__BG_GREY,
                    "font": self.__FONT
                }
            },
            "TNotebook": {
                "configure": {
                    "tabmargins": [2, 5, 0, 0],
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [10, 2]
                },
                "map": {
                    "background": [("selected", self.__FG_GREY)],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            }
        })
        style.theme_use('st')

        tab_control = ttk.Notebook(self.root)

        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='主页')
        self.__tab1_content(tab1)

        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='设置')
        self.__tab2_content(tab2)

        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text='关于')

        tab_control.place(x=0, y=0, width=900, height=550)

    def __tab1_content(self, tab_name):
        dir_section = tk.LabelFrame(tab_name, text='请输入目录信息', background=self.__BG_GREY, font=self.__FONT)
        dir_section.place(x=10, y=10, width=880, height=480)

        tk.Label(dir_section, text='待整理路径:', background=self.__BG_GREY,
                 font=self.__FONT).place(x=2, y=10, width=110, height=30)
        prepare_label = tk.Label(dir_section, background=self.__WHITE, relief='solid', anchor='w',
                                 borderwidth=1, font=self.__FONT)
        prepare_label.place(x=112, y=10, width=600, height=30)
        tk.Button(dir_section, text='选择输入路径', justify=tk.CENTER, font=self.__FONT,
                  command=lambda: self.__get_path(prepare_label)).place(x=720, y=10, width=150, height=30)

        tk.Label(dir_section, text='输出文件夹:', background=self.__BG_GREY,
                 font=self.__FONT).place(x=2, y=60, width=110, height=30)
        output_label = tk.Label(dir_section, background=self.__WHITE, relief='solid', anchor='nw',
                                borderwidth=1, font=self.__FONT)
        output_label.place(x=112, y=60, width=600, height=30)
        tk.Button(dir_section, text='选择输出路径', justify=tk.CENTER, font=self.__FONT,
                  command=lambda: self.__get_path(output_label)).place(x=720, y=60, width=150, height=30)

        tk.Button(dir_section, text='开始整理', justify=tk.CENTER, font=self.__FONT,
                  command=lambda: self.__start_running(prepare_label['text'],
                                                       output_label['text'])).place(x=10, y=110, width=150, height=30)

        attention = '请务必确认路径选择正确，不然可能会造成数据丢失的严重后果!!!'
        tk.Label(dir_section, text=attention, background=self.__BG_GREY, font=("Microsoft YaHei", 10),
                 anchor='w', foreground="#222222", ).place(x=180, y=110, width=500, height=30)

        tk.Label(dir_section, text='信息和日志:', background=self.__BG_GREY, font=self.__FONT,
                 justify=tk.RIGHT).place(x=2, y=160, width=110, height=30)

        info = scrolledtext.ScrolledText(dir_section)
        info.place(x=10, y=200, width=860, height=250)
        info.insert(tk.INSERT, "Some text")
        info.insert(tk.INSERT, "asfasdfsadfsadfsadfsadf")
        info.insert(tk.INSERT, "Some text\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        info.insert(tk.END, " in ScrolledText")
        info.config(state=tk.DISABLED)

    def __tab2_content(self, tab_name):
        sort_section = tk.LabelFrame(tab_name, text='影片整理设置', background=self.__BG_GREY, font=self.__FONT)
        sort_section.place(x=10, y=10, width=880, height=200)

        proxy_section = tk.LabelFrame(tab_name, text='代理服务器设置', background=self.__BG_GREY, font=self.__FONT)
        proxy_section.place(x=10, y=230, width=880, height=200)

        self.radio_var = tk.BooleanVar()
        self.radio_var.set(False)
        unused_proxy = tk.Radiobutton(proxy_section, background=self.__BG_GREY, activebackground=self.__BG_GREY,
                                     font=self.__FONT, anchor='nw', text='不使用代理',
                                     value=False, variable=self.radio_var)
        unused_proxy.place(x=30, y=10, width=150, height=30)
        use_proxy = tk.Radiobutton(proxy_section, background=self.__BG_GREY, activebackground=self.__BG_GREY,
                                   font=self.__FONT, text='使用代理', anchor='nw', value=True, variable=self.radio_var)
        use_proxy.place(x=30, y=70, width=150, height=30)

        tk.Label(proxy_section, text='HTTP服务器IP:', background=self.__BG_GREY,
                 font=self.__FONT, anchor='ne').place(x=200, y=10, width=150, height=30)
        ip = tk.Entry(proxy_section, font=self.__FONT)
        ip.place(x=360, y=10, width=150, height=30)
        ip.insert(0, '127.0.0.1')

        tk.Label(proxy_section, text='端口:', background=self.__BG_GREY,
                 font=self.__FONT, anchor='ne').place(x=530, y=10, width=150, height=30)
        port = tk.Entry(proxy_section, font=self.__FONT)
        port.place(x=690, y=10, width=150, height=30)
        port.insert(0, '8087')

        tk.Label(proxy_section, text='用户名:', background=self.__BG_GREY,
                 font=self.__FONT, anchor='ne').place(x=200, y=70, width=150, height=30)
        user_name = tk.Entry(proxy_section, font=self.__FONT)
        user_name.place(x=360, y=70, width=150, height=30)

        tk.Label(proxy_section, text='密码:', background=self.__BG_GREY,
                 font=self.__FONT, anchor='ne').place(x=530, y=70, width=150, height=30)
        pwd = tk.Entry(proxy_section, font=self.__FONT)
        pwd.place(x=690, y=70, width=150, height=30)

    def __get_path(self, label):
        path = filedialog.askdirectory()
        # print(path)
        label.config(text=path)

    def __start_running(self, src, dst):
        print(src, dst)
        # javer_Assist.main(src, dst)


MainGUI().root.mainloop()
