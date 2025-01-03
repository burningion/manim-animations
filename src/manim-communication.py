from manim import *
import numpy as np

config.frame_height = 7
config.frame_width = 19
config.background_color = WHITE
config.default_font = "Andale Mono"

class CommunicationModel(Scene):
    def construct(self):
        # Create shapes for person side
        sender_field_color = ManimColor((241, 172, 75))
        receiver_field_color = ManimColor((75, 161, 241))
        box_color = ManimColor((159, 168,178))
        
        person = Rectangle(height=2, width=3, color=GREEN, fill_opacity=0.4)
        person_encoder = Triangle(color=BLUE, fill_opacity=0.6).scale(2).rotate(-PI/2)  # Rotated 90 degrees
        shared_experience_text = MarkupText("Shared\nExperience", font="Helvetica").scale(.6).set_color(BLACK)
        shared_experience_text.move_to(ORIGIN + [0, -2.0, 0])
        # Create shapes for LLM side
        llm = Rectangle(height=2, width=3, color=RED, fill_opacity=0.4)
        llm_decoder = Triangle(color=ORANGE, fill_opacity=0.4).scale(2).rotate(PI/2)  # Rotated -90 degrees
        
        person_text = MarkupText("Sender's Field of Experience", font="Helvetica").scale(.6).set_color(BLACK)
        llm_text = MarkupText("Receiver's Field of Experience", font="Helvetica").scale(.6).set_color(BLACK)

        # Create signal rectangle
        signal = RoundedRectangle(height=1.5, width=2, color=PURPLE, fill_opacity=0.5, corner_radius=.2)
        signal_text = MarkupText("<b>Signal</b>", font="Helvetica").scale(0.8).set_color(WHITE)
        signal_group = VGroup(signal, signal_text)
        
        # Create context ellipses
        person_context = Ellipse(width=12, height=8, color=sender_field_color, fill_opacity=.6)
        llm_context = Ellipse(width=12, height=8, color=receiver_field_color, fill_opacity=.6)
        
        # Position all elements
        person.move_to(LEFT * 7.5)
        person_text.move_to(LEFT * 5 + [.5, -2.5, 0])
        person_encoder.next_to(person, RIGHT, buff=0)  # Reduced buffer to touch
        
        llm.move_to(RIGHT * 7.5) 
        llm_text.move_to(RIGHT * 5 + [-.3, -2.5, 0])
        llm_decoder.next_to(llm, LEFT, buff=0)        # Reduced buffer to touch
        
        signal_group.move_to(ORIGIN)
        
        person_context.move_to(LEFT * 3.3)
        llm_context.move_to(RIGHT * 3.3)
        
        # Add labels
        person_label = MarkupText("<b>Sender</b>", font="Helvetica").scale(0.7).move_to(person)
        llm_label = MarkupText("<b>Receiver</b>", font="Helvetica").scale(0.7).move_to(llm)
        
        # Add encoder/decoder labels
        person_encoder_label = MarkupText("<b>Encoder</b>", font="Helvetica", color=WHITE).scale(0.8).move_to(person_encoder)
        llm_decoder_label = MarkupText("<b>Decoder</b>", font="Helvetica", color=WHITE).scale(0.8).move_to(llm_decoder)
        
        line1 = Arrow(person_encoder, signal.get_left(), buff=0, color=BLACK)    
        line2 = Arrow(signal.get_right(), llm_decoder, buff=0, color=BLACK)

        # Position labels above triangles
        #person_encoder_label.next_to(person_encoder, UP, buff=0.3)
        #llm_decoder_label.next_to(llm_decoder, UP, buff=0.3)
        
        # Create message dot that will travel through the system
        message = Dot(color=WHITE, radius=0.2)
        message.next_to(person, DOWN, buff=0.3)
        message_star = Star(color=WHITE, fill_opacity=1, stroke_width=1, stroke_color=BLACK).scale(0.3).move_to(message)
        message_star_copy = message_star.copy()
        message_star_copy.move_to(llm_decoder.get_center() + [0, -.5, 0]).set_color(YELLOW)
        message_label = MarkupText("<b>Message</b>", font="Helvetica", color=BLACK).scale(0.5).next_to(message, DOWN, buff=0.3)
        message.move_to(person_encoder.get_center() + [0, -.5, 0])
        # Initial setup animation
        self.add(llm_context, person_context, person, llm, person_text, llm_text,
                    person_encoder, llm_decoder, signal_group, person_label, llm_label,
                    person_encoder_label, llm_decoder_label, shared_experience_text,
                    line1, line2)
        self.wait(0.5)
        label_offset = [0, -.9, 0]
        # 1. Message starts in person (highlight person)
        self.play(
            Create(message_star),
            Write(message_label),
            person.animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        self.wait(0.5)
        
        # 2. Message moves to encoder
        self.play(
            message_star.animate.move_to(person_encoder.get_center() + [0, -.5, 0]).set_color(YELLOW),
            message_label.animate.move_to(person_encoder.get_center() + label_offset),
            person_encoder.animate.set_fill(BLUE, opacity=0.8),
            person_encoder_label.animate.set_color(WHITE),
            run_time=1
        )
        self.wait(0.5)
        
        # 3. Message transforms in encoder
        self.play(
            Transform(message_star, message),
            run_time=0.5
        )
        
        # 4. Message moves to signal
        self.play(
            message_star.animate.move_to(signal.get_center() + [0, -.5, 0]).set_stroke(width=1, color=BLACK),
            message_label.animate.move_to(signal.get_center() + label_offset),
            signal.animate.set_fill(PURPLE, opacity=0.9),
            run_time=1
        )
        self.wait(0.5)
        
        # 5. Message moves to decoder
        self.play(
            message_star.animate.move_to(llm_decoder.get_center() + [0, -.5, 0]),
            message_label.animate.move_to(llm_decoder.get_center() + label_offset),
            llm_decoder.animate.set_fill(ORANGE, opacity=0.8),
            llm_decoder_label.animate.set_color(WHITE),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            Transform(message_star, message_star_copy),
        )
        self.wait(0.5)

        # 6. Message arrives at LLM
        self.play(
            message_star.animate.next_to(llm, DOWN, buff=0.3).set_color(WHITE).set_stroke(width=1, color=BLACK),
            message_label.animate.next_to(llm, DOWN, buff=0.9),
            llm.animate.set_fill(RED, opacity=0.8),
            run_time=1
        )
        self.wait(0.5)
        
        # Reset colors
        self.play(
            person.animate.set_opacity(.4),
            person_encoder.animate.set_opacity(.4),
            #signal.animate.set_fill(opacity=0),
            llm_decoder.animate.set_opacity(.4),
            signal.animate.set_opacity(.5),
            llm.animate.set_opacity(.4),  
            message_star.animate.set_opacity(0),
            message_label.animate.set_opacity(0),
            run_time=1
        )
        
        self.wait(1)



if __name__ == "__main__":
    # Command line: manim -pql communication_model.py CommunicationModel
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_height = 8
    config.frame_width = 18