from manim import *
import random

class BandwidthComparison(Scene):
    def construct(self):
        # Use white background with dark text
        self.camera.background_color = WHITE
        
        # Create title
        title = Text("Human Information Processing", color=BLACK).scale(0.8)
        title.to_edge(UP)
        
        # Create labels for the two rates
        thought_label = Text("Conscious Thought\n10 bits/s", color=BLACK).scale(0.6)
        sensory_label = Text("Sensory Input\n1 Gbit/s", color=BLACK).scale(0.6)
        
        # Position labels
        thought_label.to_edge(LEFT).shift(UP * 1)
        sensory_label.to_edge(LEFT).shift(DOWN * 1)
        
        # Create rectangles to represent the bandwidths
        thought_rect = Rectangle(
            width=0.1,  # Very small width for 10 bits
            height=0.5,
            fill_color=BLUE_E,
            fill_opacity=1,
            stroke_color=BLUE_E
        )
        
        sensory_rect = Rectangle(
            width=10,  # 100,000,000 times wider
            height=0.5,
            fill_color=RED_E,
            fill_opacity=1,
            stroke_color=RED_E
        )
        
        # Position rectangles
        thought_rect.next_to(thought_label, RIGHT, buff=0.5)
        sensory_rect.next_to(sensory_label, RIGHT, buff=0.5)
        
        # Create explanatory text
        explanation = Text(
            "The difference is about 100 million times!",
            color=BLACK
        ).scale(0.6)
        explanation.next_to(sensory_rect, DOWN, buff=1)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        
        self.play(
            Write(thought_label),
            Create(thought_rect)
        )
        self.wait(1)
        
        self.play(
            Write(sensory_label),
            Create(sensory_rect)
        )
        self.wait(1)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Add a zooming animation to emphasize the scale
        zoom_rect = Rectangle(
            width=thought_rect.width * 1.5,
            height=thought_rect.height * 1.5,
            color=GREEN
        ).move_to(thought_rect)
        
        self.play(Create(zoom_rect))
        self.play(
            zoom_rect.animate.scale(50),
            run_time=3
        )
        self.wait(1)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

class DataRateVisualization(Scene):
    def construct(self):
        # Use white background
        self.camera.background_color = WHITE
        
        # Title
        title = Text("What is 1 Gigabit per second?", color=BLACK).scale(0.8)
        title.to_edge(UP)
        
        # Create comparisons
        comparisons = VGroup()
        
        # 1. Text messages (assume 100 bytes each)
        texts = self.create_comparison(
            "Text Messages",
            "1,250,000 per second",
            "💬",
            BLACK
        )
        
        # 2. High-quality photos (assume 5MB each)
        photos = self.create_comparison(
            "HD Photos",
            "25 per second",
            "📷",
            BLACK
        )
        
        # 3. Music (assume 320kbps MP3)
        music = self.create_comparison(
            "Music Tracks",
            "3,125 songs playing simultaneously",
            "🎵",
            BLACK
        )
        
        # 4. Netflix HD video (assume 5 Mbps)
        netflix = self.create_comparison(
            "Netflix HD Streams",
            "200 streams simultaneously",
            "🎬",
            BLACK
        )
        
        # Position all comparisons
        comparisons = VGroup(texts, photos, music, netflix).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.75
        ).next_to(title, DOWN, buff=1)
        
        # Progress bar to show one second passing
        progress_bar = Rectangle(
            width=10,
            height=0.2,
            color=BLACK
        ).to_edge(DOWN, buff=1)
        
        progress = Rectangle(
            width=0,
            height=0.2,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=0
        ).align_to(progress_bar, LEFT)
        
        time_label = Text("0.0s", color=BLACK).scale(0.6)
        time_label.next_to(progress_bar, DOWN)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(0.5)
        
        # Reveal each comparison
        for comp in [texts, photos, music, netflix]:
            self.play(Write(comp), run_time=1)
            self.wait(0.5)
        
        # Add and animate progress bar
        self.play(
            Create(progress_bar),
            Write(time_label)
        )
        
        # Animate one second passing
        self.play(
            progress.animate.match_width(progress_bar),
            time_label.animate.become(
                Text("1.0s", color=BLACK).scale(0.6).next_to(progress_bar, DOWN)
            ),
            run_time=1,
            rate_func=linear
        )
        
        self.wait(2)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def create_comparison(self, title, amount, emoji, color):
        return VGroup(
            Text(f"{emoji} {title}:", color=color).scale(0.6),
            Text(amount, color=color).scale(0.5)
        ).arrange(RIGHT, buff=0.5)

class HumanProcessingRate(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Title
        title = Text("Human Information Processing Rate (~10 bits/s)", color=BLACK, font="Helvetica").scale(0.8)
        title.to_edge(UP)
        
        # Create examples from the paper
        examples = VGroup()
        
        # 1. Tetris Pro Gaming
        tetris = self.create_example(
            "Professional Tetris",
            "~7 bits/s",
            "4 orientations × 9 positions\n3-4 pieces/second",
            "🎮"
        )
        
        # 2. Fitts' Motor Tasks
        motor = self.create_example(
            "Rapid Motor Tasks",
            "10-12 bits/s",
            "Moving forearms between\ntarget areas",
            "🎯"
        )
        
        # 3. Choice Reaction (Hick's Law)
        reaction = self.create_example(
            "Choice Reaction",
            "~5 bits/s",
            "Responding to random\nlight patterns",
            "💡"
        )
        
        # 4. Professional Gaming (StarCraft)
        starcraft = self.create_example(
            "StarCraft Pro Gaming",
            "~16.7 bits/s",
            "1000 actions/minute\nduring intense battles",
            "⚔️"
        )
        
        # Position all examples
        examples = VGroup(tetris, motor, reaction, starcraft).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.75
        ).next_to(title, DOWN, buff=1)
        
        # Add a real-time visualization
        timeline = NumberLine(
            x_range=[0, 1, 0.1],
            length=10,
            color=BLACK,
            include_numbers=True
        )
        
        time_label = Text("Time (seconds)", color=BLACK, font="Helvetica").scale(0.5)
        time_label.next_to(timeline, DOWN)
        
        dot = Dot(color=BLUE_E)
        dot.move_to(timeline.n2p(0))
        
        # Create bit counter
        bit_counter = Text("Bits processed: 0", color=BLACK, font="Helvetica").scale(0.6)
        bit_counter.next_to(timeline, UP, buff=0.5)
        
        # Group timeline elements
        timeline_group = VGroup(timeline, time_label, bit_counter, dot)
        timeline_group.move_to(ORIGIN)  # Center the timeline
        
        # Animation sequence
        self.play(Write(title))
        self.wait(0.5)
        
        # Show each example
        for example in [tetris, motor, reaction, starcraft]:
            self.play(Write(example), run_time=1)
        
        # Wait for 2 seconds to let viewer read
        self.wait(2)
        
        # Fade examples and title to white
        self.play(
            *[mob.animate.set_color(WHITE) for mob in [*examples, title]],
            run_time=1
        )
        
        # Show timeline and counter
        self.play(
            Create(timeline),
            Write(time_label),
            Write(bit_counter),
            Create(dot)
        )
        
        # Animate one second passing with dot and counter
        def update_counter(mob, alpha):
            value = int(alpha * 10)
            mob.become(
                Text(f"Bits processed: {value}", color=BLACK)
                .scale(0.6)
                .next_to(timeline, UP, buff=0.5)
            )
        
        self.play(
            dot.animate.move_to(timeline.n2p(1)),
            UpdateFromAlphaFunc(bit_counter, update_counter),
            run_time=1,
            rate_func=linear
        )
        
        self.wait(2)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def create_example(self, title, rate, details, emoji):
        return VGroup(
            Text(f"{emoji} {title}:", color=BLACK, font="Helvetica").scale(0.6),
            Text(rate, color=BLUE_E, font="Helvetica").scale(0.5),
            Text(details, color=GRAY_E, font="Helvetica").scale(0.4)
        ).arrange(RIGHT, buff=0.5, aligned_edge=UP)

# To render:
# manim -pqh human_processing_rate.py HumanProcessingRate