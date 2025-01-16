from manim import *
import numpy as np

import os

asset_folder = "../video_assets" # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"

class ThinkingAnimation(Animation):
    def __init__(
        self,
        position=ORIGIN,  # Added position parameter
        radius=3,
        num_dots=8,
        color=BLACK,
        rate_func=linear,
        run_time=2,
        **kwargs
    ):
        # Create a VGroup to hold all the dots
        self.circle_group = VGroup()
        self.num_dots = num_dots
        self.radius = radius
        
        # Create dots arranged in a circle
        for i in range(num_dots):
            angle = i * TAU / num_dots
            dot = Dot(
                point=radius * RIGHT,
                color=color,
                radius=0.15
            ).rotate(angle, about_point=ORIGIN)
            self.circle_group.add(dot)
        
        # Move the entire group to the specified position
        self.circle_group.move_to(position)
            
        super().__init__(
            self.circle_group,
            rate_func=rate_func,
            run_time=run_time,
            **kwargs
        )

    def interpolate_mobject(self, alpha):
        for i, dot in enumerate(self.circle_group):
            phase = alpha * TAU + (i * TAU / self.num_dots)
            opacity = (np.sin(phase) + 1) / 2
            dot.set_opacity(opacity)

class CurlyBraceTransformation(Scene):
    def construct(self):
        # Set the background color to white
        self.camera.background_color = WHITE
        rect_color = ManimColor((241, 172, 75))
        think_color = ManimColor((255, 182, 55))
        # First set of braces (top)
        think_loop = ThinkingAnimation(
            radius=.4,     # Smaller circle
            num_dots=10,    # More dots
            color=GREY_E,   # colors man
            run_time=2,   # Faster animation
            position=np.array([-5.2,1.8,0])
        )
        second_think_loop = ThinkingAnimation(
            radius=.4,     # Smaller circle
            num_dots=10,    # More dots
            color=GREY_E,   # colors man
            run_time=2,   # Faster animation
            position=np.array([-5.2,1.8,0])
        )
        third_think_loop = ThinkingAnimation(
            radius=.4,     # Smaller circle
            num_dots=10,    # More dots
            color=GREY_E,   # colors man
            run_time=2,   # Faster animation
            position=np.array([-5.2,1.8,0])
        )

        dashed_line = DashedLine(
            start=[-4, .30, 0],  # Your first point
            end=[-2, .30, 0],    # Your second point
            dash_length=0.2,  # Length of each dash
            dashed_ratio=0.5,  # Ratio of dash to space
            color=BLACK
        )

        small_brace_top = Tex(r"\{\_\}", color=BLACK).scale(1.5)
        small_brace_top.move_to(LEFT * 2 + UP * 2.5)
        prompt_top = Text("Prompt", color=BLACK, font="Helvetica").next_to(small_brace_top, DOWN, buff=0.5)
        neural2 = SVGMobject(f"{asset_folder}/neural2.svg").scale(0.5)
        neural2.move_to([3.1, 3, 0])
        neural3 = SVGMobject(f"{asset_folder}/neural2.svg").scale(0.5)
        neural3.move_to([3.1, -1.1, 0])
        input = SVGMobject(f"{asset_folder}/perceptionw1.svg").scale(1).stretch(factor=-1, dim=0)
        input.move_to([-5, 0, 0])
        rect = RoundedRectangle(height=5, width=3.5, corner_radius=0.2, color=rect_color, fill_opacity=1)
        rect.move_to([-5, -.2, 0])
        thinking = MarkupText("User thinking\nat 10 bits / second", font="Helvetica", color=BLACK, font_size=28).next_to(input, DOWN, buff=0.5)

        large_brace_top = Tex(r"\{\_\}", color=BLACK).scale(5)
        large_brace_top.move_to(RIGHT * 3 + UP * 2.5)
        response_top = Text("LLM Response", color=BLACK, font="Helvetica").next_to(large_brace_top, DOWN, buff=0.5)
        
        arrow_top = Arrow(
            start=small_brace_top.get_right(),
            end=large_brace_top.get_left(),
            buff=0.5,
            color=BLACK
        )

        # Second set of braces (bottom)
        small_brace_bottom = Tex(r"\{\_\}", color=BLACK).scale(1.5)
        small_brace_bottom.move_to(LEFT * 2 + DOWN * 1.5)
        prompt_bottom = Text("Prompt", color=BLACK, font="Helvetica").next_to(small_brace_bottom, DOWN, buff=0.5)
        
        large_brace_bottom = Tex(r"\{\_\}", color=BLACK).scale(4.5)
        large_brace_bottom.move_to(RIGHT * 3 + DOWN * 1.5)
        response_bottom = Text("LLM Response", color=BLACK, font="Helvetica").next_to(large_brace_bottom, DOWN, buff=0.5)
        
        arrow_bottom = Arrow(
            start=small_brace_bottom.get_right(),
            end=large_brace_bottom.get_left(),
            buff=0.5,
            color=BLACK
        )

        # Add dashed line separator
        '''
        dashed_line = DashedLine(
            start=LEFT * 7,  # Extend a bit past the left side
            end=RIGHT * 1.5,   # Extend a bit past the right side
            color=BLACK,
            dash_length=0.2,
            dashed_ratio=0.5
        ).move_to(DOWN * 0.1)  # Position between the two conversations
        '''
        self.add(rect, input, thinking)
        self.wait(.5)
        self.play(think_loop)
        self.remove(think_loop.circle_group)
        self.play(
            Flash(input, color=BLUE_E, flash_radius=1.2, line_width=12, num_lines=24, line_stroke_width=14),
        )
        # Add all elements to scene
        self.play(
            Write(small_brace_top),
            Create(prompt_top),
            run_time=.5
        )

        self.play(
            Write(arrow_top),
            run_time=1
        )
        self.play(
            Write(large_brace_top),
            Create(response_top),
            FadeIn(neural2),
            run_time=2
        )
        '''
        self.play(
            *[
                ApplyMethod(
                    dashed_line.shift, 
                    dashed_line.get_vector() * -.6,  # Controls how far dashes move
                    rate_func=lambda t: t % 1,  # Makes the animation loop
                    run_time=2
                )
                for _ in range(2)  # How many cycles
            ]
        )
        dashed_line.set_opacity(0)
        '''
        self.play(second_think_loop)
        self.remove(second_think_loop.circle_group)
        self.play(
            Flash(input, color=BLUE_E, flash_radius=1.2, line_width=6, num_lines=24, line_stroke_width=14),
        )
        self.play(
            Write(small_brace_bottom),
            run_time=1
        )


        self.play(
            Create(prompt_bottom),
            Create(arrow_bottom),
            run_time=.5
        )
        self.play(
            Write(large_brace_bottom),
            FadeIn(neural3),
            Create(response_bottom),
            run_time=.5
        )
        '''
        dashed_line.set_opacity(1)
        self.play(
            *[
                ApplyMethod(
                    dashed_line.shift, 
                    dashed_line.get_vector() * -.6,  # Controls how far dashes move
                    rate_func=lambda t: t % 1,  # Makes the animation loop
                    run_time=2
                )
                for _ in range(2)  # How many cycles
            ]
        )
        dashed_line.set_opacity(0)
        '''
        # Add dashed line last
        '''
        self.play(
            Create(dashed_line),
            run_time=1
        )
        '''
        self.play(third_think_loop)
        self.remove(third_think_loop.circle_group)
        self.play(
            Flash(input, color=BLUE_E, flash_radius=1.2, line_width=12, num_lines=24, line_stroke_width=14),
        )
        
        self.wait(1)

if __name__ == "__main__":
    # Command to render:
    # manim -pql scene.py CurlyBraceTransformation
    # Use -pqh for high quality
    scene = CurlyBraceTransformation()
    scene.render()