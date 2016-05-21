#coding:utf-8
'''
Created on 2015年10月26日 下午3:32:42

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: create render layer

'''

import pymel.core as pm

from lightRenderData import ProjNameMatch

import aov_tool as at
import CreateNodeGroup as CNG


#创建显示层
#包括: chr_color, bg_color, IDP, shadow, RGBlight, FOGlight

LAYER_FILENAME = {'chr_color':'CHRcolor',
                  'night_chr_color':'CHRcolor',
                  'bg_color':'BGcolor',
                  'chr_idp1':'CHRidp1',
                  'chr_idp2':'CHRidp2',
                  'chr_idp3':'CHRidp3',
                  'bg_idp1':'BGidp1',
                  'bg_idp2':'BGidp2',
                  'bg_idp3':'BGidp3',
                  'shadow':'shadow',
                  'RGBlight':'RGBlight',
                  'FOGlight':'FOGlight'}

def saveFile(describe):
    #按照描述保存文件
    #
    #参数describe: 需要输入描述字符串, 如: 'CHRcolor'等, 保存文件时加入到文件名中.
    #
    pnm = ProjNameMatch()
    fileName = pm.Env().sceneName().namebase
    dir = pnm.setFileName(fileName)
    dir = pm.Path(pnm.getProjDirectorys()[-1]+pnm.getProjDirectorys()[0]+'/scenes')
    project_name = pnm.getResults('project_name')
    episode_number = pnm.getResults('episode_number')
    session_number = pnm.getResults('session_number')
    scene_number = pnm.getResults('scene_number')
    scene_describe = LAYER_FILENAME[describe]
    process_name = 'lr'
    version_number = 'c001'
    newFileName = '_'.join([project_name, episode_number, session_number, scene_number, scene_describe, process_name, version_number])
    filePrefix = '_'.join([project_name, episode_number, session_number, scene_number, scene_describe, process_name])
    versions = []
    for f in dir.files():
        subpnm = ProjNameMatch()
        if filePrefix in f.name:
            subpnm.setFileName(f.name)
            versions.append(subpnm.getResults('version_number'))
    if versions:
        versions.sort()
        version_number = 'c'+ str(int(versions[-1][1:])+1).zfill(3)
    newFileName = '_'.join([project_name, episode_number, session_number, scene_number, scene_describe, process_name, version_number])
    try:
        pm.saveAs("{0}/{1}.mb".format(dir, newFileName))
        return newFileName
    except:
        raise "save this file failure!!!"
    
def createRenderLayer(name):
    #创建渲染层
    #
    #参数name: 需要输入渲染层的名字
    #
    #获取所有的模型对象
    allgeos = getallGeos()
    topgrp = list(set([i.getParent(-1) for i in allgeos]))
    
    members = getallTops()
    #切换渲染器
    try:
        defaultLayer = pm.nodetypes.RenderLayer.defaultRenderLayer()
        defaultLayer.setCurrent()
    except:
        pass
    
    #删除所有的AOV
    at.delAOV()
    
    #删除所有的渲染层
    renderLayers = pm.ls(type = 'renderLayer')
    for rl in renderLayers:
        if 'defaultRenderLayer' not in rl.name():
            pm.delete(rl)
        
    #创建渲染层
    if name == "bg_color":
        for key in ['AO', 'NOM', 'Fre', 'Z']:
            at.createAOV(key)
        members = getsetTops() + getlightTops()
    elif name == "chr_color":
        for key in ['AO', 'NOM', 'Fre', 'sss']:
            at.createAOV(key)
        im = importLight()
        members = getchrandpropTops() + im
    elif name == "night_chr_color":
        for key in ['AO', 'NOM', 'Fre', 'sss']:
            at.createAOV(key)
        im = importLight()
        members = getchrandpropTops() + im
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
    
    if name == 'night_chr_color':
        layerName = 'chr_color'
    else :
        layerName = name
    try:
        layer = pm.nodetypes.RenderLayer.findLayerByName(layerName)
    except:
        layer = pm.createRenderLayer(name = layerName, e=1)
    try:
        defaultLayer = pm.nodetypes.RenderLayer.defaultRenderLayer()
        defaultLayer.renderable.set(0)
    except:
        pass
    layer.setCurrent()
    if members:
        layer.addMembers(members)
    try:
        saveFile(name)
    except:
        pass
    
    
def importLight(path = "Z:/Proj/SENBA/Senba_link/Render/chr_light/chr_light.mb"):
    #chr_color层需要导入默认灯光
    #
    #参数path: 要导入的文件的路径
    #
    #返回值是导入的对象列表
    importNode = pm.importFile(path, returnNewNodes = 1)
    return importNode

def getallTops():
    return pm.ls(assemblies = 1)

def getchrandpropTops():
    #获取角色道具组
    return [i for i in pm.ls(assemblies = 1) if 'charRigGrp' in i.name() or 'CharRigGrp' in i.name() or 'PropRigGrp' in i.name()]

def getsetTops():
    #获取场景组
    return pm.ls(regex = '*:*SetRigGrp')

def getlightTops():
    #获取灯光组
    return list(set([l.getParent(-1) for l in pm.ls(lights = 1)]))

def getallGeos():
    #获取模型对象
    geos = [i for i in pm.ls(type = "mesh") + pm.ls(type = "nurbsSurface") if not i.isIntermediateObject()]
    return geos
  
def delAllShaders(geos):
    #删除所有材质球
    #
    #参数geos: 模型对象
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
    #设置对象属性
    #
    #参数obj: 模型对象
    #
    #参数attr: 属性名
    #
    #参数value: 属性值
    try:
        obj.attr(attr).set(value)
    except:
        print "cannot set {0}.{1} value".format(obj, attr)
    return True
    
def getObjAttr(obj, attr):
    #获取对象属性
    #
    #参数obj: 模型对象
    #
    #参数attr: 属性名
    #
    return obj.attr(attr).get()