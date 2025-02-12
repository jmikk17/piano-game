import pygame
from cfg import std_cfg
from assets import GameAssets
from music_engine import MusicPlayer
import auxil
import test

# Array for currently pressed notes
# Maybe move this?
play_state = {key: False for key in auxil.keys}

class Game:
    def __init__(self,data,layout):
        self.assets = GameAssets()
        self.assets.load()
        self.layout = layout

        # MOVE TO CFG?
        # TODO standardize this with layout class for scaling of screen size
        self.lines = 5
        self.line_thick = 2
        self.line_gap = 20
        self.line_lower = 200
        self.line_left = 240
        self.line_right = 1280

        self.play_box = (350,100,50,130) 
        self.play_width = self.play_box[2]/2
        self.play_center = self.play_box[0] + self.play_width

        self.play_b_delay = ((1200 - self.play_center) / std_cfg.NOTE_VELOCITY) 
        # 1200 = where we spawn notes
        # self.play_center = where we register hit
        # -5 = adjustment for center of note ish

        # TODO test screen scaling with music timing etc.
        self.musicplayer = MusicPlayer(data,self.assets,self.play_center,self.play_width, self.play_b_delay)

        # sprite test!
        self.trumpet_time = 0
        self.current_trumpet = 0

    def draw(self,screen):
        if self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(auxil.WHITE)

        for i in range(self.lines):
            pygame.draw.line(screen, auxil.BLACK, 
                             (self.line_left, self.line_lower-i*self.line_gap), (self.line_right, self.line_lower-i*self.line_gap),self.line_thick)
        screen.blit(self.assets.note_pictures["g"], (200, 74))
        self.play_box = pygame.draw.rect(screen,(0,255,0),self.play_box) # x,y,width,height

        self.musicplayer.draw(screen)

        # TODO function to print score here

        # sprite test!
        screen.blit(self.assets.trumpet[self.current_trumpet], (500, 500))


    def update(self,dt):
        key_state = auxil.check_keyboard()
        status = self.musicplayer.update(dt,key_state)
        #auxil.handle_quit() # this is not optimal, should be handled when we loop over events anyways

        # sprite test!
        self.trumpet_time += dt
        if self.trumpet_time >= 0.1:
            self.trumpet_time = 0
            self.current_trumpet = (self.current_trumpet + 1) % len(self.assets.trumpet)

        return status

    def update_manager_ui(self, layout):
        # TODO
        print("Game ui update")
