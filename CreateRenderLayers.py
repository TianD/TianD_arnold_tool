#coding:utf-8
'''
Created on 2015年10月26日 下午3:32:42

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import pymel.core as pm

from lightRenderData import ProjNameMatch

import aov_tool as at
import CreateNodeGroup as CNG


#创建显示层
#包括: chr_color, bg_color, IDP, shadow, OCCshadow, RGBlight, FOGlight
def saveFile(describe, dir = None):
    pnm = ProjNameMatch()
    if not dir:
        dir = pm.Env().sceneName().dirname()
    else :
        dir = pnm.setFileName()
    fileName = pm.Env().sceneName().namebase
    pnm.setFileName(fileName)
    if not dir:
        dir = pm.Env().sceneName().dirname()
    else :
        dir = pm.Path(pnm.getProjDirectorys()[-1]+pnm.getProjDirectorys()[0]+'/scenes')
    print dir
    project_name = pnm.getResults('project_name')
    episode_number = pnm.getResults('episode_number')
    session_number = pnm.getResults('session_number')
    scene_number = pnm.getResults('scene_number')
    scene_describe = pnm.getResults('scene_describe')
    process_name = 'lr'
    version_number = 'c001'
    newFileName = '_'.join([project_name, episode_number, session_number, scene_number, describe, process_name, version_number])
    filePrefix = '_'.join([project_name, episode_number, session_number, scene_number, describe, process_name])
    versions = []
    for f in dir.files():
        subpnm = ProjNameMatch()
        if filePrefix in f.namebase:
            subpnm.setFileName(f)
            versions.append(subpnm.getResults('version_number'))
    if versions:
        versions.sort()
        version_number = 'c'+ str(int(versions[-1][1:])+1)
        newFileName = '_'.join([project_name, episode_number, session_number, scene_number, describe, process_name, version_number])
    try:
        pm.saveAs("{0}/{1}.mb".format(dir, newFileName))
        return newFileName
    except:
        raise "save this file failure!!!"
    
def createRenderLayer(name):
    allgeos = getallGeos()
    topgrp = list(set([i.getParent(-1) for i in allgeos]))
    
    try:
        defaultLayer = pm.nodetypes.RenderLayer.defaultRenderLayer()
        defaultLayer.setCurrent()
    except:
        pass
    
    at.delAOV()
    
    renderLayers = pm.ls(type = 'renderLayer')
    for rl in renderLayers:
        if 'defaultRenderLayer' not in rl.name():
            pm.delete(rl)
    
    if name == "bg_color":
        for key in at.DEFAULT_AOV_DATA_TYPES.keys():
            at.createAOV(key)
    elif name == "chr_color":
        for key in at.DEFAULT_AOV_DATA_TYPES.keys():
            at.createAOV(key)
        importLight()
    elif name in ["chr_idp1", "chr_idp2", "chr_idp3", "bg_idp1", "bg_idp2", "bg_idp3"]:
        delAllShaders(topgrp)
        shader, sg = CNG.createIDPNode('Maeet')
        CNG.assignShader(topgrp, shader, sg)
    elif name == "shadow":
        delAllShaders(topgrp)
        at.createAOV('COCC')
        shader, sg = CNG.createShadow()
        CNG.assignShader(topgrp, shader, sg)
    elif name == "RGBlight":
        delAllShaders(topgrp)
        shader, sg = CNG.createRGBlight()
        CNG.assignShader(topgrp, shader, sg)
    elif name == "FOGlight":
        delAllShaders(topgrp)
        shader, sg = CNG.createFOGlight()
        CNG.assignShader(topgrp, shader, sg)
    else :
        pass
    
    try:
        layer = pm.nodetypes.RenderLayer.findLayerByName(name)
    except:
        layer = pm.createRenderLayer(name = name, e=1)
    try:
        defaultLayer = pm.nodetypes.RenderLayer.defaultRenderLayer()
        defaultLayer.renderable.set(0)
    except:
        pass
    layer.setCurrent()
    layer.addMembers(getallTops())
    saveFile(name)
    
    
def importLight(path = "Z:/Proj/SENBA/Senba_link/Render/chr_light/chr_light.mb"):
    #chr_color导入默认灯光
    #参数path是要导入的文件的路径
    #返回值是导入的对象列表
    importNode = pm.importFile(path, returnNewNodes = 1)
    return importNode

def getallTops():
    return pm.ls(assemblies = 1)

def getallGeos():
    pm.waitCursor(state=1)
    geos = [i for i in pm.ls(type = "mesh") + pm.ls(type = "nurbsSurface") if not i.isIntermediateObject()]
    pm.waitCursor(state=0)
    return geos
  
def delAllShaders(geos):
    try:
        defaultShader = pm.PyNode("lambert1")
        defaultSG = pm.PyNode("initialShadingGroup")
    except:
        defaultShader, defaultSG = pm.createSurfaceShader('lambert', name = 'lambert1')
    pm.waitCursor(state=1)
    pm.sets(defaultSG, forceElement = geos)
    pm.mel.MLdeleteUnused()
    pm.waitCursor(state=0)

def setObjAttr(obj, attr, value):
    try:
        obj.attr(attr).set(value)
    except:
        print "cannot set {0}.{1} value".format(obj, attr)
    return True
    