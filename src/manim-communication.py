from manim import *
import numpy as np

config.frame_height = 7
config.frame_width = 19
config.background_color = WHITE
config.default_font = "Andale Mono"

class CommunicationModel(Scene):
    def construct(self):
        #self.camera.background_color = (230, 230, 230)
        # Create shapes for person side

        sender_field_color = ManimColor((241, 172, 75))
        sender_end_color = ManimColor((151, 108, 47))
        receiver_field_color = ManimColor((75, 161, 241))
        receiver_end_color = ManimColor((47, 101, 151))
        box_color = ManimColor((159, 168,178))
        
        person = RoundedRectangle(height=2, width=4, color=box_color, fill_opacity=1, corner_radius=.1)
        person.stroke_color = BLACK
        person_encoder = Triangle(color=box_color, fill_opacity=1).scale(1.1).rotate(-PI/2)  # Rotated 90 degrees
        person_encoder.stroke_color = BLACK
        shared_experience_text = MarkupText("Shared\nExperience", font="Helvetica").scale(.6).set_color(BLACK)
        shared_experience_text.move_to(ORIGIN + [0, -2.0, 0])
        # Create shapes for LLM side
        llm = RoundedRectangle(height=2, width=4, color=box_color, fill_opacity=1, corner_radius=.1)
        llm.stroke_color = BLACK
        llm_decoder = Triangle(color=box_color, fill_opacity=1).scale(1.1).rotate(PI/2)  # Rotated -90 degrees
        llm_decoder.stroke_color = BLACK

        person_text = MarkupText("Sender's Field of Experience", font="Helvetica").scale(.7).set_color(BLACK)
        llm_text = MarkupText("Receiver's Field of Experience", font="Helvetica").scale(.7).set_color(BLACK)

        # Create signal rectangle
        signal = RoundedRectangle(height=1.5, width=2, color=box_color, fill_opacity=1, corner_radius=.1)
        signal.stroke_color = BLACK
        signal_text = MarkupText("<b>Signal</b>", font="Helvetica").scale(0.8).set_color(WHITE)
        signal_group = VGroup(signal, signal_text)
        
        # Create context ellipses
        person_context = Ellipse(width=12, height=8, color=sender_field_color, fill_opacity=.7).set_fill(color=[sender_field_color, sender_end_color]).set_stroke(width=10, color=sender_field_color)
        llm_context = Ellipse(width=12, height=8, color=receiver_field_color, fill_opacity=.7).set_fill(color=[receiver_field_color, receiver_end_color]).set_stroke(width=10, color=receiver_field_color)
        
        # Position all elements
        person.move_to(LEFT * 6)
        person_text.move_to(LEFT * 5 + [.2, -2.5, 0])
        person_encoder.next_to(person, RIGHT, buff=0)  # Reduced buffer to touch
        
        llm.move_to(RIGHT * 6) 
        llm_text.move_to(RIGHT * 5 + [-.2, -2.5, 0])
        llm_decoder.next_to(llm, LEFT, buff=0)        # Reduced buffer to touch
        
        signal_group.move_to(ORIGIN)
        
        person_context.move_to(LEFT * 3.3)
        llm_context.move_to(RIGHT * 3.3)
        
        # Add labels
        person_label = MarkupText("<b>Sender</b>", font="Helvetica", color=BLACK).scale(0.7).move_to(person)
        llm_label = MarkupText("<b>Receiver</b>", font="Helvetica", color=BLACK).scale(0.7).move_to(llm)
        
        # Add encoder/decoder labels
        person_encoder_label = MarkupText("<b>Encode</b>", font="Helvetica").scale(0.5).move_to(person_encoder)
        llm_decoder_label = MarkupText("<b>Decode</b>", font="Helvetica").scale(0.5).move_to(llm_decoder)
        
        line1 = Arrow(person_encoder, signal.get_left(), buff=0, color=BLACK)    
        line2 = Arrow(signal.get_right(), llm_decoder, buff=0, color=BLACK)

        # Position labels above triangles
        #person_encoder_label.next_to(person_encoder, UP, buff=0.3)
        #llm_decoder_label.next_to(llm_decoder, UP, buff=0.3)
        
        perception = SVGMobject("perception.svg").scale(.9).move_to(person_context.get_center() + [-.5, 2.4, 0])
        perception2 = perception.copy().move_to(llm_context.get_center() + [.5, 2.4, 0]).stretch(factor=-1, dim=0)
        # Create message dot that will travel through the system
        message = SVGMobject("mailb.svg").scale(0.3)
        message_star = SVGMobject("letterb.svg").scale(0.5).next_to(person, LEFT, buff=-1)
        message_star_copy = message_star.copy()
        message_star_copy.move_to(llm_decoder.get_center() + [0, -1, 0])
        message_label = MarkupText("<b></b>", font="Helvetica", color=BLACK).scale(0.5).next_to(message, DOWN, buff=0.3)
        message.move_to(person_encoder.get_center() + [0, -1, 0])
        # Initial setup animation
        self.add(llm_context, person_context, person, llm, person_text, llm_text,
                    person_encoder, llm_decoder, signal_group, person_label, llm_label,
                    person_encoder_label, llm_decoder_label, shared_experience_text,
                    line1, line2, perception, perception2)
        self.wait(0.5)
        label_offset = [0, -.9, 0]
        # 1. Message starts in person (highlight person)
        self.play(
            Create(message_star),
            Write(message_label),
            person.animate.set_fill(GREEN, opacity=1),
            run_time=1
        )
        self.wait(0.5)
        
        # 2. Message moves to encoder
        self.play(
            message_star.animate.move_to(person_encoder.get_center() + [0, -1., 0]),
            message_label.animate.move_to(person_encoder.get_center() + label_offset),
            person_encoder.animate.set_fill(BLUE, opacity=1),
            person_encoder_label.animate.set_fill(WHITE),
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
            message_star.animate.move_to(signal.get_center() + [0, -1.05, 0]).set_stroke(width=1, color=BLACK),
            message_label.animate.move_to(signal.get_center() + label_offset),
            signal.animate.set_fill(PURPLE, opacity=0.9),
            person_encoder.animate.set_fill(box_color),
            person.animate.set_fill(box_color),
            run_time=1
        )
        self.wait(0.5)
        
        # 5. Message moves to decoder
        self.play(
            message_star.animate.move_to(llm_decoder.get_center() + [0, -1, 0]),
            message_label.animate.move_to(llm_decoder.get_center() + label_offset),
            llm_decoder.animate.set_fill(ORANGE, opacity=0.8),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            Transform(message_star, message_star_copy),
        )
        self.wait(0.5)

        # 6. Message arrives at LLM
        self.play(
            message_star.animate.next_to(llm, RIGHT, buff=-1).set_color(BLACK),
            message_label.animate.next_to(llm.get_center() + label_offset + [0, .5, 0]),
            llm.animate.set_fill(RED, opacity=0.8),
            signal.animate.set_fill(box_color),
            run_time=1
        )
        self.wait(0.5)
        
        # Reset colors
        self.play(
            llm.animate.set_fill(box_color),  
            message_star.animate.set_opacity(0),
            llm_decoder.animate.set_fill(box_color),
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