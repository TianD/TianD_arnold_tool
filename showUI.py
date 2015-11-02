#coding:utf-8
'''
Created on 2015年10月27日 下午3:43:00

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
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
        self.idp_a_btn.clicked.connect(partial(self.createShaderCmd, 'A'))
        self.idp_maeet_btn.clicked.connect(partial(self.createShaderCmd, 'Maeet'))
        
        self.shadow_btn.clicked.connect(partial(self.createLayerCmd, 'shadow'))
                
        self.rgblight_btn.clicked.connect(partial(self.createLayerCmd, 'RGBlight'))
        
        self.foglight_btn.clicked.connect(partial(self.createLayerCmd, 'FOGlight'))
        
        self.aiOpaque_check.stateChanged.connect(partial(self.setAttr, 'aiOpaque'))
        self.castsShadows_check.stateChanged.connect(partial(self.setAttr, 'castsShadows'))
        self.primaryVisibility_check.stateChanged.connect(partial(self.setAttr, 'primaryVisibility'))
        
        self.initArnold()
        
    def initArnold(self):
        self.arnold = ast.ArnoldSetting()
        self.arnold.setRender()
        self.arnold.setRenderCommon()
    
    def setRenderCmd(self):
        self.arnold.setRenderCommon()
    
    def setProjCmd(self):
        pm.mel.eval('source "lightRendering.mel"')
        pm.mel.projectSet()
        
    def replaceCmd(self):
        ReplaceReference.startReplaceL2H()
        
    def importCmd(self):
        ReplaceReference.importRef()
        
    def createLayerCmd(self, name):
        CRL.createRenderLayer(name)
        self.arnold.setRenderLayer(name)
        
    def setAttr(self, attr, value):
        if value == 2:
            value = 1
        else :
            value = 0
        allgeos = CRL.getallGeos()
        for geo in allgeos:
            CRL.setObjAttr(geo, attr, value)
            
    def createShaderCmd(self, name):
        geos = pm.ls(sl=1)
        shader, sg = CNG.createIDPNode(name)
        CNG.assignShader(geos, shader, sg)

    
if __name__ == '__main__':
    a = ArnoldTool()
    a.show()