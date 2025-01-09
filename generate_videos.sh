
uv run manim -r 320,200 --format=gif src/manim-communication.py CommunicationModel
cp media/videos/manim-communication/200p60/CommunicationModel_ManimCE_v0.18.1.gif ./assets/communication.gif
uv run manim  --resolution "1280,720" src/manim-communication.py CommunicationModel
uv run manim -r 320,200 --format=gif src/media-decision.py DecisionTreeAnimation
cp media/videos/media-decision/200p60/DecisionTreeAnimation_ManimCE_v0.18.1.gif ./assets/media-decision.gif
uv run manim  --resolution "1280,720" src/media-decision.py DecisionTreeAnimation
uv run manim -r 320,200 --format=gif src/radar-chart.py MultipleRadarCharts
cp media/videos/radar-chart/200p60/MultipleRadarCharts_ManimCE_v0.18.1.gif ./assets/radar-chart.gif
uv run manim  --resolution "1280,720" src/radar-chart.py MultipleRadarCharts
