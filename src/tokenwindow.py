from manim import *
import numpy as np

import os

asset_folder = "../video_assets" # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"

# Create the folder if it doesn't exist - now relative to the *correct* asset_folder
if not os.path.exists(asset_folder):
    os.makedirs(asset_folder)

# Create dummy svg files if they don't exist (for local testing) - using the *correct* asset_folder
if not os.path.exists(os.path.join(asset_folder, "neural2.svg")):
    with open(os.path.join(asset_folder, "neural2.svg"), "w") as f:
        f.write('<svg><rect width="100" height="100" fill="red"/></svg>') # Placeholder SVG


if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets" # Redundant, already defined above - but keeping for consistency with your original code

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

class ContextWindowAnimation(Scene):
    def construct(self):
        # Set the background color to white - Ensuring white background
        self.camera.background_color = WHITE
        rect_color = ManimColor((241, 172, 75))
        neural_rect_color = ManimColor((158, 162, 184))
        think_color = ManimColor((255/255, 182/255, 55/255)) # Scaled to 0-1 range
        used_color = BLUE_D
        available_color = ManimColor(BLUE_E, alpha=0.5) # Using ManimColor as suggested

        # Context Window Rectangle - Moved further down
        window_width = 10
        window_height = 0.7 # Slightly thinner context window
        context_window_rect = Rectangle(width=window_width, height=window_height, color=BLACK).move_to(DOWN*2.5) # Moved down significantly
        context_window_fill = Rectangle(width=window_width, height=window_height, color=available_color, fill_opacity=1).move_to(DOWN*2.5).align_to(context_window_rect, LEFT) # Moved down, aligned left initially
        context_window_group = VGroup(context_window_rect, context_window_fill).move_to(DOWN * 2.5) # Group moved down even further

        context_label = Text("200k Token Context Window", color=BLACK, font="Helvetica", font_size=20).next_to(context_window_rect, UP, buff=0.1) # Smaller font for context label

        # Neural Network Icon
        neural_net = SVGMobject(os.path.join(asset_folder, "neural2.svg")).scale(0.45).move_to(RIGHT * 5 + UP * 1.5) # Vertically Aligned with User Input
        llm_label = Text("Neural Network", color=BLACK, font="Helvetica", font_size=20).next_to(neural_net, DOWN, buff=0.2) # LLM Label

        # Input Icon (User) -  Using a blue square Mobject directly - as in the image
        input_icon = SVGMobject(os.path.join(asset_folder, "perceptionw1.svg")).scale(.5).move_to(LEFT * 5 + UP * 1.5).stretch(factor=-1, dim=0) # Blue Square, Vertically Aligned with NN
        rect = RoundedRectangle(height=4.5, width=3.5, corner_radius=0.2, color=rect_color, fill_opacity=1)
        neural_rect = RoundedRectangle(height=4.5, width=3.5, corner_radius=0.2, color=neural_rect_color, fill_opacity=1)
        neural_rect.move_to([5, .82, 0])
        llm_label = MarkupText("Language Model", font="Helvetica", color=BLACK, font_size=28).next_to(neural_net, DOWN, buff=0.2)
        rect.move_to([-5, .82, 0])
        thinking = MarkupText("User thinking\nat 10 bits / second", font="Helvetica", color=BLACK, font_size=28).next_to(input_icon, DOWN, buff=0.2)

        # Thinking Animation
        think_loop = ThinkingAnimation(
            radius=.25,     # Smaller circle
            num_dots=8,    # Fewer dots
            color=GREY_E,   # colors man
            run_time=1.5,   # Faster animation
            position=neural_net.get_bottom() + DOWN*1.4 # Positioned near NN, adjusted
        )

        # --- Prompt and Response Functions - Fixed Vertical Position ---
        prompt_response_y_pos = 1 # Fixed Y position for prompts and responses in the middle row
        def create_prompt_response(prompt_text, response_text): # Removed position_y argument
            prompt_brace = Tex(r"\{\_\}", color=BLACK).scale(0.8).move_to(LEFT * 2 + UP * prompt_response_y_pos) # Fixed Y
            prompt_label = Text(prompt_text, color=BLACK, font="Helvetica", font_size=16).next_to(prompt_brace, DOWN, buff=0.1)
            response_brace = Tex(r"\{\_\}", color=BLACK).scale(2.5).move_to(RIGHT * 2 + UP * prompt_response_y_pos) # Fixed Y
            response_label = Text(response_text, color=BLACK, font="Helvetica", font_size=16).next_to(response_brace, DOWN, buff=0.1)
            arrow = Arrow(start=prompt_brace.get_right(), end=response_brace.get_left(), buff=0.2, color=BLACK, stroke_width=2) # Thinner arrow
            return VGroup(prompt_brace, prompt_label, response_brace, response_label, arrow)

        # --- Animation Sequence ---
        self.add(rect, neural_rect, context_window_group, context_label, neural_net, llm_label, input_icon, thinking) # Added llm_label
        self.wait(0.5)

        # --- Turn 1 ---
        turn1_group = create_prompt_response("Prompt 1\n(5k tokens)", "Response 1\n(15k tokens)") # No position argument now
        self.play(Write(turn1_group[0:2]), Create(turn1_group[4]), run_time=0.5)
        self.play(think_loop)
        self.remove(think_loop.circle_group)
        self.play(Write(turn1_group[2:4]), run_time=1)
        self.wait(0.5)

        # Update Context Window Fill
        initial_fill_width = window_width
        used_tokens_turn1 = 5000 + 15000 # Example token counts
        total_used_tokens = used_tokens_turn1
        fraction_total_used = total_used_tokens / 200000
        new_fill_width_turn1 = initial_fill_width * (1 - fraction_total_used)

        # Ensure fill starts aligned and shrinks within bounds
        self.play(
            context_window_fill.animate.become(Rectangle(width=new_fill_width_turn1, height=window_height, color=used_color, fill_opacity=1).move_to(context_window_rect, LEFT)).set_color(used_color),
            run_time=1
        )
        self.play(FadeOut(turn1_group), run_time=0.5) # Fade out turn 1 group
        self.wait(0.5)

        # --- Turn 2 ---
        turn2_group = create_prompt_response("Prompt 2\n(8k tokens)", "Response 2\n(22k tokens)") # No position argument
        self.play(Write(turn2_group[0:2]), Create(turn2_group[4]), run_time=0.5)
        self.play(think_loop)
        self.remove(think_loop.circle_group)
        self.play(Write(turn2_group[2:4]), run_time=1)
        self.wait(0.5)

        # Update Context Window Fill Again
        used_tokens_turn2 = 8000 + 22000 # Example token counts
        total_used_tokens += used_tokens_turn2
        fraction_total_used = total_used_tokens / 200000
        new_fill_width_total = initial_fill_width * (1 - fraction_total_used)

        # Ensure fill starts aligned and shrinks within bounds
        self.play(
            context_window_fill.animate.become(Rectangle(width=new_fill_width_total, height=window_height, color=used_color, fill_opacity=1).move_to(context_window_rect, LEFT)).set_color(used_color),
            run_time=1
        )
        self.play(FadeOut(turn2_group), run_time=0.5) # Fade out turn 2 group
        self.wait(0.5)

        # --- Turn 3 - Middle Row ---
        turn3_group = create_prompt_response("Prompt 3\n(15k tokens)", "Response 3\n(50k tokens)") # No position argument
        self.play(Write(turn3_group[0:2]), Create(turn3_group[4]), run_time=0.5)
        self.play(think_loop)
        self.remove(think_loop.circle_group)
        self.play(Write(turn3_group[2:4]), run_time=1)
        self.wait(0.5)

        # Update Context Window Fill Again for Turn 3
        used_tokens_turn3 = 15000 + 50000 # Example token counts
        total_used_tokens += used_tokens_turn3
        fraction_total_used = total_used_tokens / 200000
        new_fill_width_total = initial_fill_width * (1 - fraction_total_used)

        # Ensure fill starts aligned and shrinks within bounds
        self.play(
            context_window_fill.animate.become(Rectangle(width=new_fill_width_total, height=window_height, color=used_color, fill_opacity=1).move_to(context_window_rect, LEFT)).set_color(used_color),
            run_time=1
        )
        self.play(FadeOut(turn3_group), run_time=0.5) # Fade out turn 3 group
        self.wait(2) # Longer wait at the end

if __name__ == "__main__":
    # Command to render:
    # manim -pql scene.py ContextWindowAnimation
    # Use -pqh for high quality
    scene = ContextWindowAnimation()
    scene.render()