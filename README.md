# Manim Animations

This is a repo for my manim animations.

This repo uses `uv` in order to manage dependencies.

```
$ uv sync
$ uv run manim  --resolution "1280,720" manim-communication.py CommunicationModel
```

To generate gifs:

```
$ uv run manim -r 640,480 --format=gif manim-communication.py CommunicationModel
```

Media files will be output into the `media/` directory.

![Communication Animation](./assets/communication.gif)