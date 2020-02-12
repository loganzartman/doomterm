from termpixels import Color
from termpixels.app import LegacyApp
from random import randint

# http://fabiensanglard.net/doom_fire_psx/

TITLE = u"""
   ▄▄▄▄▀ ▄███▄   █▄▄▄▄ █▀▄▀█ █ ▄▄  ▄█     ▄  ▄███▄   █      ▄▄▄▄▄   
▀▀▀ █    █▀   ▀  █  ▄▀ █ █ █ █   █ ██ ▀▄   █ █▀   ▀  █     █     ▀▄ 
    █    ██▄▄    █▀▀▌  █ ▄ █ █▀▀▀  ██   █ ▀  ██▄▄    █   ▄  ▀▀▀▀▄   
   █     █▄   ▄▀ █  █  █   █ █     ▐█  ▄ █   █▄   ▄▀ ███▄ ▀▄▄▄▄▀    
  ▀      ▀███▀     █      █   █     ▐ █   ▀▄ ▀███▀       ▀          
                  ▀      ▀     ▀       ▀                            
"""
TITLE_W = max(len(l) for l in TITLE.splitlines())

COLOR_MAP = [Color(i[0], i[1], i[2]) for i in [
    (0x07,0x07,0x07), (0x1F,0x07,0x07), (0x2F,0x0F,0x07), (0x47,0x0F,0x07),
    (0x57,0x17,0x07), (0x67,0x1F,0x07), (0x77,0x1F,0x07), (0x8F,0x27,0x07),
    (0x9F,0x2F,0x07), (0xAF,0x3F,0x07), (0xBF,0x47,0x07), (0xC7,0x47,0x07),
    (0xDF,0x4F,0x07), (0xDF,0x57,0x07), (0xDF,0x57,0x07), (0xD7,0x5F,0x07),
    (0xD7,0x5F,0x07), (0xD7,0x67,0x0F), (0xCF,0x6F,0x0F), (0xCF,0x77,0x0F),
    (0xCF,0x7F,0x0F), (0xCF,0x87,0x17), (0xC7,0x87,0x17), (0xC7,0x8F,0x17),
    (0xC7,0x97,0x1F), (0xBF,0x9F,0x1F), (0xBF,0x9F,0x1F), (0xBF,0xA7,0x27),
    (0xBF,0xA7,0x27), (0xBF,0xAF,0x2F), (0xB7,0xAF,0x2F), (0xB7,0xB7,0x2F),
    (0xB7,0xB7,0x37), (0xCF,0xCF,0x6F), (0xDF,0xDF,0x9F), (0xEF,0xEF,0xC7),
    (0xFF,0xFF,0xFF)]]

class DoomTerm(LegacyApp):
    def __init__(self):
        super().__init__(framerate=24)

    def on_start(self):
        self.need_resize = True

    def on_resize(self):
        self.need_resize = True

    def do_resize(self):
        self.heightmap = [0 for _ in range(self.screen.w*self.screen.h*2)]
        y = self.screen.h*2 - 1
        for x in range(self.screen.w):
            self.heightmap[y*self.screen.w + x] = len(COLOR_MAP)
        self.need_resize = False

    def propagate(self, i):
        v = self.heightmap[i]
        if v == 0:
            self.heightmap[i - self.screen.w] = 0
        else:
            rand_i = randint(0, 3)
            dst = i - rand_i + 1
            self.heightmap[dst - self.screen.w] = max(0, v - (rand_i & 3))

    def on_frame(self):
        if self.need_resize:
            self.do_resize()
        for x in range(self.screen.w):
            for y in range(1, self.screen.h*2):
                i = y*self.screen.w + x
                self.propagate(i)
        
        self.screen.clear()
        self.screen.print(TITLE, self.screen.w // 2 - TITLE_W // 2, 2, fg=Color.rgb(1,1,1), bg=Color.rgb(0,0,0))
        for x in range(self.screen.w):
            for y in range(0, self.screen.h):
                i = y*2*self.screen.w + x
                top = min(36, self.heightmap[i])
                bot = min(36, self.heightmap[i+self.screen.w])
                if top > 0 or bot > 0:
                    self.screen.print("▄", x, y, bg=COLOR_MAP[top], fg=COLOR_MAP[bot])
        self.screen.update()

if __name__ == "__main__":
    DoomTerm().run()

