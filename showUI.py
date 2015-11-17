#coding:utf-8
'''
Created on 2015年10月27日 下午3:43:00

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: the UI of arnold tool
'''
# import sys
# uiPath = 'E:/Scripts/Eclipse/TianD_arnold_tool'
# uiPath in sys.path or sys.path.append(uiPath)
import os

from functools import partial

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import pymel.core as pm

import uiTool

import aov_tool as at
import arnold_setting as ast
import CreateNodeGroup as CNG
import CreateRenderLayers as CRL

#导入GDC网渲模块
import idmt.maya.musterCheckIn.MusterCheckIn as mck

import ReplaceReference

reload(at)
reload(ast)
reload(CNG)
reload(CRL)
reload(ReplaceReference)

uiPath = os.environ['XBMLANGPATH'].split(";")[1] + "/TianD_KX_TOOL/arnold_tool"

form_class, base_class = uic.loadUiType('%s/arnold_layer_tool.ui' %uiPath)
class ArnoldTool(form_class, base_class):
    
    def __init__(self, parent = uiTool.getMayaWindow()):
                
        super(ArnoldTool, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.project_btn.clicked.connect(self.setProjCmd)
        
        self.setRender_btn.clicked.connect(self.setRenderCmd)
        
        self.replace_btn.clicked.connect(self.replaceCmd)
        
        self.import_btn.clicked.connect(self.importCmd)
        
        self.chr_color_btn.clicked.connect(partial(self.createLayerCmd, 'chr_color'))
        
        self.bg_color_btn.clicked.connect(partial(self.createLayerCmd, 'bg_color'))
        
        self.chr_idp1_btn.clicked.connect(partial(self.createLayerCmd, 'chr_idp1'))
        self.chr_idp2_btn.clicked.connect(partial(self.createLayerCmd, 'chr_idp2'))
        self.chr_idp3_btn.clicked.connect(partial(self.createLayerCmd, 'chr_idp3'))
        
        self.bg_idp1_btn.clicked.connect(partial(self.createLayerCmd, 'bg_idp1'))
        self.bg_idp2_btn.clicked.connect(partial(self.createLayerCmd, 'bg_idp2'))
        self.bg_idp3_btn.clicked.connect(partial(self.createLayerCmd, 'bg_idp3'))
        
        self.idp_r_btn.clicked.connect(partial(self.createShaderCmd, 'R'))
        self.idp_g_btn.clicked.connect(partial(self.createShaderCmd, 'G'))
        self.idp_b_btn.clicked.connect(partial(self.createShaderCmd, 'B'))
        
        self.idp_y_btn.clicked.connect(partial(self.createShaderCmd, 'Y'))
        self.idp_p_btn.clicked.connect(partial(self.createShaderCmd, 'P'))
        self.idp_c_btn.clicked.connect(partial(self.createShaderCmd, 'C'))
        
        self.idp_a_btn.clicked.connect(partial(self.createShaderCmd, 'A'))
        self.idp_maeet_btn.clicked.connect(partial(self.createShaderCmd, 'Maeet'))
        
        self.shadow_btn.clicked.connect(partial(self.createLayerCmd, 'shadow'))
                
        self.rgblight_btn.clicked.connect(partial(self.createLayerCmd, 'RGBlight'))
        
        self.foglight_btn.clicked.connect(partial(self.createLayerCmd, 'FOGlight'))
        
        self.aiOpaque_btn.clicked.connect(partial(self.setAttr, 'aiOpaque'))
        self.castsShadows_btn.clicked.connect(partial(self.setAttr, 'castsShadows'))
        self.primaryVisibility_btn.clicked.connect(partial(self.setAttr, 'primaryVisibility'))
        
        self.netRender_btn.clicked.connect(self.netRenderCmd)
        
        self.deadline_btn.clicked.connect(self.deadlineCmd)
        
        self.initArnold()
        
    def initArnold(self):
        #初始化渲染器
        self.arnold = ast.ArnoldSetting()
        self.setRenderCmd()
    
    def setRenderCmd(self):
        #设置渲染器按钮命令
        self.arnold.setRender()
        self.arnold.setRenderCommon()
    
    def setProjCmd(self):
        #创建工程目录按钮命令
        pm.mel.eval('source "lightRendering.mel"')
        pm.mel.projectSet()
        
    def replaceCmd(self):
        #替换参考按钮命令
        ReplaceReference.startReplaceL2H()
        
    def importCmd(self):
        #导入参考按钮命令
        ReplaceReference.importRef()
        
    def createLayerCmd(self, name):
        #创建渲染层按钮命令
        if name == 'chr_idp1':
            idp_dic = CNG.makeidp1Dic()
        elif name == 'chr_idp2':
            idp_dic = CNG.makeidp2Dic()
        elif name == 'chr_idp3' or name == 'bg_idp3':
            idp_dic = CNG.makeidp3Dic()
        else :
            idp_dic = {}
        CRL.createRenderLayer(name)
        self.arnold.setRenderLayer(name)
        if idp_dic:
            for key, value in idp_dic.items():
                if value:
                    self.createShaderCmd(key, value)

        
    def setAttr(self, attr):
        #修改模型属性按钮命令
        sel = pm.ls(sl=1)
        for i in sel:
            geos = i.getChildren(ad=1, type = "mesh")
            for geo in geos:
                value = CRL.getObjAttr(geo, attr)
                if value :
                    CRL.setObjAttr(geo, attr, 0)
                else :
                    CRL.setObjAttr(geo, attr, 1)
            
    def createShaderCmd(self, name, objs = None):
        #创建IDP材质球按钮命令 
        print name
        if objs : 
            geos = objs
        else :
            geos = pm.ls(sl=1)
        shader, sg = CNG.createIDPNode(name)
        CNG.assignShader(geos, shader, sg)

    def netRenderCmd(self):
        #提交网渲按钮命令
        mck.main()
        
    def deadlineCmd(self):
        #提交deadline按钮命令
        pass

    
if __name__ == '__main__':
    a = ArnoldTool()
    a.show()