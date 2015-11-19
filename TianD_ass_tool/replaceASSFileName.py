#coding:utf-8
'''
Created on 2015年11月18日 下午3:53:11

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import re

import pymel.core as pm

import ass_tool as at 
            
PROJ_SETS_SOURCEIMAGES_PATH_DIC = {
                "XFTL":  "//kaixuan.com/kx/Proj/Priject/xuanfengtuoluo/Project/sourceimages/sets/",             
                "SB": "//kaixuan.com/kx/Proj/SENBA/Project/sourceimages/sets/",
            }

rule = "(?P<proj>SB|XFTL)_(?P<scene>[cps]\d+\w*)_(?P<obj>\w*)_(?P<type>\w*)_(?P<size>\dk)"

def main():
    sel = pm.ls(sl=1)
    
    for i in sel:
        standin = i.getShape(type = "aiStandIn")
        if standin :
            ass_file = standin.dso.get()
            ass_name = pm.Path(ass_file).parent.namebase
            at.loadASS(ass_file)
            for n in at.getASSNode("MayaFile"):
                filename = at.getASSParameter(n, "filename")
                
                namebase = pm.Path(filename).namebase
                ext = pm.Path(filename).ext
                ma = re.match(rule, name)
                if ma:
                    proj = ma.group("proj")
                    scene = ma.group("scene")
                    path = PROJ_SETS_SOURCEIMAGES_PATH_DIC[proj]
                    fileinSer = os.path.join(path + scene, name+ext)
                    
                at.setASSParameter(n, "filename", fileinSer)
            at.saveASS(ass_file)