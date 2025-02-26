import random

import objc
from PyObjCTools import AppHelper
from Foundation import NSObject
from AppKit import NSApplication, NSWindow, NSButton, NSView, NSColor
from SceneKit import *


class GameScene(NSObject):
    def init(self):
        self = objc.super(objc.lookUpClass('GameScene'), self).init()
        if self is None:
            return None

        CGimg = globals()['NSImage'].alloc().initWithContentsOfFile_('galactika.jpeg')

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            (globals()['CGRect'](100, 100), globals()['CGRect'](800, 600)),
            15,
            globals()['NSBackingStoreRetained'],
            True)
        self.window.setTitle_('3D Mini Game')
        menu = globals()['NSMenu'].alloc().initWithTitle_('Quit')
        self.window.setMenu_(menu)

        self.scene_view = globals()['SCNView'].alloc().initWithFrame_(((0, 0), (800, 600)))
        self.scene = globals()['SCNScene'].scene()

        self.scene.background().setContents_(CGimg)
        self.setup_camera()
        self.setup_light()
        self.scene_view.setScene_(self.scene)
        self.scene_view.setBackgroundColor_(globals['NSColor'].whiteColor())

        self.window.contentView().addSubview_(self.scene_view)
        self.window.makeKeyAndOrderFront_(None)

        self.character = globals()['SCNNode'].node()
        self.character.setGeometry_(globals()['SCNSphere'].sphereWithRadius_(1.5))
        self.character.geometry().firstMaterial().diffuse().setContents_(NSColor.redColor())
        self.character.setPosition_((0.5, 0.5, 0))
        self.scene.rootNode().addChildNode_(self.character)

        self.create_objects()

        white = NSColor.whiteColor()
        button_up = NSButton.alloc().initWithFrame_(((10, 520), (80, 30)))
        button_up.setTitle_('Up')
        button_up.setBezelColor_(white)
        button_up.setTarget_(self)
        button_up.setAction_('moveUp:')

        button_down = NSButton.alloc().initWithFrame_(((10, 480), (80, 30)))
        button_down.setTitle_('Down')
        button_down.setBezelColor_(white)
        button_down.setTarget_(self)
        button_down.setAction_('moveDown:')

        button_left = NSButton.alloc().initWithFrame_(((10, 440), (80, 30)))
        button_left.setTitle_('Left')
        button_left.setBezelColor_(white)
        button_left.setTarget_(self)
        button_left.setAction_('moveLeft:')

        button_right = NSButton.alloc().initWithFrame_(((10, 400), (80, 30)))
        button_right.setTitle_('Right')
        button_right.setBezelColor_(white)
        button_right.setTarget_(self)
        button_right.setAction_('moveRight:')

        for btns in [button_up, button_down, button_left, button_right]:
            self.window.contentView().addSubview_(btns)

        return self

    def setup_camera(self):
        self.camera_node = globals()['SCNNode'].node()
        self.camera_node.setCamera_(globals()['SCNCamera'].camera())
        self.camera_node.setPosition_((0, 5, 10))
        self.camera_node.lookAt_(globals()['SCNVector3'](0, 0, 1))
        self.scene.rootNode().addChildNode_(self.camera_node)

    @objc.IBAction
    def moveUp_(self, sender):
        self.camera_node.setPosition_(
            globals()['SCNVector3'](self.camera_node.position().x,
                                    self.camera_node.position().y,
                                    self.camera_node.position().z - 1))
        sender.setBackgroundColor_(NSColor.blackColor())

    @objc.IBAction
    def moveDown_(self, sender):
        self.camera_node.setPosition_(
            globals()['SCNVector3'](self.camera_node.position().x,
                                    self.camera_node.position().y,
                                    self.camera_node.position().z + 1))
        sender.setBackgroundColor_(NSColor.blackColor())

    @objc.IBAction
    def moveLeft_(self, sender):
        self.camera_node.setPosition_(
            globals()['SCNVector3'](self.camera_node.position().x + 1,
                                    self.camera_node.position().y,
                                    self.camera_node.position().z))
        sender.setBackgroundColor_(NSColor.blackColor())

    @objc.IBAction
    def moveRight_(self, sender):
        self.camera_node.setPosition_(
            globals()['SCNVector3'](self.camera_node.position().x - 1,
                                    self.camera_node.position().y,
                                    self.camera_node.position().z))
        sender.setBackgroundColor_(NSColor.blackColor())

    def setup_light(self):
        light_node = globals()['SCNNode'].node()
        light = globals()['SCNLight'].light()
        light.setType_(globals()['SCNLightTypeOmni'])
        light_node.setOpacity_(0)
        light.setColor_(NSColor.whiteColor())
        light_node.setLight_(light)
        light_node.setPosition_((0, 10, 10))
        light_node.setCastsShadow_(globals()['SCNShadowModeForward'])

        self.scene.rootNode().addChildNode_(light_node)

    def create_objects(self):
        for i in range(-5, 7, 2):
            for j in range(-5, 6, 2):
                if (i + j) % 4 == 0:
                    square = globals()['SCNNode'].node()
                    square.setGeometry_(globals()['SCNBox'].boxWithWidth_height_length_chamferRadius_(1, 0.1, 1, 0))
                    square.geometry().firstMaterial().diffuse().setContents_(NSColor.blueColor())
                    square.setPosition_((i, 0.5, j))
                else:
                    sphere = globals()['SCNNode'].node()
                    sphere.setGeometry_(globals()['SCNSphere'].sphereWithRadius_(0.5))
                    sphere.geometry().firstMaterial().diffuse().setContents_(NSColor.yellowColor())
                    sphere.setPosition_((i, 0.5, j))

                    self.scene.rootNode().addChildNode_(square if (i + j) % 4 == 0 else sphere)

    def move_character(self, dx, dz):
        new_x = max(min(self.character.position().x + dx, 5), -5)
        new_z = max(min(self.character.position().z + dz, 5), -5)
        self.character.setPosition_((new_x, self.character.position().y, new_z))


if __name__ == '__main__':
    app = NSApplication.sharedApplication()
    delegate = GameScene.alloc().init()
    app.run()
    AppHelper.runEventLoop()

