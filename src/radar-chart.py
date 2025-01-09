from manim import *
import numpy as np

class RadarChart(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Define the number of variables and the data
        n_vars = 6
        data = {
            '<b>Attention</b>': 0.8,    # Scale from 0-1
            '<b>Pace</b>': 0.7,
            '<b>Interactivity</b>': 0.9,
            '<b>Rewards</b>': 0.6,
            '<b>Social Value</b>': 0.75,
            '<b>Stickiness</b>': 0.85
        }
        
        # Calculate angles for each axis
        angles = [i * (2*PI/n_vars) for i in range(n_vars)]
        
        # Create the axes
        axes = VGroup()
        labels = VGroup()
        for i, (label, angle) in enumerate(zip(data.keys(), angles)):
            # Create axis line
            axis = Line(ORIGIN, 3 * UP, color=BLACK).rotate(angle, about_point=ORIGIN)
            axes.add(axis)
            
            # Create label
            text = MarkupText(label, color=BLACK, font_size=24, font="Helvetica")
            # Position label at end of axis with small offset
            text.next_to(axis.get_end(), direction=axis.get_unit_vector(), buff=0.2)
            labels.add(text)
        
        # Create circles for reference
        circles = VGroup()
        for i in range(1, 5):
            circle = Circle(radius=i*0.75)
            circle.set_stroke(GREY_A, opacity=1)
            circles.add(circle)
        
        # Create data points and filled shape
        points = []
        for value, angle in zip(data.values(), angles):
            point = 3 * value * np.array([np.sin(angle), np.cos(angle), 0])
            points.append(point)
        
        # Create the filled polygon
        polygon = Polygon(*points, color=BLUE, fill_opacity=0.3)
        
        # Create dots at data points
        dots = VGroup(*[Dot(point) for point in points])
        
        # Animate everything
        self.play(
            Create(axes),
            Create(circles),
            Write(labels),
            run_time=2
        )
        self.play(
            Create(polygon),
            Create(dots),
            run_time=2
        )
        self.wait(2)