# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : TkMessage.py
# @Created  : 2020/2/12 1:48 PM
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

from tkinter import messagebox

def info(msg, title="提示"):
    messagebox.showinfo(title, msg)

def warning(msg, title="警告"):
    messagebox.showwarning(title, msg)

def error(msg, title="错误"):
    messagebox.showwarning(title, msg)