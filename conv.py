# -*- coding: utf-8 -*-

import os
import sys
import Image
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

pakFileList = []
fileSize = 0
folderCount = 0
imagesWithAlpha = 0
imagesWithoutAlpha = 0
paksdir = "./paks/"
tmpdir = "./tmp000/"
dstdir = "./dst000/"

#absolutepathprefix = os.popen("pwd").read().strip()
scriptdir = "/home/kkszysiu/doom3tgatoetc1/"
sdkdir = "/home/kkszysiu/Pobrane/android-sdk-linux/"
imagemagickdir = "/home/kkszysiu/Dokumenty/imagemagick/bin/" # leave blank if default

for root, subFolders, files in os.walk(paksdir):
    for file in files:
        f = os.path.join(root, file)
        pakFileList.append(f)

print "Found pak files: ", pakFileList

for pakFile in pakFileList:
    pakFName = os.path.basename(pakFile).replace(".pk4", "")

    mkdir_p( scriptdir+"/"+pakFName+"/" )
    cmd = "unzip -u "+scriptdir+"/"+pakFile+" -d "+scriptdir+"/"+pakFName+"/"
    print "cmd:", cmd
    os.system(cmd)

for pakFile in pakFileList:
    pakFName = os.path.basename(pakFile).replace(".pk4", "")
    rootdir = "./"+pakFName+"/"
    fileList = []

    for root, subFolders, files in os.walk(rootdir):
        folderCount += len(subFolders)
        for file in files:
            f = os.path.join(root, file)
            fileSize = fileSize + os.path.getsize(f)

            splitext = os.path.splitext(f)
            if splitext[1] == ".tga":
                fileList.append(f)

    for imagef in fileList:
        cmd = imagemagickdir+"identify -format '%[channels]' "+imagef
        imgchannel = os.popen(cmd).read().strip()

        if imgchannel == "srgba" or imgchannel == "rgba":
            imagesWithAlpha += 1
        else:
            imagesWithoutAlpha += 1

            filetmpdir = os.path.dirname(imagef).replace(rootdir, tmpdir)
            filedstdir = os.path.dirname(imagef).replace(rootdir, dstdir)
            mkdir_p( filetmpdir )
            mkdir_p( filedstdir )
            splitext = os.path.splitext(imagef)
            fname = os.path.basename(imagef).replace(splitext[1], "")
            
            pngpath = "%s/%s.png" % (filetmpdir, fname)

            cmd = imagemagickdir+"convert "+imagef+" "+pngpath
            os.system(cmd)
            
            pkmpath = pngpath.replace(tmpdir, dstdir).replace(".png", ".pkm")
            
            cmd = sdkdir+"/tools/etc1tool "+scriptdir+"/"+pngpath+" --encode -o "+scriptdir+"/"+pkmpath
            print "cmd:", cmd
            os.system(cmd)


    print("Total Size is {0} bytes".format(fileSize))
    print("Total Files ", len(fileList))
    print("Total Folders ", folderCount) 
    print ("Images with alpha: ", imagesWithAlpha)
    print ("Images without alpha: ", imagesWithoutAlpha)

#import shutil
#shutil.rmtree('one/two/three')