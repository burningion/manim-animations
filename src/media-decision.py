from manim import *

class DecisionTreeAnimation(Scene):
    def construct(self):
        # Create the decision circle at the top
        self.camera.background_color = WHITE
        decision_circle = SVGMobject("../video_assets/decision.svg")
        decision_text = MarkupText("<b>Media Decision</b>", font="Helvetica", font_size=36, color=BLACK)
        decision_text.next_to(decision_circle, DOWN, buff=.5)
        decision_group = VGroup(decision_circle, decision_text)
        decision_group.shift(UP * 2)

        # Create the bottom nodes
        options = ["TV Show", "Social Media", "Movie Theater"]
        bottom_circles = VGroup(*[Circle(radius=1.0) for _ in options])
        bottom_texts = VGroup(*[Text(text, font_size=36, color=BLACK, font="Helvetica") for text in options])
        
        # Position bottom nodes
        bottom_circles.arrange(RIGHT, buff=1.5)
        bottom_circles.shift(DOWN * 2.5)
        
        for text, circle in zip(bottom_texts, bottom_circles):
            text.next_to(circle, ORIGIN)
        
        bottom_groups = VGroup(*[
            VGroup(circle, text) 
            for circle, text in zip(bottom_circles, bottom_texts)
        ])

        # Create arrows
        arrows = VGroup(*[
            Arrow(
                start=decision_circle.get_bottom() + DOWN * 1,
                end=circle.get_top(),
                buff=0.3,
                stroke_width=4,
                color=BLACK
            ) 
            for circle in bottom_circles
        ])

        # Animation sequence
        # Draw the decision circle
        self.play(Create(decision_circle))
        # Fade in the decision text
        self.play(Write(decision_text))
        # Draw the arrows one by one
        for arrow in arrows:
            self.play(Create(arrow), run_time=1)
        # Draw bottom circles and their text simultaneously
        for bottom_group in bottom_groups:
            self.play(
                Create(bottom_group[0]),
                Write(bottom_group[1]),
                run_time=1
            )
        
        # Pause at the end to show the complete diagram
        self.wait(2)

if __name__ == "__main__":
    # Command to render:
    # manim -pqh decision_tree.py DecisionTreeAnimation
    pass