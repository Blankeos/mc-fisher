import pystray
from screeninfo import get_monitors

import tkinter as tk

root = tk.Tk()
root.overrideredirect(True) # Makes the window handles not visible (x, -, [])

# Set the size of my window to whatever I like
WIN_WIDTH = 500
WIN_HEIGHT = 500

root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{(get_monitors()[0].width - WIN_WIDTH)//2}+{(get_monitors()[0].height - WIN_HEIGHT)//2}")

# root.attributes('-transparentcolor', 'white', '-topmost', 1)
# root.config(bg='white')

# canvas = tk.Canvas(root, width=WIN_WIDTH, height=WIN_HEIGHT, bg='white')

root.lift()
root.wm_attributes("-topmost", True)
# root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")


canvas = tk.Canvas(root, bg='white', height=500, width=500, takefocus=0)
canvas.pack()

canvas.create_line(250, 0, 250, 500, fill='red', width=2)
canvas.create_line(0, 250, 500, 250, fill='red', width=2)

root.unbind_all('<<NextWindow>>')
root.mainloop()