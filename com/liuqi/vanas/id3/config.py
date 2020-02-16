# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : id3attr.py
# @Created  : 2020/2/12 10:28 AM
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

from enum import Enum,unique,auto
import mutagen.id3

ID3V1_DEFAULT_CODE = "gbk"

@unique
class Mp3Info (Enum):

    # 时间 秒
    TIME = ("time",0)
    # 歌曲名称
    TITLE = ("title","")
    # 专辑名称
    ALBUM = ("album","")
    # 艺术家
    ARTIST = ("artist","")
    # 作曲
    COMPOSTER = ("composter","")
    # 组
    GROUPING = ("grouping","")
    # 类型
    GENRE = ("genre","0/0")
    # 轨道
    TRACK = ("track","0/0")
    #
    DISC = ("disc","")
    # 发布年份
    YEAR = ("year","")
    # bpm
    BPM = ("bpm","")
    # 评分
    #RATING = ("rating","")
    # 歌词
    LYRICE = ("lyrics","")
    # 评论
    COMMENTS = ("comments","")
    # 图片地址
    IMAGE = ("image",None)

    def __init__(self , title, dval):
        self._title = title
        self._dval = dval

    @property
    def title(self):
        return self._title

    @property
    def dval(self):
        """
        默认值
        :return:
        """
        return self._dval


@unique
class Id3Tag (Enum):

    # 歌曲名称
    TITLE = ("TIT2", Mp3Info.TITLE.title , mutagen.id3.TIT2)
    # 专辑名称
    ALBUM = ("TALB", Mp3Info.ALBUM.title , mutagen.id3.TALB)
    # 艺术家
    ARTIST = ("TPE1", Mp3Info.ARTIST.title , mutagen.id3.TPE1)
    # 作曲
    COMPOSTER = ("TCOM", Mp3Info.COMPOSTER.title,mutagen.id3.TCOM)
    # 组
    GROUPING = ("TIT1", Mp3Info.GROUPING.title,mutagen.id3.TIT1)
    # 类型
    GENRE = ("TCON", Mp3Info.GENRE.title,mutagen.id3.TCON)
    # 轨道
    TRACK = ("TRCK", Mp3Info.TRACK.title,mutagen.id3.TRCK)
    #
    DISC = ("TPOS", Mp3Info.DISC.title,mutagen.id3.TPOS)
    # 发布年份
    YEAR = ("TDRC", Mp3Info.YEAR.title,mutagen.id3.TDRC)
    # bpm
    BPM = ("TBPM", Mp3Info.BPM.title,mutagen.id3.TBPM)
    # 评分 未找到字段
    #RATING = ("rating", Id3Attribute.RATING.title)
    # 歌词
    LYRICE = ("USLT::eng", Mp3Info.LYRICE.title,mutagen.id3.USLT)
    # 评论
    COMMENTS = ("COMM::eng", Mp3Info.COMMENTS.title,mutagen.id3.COMM)
    # 图片地址
    IMAGE = ("APIC:", Mp3Info.IMAGE.title,mutagen.id3.APIC)

    def __init__(self , tag_name, title, id3_obj):
        self._tag_name = tag_name
        self._title = title
        self._id3_obj = id3_obj

    @property
    def tag_name(self):
        return self._tag_name

    @property
    def title(self):
        return self._title

    @property
    def id3_obj(self):
        return self._id3_obj

@unique
class Id3Encodeing(Enum):

    ISO88592 = 0 , "ISO-8859-1"

    UTF16B = 1 , "UTF16 with BOM"

    UTF16BE = 2 , "UTF-16BE without BOM"

    UTF8 = 3 , "UTF8"

    def __init__(self,code,text):
        self._code = code
        self._text = text

    @property
    def code(self):
        return self._code

    @property
    def text(self):
        return self._text

    @staticmethod
    def get_by_text(text):
        for name, member in Id3Encodeing.__members__.items():
            if text == member.text:
                return member

    @staticmethod
    def get_by_code(code):
        for name, member in Id3Encodeing.__members__.items():
            if code == member.code:
                return member

    def equal_text(self,_text):
        if self.text == _text:
            return self


