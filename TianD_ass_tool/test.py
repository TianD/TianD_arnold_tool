#coding:utf-8
'''
Created on 2015年12月10日 上午10:50:01

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import os, os.path

import ass_tool


if __name__ == "__main__":
    for roots, dirs, files in os.walk("E:\\ArnoldStandIn"):
        for f in files:
            ass_tool.loadASS(os.path.join(roots, f))
            for n in ass_tool.getASSNode("MayaFile"):
                print n
                filename = ass_tool.getASSParameter(n, "filename")
                print filename
                newfilename = filename.replace("//kaixuan.com/kx", "Z:")
                print newfilename
                ass_tool.setASSParameter(n, "filename", newfilename)
            ass_tool.saveASS(os.path.join(roots, f))