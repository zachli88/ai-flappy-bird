import pygame
import random
import config
import brain

class Player:
    def __init__(self):
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_network()
        self.fitness = 0
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    
    def sky_collision(self):
        return bool(self.rect.y < 30)
    
    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.bottom_rect) or pygame.Rect.colliderect(self.rect, p.top_rect)
        
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            self.vel += 0.25
            if self.vel > 5:
                self.vel = 5
            self.rect.y += self.vel
            self.fitness += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not (self.flap or self.sky_collision()):
            self.flap = True
            self.vel = -5
        if self.vel >= 2:
            self.flap = False

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    @staticmethod
    def closest_pipe():
        for pipe in config.pipes:
            if not pipe.passed:
                return pipe
    
    def look(self):
        if config.pipes:
            pipe = self.closest_pipe()
            # Top pipe
            self.vision[0] = (self.rect.center[1] - pipe.top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center, (pipe.x, pipe.top_rect.bottom))
            # Mid pipe
            self.vision[1] = (pipe.x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center, (pipe.x, self.rect.center[1]))
            # Bottom pipe
            self.vision[2] = (pipe.bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center, (pipe.x, pipe.bottom_rect.top))

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_network()
        return clone