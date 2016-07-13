#coding:utf-8
'''
Created on 2015年11月13日 下午3:55:54

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: ass function
'''

# import arnold module
from arnold import ai_nodes, ai_render, ai_plugins, ai_msg, ai_dotass, ai_node_entry, ai_params, ai_universe

# make funciton dic used for different types of parameters call differnet method
PARAMETER_FUNCTION_DIC = {
                          "BYTE": [ai_nodes.AiNodeSetByte, ai_nodes.AiNodeGetByte],
                          "INT": [ai_nodes.AiNodeSetInt, ai_nodes.AiNodeGetInt],
                          "UINT": [ai_nodes.AiNodeSetUInt, ai_nodes.AiNodeGetUInt],
                          "BOOL": [ai_nodes.AiNodeSetBool, ai_nodes.AiNodeGetBool],
                          "FLOAT": [ai_nodes.AiNodeSetFlt, ai_nodes.AiNodeGetFlt],
                          "RGB": [ai_nodes.AiNodeSetRGB, ai_nodes.AiNodeGetRGB],
                          "RGBA": [ai_nodes.AiNodeSetRGBA, ai_nodes.AiNodeGetRGBA],
                          "VEC": [ai_nodes.AiNodeSetVec, ai_nodes.AiNodeGetVec],
                          "POINT": [ai_nodes.AiNodeSetPnt, ai_nodes.AiNodeGetPnt],
                          "POINT2": [ai_nodes.AiNodeSetPnt2, ai_nodes.AiNodeGetPnt2],
                          "STRING": [ai_nodes.AiNodeSetStr, ai_nodes.AiNodeGetStr],
                          "PTR": [ai_nodes.AiNodeSetPtr, ai_nodes.AiNodeGetPtr],
                          "ARRAY": [ai_nodes.AiNodeSetArray, ai_nodes.AiNodeGetArray],
                          "pMTX": [ai_nodes.AiNodeSetMatrix, ai_nodes.AiNodeGetMatrix],
                          "ENUM": [ai_nodes.AiNodeSetStr, ai_nodes.AiNodeGetStr],
                          }

def loadASS(ass_file, AiPluginsPath = 'C:/solidangle/mtoadeploy/2014/shaders'):
    '''
    Load ass file
    '''
    
    ai_render.AiBegin()
    
    ai_plugins.AiLoadPlugins(AiPluginsPath)
    
    ai_msg.AiMsgSetConsoleFlags(ai_msg.AI_LOG_ALL)
    
    ai_dotass.AiASSLoad(ass_file, ai_node_entry.AI_NODE_ALL)
    
def saveASS(ass_file):
    '''
    Save ass file
    '''

    ai_dotass.AiASSWrite(ass_file, ai_node_entry.AI_NODE_ALL, False)
    
    ai_render.AiEnd()

def endWithoutSave():
    '''
    End without save
    '''
    ai_render.AiEnd()

def getASSParamType(node, parameter):
    '''
    Get the type of node parameter
    '''

    nentry = ai_nodes.AiNodeGetNodeEntry(node)
    
    count = ai_node_entry.AiNodeEntryGetNumParams(nentry)
    for i in range(count):

        pentry = ai_node_entry.AiNodeEntryGetParameter(nentry, i)

        pname = ai_params.AiParamGetName(pentry)

        if parameter == pname:

            ptypeIndex = ai_params.AiParamGetType(pentry)

            ptype = ai_params.AiParamGetTypeName(ptypeIndex)
            return ptype
    
def getASSParameter(node, parameter):
    '''
    Get the value of node parameter
    '''
    ptype = getASSParamType(node, parameter)
    
    link = ai_nodes.AiNodeGetLink(node, parameter)
    
    if link:
        value = link
    else :
        if PARAMETER_FUNCTION_DIC.has_key(ptype):
            value = PARAMETER_FUNCTION_DIC[ptype][1](node, parameter)
    return value
    
def setASSParameter(node, parameter, value):
    '''
    Set the value of node parameter
    '''
    ptype = getASSParamType(node, parameter)
    if PARAMETER_FUNCTION_DIC.has_key(ptype):
        try:
            value = PARAMETER_FUNCTION_DIC[ptype][0](node, parameter, value)
        except:
            raise ValueError, 'Set value failure'
    else :
        print "no set"
    
def listASSNodes(nodeType = None, nameFilter = None, mask = ai_node_entry.AI_NODE_SHADER):
    '''
    List nodes in file
    '''
    # param     nodeType:     [string] 节点类型
    # param     nameFilter:   [list] 指定节点名称, 如果是None, 就是指定类型的所有节点; 如果是列表, 就匹配列表中的节点名称
    # param     mask:         [global variable] ai_node_entry内定义的节点类型的种类, 包括:
    #            AI_NODE_UNDEFINED =  0x0000  ## Undefined type
    #            AI_NODE_OPTIONS =    0x0001  ## Options node (following the "singleton" pattern, there is only one options node)
    #            AI_NODE_CAMERA =     0x0002  ## Camera nodes (\c persp_camera, \c fisheye_camera, etc)
    #            AI_NODE_LIGHT =      0x0004  ## Light source nodes (\c spot_light, etc)
    #            AI_NODE_SHAPE =      0x0008  ## Geometry nodes (\c sphere, \c polymesh, etc)
    #            AI_NODE_SHADER =     0x0010  ## Shader nodes (\c lambert, \c shadingEngine, \c texture etc)
    #            AI_NODE_OVERRIDE =   0x0020  ## EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes
    #            AI_NODE_DRIVER =     0x0040  ## Output driver nodes (\c driver_tiff, etc)
    #            AI_NODE_FILTER =     0x0080  ## Pixel sample filter nodes (\c box_filter, etc
    #            AI_NODE_ALL =        0xFFFF  ## Bitmask including all node types, used by AiASSWrite()
    
    nodeLst = []
        
    iter = ai_universe.AiUniverseGetNodeIterator(mask)
    while not ai_universe.AiNodeIteratorFinished(iter):
        node = ai_universe.AiNodeIteratorGetNext(iter)
                        
        if ai_nodes.AiNodeIs( node, nodeType ):
            if nameFilter:
                name = node.AiNodeGetName( node )
                if name in nameFilter:
                    nodeLst.append(node)
                else :
                    continue
            else :
                nodeLst.append(node)
                
    ai_universe.AiNodeIteratorDestroy(iter)
    
    return nodeLst

if __name__ == '__main__':
    
    ass_file = "E:\\maya\\guanmu.ass"
    loadASS(ass_file)
    for n in listASSNodes("MayaFile"):
        filename = getASSParameter(n, "filename")
        print filename
    saveASS(ass_file)
    #endWithoutSave()