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
import traceback

import os
import struct

from com.liuqi.vanas.id3.config import Mp3Info
from com.liuqi.vanas.id3.config import Id3Tag
from com.liuqi.vanas.id3.config import Id3Encodeing

from com.liuqi.vanas.id3.config import ID3V1_DEFAULT_CODE

'''
ID3 V1,V2 信息 参考资料
https://blog.csdn.net/liuyan4794/article/details/7747769
'''


class ID3V1:

    def __init__(self,filePath):
        self._filePath = filePath

    def save(self , id3_info):
        """
        保存 id3 v1 信息
        :param id3_info: 用户的 id3 信息
        :return:
        """
        # 读取当前的数据
        all_bytes, last128_bytes = self._getBytesData()

        # 获取保存数据
        save_data = self._getSaveData(all_bytes, last128_bytes, id3_info)

        fileStream = open(self._filePath, "wb")
        try:
            #print(save_data[-128:])
            fileStream.write(save_data)
        except Exception as e:
            # 出现异常，写入原始字节，保持数据不变
            fileStream.write(all_bytes)
            print("Save mp3 ID3 V1 Error.",e)
            traceback.print_exc()
        finally:
            if fileStream:
                fileStream.close()

    def _getSaveData(self , all_bytes, last128_bytes , id3_info):
        """
        获取保存的字节数据
        :param all_bytes: 当前文件的所有字节
        :param last128_bytes: 最后 128 位字节
        :param id3_info: 用户的 id3 信息
        :return:
        """

        '''
        ID3v1 在文件结尾，以字符串“TAG”为标识，其长度是固定的 128 个字节
        Header[3]       长度 3    固定值 TAG
        Title[30]       长度 30
        Artist[30]      长度 30
        Album[30]       长度 30
        Year[4]         长度 4
        Comment[30]     长度 28-30 懒得搞，统一 30，并占用 Track 的字节
        Genre           长度 1 -----懒得设置枚举，都为空
        Track           长度 1 -----不需要

        3+30+30+30+4+30+1 = 128

        ①如果MP3的注释＝30字节，那么就要占用 Reserved 和 Track 两个字节，这要看 Reserved 是否＝0，如果＝0，那么注释有 28 个字节。如果不是，那么注释有 30 个字节。当注释＝30 个字节的时候，那就没有 Track 了。
        ②如果 MP3 文件后面虽然有“TAG”三个字母，但字母后面全是0，那就不是一个合法的 ID3V1 信息，应该认为没有 ID3V1 信息。
        ③ID3V1 的各项信息都是顺序存放，没有任何标识将其分开，一般用 0补足规定的长度。比如歌曲名有 20 个字节，则在歌曲名后要补足 10 个 0，否则将造成信息错误。
        ④歌曲风格共 148 种，用编号表示，表2列出了前 30 种的风格与编号对照，详情可上网查询。
        '''

        #print("Music last 128k >> ",last128_bytes)

        header = self._encodeData('TAG')

        # 组装 ID3 V1 信息，注意必须严格按照长度
        # 假设全部是中文，中文占 2 个字节,那么30 个字节只能输入 15 个中文，截取 15
        id3V1_128k = struct.pack('3s30s30s30s4s30ss',
                          header,
                          self._encodeData(id3_info[Id3Tag.TITLE.title][:15]),
                          self._encodeData(id3_info[Id3Tag.ARTIST.title][:15]),
                          self._encodeData(id3_info[Id3Tag.ALBUM.title][:15]),
                          self._encodeData(id3_info[Id3Tag.YEAR.title][:4]),
                          self._encodeData(id3_info[Id3Tag.COMMENTS.title][:15]),
                          self._encodeData("")
                        )

        # 判断是替换还是添加
        if last128_bytes[0:3] != header:
            # 最后 128 字节 不是以 TAG 开头，没有 ID3 V1
            return (all_bytes + id3V1_128k)
        else:
            # 以 TAG 开头， 有 ID3 V1 信息，直接替换最后 128 位
            return (all_bytes[0:-128] + id3V1_128k)

    def _getBytesData(self):
        """
        读取文件字节
        :param filePath: 文件路径
        :return: all,last128
        """
        # 打开文件
        audio_file = open(os.path.join(self._filePath), "rb")
        # 全部字节
        all_data = audio_file.read()
        # 最后 128 位字节
        audio_file.seek(-128, 2)
        last128_data = audio_file.read()

        audio_file.close()

        return all_data,last128_data

    def _encodeData(self,text):
        """
        字符编码
        :param text:
        :return:
        """
        return text.encode(ID3V1_DEFAULT_CODE)


class ID3V2:

    def __init__(self,audio):
        self._v2 = self.__default()
        self._audio = audio

    def __default(self):
        _id3V2 = {}
        for key, member in Mp3Info.__members__.items():
            _id3V2[member.title] = member.dval
        return _id3V2

    def info(self):
        """
        获取 v2 信息
        :return:
        """
        for key,member in Id3Tag.__members__.items():
            data = self.__getTag(member.tag_name)
            if(data != None):
                if(key == Id3Tag.LYRICE.name):
                    self._v2[member.title] = data.text
                elif(key == Id3Tag.IMAGE.name):
                    self._v2[member.title] = data.data
                else:
                    self._v2[member.title] = data.text[0]

        return self._v2

    def __getTag(self , tagname):
        """
        获取标签值
        :param tagname:
        :return:
        """
        if(tagname in self._audio.tags):
            return self._audio.tags[tagname]
        else:
            return None

    def __data_encoding(self, data , encoding):
        if(Id3Encodeing.ISO88592.code == encoding):
            return data.encode("GBK")

        return data

    def save(self, id3_info, encoding):

        '''
        encoding

        0 ISO-8859-1
        1 UTF16 with BOM
        2 UTF-16BE without BOM
        3 UTF8
        '''

        try:

            for key in id3_info:

                if (key is Id3Tag.TITLE.title):
                    self._audio[Id3Tag.TITLE.tag_name] = mutagen.id3.TIT2(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.ALBUM.title):
                    self._audio[Id3Tag.ALBUM.tag_name] = mutagen.id3.TALB(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.ARTIST.title):
                    self._audio[Id3Tag.ARTIST.tag_name] = mutagen.id3.TPE1(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.COMPOSTER.title):
                    self._audio[Id3Tag.COMPOSTER.tag_name] = mutagen.id3.TCOM(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.GROUPING.title):
                    self._audio[Id3Tag.GROUPING.tag_name] = mutagen.id3.TIT1(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.GENRE.title):
                    self._audio[Id3Tag.GENRE.tag_name] = mutagen.id3.TCON(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.TRACK.title):
                    self._audio[Id3Tag.TRACK.tag_name] = mutagen.id3.TRCK(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.DISC.title):
                    self._audio[Id3Tag.DISC.tag_name] = mutagen.id3.TPOS(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.YEAR.title):
                    self._audio[Id3Tag.YEAR.tag_name] = mutagen.id3.TDRC(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.BPM.title):
                    self._audio[Id3Tag.BPM.tag_name] = mutagen.id3.TBPM(
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.COMMENTS.title):
                    self._audio[Id3Tag.COMMENTS.tag_name] = mutagen.id3.COMM(
                        lang = 'eng',
                        encoding=encoding,
                        text=[self.__data_encoding(id3_info[key], encoding)]
                    )
                elif (key is Id3Tag.LYRICE.title):
                    self._audio[Id3Tag.LYRICE.tag_name] = mutagen.id3.USLT(
                        lang='eng',
                        encoding=encoding,
                        text=self.__data_encoding(id3_info[key], encoding)
                    )
                elif (key is Id3Tag.IMAGE.title and id3_info[key] != None):
                    # 图片始终用 UTF8 编码
                    self._audio[Id3Tag.IMAGE.tag_name] = mutagen.id3.APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        data=id3_info[key]
                    )

            #print(self._audio)

            self._audio.save()

            return True
        except Exception as e:
            print('VanasMetaId3 save Error >> ', e)
            traceback.print_exc()
            return False


class ID3:

    def __init__(self , filePath):

        #print(">>>>>>>>>>>>>. ID3 onload start.")
        # 不建议用 EasyID3 获取不到歌词，图片等信息
        _audio = MP3(filePath)

        self._v1 = ID3V1(filePath)
        self._v2 = ID3V2(_audio)

        #print(_audio)
        #print(">>>>>>>>>>>>>. ID3 onload End.")

    def info(self):
        """
        获取mp3 id3 用v2 显示
        :return:
        """
        return self._v2.info()

    def save(self, id3_info , encoding=Id3Encodeing.UTF8.code , save_v1=True):
        """
        保存用户填写的歌曲信息
        :param id3_info: 用户的 id3 信息
        :param encoding: 字符编码 参考 Id3Encodeing
        :param save_v1: 是否保存 V1 默认 True
        :return:
        """

        flag = self._v2.save(id3_info,encoding)

        if flag and save_v1:
            self._v1.save(id3_info)

        return flag




