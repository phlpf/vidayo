import pygame
from pygame.constants import * 
import scene
from os import listdir
import os.path

def player_func(sc, screen, objects, frames, events):
    if menu_func.is_first == True:
        height = screen.get_height()-(screen.get_height()/5)
        normal_height = (screen.get_height()/30)*2
        sc.add_obj(normal_height, height, screen.get_width()/5, screen.get_height()/5, (255, 0, 0), "back")
        menu_func.is_first = False
    
    
player_func.frame = 0
player_func.is_first = True

def menu_func(sc, screen, objects, frames, events):
    if menu_func.is_first == True:
        normal_height = (screen.get_height()/30)*2
        sc.add_obj(normal_height, normal_height+5, screen.get_width()/5, normal_height, (255, 0, 0), "hello!")
        sc.add_obj(0, (normal_height+5)*2, screen.get_width(), normal_height, (0, 0, 255), "Available Videos:")
        onlyfiles = [f for f in listdir(".") if os.path.isfile(f)]
        menu_func.video_start = len(sc.objects)
        for f in onlyfiles:
            if f[-4:] == ".mp4":
                sc.add_obj(normal_height, (normal_height+5)*(len(sc.objects)+1), len(f)*30, normal_height, (0, 255, 0), f)
        menu_func.is_first = False
    for i in range(menu_func.video_start, len(sc.objects)):
        if sc.objects[i].check_hit(screen, events):
            filename = sc.objects[i].caption
            new_scene = scene.Scene(screen, player_func, sc.font)
            new_scene.load_video(filename)
            sc = new_scene
            
menu_func.video_start = 0
menu_func.is_first = True

pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Ubuntu Mono', 40)

screen = pygame.display.set_mode([1500, 900])

menu = scene.Scene(screen, menu_func, myfont)

main_scene = menu

i = 0

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            running = False
    main_scene.main_loop(events)
    i+=1;
    pygame.display.flip()

pygame.quit()