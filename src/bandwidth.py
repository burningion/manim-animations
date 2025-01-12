from manim import *
import random, math
import numpy as np
class SimpleRateComparison(Scene):
    def construct(self):
        # Set white background
        self.camera.background_color = WHITE
        
        # Title
        title = Text("Information Processing Rates", color=BLACK)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create two simple rectangles to show scale
        neural = Rectangle(width=10, height=0.5, color=BLUE_E)
        neural.shift(UP * 2)
        
        conscious = Rectangle(width=0.1, height=0.5, color=RED_E)  # 1/100 width
        conscious.shift(DOWN * 2)
        
        # Labels
        neural_label = Text("1 Gbit/s", color=BLACK).scale(0.8)
        neural_label.next_to(neural, RIGHT)
        
        conscious_label = Text("10 bit/s", color=BLACK).scale(0.8)
        conscious_label.next_to(conscious, RIGHT)
        
        # Show the basic shapes
        self.play(
            Create(neural),
            Write(neural_label)
        )
        self.play(
            Create(conscious),
            Write(conscious_label)
        )
        
        # Add bit counters
        neural_bits = VGroup(*[
            Dot(color=BLUE_E, radius=0.05)
            for _ in range(20)
        ])
        
        conscious_bit = Dot(color=RED_E, radius=0.05)
        
        # Position bits
        for i, bit in enumerate(neural_bits):
            bit.move_to(neural.get_left() + RIGHT * 0.5 + RIGHT * i * 0.4)
        
        conscious_bit.move_to(conscious.get_left())
        
        self.add(neural_bits, conscious_bit)
        
        # Simple animation to show rate difference
        for _ in range(50):  # 5 seconds
            # Neural animation - rapid movement
            self.play(
                *[bit.animate.shift(RIGHT * 0.2) for bit in neural_bits],
                conscious_bit.animate.shift(RIGHT * 0.002),  # Much slower
                run_time=0.1
            )
            
            # Reset bits that go too far
            for bit in neural_bits:
                if bit.get_center()[0] > neural.get_right()[0]:
                    bit.move_to(neural.get_left() + RIGHT * 0.5)
            
            if conscious_bit.get_center()[0] > conscious.get_right()[0]:
                conscious_bit.move_to(conscious.get_left())
        
        self.wait()


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