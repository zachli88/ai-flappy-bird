import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(30)

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def generate_pipes():
    config.pipes.append(components.Pipe(config.win_width))

def draw_generation(generation):
    font = pygame.font.Font(None, 36)
    generation_text = font.render(f"Generation: {generation}", True, (255, 255, 255))
    config.window.blit(generation_text, (10, 10))

def main():
    pipes_spawn_time = 0
    generation = 1
    while True:
        quit_game()

        config.window.fill((0, 0, 0))

        # Display generation
        draw_generation(generation)

        # Spawn ground
        config.ground.draw(config.window)

        # Spawn pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)
        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            population.natural_selection()
            generation += 1

        clock.tick(60)
        pygame.display.flip()

main()