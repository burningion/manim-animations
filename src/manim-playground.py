from manim import *
from manim.opengl import *

class PlaygroundModel(Scene):
    def construct(self):
        circle = Circle()
         
        circle.set_color_by_gradient([PINK, BLUE]).set_fill(opacity=.9) 
        circle1 = Circle(fill_color=RED, fill_opacity=0.5)
        circle2 = Circle()
        circle2.set_color_by_gradient([BLUE, PINK]).set_fill(opacity=.9)
        circle2.shift(RIGHT * 8)
        cirlce3 = Circle(fill_color=ORANGE, fill_opacity=0.5)
        cirlce3.shift(LEFT * 8)
        self.play(GrowFromCenter(circle),
                  GrowFromCenter(circle1))
        self.play(Transform(circle, circle2),
                  Transform(circle1, cirlce3))
