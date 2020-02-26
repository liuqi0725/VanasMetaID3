## VanasMetaID3 是一个简单修改 MP3 ID3 信息的工具

### 前言

现在听个音乐太难了,各大播放器在版权争夺下搞得一个音乐市场乌烟瘴气。有些歌这个平台可以听有些歌那个平台可以听。想听全就都买 VIP。懒得折腾了,还是回到起点吧"==下载音乐=="。因为主要上下班开车听听歌,发现下载下来的音乐很多都没有 id3 信息，网上找一些编辑 ID3 信息的编辑后，还是乱码。原因是现在基本都是 ID3 V2 信息了，没有写入 ID3 V1 信息。那么一些老款车或者中控都不支持 ID3 V2(比如我的车时 2012 款)，就会显示乱码。就想用 python 随便写一个来用用

### 开发环境

+ Python 3.8
+ MacOS Catalina 10.15.3 

### 引入包

+ mutagen 1.44.0
+ Pillow 7.0.0
+ tkinter 8.6 

### 关于 tkinter 包的说明

+ 如果是[python](https://www.python.org)官网下载安装,python3.7.x 以上都默认安装的 tkinter 8.6。

+ 如果是 brew 安装,当前最新版是 3.7.6 ,tkinter 是 8.5

**如果tkinter 是 8.5 ,会出现输入框无法输入中文的 bug。这个在 [python官网上有说明](https://www.python.org/download/mac/tcltk/)**

网上有很多解决办法,看你怎么选择,我懒得折腾,直接 brew 安装的卸载了。从官网下的 3.8 来安装

### 功能

#### V0.1
    
  + 读取 mp3 文件
  + 从文件夹中读取 mp3 文件
  + 读取 mp3 ID3 信息(图片、歌词、标题、专辑....)
  + 修改 mp3 ID3 信息
  
  > 注意 图片、歌词等属于 V2 信息，V1 信息只有文件末尾的 128k 的数据，代码里有说明

  ![](http://pic.fangxutuwen.com/15827086640315.jpg)

  ![](http://pic.fangxutuwen.com/15827087089609.jpg)

### 打包成可执行的 APP

**先安装 `py2app` , 当前最新是 0.21**
```bash
pip3 install py2app
```

**打包成 APP**

如需设置 app，请修改`setup.py`, 具体设置方法参考 [py2app-0.21-Doc](https://py2app.readthedocs.io/en/latest/index.html)

```bash
# 项目目录下执行 
# 如果要拷贝到其他没有 python 环境的机器使用 去掉`-A` 打包所有包
python3 setup.py py2app -A
```

**app 存放在项目目录 py2app 创建的 dist 目录下**
