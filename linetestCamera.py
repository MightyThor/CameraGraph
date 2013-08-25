import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ReferenceListProperty, \
NumericProperty, ListProperty
from kivy.properties import ObjectProperty, ListProperty
#from kivy.vector import Vector
#from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.button import Button

import math

Builder.load_string('''
#:kivy 1.7.0

<GraphView>:
    newdot: graphdot
    size: root.size
    canvas:
        PushMatrix
        Translate:
            xy: self.pos
        Color:
            rgba: 2, 0, .5, 1
        Line:
            points: self.points
            width: 2
        PopMatrix
    GraphDot:
        pos: root.center
        id: graphdot


<GraphView_2>:
    newdot2: graphdot2
    canvas:
        PushMatrix
        Translate:
            xy: self.pos
        Color:
            rgba: 1, 1, .5, 1
        Line:
            points: self.points
            width: 2
        PopMatrix
    GraphDot_2:
        id: graphdot2


<GraphDot>:
    size: 20,20
    pos: root.pos
    canvas:
        Color:
            rgba: 2, 0, .5, 1
        Ellipse:
            size: self.size
            pos: self.center

<GraphDot_2>:
    size: 20, 20
    canvas:
        Color:
            rgba: 1, 1, .5, 1
        Ellipse:
            size: self.size
            pos: self.center
''')


#TODO: The graphing dot for the first graphview isn't translating properly
class GraphDot(Widget):
    pass

class GraphDot_2(Widget):
    pass

class GraphView(Widget):
    newdot = ObjectProperty()
    points = ListProperty([])

    old_position = [0, 0]
    counter = 0.0

    def update(self, dt):
        self.counter += 0.2
        new_point = [
            self.counter * 5.,
            50. * math.sin(self.counter) + self.height / 2.
            ]
        self.add_point(new_point)

    def add_point(self, new_position):
        self.newdot.center_y = new_position[1]
        self.newdot.center_x = new_position[0]

        self.old_position = new_position[:]

#        print new_position

        self.points.extend(self.old_position + new_position)
        if new_position[0] > self.width:
            self.counter = 0.0
            self.old_position = [0, 0]
            #Once the canvas is cleared the line doesn't come back
            #TODO: need to be able to redraw the line?
            self.canvas.clear()

class GraphView_2(Widget):
    newdot2 = ObjectProperty()
    points = ListProperty([])

    old_position = [0, 0]
    counter = 0.0

    def update(self, dt):
        self.counter += 0.2
        new_point = [
            self.counter * 5.,
            50. * math.sin(self.counter) + self.height / 2.
            ]
        self.add_point(new_point)

    def add_point(self, new_position):
        self.newdot2.center_y = new_position[1]
        self.newdot2.center_x = new_position[0]

        self.old_position = new_position[:]

#        print new_position

        self.points.extend(self.old_position + new_position)
        if new_position[0] > self.width:
            self.counter = 0.0
            self.old_position = [0, 0]
            #self.canvas.clear()


class CameraView(Camera):

    pass

class BlankView(Widget):
    pass


class SimpleGraphApp(App):
    starting_point = [0, 0]

    def build(self):
        root = FloatLayout()
        layer = GridLayout(rows = 2)

        cameraview = CameraView(resolution = (640, 480), play = True)

        graphview = GraphView()
        #graphview2 = GraphView_2()
        blankview = BlankView()

        layer.add_widget(graphview)
        layer.add_widget(blankview)
        #layer.add_widget(graphview2)

        Clock.schedule_interval(graphview.update, 1/5)
        #Clock.schedule_interval(graphview2.update, 1/5)

        root.add_widget(cameraview)
        root.add_widget(layer)

        return root

if __name__ == '__main__':
    SimpleGraphApp().run()
