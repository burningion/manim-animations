from manim import *

class FormulaInBox:  # Remove Scene inheritance since we're just using it as a factory
    def create_formula(self):  # Rename construct to create_formula
        # Create the formula
        formula = MathTex(
            r"\text{Probability of Choice} = \frac{\text{Possible Rewards}}{\text{Required Effort}}",
            color=BLACK
        ).scale(0.8)
        
        # Create a box around the formula
        box = SurroundingRectangle(
            formula,
            buff=0.5,
            corner_radius=0.2,
            color=BLUE
        )
        
        # Group the formula and box together
        formula_group = VGroup(formula, box)
        
        return formula_group

# Your main scene
class MainScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Create the formula using the helper class
        formula_maker = FormulaInBox()
        formula_group = formula_maker.create_formula()
        
        # Position the formula
        formula_group.scale(0.7)  # Make it a bit smaller
        formula_group.to_corner(UR)  # Move to upper right
        
        # Your existing animations...
        # For example, create a star like in the previous scene
        star = RegularPolygram(num_vertices=5, radius=2, density=2, color=YELLOW)
        star.shift(LEFT * 2)  # Move star to the left side
        
        # Animation sequence
        # 1. Show the formula first
        self.play(Write(formula_group), run_time=2)
        
        # 2. Then animate the star
        self.play(Create(star), run_time=1.5)
        
        # 3. Animate them together
        self.play(
            Rotate(star, angle=TAU, rate_func=smooth),
            formula_group.animate.scale(1.1).set_color(YELLOW),
            run_time=2
        )
        
        # 4. Return formula to original state
        self.play(
            formula_group.animate.scale(1/1.1).set_color(BLUE)
        )
        
        # Hold the final frame
        self.wait(1)

if __name__ == "__main__":
    scene = MainScene()
    scene.render()