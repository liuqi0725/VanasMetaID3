# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : Mp3Id3.py
# @Created  : 2020/2/11 9:49 PM
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

from mutagen.mp3 import MP3
import mutagen.id3
from mutagen.easyid3 import EasyID3

from com.liuqi.vanas.id3.config import Mp3Info
from com.liuqi.vanas.id3.config import Id3Tag



class ID3 :

    def __init__(self , filePath):

        # id3info = MP3(filePath, ID3=EasyID3)
        # for k, v in id3info.items():
        #     print(k)

        self.__audio = MP3(filePath)
        self.__id3clear()
        self.__parseInfo()

    def __id3clear(self):

        self.__id3 = {}
        for key, member in Mp3Info.__members__.items():
            self.__id3[member.value[0]] = member.value[1]

    def info(self):
        return self.__id3

    def image(self):
        return self.__id3[Mp3Info.IMAGE.value[0]]


    def __parseInfo(self):
        # self.__getTime()
        # self.__getTitle()
        # self.__getAlbum()
        # self.__getArtist()
        # self.__getGrouping()
        # self.__getTrack()
        # self.__getDisc()
        # self.__getBpm()
        # self.__getComposter()
        # self.__getGenre()
        # self.__getYear()
        # self.__getImage()
        # self.__getComments()
        # self.__getLyrics()

        self.__getTags()

    def __getTags(self):

        for key,member in Id3Tag.__members__.items():
            data = self.__getTag(member.value[0])
            if(data != None):
                if(key == Id3Tag.LYRICE.name):
                    self.__id3[member.value[1]] = data.text
                elif(key == Id3Tag.IMAGE.name):
                    self.__id3[member.value[1]] = data.data
                else:
                    self.__id3[member.value[1]] = data.text[0]

    # def __getTitle(self):
    #     data = self.__getTag("TIT2")
    #     if (data != None):
    #         self.__id3[Mp3Info.TITLE.value[0]] = data.text[0]
    #
    # def __getAlbum(self):
    #     data = self.__getTag("TALB")
    #     if (data != None):
    #         self.__id3[Mp3Info.ALBUM.value[0]] = data.text[0]
    #
    # def __getArtist(self):
    #     data = self.__getTag("TPE1")
    #     if (data != None):
    #         self.__id3[Mp3Info.ARTIST.value[0]] = data.text[0]
    #
    # def __getGrouping(self):
    #     data = self.__getTag("TIT1")
    #     if (data != None):
    #         self.__id3[Mp3Info.GROUPING.value[0]] = data.text[0]
    #
    # def __getGenre(self):
    #     data = self.__getTag("TCON")
    #     if (data != None):
    #         self.__id3[Mp3Info.GENRE.value[0]] = data.text[0]
    #
    # def __getComposter(self):
    #     data = self.__getTag("TCOM")
    #     if (data != None):
    #         self.__id3[Mp3Info.COMPOSTER.value[0]] = data.text[0]
    #
    # def __getYear(self):
    #     data = self.__getTag("TDRC")
    #     if (data != None):
    #         self.__id3[Mp3Info.YEAR.value[0]] = data.text[0]
    #
    # def __getTrack(self):
    #     data = self.__getTag("TRCK")
    #     if (data != None):
    #         self.__id3[Mp3Info.TRACK.value[0]] = data.text[0]
    #
    # def __getDisc(self):
    #     data = self.__getTag("TPOS")
    #     if (data != None):
    #         self.__id3[Mp3Info.DISC.value[0]] = data.text[0]
    #
    # def __getBpm(self):
    #     data = self.__getTag("TBPM")
    #     if (data != None):
    #         self.__id3[Mp3Info.BPM.value[0]] = data.text[0]
    #
    # def __getComments(self):
    #     data = self.__getTag("COMM::eng")
    #     if (data != None):
    #         self.__id3[Mp3Info.COMMENTS.value[0]] = data.text[0]
    #
    # def __getLyrics(self):
    #     data = self.__getTag("USLT::eng")
    #     if (data != None):
    #         self.__id3[Mp3Info.LYRICE.value[0]] = data.text
    #         #print(data.text)
    #
    # def __getImage(self):
    #     data = self.__getTag("APIC:")
    #     if (data != None):
    #         self.__id3[Mp3Info.IMAGE.value[0]] = data.data
    #
    # def __getTime(self):
    #     self.__id3[Mp3Info.TIME.value[0]] = self.__audio.info.length
    #

    def __getTag(self , tagname):
        """
        获取标签值
        :param tagname:
        :return:
        """
        if(tagname in self.__audio.tags):
            return self.__audio.tags[tagname]
        else:
            return None

    def save(self, id3):

        '''
        0 ISO-8859-1
        1 UTF16 with BOM
        2 UTF-16BE without BOM
        3 UTF8
        '''
        encoding = 3

        for key in id3:

            if(key is Id3Tag.TITLE.value[1]):
                self.__audio[Id3Tag.TITLE.value[0]] = mutagen.id3.TIT2(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif(key is Id3Tag.ALBUM.value[1]):
                self.__audio[Id3Tag.ALBUM.value[0]] = mutagen.id3.TALB(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.ARTIST.value[1]):
                self.__audio[Id3Tag.ARTIST.value[0]] = mutagen.id3.TPE1(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.COMPOSTER.value[1]):
                self.__audio[Id3Tag.COMPOSTER.value[0]] = mutagen.id3.TCOM(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.GROUPING.value[1]):
                self.__audio[Id3Tag.GROUPING.value[0]] = mutagen.id3.TIT1(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.GENRE.value[1]):
                self.__audio[Id3Tag.GENRE.value[0]] = mutagen.id3.TCON(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.TRACK.value[1]):
                self.__audio[Id3Tag.TRACK.value[0]] = mutagen.id3.TRCK(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.DISC.value[1]):
                self.__audio[Id3Tag.DISC.value[0]] = mutagen.id3.TPOS(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.YEAR.value[1]):
                self.__audio[Id3Tag.YEAR.value[0]] = mutagen.id3.TDRC(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.BPM.value[1]):
                self.__audio[Id3Tag.BPM.value[0]] = mutagen.id3.TBPM(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.COMMENTS.value[1]):
                self.__audio[Id3Tag.COMMENTS.value[0]] = mutagen.id3.COMM(
                    encoding=encoding,
                    text=[id3[key]]
                )
            elif (key is Id3Tag.LYRICE.value[1]):
                self.__audio[Id3Tag.LYRICE.value[0]] = mutagen.id3.USLT(
                    encoding=encoding,
                    lang='eng',
                    text=id3[key]
                )
            elif (key is Id3Tag.IMAGE.value[1] and id3[key] != None):
                self.__audio[Id3Tag.IMAGE.value[0]] = mutagen.id3.APIC(
                    encoding=encoding,
                    mime='image/jpeg',
                    type=3,
                    data=id3[key]
                )

        try:
            self.__audio.save()
            return True
        except Exception as e:
            print('VanasMetaId3 save Error >> ',e)
            return False

