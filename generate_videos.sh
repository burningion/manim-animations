
RENDERING_MODE=True uv run manim -r 320,200 --format=gif src/manim-communication.py CommunicationModel
cp media/videos/manim-communication/200p60/CommunicationModel_ManimCE_v0.18.1.gif ./assets/communication.gif
RENDERING_MODE=True uv run manim  --resolution "1280,720" src/manim-communication.py CommunicationModel
RENDERING_MODE=True uv run manim -r 320,200 --format=gif src/media-decision.py DecisionTreeAnimation
cp media/videos/media-decision/200p60/DecisionTreeAnimation_ManimCE_v0.18.1.gif ./assets/media-decision.gif
RENDERING_MODE=True uv run manim  --resolution "1280,720" src/media-decision.py DecisionTreeAnimation
RENDERING_MODE=True uv run manim -r 320,200 --format=gif src/radar-chart.py MultipleRadarCharts
cp media/videos/radar-chart/200p60/MultipleRadarCharts_ManimCE_v0.18.1.gif ./assets/radar-chart.gif
RENDERING_MODE=True uv run manim  --resolution "1280,720" src/radar-chart.py MultipleRadarCharts
RENDERING_MODE=True uv run manim -r 320,200 --format=gif src/curly.py CurlyBraceTransformation
cp media/videos/curly/200p60/CurlyBraceTransformation_ManimCE_v0.18.1.gif ./assets/curly.gif
RENDERING_MODE=True uv run manim  --resolution "1280,720" src/curly.py CurlyBraceTransformation
RENDERING_MODE=True uv run manim -r 320,200 --format=gif src/filter.py FilterAnimation
cp media/videos/filter/200p60/FilterAnimation_ManimCE_v0.18.1.gif ./assets/filter.gif
RENDERING_MODE=True uv run manim  --resolution "1280,720" src/filter.py FilterAnimation
