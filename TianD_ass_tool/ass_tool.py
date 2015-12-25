#coding:utf-8
'''
Created on 2015年11月13日 下午3:55:54

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

# 导入模块
from arnold import ai_nodes, ai_render, ai_plugins, ai_msg, ai_dotass, ai_node_entry, ai_params, ai_universe
# ai_nodes module         #    主要是对节点的操作, 包括节点的创建与查询、 节点链接的创建、删除与查询、节点参数的set与get
# ai_render module        #    主要是begin 和 end
# ai_plugins module       #    加载插件
# ai_msg module           #    主要是显示日志等
# ai_dotass module        #    主要是对ass文件的读写
# ai_node_entry module    #    不太理解这个模块, 这里用这个模块查询了节点内包含的属性数量和序号
# ai_params module        #    主要是对节点参数的操作, 包括节点参数的类型和名称的查询等
# ai_universe module      #    主要是生成和销毁迭代器, 包括节点、aov等. 

# 构造字典, 对于不同类型的参数调用不同的方法来set和get值
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

def loadASS(ass_file):
    
    # 开始
    ai_render.AiBegin()
    
    # 必须加载这个路径下的插件arnold api 才能识别maya的插件
    ai_plugins.AiLoadPlugins('C:/solidangle/mtoadeploy/2014/shaders')
    
    #在控制台显示运行日志
    #ai_msg.AiMsgSetConsoleFlags(ai_msg.AI_LOG_ALL)
    
    # 载入ass文件
    ai_dotass.AiASSLoad(ass_file, ai_node_entry.AI_NODE_ALL)
    
def saveASS(ass_file):
    
    # 保存文件
    ai_dotass.AiASSWrite(ass_file, ai_node_entry.AI_NODE_ALL, False)
    
    # 结束
    ai_render.AiEnd()

def endWithoutSave(ass_file):
    # 如果不修改内容, 可以选择不保存直接退出
    # 结束
    ai_render.AiEnd()

def getASSParamType(node, parameter):
    # 获取参数类型
    
    # 获取node entry 
    nentry = ai_nodes.AiNodeGetNodeEntry(node)
    # 获取节点参数个数
    count = ai_node_entry.AiNodeEntryGetNumParams(nentry)
    
    # 循环查找指定参数的类型
    for i in range(count):
        # 获取parameter entry
        pentry = ai_node_entry.AiNodeEntryGetParameter(nentry, i)
        # 获取参数名
        pname = ai_params.AiParamGetName(pentry)

        if parameter == pname:
            # 获取参数类型序号
            ptypeIndex = ai_params.AiParamGetType(pentry)
            # 获取参数类型名称
            ptype = ai_params.AiParamGetTypeName(ptypeIndex)
            return ptype
    
def getASSParameter(node, parameter):
    # 获取节点属性值
    
    ptype = getASSParamType(node, parameter)
    # 获取属性连接节点
    link = ai_nodes.AiNodeGetLink(node, parameter)
    
    if link:
        # 如果存在连接就取到连接的节点
        value = link
    else :
        # 如果没有连接就判断是否在字典中, 如果在字典中就调用取值方法, 否则就返回None
        if PARAMETER_FUNCTION_DIC.has_key(ptype):
            value = PARAMETER_FUNCTION_DIC[ptype][1](node, parameter)
    return value
    
def setASSParameter(node, parameter, value):
    # 设置节点属性值
    
    ptype = getASSParamType(node, parameter)
    # 如果在字典中, 就调用相应的赋值方法
    if PARAMETER_FUNCTION_DIC.has_key(ptype):
        value = PARAMETER_FUNCTION_DIC[ptype][0](node, parameter, value)
    else :
        print "no set"
    
def getASSNode(nodeType = None, nameFilter = None, mask = ai_node_entry.AI_NODE_SHADER):
    # 获取.ass文件中的节点
    #
    # 参数ass_file: [string] ass文件路径
    # 参数nodeType: [string] 节点类型
    # 参数nameFilter: [list] 指定节点名称, 如果是None, 就是指定类型的所有节点; 如果是列表, 就匹配列表中的节点名称
    # 参数mask: [global variable] ai_node_entry内定义的节点类型的种类, 包括:
    #            AI_NODE_UNDEFINED =  0x0000  ## Undefined type
    #            AI_NODE_OPTIONS =    0x0001  ## Options node (following the "singleton" pattern, there is only one options node)
    #            AI_NODE_CAMERA =     0x0002  ## Camera nodes (\c persp_camera, \c fisheye_camera, etc)
    #            AI_NODE_LIGHT =      0x0004  ## Light source nodes (\c spot_light, etc)
    #            AI_NODE_SHAPE =      0x0008  ## Geometry nodes (\c sphere, \c polymesh, etc)
    #            AI_NODE_SHADER =     0x0010  ## Shader nodes (\c lambert, etc)
    #                maya的file节点、shadingEngine节点、shader节点都属于这个范围
    #            AI_NODE_OVERRIDE =   0x0020  ## EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes
    #            AI_NODE_DRIVER =     0x0040  ## Output driver nodes (\c driver_tiff, etc)
    #            AI_NODE_FILTER =     0x0080  ## Pixel sample filter nodes (\c box_filter, etc
    #            AI_NODE_ALL =        0xFFFF  ## Bitmask including all node types, used by AiASSWrite()
    
    # 返回节点列表
    nodeLst = []
        
    # 获取shader类型的节点的迭代器, maya的节点在arnold 中都是shader类型
    iter = ai_universe.AiUniverseGetNodeIterator(mask)
    while not ai_universe.AiNodeIteratorFinished(iter):
        node = ai_universe.AiNodeIteratorGetNext(iter)
               
        # Is the node a MayaFile?
        # 判断节点是否是maya的file节点                
        if ai_nodes.AiNodeIs( node, nodeType ):
            if nameFilter:
                name = node.AiNodeGetName( node )
                if name in nameFilter:
                    nodeLst.append(node)
                else :
                    continue
            else :
                nodeLst.append(node)
                
    # 循环完所有的节点之后, 销毁迭代器
    ai_universe.AiNodeIteratorDestroy(iter)

    return nodeLst

'''   
#### example script
def replaceASSParameter(ass_file, nodeType, parameter, replacefrom, replaceto, nameFilter = None, mask = ai_node_entry.AI_NODE_SHADER):
    # 替换ass文件中的属性值
    #
    # 参数ass_file: [string] ass文件路径
    # 参数nodeType: [string] 节点类型
    # 参数parameter: [string] 参数名
    # 参数replacefrom: [string] 需要被替换的字符
    # 参数replaceto: [string] 替换成什么字符
    # 参数nameFilter: [list] 指定节点名称, 如果是None, 就是指定类型的所有节点; 如果是列表, 就匹配列表中的节点名称
    # 参数mask: [global variable] ai_node_entry内定义的节点类型的种类, 包括:
    #            AI_NODE_UNDEFINED =  0x0000  ## Undefined type
    #            AI_NODE_OPTIONS =    0x0001  ## Options node (following the "singleton" pattern, there is only one options node)
    #            AI_NODE_CAMERA =     0x0002  ## Camera nodes (\c persp_camera, \c fisheye_camera, etc)
    #            AI_NODE_LIGHT =      0x0004  ## Light source nodes (\c spot_light, etc)
    #            AI_NODE_SHAPE =      0x0008  ## Geometry nodes (\c sphere, \c polymesh, etc)
    #            AI_NODE_SHADER =     0x0010  ## Shader nodes (\c lambert, etc)
    #                maya的file节点、shadingEngine节点、shader节点都属于这个范围
    #            AI_NODE_OVERRIDE =   0x0020  ## EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes
    #            AI_NODE_DRIVER =     0x0040  ## Output driver nodes (\c driver_tiff, etc)
    #            AI_NODE_FILTER =     0x0080  ## Pixel sample filter nodes (\c box_filter, etc
    #            AI_NODE_ALL =        0xFFFF  ## Bitmask including all node types, used by AiASSWrite()
    

    # 开始
    ai_render.AiBegin()
    
    # Load the mtoa shaders, which include maya built-in nodes
    # 载入mtoa插件里的材质球, 内中记录了maya的节点
    # 必须加载这个路径下的插件arnold api 才能识别maya的插件
    ai_plugins.AiLoadPlugins('C:/solidangle/mtoadeploy/2014/shaders')
    
    #在控制台显示运行日志
    ai_msg.AiMsgSetConsoleFlags(ai_msg.AI_LOG_ALL)
    
    # 载入ass文件
    ai_dotass.AiASSLoad(ass_file, ai_node_entry.AI_NODE_ALL)
    
    # 获取shader类型的节点的迭代器, maya的节点在arnold 中都是shader类型
    iter = ai_universe.AiUniverseGetNodeIterator(mask)
    while not ai_universe.AiNodeIteratorFinished(iter):
        node = ai_universe.AiNodeIteratorGetNext(iter)
        
        print ai_nodes.AiNodeGetName( node )
        
        # Is the node a MayaFile?
        # 判断节点是否是maya的file节点                
        if ai_nodes.AiNodeIs( node, nodeType ):
            
            if nameFilter:
                
                name = ai_nodes.AiNodeGetStr(node, "name")
                
                if name in nameFilter:
                    pass
                
                else :
                    continue
                        
            # 获取MayaFile节点的filename属性值
            filename = ai_nodes.AiNodeGetStr( node, parameter )
            
            # 替换路径
            newname = filename.replace( replacefrom, replaceto )
            
            # 修改MayaFile节点的filename属性值
            ai_nodes.AiNodeSetStr(node, parameter, newname)

#             # 创建MayaFile节点
#             n = ai_nodes.AiNode("MayaFile");
#             # 设置属性值
#             ai_nodes.AiNodeSetStr(n, "filename", name.replace( 'E:/', 'E:/maya/' ))
    
    # 循环完所有的节点之后, 销毁迭代器
    ai_universe.AiNodeIteratorDestroy(iter)
    
    # 保存文件
    ai_dotass.AiASSWrite(ass_file, AI_NODE_ALL, False)
    
    # 结束
    ai_render.AiEnd()
    
'''    

if __name__ == '__main__':
    
    ass_file = "E:\\maya\\pSphere2.ass"
    loadASS(ass_file)
    for n in getASSNode("MayaChecker"):
        value = getASSParameter(n, "color1")
        #newfilename = filename.replace("E:/", "E:/maya/")
        #setASSParameter(n, "filename", newfilename)
        print value
    saveASS(ass_file)