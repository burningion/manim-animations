from manim import *
import numpy as np

class FlexibleGraphAnimation(Scene):
    def __init__(self, x_values=None, y_values=None, x_label="X-Axis", y_label="Y-Axis", title="Graph"):
        super().__init__()
        # Default values if none provided
        self.x_values = x_values if x_values is not None else list(range(6))
        self.y_values = y_values if y_values is not None else [1, 4, 2, 8, 5, 7]
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        
        # Validate input
        if len(self.x_values) != len(self.y_values):
            raise ValueError("X and Y value lists must be the same length")
    
    def create_axes(self):
        # Calculate appropriate ranges for axes
        x_min, x_max = min(self.x_values), max(self.x_values)
        y_min, y_max = min(self.y_values), max(self.y_values)
        
        # Add padding to ranges
        x_padding = 0
        y_padding = 0
        
        # Create axes with dynamic ranges
        return Axes(
            x_range=[x_min - x_padding, x_max + x_padding, (x_max - x_min) / 10],
            y_range=[y_min - y_padding, y_max + y_padding, (y_max - y_min) / 10],
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "tick_size": 0.1,
                "color": self.black,
                "decimal_number_config": {
                    "color": self.black
                }
            },
            x_axis_config={"numbers_to_include": np.arange(int(x_min), int(x_max) + 1)},
            y_axis_config={"numbers_to_include": np.arange(int(y_min), int(y_max) + 1)},
            x_length=10,
            y_length=6
        )
    
    def create_labels(self, axes):
        # Create axis labels
        x_label = Text(self.x_label, font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text(self.y_label, font_size=24).next_to(axes.y_axis, LEFT)
        
        # Create title
        title = Text(self.title, font_size=36).to_edge(UP)
        
        return x_label, y_label, title
    
    def create_data_points(self, axes):
        # Convert data points to coordinates
        points = [axes.coords_to_point(x, y) for x, y in zip(self.x_values, self.y_values)]
        
        # Create the graph line
        graph = VMobject()
        graph.set_points_smoothly([*points])
        graph.set_color("#87c2a5"   )
        
        # Create dots for each point
        dots = VGroup(*[Dot(point, color="#525893") for point in points])
        
        # Create labels for data points
        value_labels = VGroup(*[
            Text(f"({x}, {y})", font_size=16, color=self.black).next_to(dot, UP)
            for x, y, dot in zip(self.x_values, self.y_values, dots)
        ])
        
        return graph, dots, value_labels
    
    def construct(self):
        # Create the elements
        self.camera.frame_height = 10
        self.camera.frame_width = 16
        self.camera.background_color = "#ece6e2"
        self.black = "#343434"
        Text.set_default(font="Helvetica", color=self.black)
        axes = self.create_axes()
        x_label, y_label, title = self.create_labels(axes)
        graph, dots, value_labels = self.create_data_points(axes)
        
        # Initial animations
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Graph creation animation
        self.play(Create(graph), run_time=2)
        
        # Animate dots appearing
        self.play(Create(dots))
        
        # Animate value labels
        self.play(Write(value_labels))
        
        # Sequential point highlighting
        for dot, label in zip(dots, value_labels):
            self.play(
                dot.animate.scale(1.5).set_color("#e07a5f"),
                label.animate.scale(1.2),
                rate_func=there_and_back,
                run_time=0.5
            )
        
        # Final pause
        self.wait(2)

# Example usage:
if __name__ == "__main__":
    # Sample data
    x_data = [1, 2, 3, 4, 5, 6]
    y_data = [3, 7, 2, 9, 4, 6]
    
    # Configure scene settings
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_height = 10
    config.frame_width = 16
    
    # Create and render the scene with custom data and labels
    scene = FlexibleGraphAnimation(
        x_values=x_data,
        y_values=y_data,
        x_label="Time (seconds)",
        y_label="Temperature (°C)",
        title="Temperature Over Time"
    )
    scene.render()