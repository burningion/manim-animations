
uv run manim -r 800,600 --format=gif src/manim-communication.py CommunicationModel
cp media/videos/manim-communication/600p60/CommunicationModel_ManimCE_v0.18.1.gif ./assets/communication.gif
uv run manim  --resolution "1280,720" src/manim-communication.py CommunicationModel
uv run manim -r 800,600 --format=gif src/media-decision.py DecisionTreeAnimation
cp media/videos/media-decision/600p60/DecisionTreeAnimation_ManimCE_v0.18.1.gif ./assets/media-decision.gif
uv run manim  --resolution "1280,720" src/media-decision.py DecisionTreeAnimation
