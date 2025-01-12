from manim import *
import os

asset_folder = "../video_assets" # Path to assets folder for preview

if os.environ.get("RENDERING_MODE"):
    asset_folder = "./video_assets"

class DecisionTreeAnimation(Scene):
    def construct(self):
        # Create the decision circle at the top
        self.camera.background_color = WHITE
        decision_circle = SVGMobject(f"{asset_folder}/decision.svg")
        decision_text = MarkupText("<b>Media Decision</b>", font="Helvetica", font_size=36, color=BLACK)
        decision_text.next_to(decision_circle, DOWN, buff=.5)
        decision_group = VGroup(decision_circle, decision_text)
        decision_group.shift(UP * 2)

        # Create the initial bottom nodes
        options = ["<b>TV Show</b>", "<b>Movie Theater</b>", "<b>Social Media</b>"]
        scores = ["Commitment: 30-60mins\n\nRewards: 6\n\nAttention Cost: 5", "Commitment: 1-2.5 hrs\n\nRewards: 7.5\n\nAttention Cost: 8", "Commitment: 15s-3.5hrs\n\nRewards: ??\n\nAttention Cost: 4"]
        filenames = [f"{asset_folder}/tv-show.svg", f"{asset_folder}/movie-theater.svg", f"{asset_folder}/social-media.svg"]
        bottom_circles = VGroup(*[SVGMobject(file).scale(.5) for file in filenames])
        bottom_texts = VGroup(*[MarkupText(text, font_size=24, color=BLACK, font="Helvetica") for text in options])
        score_texts = VGroup(*[Text(score, font_size=20, color=BLACK, font="Helvetica") for score in scores])
        
        # Position bottom nodes
        bottom_circles.arrange(RIGHT, buff=3.0)
        bottom_circles.shift(DOWN * 2.5)
        
        for text, circle, score in zip(bottom_texts, bottom_circles, score_texts):
            text.next_to(circle, DOWN, buff=0.7)
            score.next_to(text, DOWN, buff=0.5)
        
        bottom_groups = VGroup(*[
            VGroup(circle, text, score) 
            for circle, text, score in zip(bottom_circles, bottom_texts, score_texts)
        ])

        # Create arrows
        arrows = VGroup(*[
            Arrow(
                start=decision_circle.get_bottom() + DOWN * 1,
                end=circle.get_top(),
                buff=0.4,
                stroke_width=4,
                color=BLACK
            ) 
            for circle in bottom_circles
        ])

        # Initially hide score texts
        for score in score_texts:
            score.set_opacity(0)

        # First part of animation (same as before)
        self.play(Create(decision_circle))
        self.play(Write(decision_text))
        for arrow in arrows:
            self.play(Create(arrow), run_time=1)
        for group in bottom_groups:
            self.play(
                Create(group[0]),
                Write(group[1]),
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

        # Move bottom elements up
        target_y = 0
        animations = []
        for group in bottom_groups:
            target_pos = group.get_center().copy()
            target_pos[1] = target_y
            animations.append(group.animate.move_to(target_pos))

        self.play(*animations, run_time=1.5)

        # Fade in scores
        for group in bottom_groups:
            score = group[2]
            self.play(
                score.animate.set_opacity(1),
                run_time=0.5
            )

        self.wait(5)

        # Create new elements for Books and Podcast
        new_options = ["<b>Book</b>", "<b>Podcast</b>"]
        new_scores = ["Commitment: 30+ hrs (??)\n\nRewards: 6-10\n\nAttention Cost: 9", "Commitment: 30-60mins\n\nRewards: 6\n\nAttention Cost: 3"]
        new_filenames = [f"{asset_folder}/books.svg", f"{asset_folder}/podcast.svg"]
        
        # Create new elements starting small and invisible
        new_circles = VGroup(*[SVGMobject(file).scale(0.1) for file in new_filenames])  # Start very small
        new_texts = VGroup(*[MarkupText(text, font_size=24, color=BLACK, font="Helvetica").set_opacity(0) 
                            for text in new_options])
        new_score_texts = VGroup(*[MarkupText(score, font_size=20, color=BLACK, font="Helvetica") .set_opacity(0) 
                                 for score in new_scores])

        # Position new elements at the same x-coordinates as the elements they're replacing
        for i, (new_circle, new_text, new_score) in enumerate(zip(new_circles, new_texts, new_score_texts)):
            old_group = bottom_groups[i]
            new_circle.move_to(old_group[0])
            new_text.move_to(old_group[1])
            new_score.move_to(old_group[2])

        # Fade out old elements (first two groups) and fade in/expand new ones
        for i in range(2):  # Only replace first two groups
            if i == 1:
                self.play(
                    FadeOut(bottom_groups[i]),
                    new_texts[0].animate.set_opacity(1),
                    new_score_texts[0].animate.set_opacity(1),
                    new_circles[i].animate.scale(5),  # Scale up to final size
                    run_time=1
                )
            else:
                self.play(
                    FadeOut(bottom_groups[i]),
                    new_circles[i].animate.scale(5),
                    run_time=1
                )

        self.play(
                new_texts[1].animate.set_opacity(1),
                new_score_texts[1].animate.set_opacity(1),
                run_time=1
        )
        self.wait(2)
if __name__ == "__main__":
    # Command to render:
    # manim -pqh decision_tree.py DecisionTreeAnimation
    pass