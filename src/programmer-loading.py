from manim import *
import numpy as np
import random
import os

asset_folder = "../video_assets"  # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"


class IdeaLoadingAnimation(Scene):
    def construct(self):
        # Set the background color
        self.camera.background_color = WHITE
        rect_color = ManimColor((241, 172, 75))
        input_svg = SVGMobject(f"{asset_folder}/perceptionw1.svg").scale(.75).move_to([0, 0, 0])
        rect = RoundedRectangle(height=5, width=3.5, corner_radius=0.2, color=rect_color, fill_opacity=1)
        rect.move_to([0, -0.2, 0])
        thinking = MarkupText("Programmer\ngathering context\nfor task", font="Helvetica", color=BLACK, font_size=24).next_to(input_svg, DOWN, buff=0.5)
        ready = MarkupText("Ready\nfor work", font="Helvetica", color=BLACK, font_size=24).next_to(input_svg, DOWN, buff=0.5)
        
        background_group = VGroup()
        background_group.set_z_index(-1)  # Set behind everything else

        # Create flowing particles (reusing from example, can be simplified if needed)
        particles = VGroup()
        for i in range(30):
            particle = Dot(
                radius=0.05,
                color=BLUE_D,
                fill_opacity=random.uniform(0.4, 0.8)
            )
            particle.move_to(
                np.array([
                    random.uniform(-7, 7),
                    random.uniform(-4, 4),
                    0,  # Explicit z=0 for particles
                ])
            )
            particles.add(particle)
        background_group.add(particles)

        waves = VGroup()
        for i in range(5):
            wave = FunctionGraph(
                lambda x: 0.5 * np.sin(x + i),
                x_range=[-7, 7],
                color=BLUE,
                stroke_opacity=0.3
            )
            wave.shift(UP * (i - 2))
            waves.add(wave)

        background_group.add(waves)

        interference_circles = VGroup()
        for radius in np.linspace(0, 3, 5):
            circle = Circle(radius=radius, stroke_color=BLUE_A, stroke_opacity=0.2)
            interference_circles.add(circle)

        background_group.add(interference_circles)

        self.add(background_group)
        self.add(rect, thinking, input_svg)

        # Placeholders for Ideas
        placeholder_x = 4  # X position for placeholders on the right
        placeholder_y_start = 2  # Starting Y position for the top placeholder
        placeholder_spacing = 2  # Vertical spacing between placeholders
        placeholder_width = 3
        placeholder_height = 1.5
        placeholder_radius = 0.2

        idea_placeholders = VGroup()
        idea_texts = VGroup()
        idea_rects = VGroup()

        idea_names = ["Problem\nDomain", "Existing\nCode", "Consequnces\nof Change"]  # Example idea names
        idea_bit_sizes = [200, 120, 340]  # Information density in bits

        for i in range(3):
            placeholder_rect = RoundedRectangle(
                height=placeholder_height, width=placeholder_width, corner_radius=placeholder_radius, color=BLUE_E, fill_opacity=0.8
            )
            placeholder_rect.move_to([placeholder_x, placeholder_y_start - i * placeholder_spacing, 0])
            idea_rects.add(placeholder_rect)

            idea_text = MarkupText(idea_names[i], font="Helvetica", color=WHITE, font_size=24)
            idea_text.move_to(placeholder_rect.get_center())
            idea_texts.add(idea_text)

            placeholder_group = VGroup(placeholder_rect, idea_text)
            idea_placeholders.add(placeholder_group)

        self.play(*[Create(placeholder) for placeholder in idea_placeholders], run_time=1)
        self.wait(0.5)

        # Idea Loading Animation
        loading_rate = 100  # bits per second
        idea_copies = []
        loading_bars = []  # To hold loading bars for each idea

        for i in range(3):
            idea_copy_rect = idea_rects[i].copy()
            idea_copy_text = idea_texts[i].copy()
            idea_copy_group = VGroup(idea_copy_rect, idea_copy_text)
            idea_copies.append(idea_copy_group)
            self.add(idea_copy_group)  # Add copies to the scene

            # Create loading bar
            loading_bar = Rectangle(
                width=placeholder_width * 0.8, height=0.2, color=GREEN, fill_opacity=0.8
            )
            loading_bar.move_to(idea_copy_rect.get_bottom() + DOWN * 0.3)
            loading_bars.append(loading_bar)
            self.add(loading_bar)

        self.play(
            *[
                (
                    idea_copies[i].animate.move_to(input_svg.get_critical_point(LEFT) + np.array([0.5, 0, 0])).scale(0.5),
                    idea_copies[i].animate.set_opacity(0.8),
                )
                for i in range(3)
            ],
            particles.animate.shift(LEFT * 0.5),  # Simplified particle shift animation
            run_time=2,
            rate_func=rate_functions.smooth,
        )
        
        self.wait(0.2)

        # Animate loading bars and fade out
        for i in range(3):
            load_duration = idea_bit_sizes[i] / loading_rate
            target_position = input_svg.get_center()  # Move towards the center of the SVG
            
            self.play(
                 loading_bars[i].animate.stretch_to_fit_width(
                    width=0,
                    about_edge=LEFT
                ).move_to(target_position), # Move towards the center of the input_svg,
                 run_time = load_duration,
                rate_func=rate_functions.linear
            )
            
            self.play(FadeOut(idea_copies[i]), run_time=0.2)
            self.remove(loading_bars[i])
        self.play(
            input_svg.animate.stretch(factor=-1, dim=0),
            Flash(input_svg.get_center(), color=BLUE_E, flash_radius=1.2, line_width=6, num_lines=24, line_stroke_width=8),
            FadeOut(thinking),
            run_time=1
        )

        self.play(
            FadeIn(ready),
            run_time=1
        )
        # Final wait
        self.wait(2)