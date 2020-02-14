# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : main2.py
# @Created  : 2020/2/9 10:01 PM
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import os

import io
from io import BytesIO

from PIL import Image, ImageTk

from com.liuqi.vanas.id3.Mp3Id3 import ID3
from com.liuqi.vanas.id3.config import Mp3Info
from com.liuqi.vanas.tools import TkMessage

import math

# 对话框
class Dialog:

    # 所有输入框
    __entrys__ = {}

    # 音乐 listbox
    __music_lb__ = []

    # 当前选择的歌曲
    __curselection_music__ = None

    # 当前选择歌曲的 id3
    __curselection_music_id3__ = None

    # 主窗体
    __masterwin__ = None

    def __init__(self , dialogName):
        self.__masterwin__ = Tk()
        self.__masterwin__.title(dialogName)
        #print(tkinter.TkVersion)

    def open(self):
        self.__create_dialog()

    def __create_dialog(self):

        frmL = Frame(self.__masterwin__ , width=250, height=700)  # music 列表
        frmRTL = Frame(self.__masterwin__ , width=250, height=250)  # ID3 信息 专辑图片
        frmRTR = Frame(self.__masterwin__ , width=200, height=250)  # ID3 信息 专辑歌词
        frmRB = Frame(self.__masterwin__ , width=450, height=400)  # ID3 信息 作者等
        frmB = Frame(self.__masterwin__ , width=450, height=50)  # 底部按钮

        # column:  对应的放置的所在的列序号
        # columnspan: 表示该组件需要横跨多少列
        # row:   对应的放置的所在的行序号
        # rowspan:  表示组件需要横跨多少行
        # ipadx:  需要注意，这个参数表示x方向的内部填充，即以内部颜色为标准向左右方向扩展
        # ipady:  同上
        # padx:  这个是表示x方向的外部填充
        # pady:  同上

        frmL.grid(row=0 , column=0 , rowspan=3 , padx=5 ,pady=5)
        frmRTL.grid(row=0 , column=1 , padx=5 ,pady=5)
        frmRTR.grid(row=0 , column=2 , padx=5 ,pady=5)
        frmRB.grid(row=1 , column=1 , columnspan=2 , padx=5 ,pady=5)
        frmB.grid(row=2 , column=1 , columnspan=2 , padx=5 ,pady=5)


        # 上传文件按钮
        Button(frmL, text="文件", command=self.__choose_musicfile).grid(row=0, column=0 )
        Button(frmL, text="文件夹", command=self.__choose_musicdir).grid(row=0, column=1)
        Button(frmL, text="清空", command=self.__clear_data).grid(row=0, column=2)

        # 歌曲清单列表
        __music_lb__ = Listbox(frmL, height=38) #? 为什么是 38?  不能设置 600
        # 绑定点击事件
        __music_lb__.bind('<ButtonRelease-1>', self.__music_lb_click)
        __music_lb__.grid(row=1, column=0, columnspan=3, pady=5, sticky=N + E + W)

        self.__music_lb__ = __music_lb__

        # ID3 信息
        # 专辑图片信息
        image = self.__create_albumimage()
        _albumimage = Label(frmRTL, image=image)
        _albumimage.grid(row=0, column=0, columnspan=2, sticky=W)
        self._albumimage = _albumimage

        # 加载图片
        Button(frmRTL, text="load", command=self.__choose_albumimage).grid(row=1, column=0)
        Button(frmRTL, text="clear", command=self.__clear_albumimage).grid(row=1, column=1)

        # 歌词
        self.__add_lyrics(frmRTR)

        # id3 信息
        self.__add_attr(frmRB)

        # 底部保存按钮
        Button(frmB, text="保存", command=self.__save_data).grid(row=0, column=0, columnspan=10)

        self.__masterwin__.mainloop()

    def __clear_data(self):
        """
        清空所有信息
        :return:
        """
        # 清空歌曲清单
        self.__music_lb__.delete(0,END)
        # 清空输入框
        self.__set_all_entry()
        # 设置图片默认值
        self.__clear_albumimage()
        # 清空当前选择
        self.__curselection_music__ = None
        # 清空 id3
        self.__curselection_music_id3__ = None
        # 清空 歌词
        self.__set_lyrics()

    def __save_data(self):
        """
        保存
        :return:
        """
        # 当前是否选择了歌曲
        if (self.__curselection_music__ == None):
            TkMessage.warning("请选择歌曲")
            return None

        '''
            把所有的输入框的值填充到当前的 id3 信息中
        '''
        for name, member in Mp3Info.__members__.items():
            entry_data = self.__get_entry(member.value[0])
            if (entry_data != None):
                # 获取值保存
                self.__curselection_music_id3__[member.value[0]] = entry_data.get()

        # 获取歌词
        self.__curselection_music_id3__[Mp3Info.LYRICE.value[0]] = self.lyrics.get(0.0, END)

        # print(self.__curselection_music_id3__)

        # 保存
        if(self.mp3.save(self.__curselection_music_id3__)):
            TkMessage.info("保存成功")
        else:
            TkMessage.error("保存失败")

    def __music_lb_click(self,event):
        """
        music listbox 点击事件
        :param event: 事件信息
        :return: None
        """
        # 判断 当元祖 不为空
        if(self.__music_lb__.curselection()):
            # 读取 id3 信息
            self.__read_music_id3(self.__music_lb__.get(self.__music_lb__.curselection()))
            self.__curselection_music__ = self.__music_lb__.curselection()

    def __read_music_id3(self , file_path):
        """
        读取mp3 的 id3v1 信息
        :param filePath: 文件路径
        :return:
        """
        self.mp3 = id3 = ID3(file_path)
        self.__curselection_music_id3__ = id3v1 = id3.v1info()
        id3image = id3v1[Mp3Info.IMAGE.value[0]]

        # 变更图片
        if(id3image != None):
            self.__replace_albumimage(self.__create_albumimage(bytes=id3image))
        else:
            self.__replace_albumimage(self.__create_albumimage())

        # 变更歌词
        self.__set_lyrics(id3v1)

        # 变更 id3 信息
        self.__set_all_entry(id3v1)

    def __add_attr(self,master):
        """
        添加属性
        :param master: 依附窗体
        :return: None
        """
        row = 0     # 第 0 行开始
        sticky = E  # 左对齐
        column = 0  # 列
        padx = 2    # 左右边距

        len = 1

        # 所有字段分 3 列 , 去掉 time , image , lyrics 枚举字段 除 2 为换列的数值
        newcolumn = math.ceil((Mp3Info.__len__() - 3) / 2)

        # 时间 、 图片不是属性
        for key,member in Mp3Info.__members__.items():

            if(member is Mp3Info.TIME):
                continue
            elif(member is Mp3Info.IMAGE):
                continue
            elif(member is Mp3Info.LYRICE):
                continue

            Label(master, text=member.value[0]).grid(row=row, column=column, sticky=sticky, padx=padx)
            self.__add_entry(member.value[0], master).grid(row=row, column=(column + 1), pady=padx)

            if (len == newcolumn):
                column += 2
                row = 0
                len = 1
            else:
                len += 1 # 数量++
                row += 1


    def __add_entry(self ,attrbute_name , root=None ):
        """
        设置输入框
        :param attrbuteName: 属性名称
        :param root: 依附的窗体
        :return: 当前输入框实体
        """
        if(root != None):
            self.__entrys__[attrbute_name] = Entry(root)
        else:
            self.__entrys__[attrbute_name] = Entry()
        return self.__entrys__[attrbute_name]

    def __get_entry(self,attrbute_name):
        """
        获取输入框
        :param attrbuteName: 属性名称
        :return: 输入框实体 , 如果没有该属性返回 None
        """
        if (attrbute_name in self.__entrys__):
            return self.__entrys__[attrbute_name]

        return None

    def __set_all_entry(self , data=None):
        """
        批量设置输入框值
        :param data: json|map 对象
        :return: None
        """
        if(data == None):
            # 清空
            for k in self.__entrys__:
                self.__set_entry(k, "")
        else:
            for k,v in data.items():
                self.__set_entry(k, v)

    def __set_entry(self ,attrbute_name, val=""):
        """
        设置输入框值值
        :param attrbuteName: 属性名称
        :param val: 值 默认为空
        :return:
        """
        if(self.__get_entry(attrbute_name) != None):
            self.__entrys__[attrbute_name].delete(0, END)
            self.__entrys__[attrbute_name].insert(0, val)

    def __create_albumimage(self , path='images/defaultAlbum.jpeg' , bytes=None , size=(230,230)):
        """
        创建专辑封面
        :param path: 图片路径 如果 bytes 不为None 通过 bytes 读取   2 选 1
        :param bytes: 图片二进制字节 如果字节为 None 通过路径读取     2 选 1
        :param size: 图片显示大小
        :return:
        """

        if (bytes != None):
            image = Image.open(BytesIO(bytes)).resize(size, Image.ANTIALIAS)
            # 替换 id3 中的信息
            self.__curselection_music_id3__[Mp3Info.IMAGE.value[0]] = bytes
        else:
            image = Image.open(path).resize(size, Image.ANTIALIAS)
            if(path != 'images/defaultAlbum.jpeg'):
                # 替换 id3 中的信息
                bytes = io.BytesIO()
                image.save(bytes, format='JPEG')
                bytes = bytes.getvalue()
                self.__curselection_music_id3__[Mp3Info.IMAGE.value[0]] = bytes

        return ImageTk.PhotoImage(image)

    def __replace_albumimage(self, img):
        """
        替换图片
        :param img: 通过 __create_albumimage 生成对象
        :return:
        """
        self._albumimage.configure(image=img)
        self._albumimage.image = img

    def __choose_albumimage(self):
        """
        选择一张专辑图片
        :return:
        """
        filename = askopenfilename(filetypes=[("image file", [".png",".jpeg",".jpg"])])
        # 替换图片
        self.__replace_albumimage(self.__create_albumimage(path=filename))

    def __clear_albumimage(self):
        """
        恢复专辑图片默认
        :return:
        """
        self.__replace_albumimage(self.__create_albumimage())

    def __add_lyrics(self,master):
        Label(master, text="歌词").grid(row=0, column=3, sticky=W)
        self.lyrics = lyrics = Text(master, width=30, height=18)
        lyrics.grid(row=1, column=3)

    def __set_lyrics(self,data=None):

        self.lyrics.delete(1.0, END)
        if(data != None):
            self.lyrics.insert(1.0, data[Mp3Info.LYRICE.value[0]])

    def __choose_musicfile(self):
        """
        选择文件响应事件
        :return: None
        """

        # 获取名称
        filename = askopenfilename(filetypes=[("mp3 file", ".mp3")])
        if(filename == ""):
            return
        # 截取路径 与 名称

        # 插入列表
        self.__music_lb__.insert(END, filename)

    def __choose_musicdir(self):
        """
        选择文件夹响应事件
        :return:
        """

        dirName = askdirectory()

        file_names = [name for name in os.listdir(dirName) if name.endswith('.mp3')]

        if file_names:
            for name in file_names:
                self.__music_lb__.insert(END, dirName + "/" + name)
