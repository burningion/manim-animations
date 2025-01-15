from manim import *
import numpy as np

import os

asset_folder = "../video_assets" # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"

class CurlyBraceTransformation(Scene):
    def construct(self):
        # Set the background color to white
        self.camera.background_color = WHITE
        
        # First set of braces (top)
        small_brace_top = Tex(r"\{\_\}", color=BLACK).scale(1.5)
        small_brace_top.move_to(LEFT * 2 + UP * 2.5)
        prompt_top = Text("Prompt", color=BLACK, font="Helvetica").next_to(small_brace_top, DOWN, buff=0.5)
        
        neural2 = SVGMobject(f"{asset_folder}/neural2.svg").scale(0.5)
        neural2.move_to([3.1, 3, 0])
        neural3 = SVGMobject(f"{asset_folder}/neural2.svg").scale(0.5)
        neural3.move_to([3.1, -1.1, 0])
        input = SVGMobject(f"{asset_folder}/perceptionw1.svg").scale(1).stretch(factor=-1, dim=0)
        input.move_to([-5, 0, 0])
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
        self.add(input)
        
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

        # Add dashed line last
        '''
        self.play(
            Create(dashed_line),
            run_time=1
        )
        '''

        self.wait(5)
        self.wait(1)

if __name__ == "__main__":
    # Command to render:
    # manim -pql scene.py CurlyBraceTransformation
    # Use -pqh for high quality
    scene = CurlyBraceTransformation()
    scene.render()