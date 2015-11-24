#_*_encoding:utf-8_*_
#-------------------------------------------------------------------------------
# Name:        自动打包工具
# Purpose:
#
# Author:      kangpeng
#
# Created:     23/11/2015
# Copyright:   (c) kangpeng 2015
# Licence:     <1.0.0>
#-------------------------------------------------------------------------------


import os, sys, shutil,zipfile

CHANNEL_LIST = 'channel_list'
SRC_APK_DIR = './src/'
OUT_APK_DIR = './out/'
SCAN_FILE_EXT = '.apk'

##查找源APK
def findApk(filePath):
    for file in os.listdir(filePath):
        if os.path.splitext(file)[1] == SCAN_FILE_EXT:
            return os.path.splitext(file)


##生成临时文件
def createFile(fileName):
    fileHandle = open ( 'META-INF/'+fileName, 'w' )
    fileHandle.write ( '' )
    fileHandle.close()

##移动渠道文件
def moveChannelFile(fileName):
    os.remove ( 'META-INF/'+fileName)

##拷贝文件
def copyFile(srcFileName,dstFileName):
    shutil.copy(srcFileName, dstFileName)

##导入渠道包
def importChannel(srcFile,channelFile):
    zipped = zipfile.ZipFile(srcFile, 'a', zipfile.ZIP_DEFLATED)
    empty_channel_file = "META-INF/{channel}".format(channel=channelFile)
    zipped.write('META-INF/'+channelFile, empty_channel_file)
    zipped.close()

##移动文件
def moveFile(fileName,outFileName):
    shutil.move(fileName, OUT_APK_DIR+outFileName)




fileHandle = open ( CHANNEL_LIST)
while 1:
    line = fileHandle.readline()
    if not line:
        break
    createFile(line.rstrip())
    srcApk = findApk(SRC_APK_DIR)
    copyFile(SRC_APK_DIR+srcApk[0]+srcApk[1],srcApk[0]+srcApk[1])
    importChannel(srcApk[0]+srcApk[1],line.rstrip())
    moveFile(srcApk[0]+srcApk[1],srcApk[0]+'_'+line.rstrip()+srcApk[1])
##    moveChannelFile(line.rstrip())
    print 'channel: %s build complete'%(line.rstrip())




