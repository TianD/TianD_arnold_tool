#coding:utf-8
'''
Created on 2015年10月21日 上午10:15:31

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:  使用mtoa.aovs 创建AOV
'''
import mtoa.aovs as aovs
import CreateNodeGroup as CNG
reload(CNG)

#定义每个AOV层的data类型
DEFAULT_AOV_DATA_TYPES = {'AO': 'rgba', 'NOM': 'rgba', 'Fre': 'rgba', 'Zdp': 'rgba', 'sss': 'rgb', 'Z': 'float'}

def createAOV(name):
    aovInterface = aovs.AOVInterface()
    
    #创建AOV
    if DEFAULT_AOV_DATA_TYPES.has_key(name):
        aovName = name
        aovType = DEFAULT_AOV_DATA_TYPES[name]
        aov = aovInterface.addAOV(aovName, aovType)        
    else :
        aovName = name
        aov = aovInterface.addAOV(aovName)
    #
    
    #创建AOV材质球
    if aovName == 'AO':
        CNG.createAO(aov.node.defaultValue)
    elif aovName == 'NOM':
        CNG.createNOM(aov.node.defaultValue)
    elif aovName == 'Fre':
        CNG.createFresnel(aov.node.defaultValue)
    elif aovName == 'Zdp':
        CNG.createZ(aov.node.defaultValue)
    elif aovName == 'COCC':
        CNG.createCOCC(aov.node.defaultValue)
    else :
        pass
        
    return aov

def delAOV():
    #删除所有的AOV
    try:
        aovInterface = aovs.AOVInterface()
        result = aovInterface.getAOVs()
        aovInterface.removeAOVs(result)
    except:
        return False
    return True
    