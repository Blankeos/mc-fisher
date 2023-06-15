import pygame
import pygame.freetype
import win32api
import win32con
import win32gui

# 1. Start
pygame.init()

# 2. Get window size and set the pygame window to fullscreen
info = pygame.display.Info()
w = info.current_w
h = info.current_h
screen = pygame.display.set_mode((w, h), pygame.NOFRAME) # For borderless, use pygame.NOFRAME

# 3. Global Variables
focus_message = "Focused"
done = False
transparency_key = (0, 0, 0)  # Transparency color
# fuchsia = (255, 0, 128)  # Transparency color
dark_red = (255, 100, 0)

# 4. Create layered window
hwnd = pygame.display.get_wm_info()["window"]
styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency_key), 0, win32con.LWA_COLORKEY) # set to transparent
# win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
#                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# 6. Draw
font = pygame.freetype.SysFont("Arial", 24)
# text = []
# text.append((font.render_to(screen, "Invisible background", 0, dark_red), (0, 10)))
# text.append((font.render_to(screen, "Press Esc to close the window", 0, dark_red), (0, 100)))
# def show_text():
#     for t in text:
#         screen.blit(t[0], t[1])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.ACTIVEEVENT:
            if hasattr(event, 'gain'):
                if event.gain == 0:
                    focus_message = "- ACTIVE"
                else:
                    focus_message = "- Press ESC to close"

    screen.fill(transparency_key)  # Transparent background
    
    text_str = f"Carlo's Intuitive Fishing Bot {focus_message}"
    screen_rect = screen.get_rect()
    text_rect = font.get_rect(text_str)
    # print(screen.get_rect().bottomleft)
    # text_rect.bottom = screen.get_rect().center
    t = font.render_to(screen, (screen_rect.bottomleft[0] + 20, screen_rect.bottomleft[1] - text_rect.height - 50), text_str, (255,255,255))

    pygame.draw.rect(screen, dark_red, pygame.Rect(30, 30, 60, 60))

    pygame.display.update()


pygame.quit()