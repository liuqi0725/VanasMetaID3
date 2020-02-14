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

@unique
class Id3Tag (Enum):

    # 歌曲名称
    TITLE = ("TIT2", Mp3Info.TITLE.value[0] , mutagen.id3.TIT2)
    # 专辑名称
    ALBUM = ("TALB", Mp3Info.ALBUM.value[0] , mutagen.id3.TALB)
    # 艺术家
    ARTIST = ("TPE1", Mp3Info.ARTIST.value[0] , mutagen.id3.TPE1)
    # 作曲
    COMPOSTER = ("TCOM", Mp3Info.COMPOSTER.value[0],mutagen.id3.TCOM)
    # 组
    GROUPING = ("TIT1", Mp3Info.GROUPING.value[0],mutagen.id3.TIT1)
    # 类型
    GENRE = ("TCON", Mp3Info.GENRE.value[0],mutagen.id3.TCON)
    # 轨道
    TRACK = ("TRCK", Mp3Info.TRACK.value[0],mutagen.id3.TRCK)
    #
    DISC = ("TPOS", Mp3Info.DISC.value[0],mutagen.id3.TPOS)
    # 发布年份
    YEAR = ("TDRC", Mp3Info.YEAR.value[0],mutagen.id3.TDRC)
    # bpm
    BPM = ("TBPM", Mp3Info.BPM.value[0],mutagen.id3.TBPM)
    # 评分 未找到字段
    #RATING = ("rating", Id3Attribute.RATING.value[0])
    # 歌词
    LYRICE = ("USLT::eng", Mp3Info.LYRICE.value[0],mutagen.id3.USLT)
    # 评论
    COMMENTS = ("COMM::XXX", Mp3Info.COMMENTS.value[0],mutagen.id3.COMM)
    # 图片地址
    IMAGE = ("APIC:", Mp3Info.IMAGE.value[0],mutagen.id3.APIC)