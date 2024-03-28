#loop through a list
import pygame as pg

clock= pg.time.Clock()

FPS = 30

frames = ["frame1", "frame2", "frame3", "frame4", "frame5", "frame6"]
# print(len(frames))

frames_length = len(frames)

current_frame = 0

print(current_frame%frames_length)
current_frame += 1
print(current_frame%frames_length)
current_frame += 1
print(current_frame%frames_length)
current_frame += 1
print(current_frame%frames_length)
current_frame += 1


# print(frames[frames_length]-1)

print(0%frames_length)

then = 0

#write a loop that prints each frame in the terminal

while True:
    now = pg.time.get_ticks()
    clock.tick(FPS)
    if now - then > 0.0000000000001:
        print(now)
        then = now
        print(frames[current_frame%frames_length])
        current_frame += 1
        print(FPS+1)
    # print(current_frame)
    if pg.time == 10000:
        pg.quit()
