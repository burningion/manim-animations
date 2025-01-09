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
        options = ["<b>TV Show</b>", "<b>Movie Theater</b>", "<b>Social Media</b>"]
        scores = ["Commitment: 30-60mins\n\nRewards: 6", "Commitment: 1-2.5 hrs\n\nRewards: 7.5", "Commitment: 15s-3.5hrs\n\nRewards: ??"]
        filenames = ["../video_assets/tv-show.svg", "../video_assets/movie-theater.svg", "../video_assets/social-media.svg"]
        bottom_circles = VGroup(*[SVGMobject(file).scale(.5) for file in filenames])
        bottom_texts = VGroup(*[MarkupText(text, font_size=24, color=BLACK, font="Helvetica") for text in options])
        score_texts = VGroup(*[MarkupText(score, font_size=20, color=BLACK, font="Helvetica") for score in scores])
        
        # Position bottom nodes
        bottom_circles.arrange(RIGHT, buff=3)
        bottom_circles.shift(DOWN * 2.5)
        
        for text, circle, score in zip(bottom_texts, bottom_circles, score_texts):
            text.next_to(circle, DOWN, buff=.5)
            score.next_to(text, DOWN, buff=.3)
        
        # Create complete bottom groups including scores
        bottom_groups = VGroup(*[
            VGroup(circle, text, score) 
            for circle, text, score in zip(bottom_circles, bottom_texts, score_texts)
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

        # Initially hide score texts
        for score in score_texts:
            score.set_opacity(0)

        # First part of animation
        self.play(Create(decision_circle))
        self.play(Write(decision_text))
        for arrow in arrows:
            self.play(Create(arrow), run_time=1)
        for group in bottom_groups:
            self.play(
                Create(group[0]),  # circle
                Write(group[1]),   # text
                run_time=1
            )
        
        self.wait(1)

        # Fade out top elements
        self.play(
            FadeOut(decision_circle),
            FadeOut(decision_text),
            FadeOut(arrows),
            run_time=1
        )

        # Move bottom elements up and reveal scores
        target_y = 0  # New vertical position (center of screen)
        animations = []
        for group in bottom_groups:
            # Create target position maintaining x-coordinate but changing y-coordinate
            target_pos = group.get_center().copy()
            target_pos[1] = target_y
            animations.append(group.animate.move_to(target_pos))

        self.play(*animations, run_time=1.5)

        # Fade in scores
        for group in bottom_groups:
            score = group[2]  # The score text is the third element in each group
            self.play(
                score.animate.set_opacity(1),
                run_time=0.5
            )

        self.wait(2)

if __name__ == "__main__":
    # Command to render:
    # manim -pqh decision_tree.py DecisionTreeAnimation
    pass