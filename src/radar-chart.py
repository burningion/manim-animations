from manim import *

class RadarChart(Scene):
    def __init__(
        self,
        data=None,
        scale=1.0,
        axis_color=BLACK,
        polygon_color=BLUE,
        polygon_opacity=0.3,
        circle_color=GREY_B,
        label_size=12,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.data = data or {
            '<b>Attention</b>': 0.8,
            '<b>Pace</b>': 0.7,
            '<b>Interactivity</b>': 0.9,
            '<b>Rewards</b>': 0.6,
            '<b>Social Value</b>': 0.75,
            '<b>Stickiness</b>': 0.85
        }
        self.scale = scale
        self.axis_color = axis_color
        self.polygon_color = polygon_color
        self.polygon_opacity = polygon_opacity
        self.circle_color = circle_color
        self.label_size = label_size
        
    def construct(self):
        self.camera.background_color = WHITE
        
        # Define the number of variables
        n_vars = len(self.data)
        
        # Calculate angles for each axis
        angles = [i * (2*PI/n_vars) for i in range(n_vars)]
        
        # Create the axes
        axes = VGroup()
        labels = VGroup()
        for i, (label, angle) in enumerate(zip(self.data.keys(), angles)):
            # Create axis line with scale
            axis = Line(
                ORIGIN, 
                3 * self.scale * UP, 
                color=self.axis_color
            ).rotate(angle, about_point=ORIGIN)
            axes.add(axis)
            
            # Create label
            text = MarkupText(
                label, 
                color=self.axis_color, 
                font_size=self.label_size,
                font="Helvetica"
            )
            # Position label at end of axis with small offset
            text.next_to(
                axis.get_end(), 
                direction=axis.get_unit_vector(), 
                buff=0.2
            )
            labels.add(text)
        
        # Create circles for reference
        circles = VGroup()
        for i in range(1, 5):
            circle = Circle(radius=i*0.75*self.scale)
            circle.set_stroke(self.circle_color, opacity=1)
            circles.add(circle)
        
        # Create data points and filled shape
        points = []
        for value, angle in zip(self.data.values(), angles):
            point = 3 * self.scale * value * np.array([
                np.sin(angle), 
                np.cos(angle), 
                0
            ])
            points.append(point)
        
        # Create the filled polygon
        polygon = Polygon(
            *points,
            color=self.polygon_color,
            fill_opacity=self.polygon_opacity
        )
        
        # Create dots at data points
        dots = VGroup(*[Dot(point) for point in points])
        
        # Store the final mobjects for reference
        self.final_mobjects = VGroup(
            axes, circles, labels, polygon, dots
        )
        
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

class MultipleRadarCharts(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Define different datasets
        datasets = [
            {
                '<b>Attention</b>': 0.8,
                '<b>Pace</b>': 0.9,
                '<b>Interactivity</b>': 0.9,
                '<b>Rewards</b>': 0.5,
                '<b>Social\nValue</b>': 0.7,
                '<b>Randomness</b>': 0.9
            },
            {
                '<b>Attention</b>': 0.9,
                '<b>Pace</b>': 0.1,
                '<b>Interactivity</b>': 0.2,
                '<b>Rewards</b>': 0.9,
                '<b>Social\nValue</b>': 0.4,
                '<b>Randomness</b>': 0.3
            },
            {
                '<b>Attention</b>': 0.95,
                '<b>Pace</b>': 0.9,
                '<b>Interactivity</b>': 0.9,
                '<b>Rewards</b>': 0.6,
                '<b>Social\nValue</b>': 0.8,
                '<b>Randomness</b>': 0.4
            }
        ]
        
        # Create three radar charts with different colors and positions
        configurations = [
            {
                'data': datasets[0],
                'scale': 0.4,
                'polygon_color': BLUE,
                'position': LEFT * 4.8 + [0, -.5, 0]
            },
            {
                'data': datasets[1],
                'scale': 0.4,
                'polygon_color': GREEN,
                'position': ORIGIN + [0, -.5, 0]
            },
            {
                'data': datasets[2],
                'scale': 0.4,
                'polygon_color': RED,
                'position': RIGHT * 4.8 + [0, -.5, 0]
            }
        ]
        chart_names = ["Social Media", "Book", "Video Game"]
        
        # Create and position each chart
        for config in configurations:
            # Create the radar chart
            radar = RadarChart(
                data=config['data'],
                scale=config['scale'],
                polygon_color=config['polygon_color']
            )
            radar.construct()
            
            # Move the chart to its position
            radar.final_mobjects.shift(config['position'])
            
            # Add title
            title = MarkupText(
                chart_names[configurations.index(config)],
                color=BLACK,
                font_size=36,
            ).next_to(radar.final_mobjects, UP)
            
            # Add everything to the scene
            self.play(
                Create(radar.final_mobjects),
                Write(title),
                run_time=2
            )
        
        self.wait(10)

# To render:
# manim -pql scene_file.py MultipleRadarCharts