# Manim Animations

This is a repo for my manim animations.

## Installation 

This repo uses `uv` in order to manage dependencies.

```
$ uv sync
$ uv run manim  --resolution "1280,720" src/manim-communication.py CommunicationModel
```

To generate gifs:

```
$ uv run manim -r 320,240 --format=gif src/manim-communication.py CommunicationModel
```

Media files will be output into the `media/` directory.

**NOTE**

There is a bug in ManimML, and you need to change the Manim library in `manim/animation/composition.py`:


```
class AnimationGroup(Animation):
    """
    ... a lot here.. keep it the same. the line we need to change is commented below, change the None to 5.0!
    """

    def __init__(
        self,
        *animations: Animation | Iterable[Animation] | types.GeneratorType[Animation],
        group: Group | VGroup | OpenGLGroup | OpenGLVGroup = None,
        run_time: float | None = 5.0, # this is the line we need to change!
        rate_func: Callable[[float], float] = linear,
        lag_ratio: float = 0,
        **kwargs,
    ) -> None:
```
### Radar Score

[![Radar Chart](./assets/radar-chart.gif)](./src/radar-chart.py)


### Communication Animation

[![Communication Animation](./assets/communication.gif)](./src/manim-communication.py)

### Media Choice

[![Media Decision](./assets/media-decision.gif)](./src/media-decision.py)


## Mind Filter 

[![Mind Filter](./assets/filter.gif)](./src/filter.py)

## Programmer Context

[![Programmer Context](./assets/programmer-loading.gif)](./src/programmer-loading.py)

## Prompt Feedback Loop

[![Curly Loop](./assets/curly.gif)](./src/curly.py)

## Prompt Feedback Loop w/ Model Context Protocol

[![Curly Loop w/ MCP](./assets/curly-mcp.gif)](./src/curly-mcp.py)

## Shrinking Token Window

[![Token Window](./assets/tokenwindow.gif)](./src/tokenwindow.py)