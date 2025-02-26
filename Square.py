
from SceneKit import *
from Foundation import NSObject


class Square(NSObject):
    def initWithPosition_(self, position):

        self.geometry = globals()['SCNBox'].boxWithWidth_height_length_chamferRadius_(1, 1, 1, 0)
        material = globals()['SCNMaterial'].material()
        material.setContents_(globals()['NSColor'].redColor())
        self.geometry.setMaterials_([material])

        self.node = globals()['SCNNode'].node()
        self.node.setGeometry_(self.geometry)

        self.node.setPosition_(position)

        return self

    def interact(self):
        # Example interaction: Change color on interaction
        current_color = self.geometry.materials()[0].diffuse.contents()
        new_color = globals()['NSColor'].blueColor() if current_color == globals()['NSColor'].redColor() \
            else globals()['NSColor'].redColor()
        self.geometry.materials()[0].setDiffuseContents_(new_color)

    def start_game_loop(self):
        def check_interactions():
            squares = [child for child in self.scene.rootNode().childNodes() if isinstance(child, globals()['SCNNode'])]
            for i in range(len(squares)):
                for j in range(i + 1, len(squares)):
                    square_a = squares[i]
                    square_b = squares[j]

                    if square_a.position().distance(square_b.position()) < 2:
                        square_a.interact(square_b)

            globals()['NSTimer'].scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                2, self, check_interactions, None, True
            )

