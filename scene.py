import pygame
import imageio
import cv2




class Object:
    def __init__(self, x, y, w, h, color, caption):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.caption = caption
    def check_hit(self, screen, events):
        mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONUP:
                if mx > self.x and mx < self.x + self.w:
                    if my > self.y and my < self.y + self.h:
                        return True
        return False
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))
        text = font.render(self.caption, True, (0, 0, 0))
        dx = (self.w - text.get_width())/2
        dy = (self.h - text.get_height())/2
        screen.blit(text, (self.x + dx, self.y + dy))

class Scene:
    def __init__(self, screen, cb, font):
        self.screen = screen
        self.cb = cb
        self.font = font
        self.objects = []
        self.frames = []
        self.framerate = 0
    def add_obj(self, x, y, w, h, color, caption):
        self.objects.append(Object(x, y, w, h, color, caption))
    def load_video(self, filename):        
        images = imageio.get_reader(filename)
        self.frames = [im for frame_num, im in enumerate(images)]
        cap=cv2.VideoCapture(filename)
        self.framerate = cap.get(cv2.CAP_PROP_FPS)
    def adjust_frame(self, surf):
        surf = pygame.transform.rotate(surf, 270)
        surf = pygame.transform.flip(surf, True, False)
        return surf
    def draw_objs(self):
        for obj in self.objects:
            obj.draw(self.screen, self.font)
    def main_loop(self, events):
        self.screen.fill((0,0,0))    
        self.cb(self, self.screen, self.objects, self.frames, events)
        self.draw_objs();
