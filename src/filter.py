from manim import *
import numpy as np
import random
import os

asset_folder = "../video_assets" # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"

class FilterAnimation(Scene):
    def construct(self):
        # Set the background color
        self.camera.background_color = WHITE
        rect_color = ManimColor((241, 172, 75))
        input = SVGMobject(f"{asset_folder}/perceptionw1.svg").scale(1).stretch(factor=-1, dim=0)
        input.move_to([0, 0, 0])
        rect = RoundedRectangle(height=5, width=3.5, corner_radius=0.2, color=rect_color, fill_opacity=1)
        rect.move_to([0, -.2, 0])
        thinking = MarkupText("Sensory input\nat 1Gbit / second", font="Helvetica", color=BLACK, font_size=28).next_to(input, DOWN, buff=0.5)
        
        background_group = VGroup()
        background_group.set_z_index(-1)  # Set behind everything else
        
        # Create flowing particles
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
                    0
                ])
            )
            particles.add(particle)
        
        # Add particles to background
        background_group.add(particles)

        # Create wave paths
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
        
        # Add waves to background
        background_group.add(waves)

        # Create interference patterns
        interference_circles = VGroup()
        for radius in np.linspace(0, 3, 5):
            circle = Circle(
                radius=radius,
                stroke_color=BLUE_A,
                stroke_opacity=0.2
            )
            interference_circles.add(circle)
        
        # Add interference circles to background
        background_group.add(interference_circles)

        # Add everything to scene
        self.add(background_group)

        # Example foreground elements (commented out - replace with your actual elements)
        self.add(rect, thinking, input)
        # rounded_rect = RoundedRectangle(height=2, width=4, corner_radius=0.5)
        # rounded_rect.set_z_index(1)  # Set in front
        # text = Text("Your text here").set_z_index(1)
        # self.add(rounded_rect, text)

        # Animations

        # Particle animations
        particle_anims = []
        for particle in particles:
            target = particle.copy()
            target.move_to(
                np.array([
                    random.uniform(-7, 7),
                    random.uniform(-4, 4),
                    0
                ])
            )
            anim = Transform(
                particle,
                target,
                run_time=random.uniform(1, 3),
                rate_func=rate_functions.linear
            )
            particle_anims.append(anim)

        # Interference pattern animations
        interference_anims = []
        for circle in interference_circles:
            anim = GrowFromCenter(
                circle,
                run_time=random.uniform(1, 2)
            )
            interference_anims.append(anim)

        # Play all animations together
        self.play(
            *particle_anims,
            *interference_anims,
            rate_func=lambda t: t
        )

