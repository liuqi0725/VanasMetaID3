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

from com.liuqi.vanas.id3.config import Id3Attribute
from com.liuqi.vanas.id3.config import Id3V1Tag



class Id3V1 :

    def __init__(self , filePath):

        # id3info = MP3(filePath, ID3=EasyID3)
        # for k, v in id3info.items():
        #     print(k)

        self.__audio = MP3(filePath)
        self.__id3v1clear()
        self.__parseInfo()

    def __id3v1clear(self):

        self.__id3V1 = {}
        for key, member in Id3Attribute.__members__.items():
            self.__id3V1[member.value[0]] = member.value[1]

    def v1info(self):
        return self.__id3V1

    def image(self):
        return self.__id3V1[Id3Attribute.IMAGE.value[0]]


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

        self.__getV1Tags()

    def __getV1Tags(self):

        for key,member in Id3V1Tag.__members__.items():
            data = self.__getTag(member.value[0])
            if(data != None):
                if(key == Id3V1Tag.LYRICE.name):
                    self.__id3V1[member.value[1]] = data.text
                elif(key == Id3V1Tag.IMAGE.name):
                    self.__id3V1[member.value[1]] = data.data
                else:
                    self.__id3V1[member.value[1]] = data.text[0]

    def __getTitle(self):
        data = self.__getTag("TIT2")
        if (data != None):
            self.__id3V1[Id3Attribute.TITLE.value[0]] = data.text[0]

    def __getAlbum(self):
        data = self.__getTag("TALB")
        if (data != None):
            self.__id3V1[Id3Attribute.ALBUM.value[0]] = data.text[0]

    def __getArtist(self):
        data = self.__getTag("TPE1")
        if (data != None):
            self.__id3V1[Id3Attribute.ARTIST.value[0]] = data.text[0]

    def __getGrouping(self):
        data = self.__getTag("TIT1")
        if (data != None):
            self.__id3V1[Id3Attribute.GROUPING.value[0]] = data.text[0]

    def __getGenre(self):
        data = self.__getTag("TCON")
        if (data != None):
            self.__id3V1[Id3Attribute.GENRE.value[0]] = data.text[0]

    def __getComposter(self):
        data = self.__getTag("TCOM")
        if (data != None):
            self.__id3V1[Id3Attribute.COMPOSTER.value[0]] = data.text[0]

    def __getYear(self):
        data = self.__getTag("TDRC")
        if (data != None):
            self.__id3V1[Id3Attribute.YEAR.value[0]] = data.text[0]

    def __getTrack(self):
        data = self.__getTag("TRCK")
        if (data != None):
            self.__id3V1[Id3Attribute.TRACK.value[0]] = data.text[0]

    def __getDisc(self):
        data = self.__getTag("TPOS")
        if (data != None):
            self.__id3V1[Id3Attribute.DISC.value[0]] = data.text[0]

    def __getBpm(self):
        data = self.__getTag("TBPM")
        if (data != None):
            self.__id3V1[Id3Attribute.BPM.value[0]] = data.text[0]

    def __getComments(self):
        data = self.__getTag("COMM::eng")
        if (data != None):
            self.__id3V1[Id3Attribute.COMMENTS.value[0]] = data.text[0]

    def __getLyrics(self):
        data = self.__getTag("USLT::eng")
        if (data != None):
            self.__id3V1[Id3Attribute.LYRICE.value[0]] = data.text
            #print(data.text)

    def __getImage(self):
        data = self.__getTag("APIC:")
        if (data != None):
            self.__id3V1[Id3Attribute.IMAGE.value[0]] = data.data

    def __getTime(self):
        self.__id3V1[Id3Attribute.TIME.value[0]] = self.__audio.info.length

    def __getTag(self , tagname):
        if(tagname in self.__audio.tags):
            return self.__audio.tags[tagname]
        else:
            return None

    def __save_str_tag(self , tag , cls , encoding, content):
        self.__audio[tag] = cls(
            encoding=encoding,
            text=[content]
        )

    def save(self, id3v1):

        audio = {}
        '''
        0 ISO-8859-1
        1 UTF16 with BOM
        2 UTF-16BE without BOM
        3 UTF8
        '''
        encoding = 3

        for key in id3v1:

            if(key is Id3V1Tag.TITLE.value[1]):
                self.__audio[Id3V1Tag.TITLE.value[0]] = mutagen.id3.TIT2(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif(key is Id3V1Tag.ALBUM.value[1]):
                self.__audio[Id3V1Tag.ALBUM.value[0]] = mutagen.id3.TALB(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.ARTIST.value[1]):
                self.__audio[Id3V1Tag.ARTIST.value[0]] = mutagen.id3.TPE1(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.COMPOSTER.value[1]):
                self.__audio[Id3V1Tag.COMPOSTER.value[0]] = mutagen.id3.TCOM(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.GROUPING.value[1]):
                self.__audio[Id3V1Tag.GROUPING.value[0]] = mutagen.id3.TIT1(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.GENRE.value[1]):
                self.__audio[Id3V1Tag.GENRE.value[0]] = mutagen.id3.TCON(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.TRACK.value[1]):
                self.__audio[Id3V1Tag.TRACK.value[0]] = mutagen.id3.TRCK(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.DISC.value[1]):
                self.__audio[Id3V1Tag.DISC.value[0]] = mutagen.id3.TPOS(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.YEAR.value[1]):
                self.__audio[Id3V1Tag.YEAR.value[0]] = mutagen.id3.TDRC(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.BPM.value[1]):
                self.__audio[Id3V1Tag.BPM.value[0]] = mutagen.id3.TBPM(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.COMMENTS.value[1]):
                self.__audio[Id3V1Tag.COMMENTS.value[0]] = mutagen.id3.COMM(
                    encoding=encoding,
                    text=[id3v1[key]]
                )
            elif (key is Id3V1Tag.LYRICE.value[1]):
                self.__audio[Id3V1Tag.LYRICE.value[0]] = mutagen.id3.USLT(
                    encoding=encoding,
                    lang='eng',
                    text=id3v1[key]
                )
            elif (key is Id3V1Tag.IMAGE.value[1] and id3v1[key] != None):
                self.__audio[Id3V1Tag.IMAGE.value[0]] = mutagen.id3.APIC(
                    encoding=encoding,
                    mime='image/jpeg',
                    type=3,
                    data=id3v1[key]
                )

        try:
            self.__audio.save()
            return True
        except Exception as e:
            print('VanasMetaId3 save Error >> ',e)
            return False

