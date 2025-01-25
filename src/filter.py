from manim import *
import numpy as np
import random
import os

asset_folder = "../video_assets" # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"

class FilterAnimation(ZoomedScene): # Changed from Scene to ZoomedScene
    CONFIG = { # Added CONFIG for ZoomedScene
        "zoom_factor": 0.3,
        "zoomed_display_height": 2, # Adjusted height and width
        "zoomed_display_width": 7,
        "image_frame_stroke_width": 3, # Reduced stroke width
        "zoomed_camera_config": {
            "default_frame_stroke_width": 1, # Reduced stroke width in zoomed camera
        },
    }
    def construct(self):
        # Set the background color
        self.camera.background_color = WHITE
        rect_color = ManimColor((241, 172, 75))
        input_svg = SVGMobject(f"{asset_folder}/perceptionw1.svg").scale(1).stretch(factor=-1, dim=0)
        input_svg.move_to([0, 0, 0])
        rect = RoundedRectangle(height=5, width=3.5, corner_radius=0.2, color=rect_color, fill_opacity=1)
        rect.move_to([0, -.2, 0])
        thinking_text = MarkupText("Sensory input\nat 1Gbit / second", font="Helvetica", color=BLACK, font_size=28).next_to(input_svg, DOWN, buff=0.5)

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
        conscious_thought_rate_text = Tex(r"Conscious thought\\at 10 bits / second", tex_template=TexFontTemplates.helvetica_fourier_it,
                           tex_environment="flushleft",
                           font_size=6,
                           color=BLACK)
        conscious_thought_rate_text.move_to([.23,.27,0]).set_z_index(4) # Position below rect

        # Add everything to scene
        self.add(background_group)
        self.add(rect, thinking_text, input_svg, conscious_thought_rate_text)

        # Background Animations (particles and interference)
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
                rate_func=rate_functions.there_and_back # Changed rate_func for particles
            )
            particle_anims.append(anim)

        interference_anims = []
        for circle in interference_circles:
            anim = GrowFromCenter(
                circle,
                run_time=random.uniform(1, 2),
                rate_func=rate_functions.there_and_back # Changed rate_func for interference
            )
            interference_anims.append(anim)

        self.play(
            *particle_anims,
            *interference_anims,
            rate_func=lambda t: t,
            run_time=4 # Adjust run_time as needed for background animation
        )

        # --- Zoom and Conscious Thought Animation ---

        zoom_duration = 3  # Duration of zoom and conscious thought animation
        zoom_factor = 10 # Adjust zoom factor as needed

        # Create dots for conscious thought
        conscious_dots = VGroup()
        num_dots = int(10 * zoom_duration) # 10 bits per second for zoom duration

        rect_zoomed = rect.copy() # Create a copy for zoomed size, not strictly needed but good practice
        rect_zoomed_center = rect.get_center()

        for _ in range(num_dots):
            dot = Dot(radius=.01, color=BLUE_D) # Smaller dots for zoomed view
            dot.move_to([-.2,.3,0]) # Start at center
            conscious_dots.add(dot)

        #conscious_dots.set_opacity(0) # Initially invisible

        # Text for conscious thought rate
        
        frame = self.zoomed_camera.frame
        frame.move_to([-.2,.3,0])
        frame.scale(zoom_factor)

        self.play(
            self.camera.frame.animate.move_to([-.2,.26,0]).scale(0.1),
            #FadeIn(conscious_thought_rate_text),
            run_time=2
        )

        dot_animations = []
        for _ in range(10):
            dot = Dot(radius=.01, color=BLUE_D)
            anim = Succession(
                Create(dot.move_to([-.2, .28, 0])),
                Transform(dot, dot.copy().move_to([-.3, .28, 0])), 
                FadeOut(dot, shift=DOWN)
            )
            dot_animations.append(anim)

        self.play(
            #FadeIn(conscious_thought_rate_text),
            AnimationGroup(*dot_animations, lag_ratio=0.1, run_time=3)
        )

        self.play(
            self.camera.frame.animate.move_to([0,0,0]).scale(10),  # scale(10) because 1/0.1 = 10
            run_time=2
        )
