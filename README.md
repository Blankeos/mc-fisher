# 🎣 McFisher

A computer vision-based **auto-fishing bot for Minecraft**. This is more of a learning project rather than for cheating. As this is a computer vision-based bot, this does not install any invasive mods into your Minecraft client, it rather acts like an actual person simulating the same inputs you make from seeing what happens in the game. Not promoting cheating in public servers, I personally use this in our private SMP server.

I used OpenCV + PyAutoGUI

I tried out several prototypes of drawing on top the screen with click-through. Pygame works the best (see examples/pgame.py). Eventually settled for OpenCV just for ease of implementation.

### Get Started

1. Make sure you have MINECRAFT opened already!
1. Open the application
1. Put the application aside, put your window's focus on Minecraft.
1. Align the greenbox on the **Fishing Bob**
1. Press **[Left Ctrl]** to get started, tracking will then start.

### How to Quit

1. Focus on the application window (Not Minecraft)
2. Press **[Q]**

### How to Restart

1. You can press and hold **[Left Ctrl]** anytime you want to reset the tracking

---

> Notes on bundling the application:
>
> ```
> pyinstaller --onefile --noconsole --icon=mcfisher.ico main.py
> ```
