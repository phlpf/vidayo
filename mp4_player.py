import pygame
from pygame.constants import * 
import scene
from os import listdir
import os.path

main_scene = None
clock = pygame.time.Clock()

def player_func(sc, screen, objects, frames, events):
    global main_scene, clock
    if player_func.is_first == True:
        height = screen.get_height()-(screen.get_height()/5)
        normal_height = (screen.get_height()/30)*2
        sc.add_obj(normal_height, height, screen.get_width()/5, screen.get_height()/5, (255, 0, 0), "back")
        print("adssad")
        player_func.is_first = False
    frame_array = sc.frames[player_func.frame]
    clock.tick(sc.framerate)
    surf = pygame.surfarray.make_surface(frame_array)
    surf = sc.adjust_frame(surf)
    player_func.frame+=1
    screen.blit(surf, (0, 0))
    if sc.objects[0].check_hit(screen, events):
        print("hit")
        main_scene = menu

def menu_func(sc, screen, objects, frames, events):
    global main_scene
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
            player_func.is_first = True
            player_func.frame = 0
            new_scene = scene.Scene(screen, player_func, sc.font)
            new_scene.load_video(filename)
            main_scene = new_scene
                    
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
