import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

commandName = 'AnimSmooth_Plugin'
menuName = 'AnimSmooth'

class MyCommandClass( OpenMayaMPx.MPxCommand ):
    
    def __init__(self):
        ''' Constructor. '''
        OpenMayaMPx.MPxCommand.__init__(self)

    def setKey(self, mField, rField, sField, startField, endField, placeSlider, *args):
        objects = cmds.ls(selection=True)
        object = objects[0]
        m = []
        r = []
        s = []
        if mField != 0:
            for i in mField:
                value = cmds.intField(i, q=True, v=True)
                m.append(value)
        if rField != 0:
            for i in rField:
                value = cmds.intField(i, q=True, v=True)
                r.append(value)
        if sField != 0:
            for i in sField:
                value = cmds.intField(i, q=True, v=True)
                s.append(value)
        start = cmds.intField(startField, q=True, v=True)
        end = cmds.intField(endField, q=True, v=True)
        relativeMiddle = cmds.intSlider(placeSlider, q=True, v=True)
        relativeMiddle = relativeMiddle / 100.0
        middle = round((end - start) * relativeMiddle) + start
        if len(m) > 0:
            cmds.setKeyframe(object, at='translateX', v=m[0], t=middle)
            cmds.setKeyframe(object, at='translateY', v=m[1], t=middle)
            cmds.setKeyframe(object, at='translateZ', v=m[2], t=middle)
        if len(r) > 0:
            cmds.setKeyframe(object, at='rotateX', v=r[0], t=middle)
            cmds.setKeyframe(object, at='rotateY', v=r[1], t=middle)
            cmds.setKeyframe(object, at='rotateZ', v=r[2], t=middle)
        if len(s) > 0:
            cmds.setKeyframe(object, at='scaleX', v=s[0], t=middle)
            cmds.setKeyframe(object, at='scaleY', v=s[1], t=middle)
            cmds.setKeyframe(object, at='scaleZ', v=s[2], t=middle)
        
    def createUI(self, pWindowTitle):        #[Start] CreateUI
        
        windowID = 'myPlugin'
        
        if cmds.window(windowID, exists = True):#If window is already open
            cmds.deleteUI('myPlugin')#close window
        
        #[Start] Create New Window    
        myWindow = cmds.window(windowID, title = pWindowTitle, sizeable = True, resizeToFitChildren = True)
        cmds.rowColumnLayout(numberOfColumns = 4, columnWidth = [(1,75), (2,60), (3,60), (4,60)], columnOffset = [(1, 'right', 3)] )#Window Grid layout
        
        #ROW 1
        cmds.text(label = 'Time Range:')
        
        #Input Start/End Keys 
        startTimeField = cmds. intField(value = cmds.playbackOptions( query = True, minTime = True))
        cmds.text(label = 'to')
        endTimeField = cmds. intField(value = cmds.playbackOptions( query = True, maxTime = True))
        
        #ROW 2
        cmds.text(label = 'Middle Key:')
        placeSlider = cmds.intSlider(min=0, max=100, value=50)
        cmds.separator(h = 10, style = 'none')#blank grid separator
        
        #ROW 3
        cmds.separator(h = 10, style = 'none')#blank grid separator
        cmds.separator(h = 10, style = 'none')#blank grid separator
        cmds.separator(h = 10, style = 'none')#blank grid separator
        cmds.separator(h = 10, style = 'none')#blank grid separator
        cmds.separator(h = 10, style = 'none')#blank grid separator
        
        #ROW 4
        #Calculated Key Options
        cmds.text(label = 'Set New Key:')
        cmds.text(label = 'X')
        cmds.text(label = 'Y')
        cmds.text(label = 'Z')
        m = []

        #ROW5
        cmds.text(label = 'Move:')
        m.append( cmds.intField())
        m.append( cmds.intField())
        m.append( cmds.intField())

        r = []
        #ROW6
        cmds.text(label = 'Rotate:')
        r.append( cmds.intField())
        r.append( cmds.intField())
        r.append( cmds.intField())

        s = []
        #ROW7
        cmds.text(label = 'Scale:')
        s.append( cmds.intField(min=1))
        s.append( cmds.intField(min=1))
        s.append( cmds.intField(min=1))
        
        #ROW8
        cmds.text(l="Apply to:")
        cmds.button(l='Translate', c=partial(self.setKey, m, 0, 0, startTimeField, endTimeField, placeSlider))
        cmds.button(l='Rotate', c=partial(self.setKey, 0, r, 0, startTimeField, endTimeField, placeSlider))
        cmds.button(l='Scale', c=partial(self.setKey, 0, 0, s, startTimeField, endTimeField, placeSlider))
        
        #ROW9
        cmds.separator(h = 10, style = 'none')#blank grid separator
        cmds.button(w = 180, label = "All", c=partial(self.setKey, m, r, s, startTimeField, endTimeField, placeSlider))
        cmds.showWindow( myWindow )      #[End] New Window
        
    def doIt(self, args):
        ''' Command execution. '''
        self.createUI('AnimSmooth ~Plugin')    #[End] Create UI


        
def cmdCreator():
    ''' Create an instance of our command. '''
    return OpenMayaMPx.asMPxPtr( MyCommandClass() )


def initializePlugin( mobject ):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    gMainWindow = mel.eval('$tmpVar=$gMainWindow')
    cmds.setParent ( gMainWindow )
    if cmds.menu(menuName, exists=True):
        print("Menu found")
    else:
        cmds.menu( menuName, parent=gMainWindow, label=menuName)
        cmds.menuItem( menuName+"Item1", label=commandName, command="import maya.cmds as mc; mc."+commandName+"()")
    try:
        mplugin.registerCommand( commandName, cmdCreator )
    except:
        print( 'Failed to register command: ' + commandName )

def uninitializePlugin( mobject ):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    cmds.deleteUI(menuName)
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( commandName )
    except:
        print( 'Failed to unregister command: ' + commandName )
