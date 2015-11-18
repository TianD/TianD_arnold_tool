#coding:utf-8
'''
Created on 2015年11月18日 下午3:53:11

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import pymel.core as pm

import ass_tool as at 
            
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
                
                
                
                at.setASSParameter(n, "filename", newfilename)
            at.saveASS(ass_file)