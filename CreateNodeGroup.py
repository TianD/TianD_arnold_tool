#coding:utf-8
'''
Created on 2015年10月21日 下午2:27:40

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: create node group or shader
'''
import pymel.core as pm

ARNOLD_IDP_TYPE = {'R':[(1,0,0),0,(1,0,0)], 
                   'G':[(0,1,0),0,(0,1,0)], 
                   'B':[(0,0,1),0,(0,0,1)],
                   'Y':[(1,1,0),0,(1,1,0)],
                   'C':[(0,1,1),0,(0,1,1)],
                   'P':[(1,0,1),0,(1,0,1)], 
                   'A':[(0,0,0),1,(1,1,1)], 
                   'Maeet':[(0,0,0),0,(0.2,0.2,0.2)],
                   }

IDP1_TYPE_DIC = {
                'R': ['_body_','_head_',],
                'B': ['eye'],
                'G': ['hair','eyebrow'],
                'Y': ['outfit'],
                'P': ['tooth'],
                'A': ['mouth'],
                }

IDP2_TYPE_LIST = ['R', 'G', 'B', 'C', 'Y', 'P', 'A']

def createZ(out = None):
    #创建Z通道节点组合
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    samplerInfo = pm.createNode('samplerInfo', name = 'z_samplerInfo_arnold')
    multiplyDivide = pm.createNode('multiplyDivide', name = 'z_multiplyDivide_arnold')
    setRange = pm.createNode('setRange', name = 'z_setRange_arnold')
    aiUtility, SG = pm.createSurfaceShader('aiUtility', name = 'zdp_arnold')
    
    #修改属性
    multiplyDivide.input2X.set(-1)
    
    setRange.minX.set(1)
    setRange.oldMinX.set(0.1)
    setRange.oldMaxX.set(500)
    
    aiUtility.shadeMode.set(2)
    
    #属性链接
    samplerInfo.pointCameraZ >> multiplyDivide.input1X
    multiplyDivide.outputX >> setRange.valueX
    setRange.message >> aiUtility.colorR
    setRange.message >> aiUtility.colorG
    setRange.message >> aiUtility.colorB
    
    if out :
        aiUtility.outColor >> out
    else :
        pass
    
    return aiUtility, SG
    
def createFresnel(out = None):
    #创建菲涅尔节点组合
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    samplerInfo = pm.createNode('samplerInfo', name = 'Fre_samplerInfo_arnold')
    ramp = pm.createNode('ramp', name = 'Fre_ramp_arnold')
    aiUtility, SG = pm.createSurfaceShader('aiUtility', name = 'Fresnel_arnold')
    
    #修改属性
    ramp.interpolation.set("Exponential Down")
    ramp.colorEntryList[2].remove(b=1)
    ramp.colorEntryList[1].position.set(1)
    ramp.colorEntryList[0].color.set(1,1,1)
    ramp.colorEntryList[1].color.set(0,0,0)
    
    aiUtility.shadeMode.set(2)
    
    #链接属性
    samplerInfo.facingRatio >> ramp.uvCoord.uCoord
    samplerInfo.facingRatio >> ramp.uvCoord.vCoord
    
    ramp.outColor >> aiUtility.color

    if out :
        aiUtility.outColor >> out
    else :
        pass
    
    return aiUtility, SG

def createAO(out = None):
    #创建AO材质球
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    aiAO, SG = pm.createSurfaceShader('aiAmbientOcclusion', name = 'ao_arnold')
    
    #修改属性
    aiAO.samples.set(5)
    
    if out :
        aiAO.outColor >> out
    else :
        pass
    
    return aiAO, SG

def createNOM(out = None):
    #创建NOM材质球
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    aiUtility, SG = pm.createSurfaceShader('aiUtility', name = 'nom_arnold')
    
    #修改属性
    aiUtility.shadeMode.set(2)
    aiUtility.colorMode.set(3)
    
    if out:
        aiUtility.outColor >> out
    else :
        pass
    
    return aiUtility, SG

def createIDPNode(key, out = None):
    #创建IDP材质组合
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    if ARNOLD_IDP_TYPE.has_key(key):
        try:
            idp_shader = pm.PyNode(key)
            SG = pm.PyNode('{0}SG'.format(key))
        except:
            idp_shader, SG = pm.createSurfaceShader('aiStandard', name = key)
            idp_shader.aiEnableMatte.set(1)
            aiMatteColor = ARNOLD_IDP_TYPE[key][0]
            aiMatteColorA = ARNOLD_IDP_TYPE[key][1]
            diffColor = ARNOLD_IDP_TYPE[key][2]
            idp_shader.aiMatteColor.set(aiMatteColor)
            idp_shader.aiMatteColorA.set(aiMatteColorA)
            idp_shader.color.set(diffColor)
    else :
        return False
    
    if out:
        idp_shader.outColor >> out
    else :
        pass
    
    return idp_shader, SG
    
def createCOCC(out = None):
    #创建AO材质球
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    aiAO, SG = pm.createSurfaceShader('aiAmbientOcclusion', name = 'cocc_arnold')
    
    #修改属性
    aiAO.samples.set(5)
    
    if out :
        aiAO.outColor >> out
    else :
        pass
    
    return aiAO, SG    
    
def createFOGlight(out = None):
    #创建FOGlight材质组合
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    FOGlight_arnold, SG = pm.createSurfaceShader("aiStandard", name = "FOGlight_arnold")
    FOGlight_arnold.aiEnableMatte.set(1)
    FOGlight_arnold.color.set(0,0,0)
    
    if out :
        FOGlight_arnold.outColor >> out
    else :
        pass
    
    return FOGlight_arnold, SG
    
def createRGBlight(out = None):
    #创建RGBlight材质组合
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    RGBlight_shader, SG = pm.createSurfaceShader("aiUtility", name = "RGBlight_arnold")
    RGBlight_shader.shadeMode.set(1)
    
    if out :
        RGBlight_shader.outColor >> out
    else :
        pass
    
    return RGBlight_shader, SG

def createShadow(out = None):
    #创建shadow材质组合
    #
    #参数out: 属性输出给哪个节点, 连接属性
    #
    #创建节点
    shadow_shader, SG = pm.createSurfaceShader("aiShadowCatcher", name = "shadow_arnold")
    shadow_shader.shadowColor.set(1,1,1)
    shadow_shader.hardwareColor.set(0,1,0)
    
    if out :
        shadow_shader.outColor >> out
    else :
        pass
    
    return shadow_shader, SG

def assignShader(obj, shader, sg):
    #给物体赋予材质球
    #
    #参数obj: 模型对象 
    #
    #参数shader: 材质球对象
    #
    #参数sg: shadingEngine对象
    #
    #创建节点
    pm.waitCursor(state=1)
    pm.sets(sg, forceElement = obj)
    pm.waitCursor(state=0)
    return shader

    
def makeidp1Dic():
    idp_dic = dict()
    
    geos = [i.getParent() for i in pm.ls(type = "mesh") if not i.isIntermediate() and (i.isVisible() == 1) and 'charRigGrp' in i.fullPath() and not 'norender' in i.fullPath()]
    
    had = []
    for geo in geos:
        for key, value in IDP1_TYPE_DIC.items():
            for v in value:
                if v in geo.fullPath():
                    idp_dic.setdefault(key, list()).append(geo.name())
                    had.append(geo)
                    break
                    
             
    no = list(set(geos) - set(had))         
    idp_dic.setdefault('C',no)
    
    return idp_dic    

def makeidp2Dic():
    idp_dic = dict()
    geos = [i for i in pm.ls(assemblies = 1) if 'charRigGrp' in i.name()]
    
    if len(geos) > 7:
        geos = geos[:7]
    for i in range(len(geos)):
        idp_dic.setdefault(IDP2_TYPE_LIST[i], geos[i])
        
    return idp_dic

if __name__ == "__main__":
    #createFresnel()
    createZ()

