#coding:utf-8
'''
Created on 2015年10月22日 上午11:20:33

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:  set arnold render common setting

'''
import pymel.core as pm

from kxTool import KXTool

pm.mel.eval('source "lightRendering.mel"')

class ArnoldSetting(object):
    
    def __init__(self):
        
        self.defaultRG = None
        self.options = None 
        self.driverNode = None
        self.filterNode = None
        self.resolution = None

    def setRender(self):
        #切换渲染器为arnold
        try:
            pm.loadPlugin("mtoa")
            pm.pluginInfo("mtoa", e=1, a=1)
        except:
            print "mtoa has been loaded!!!"
            
#         try:
#             if pm.pluginInfo("Mayatomr.mll", q=1, loaded=1):
#                 pm.unloadPlugin("Mayatomr", f=1)
#         except:
#             print "mentalRay is unloaded failure!!!"
            
            
        self.defaultRG = pm.PyNode("defaultRenderGlobals")
        self.defaultRG.currentRenderer.set("arnold")
        
        #获取以下默认节点, 没有找到就新建
        try:
            self.options = pm.PyNode('defaultArnoldRenderOptions')
        except :
            self.options = pm.createNode('aiOptions', name='defaultArnoldRenderOptions', skipSelect=True, shared=True)
        
        try:
            self.filterNode = pm.PyNode('defaultArnoldFilter')
        except:
            self.filterNode = pm.createNode('aiAOVFilter', name='defaultArnoldFilter', skipSelect=True, shared=True)
        
        try:
            self.driverNode = pm.PyNode('defaultArnoldDriver')
        except:
            self.driverNode = pm.createNode('aiAOVDriver', name='defaultArnoldDriver', skipSelect=True, shared=True)
            
        try:
            self.resolution = pm.PyNode('defaultResolution')
        except :
            self.resolution = pm.createNode('resolution', name = 'defaultResolution', skipSelect=True, shared=True)
        
        return True
        

    def setRenderCommon(self, w=1920, h=1080, dar = 1.778, MS = False):
        #
        #    render：    [defaultRenderGlobalsNode, defaultArnoldRenderOptionsNode, defaultArnoldDriverNode, defaultArnoldFilter]
        #      
        if not MS:
            kx = KXTool()
            kx.getSceneName()
            kx.analyzeSceneName()
            if kx.resolutionDic.has_key(kx.projectName):
                w = kx.resolutionDic[kx.projectName][0]
                h = kx.resolutionDic[kx.projectName][1]
                dar = kx.resolutionDic[kx.projectName][2]
            #设置渲染时间
            pm.mel.eval('setRenderRange;')
            #设置渲染相机
            if kx.projectName == 'ROCK':
                projCam = pm.ls("cam_{sq}_{se}_{sc}".format(sq = kx.episodeNumber, se = kx.sessionNumber, sc = kx.sceneNumber))
                projCam_baked = pm.ls("cam_{sq}_{se}_{sc}_baked".format(sq = kx.episodeNumber, se = kx.sessionNumber, sc = kx.sceneNumber))
                if projCam and not projCam_baked:
                    raise NameError, "no right baked camera"
                try:
                    camL = [cam for cam in projCam_baked[0].getChildren() if 'stereoCameraLeft' in cam.name()][0].getShape()
                except:
                    raise NameError, "no project camera"
                camL.renderable.set(1)
                for cam in pm.ls(type = "camera"):
                    if cam != camL:
                        cam.renderable.set(0)
                
        else :
            #设置渲染时间
            pm.mel.eval('setRenderRange;')

        
        #设置图片文件前缀名: <Camera>/<RenderLayer>/<Scene>
        imageFilePrefix = '<Camera>/<RenderLayer>/<Scene>'
        if self.defaultRG:
            self.defaultRG.imageFilePrefix.set(imageFilePrefix)
        
            #设置Frame/Animation ext属性: name.#.ext
            #根据 mel 命令 setMayaSoftwareFrameExt得来.
            #
            self.defaultRG.animation.set(1)
            self.defaultRG.putFrameBeforeExt.set(1)
            self.defaultRG.periodInExt.set(1)
            if self.defaultRG.outFormatControl.get() == 1:
                self.defaultRG.outFormatControl.set(0)
        
        if self.driverNode:
            #设置图片格式: 'exr'
            self.driverNode.aiTranslator.set('exr')
            #设置压缩格式: 'zip'
            self.driverNode.exrCompression.set(3)
            #勾选Half Precision
            self.driverNode.halfPrecision.set(1)
            #不勾Preserve Layer Name  
            self.driverNode.preserveLayerName.set(0)   
            #不勾Tiled
            self.driverNode.tiled.set(0)
            #勾选Autocrop
            #self.driverNode.autocrop.set(1)
            #不勾Append
            self.driverNode.append.set(0)
            
            #勾选Merge AOVs, 合并AOV里面所有通道
            self.driverNode.mergeAOVs.set(1)
            
        if self.resolution:
            #设置分辨率
            #pixel_aspect_ratio = (height / width) * device_aspect_ratio
            self.resolution.width.set(w)
            self.resolution.height.set(h)
            self.resolution.deviceAspectRatio.set(dar)
            
        if self.options:
            self.options.lock_sampling_noise.set(1)
            
        return True
            
     
    def setRenderLayer(self, name):
        #根据不同的渲染层设置不同的渲染器属性
        #
        #参数name: 提供渲染层的名称
        #
        if not self.options:
            return False
        else :
            pass
        
        self.driverNode.aiTranslator.set('exr')
        
        if name == 'bg_color':
            self.options.AASamples.set(4)
            self.options.GIDiffuseSamples.set(0)
            self.options.GIGlossySamples.set(0)
            self.options.GIRefractionSamples.set(0)
            self.options.sssBssrdfSamples.set(0)
            self.options.volumeIndirectSamples.set(2)
            
            self.options.lock_sampling_noise.set(1)
            
        elif name == 'chr_color':
            self.options.AASamples.set(4)
            self.options.GIDiffuseSamples.set(2)
            self.options.GIGlossySamples.set(2)
            self.options.GIRefractionSamples.set(2)
            self.options.sssBssrdfSamples.set(2)
            self.options.volumeIndirectSamples.set(2)
            
            self.options.sssUseAutobump.set(0)
            self.options.GITotalDepth.set(5)
            self.options.GIDiffuseDepth.set(1)
            self.options.GIGlossyDepth.set(1)
            self.options.GIReflectionDepth.set(2)
            self.options.GIRefractionDepth.set(2)
            self.options.GIVolumeDepth.set(0)
            self.options.autoTransparencyDepth.set(10)
            self.options.autoTransparencyThreshold.set(0.99)
            
            # add at 2016/04/19
            # add motion blur
            self.options.motion_blur_enable.set(1)
            self.options.range_type.set(0)
            self.options.ignoreMotionBlur.set(1)
            
        # add at 2015/12/30
        elif name == 'night_chr_color':
            self.options.AASamples.set(4)
            self.options.GIDiffuseSamples.set(0)
            self.options.GIGlossySamples.set(1)
            self.options.GIRefractionSamples.set(0)
            self.options.sssBssrdfSamples.set(0)
            self.options.volumeIndirectSamples.set(2)

            self.options.sssUseAutobump.set(0)
            self.options.GITotalDepth.set(6)
            self.options.GIDiffuseDepth.set(1)
            self.options.GIGlossyDepth.set(1)
            self.options.GIReflectionDepth.set(2)
            self.options.GIRefractionDepth.set(2)
            self.options.GIVolumeDepth.set(0)
            self.options.autoTransparencyDepth.set(10)
            self.options.autoTransparencyThreshold.set(0.99)
        # 
            
        elif name in ["chr_idp1", "chr_idp2", "chr_idp3", "bg_idp1", "bg_idp2", "bg_idp3", "shadow", "RGBlight", "FOGlight"]:
            self.options.AASamples.set(3)
            self.options.GIDiffuseSamples.set(0)
            self.options.GIGlossySamples.set(0)
            self.options.GIRefractionSamples.set(0)
            self.options.sssBssrdfSamples.set(0)
            self.options.volumeIndirectSamples.set(2)
            
            self.options.GITotalDepth.set(10)
            self.options.GIDiffuseDepth.set(1)
            self.options.GIGlossyDepth.set(1)
            self.options.GIReflectionDepth.set(2)
            self.options.GIRefractionDepth.set(2)
            self.options.GIVolumeDepth.set(0)
            self.options.autoTransparencyDepth.set(10)
            self.options.autoTransparencyThreshold.set(0.99)
        else :
            pass 
        return True