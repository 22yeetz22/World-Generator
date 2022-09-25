# TODO: TRY TO MAKE A HEATMAP SO YOU CAN ADD BIOMES LIKE MINECRAFT

import pygame
from perlin_noise import PerlinNoise

WIDTH = 600

raw_seed = input("Enter a seed: ")
if raw_seed.isdigit(): seed = abs(int(raw_seed))
else: seed = sum([ord(char) for char in raw_seed])

noise1 = PerlinNoise(octaves=3, seed=seed)
noise2 = PerlinNoise(octaves=8, seed=seed)
heatmap = PerlinNoise(octaves=0.7, seed=seed)

NOISE_CHANGE = 60
tile_size = 25
TILE_ITERS = round(WIDTH / tile_size)
ZOOM_CHANGE = 2

SEA_LEVEL = -0.25
MOUNTAIN_LEVEL = 0.25
SNOW_LEVEL = 0.4

DESERT_LEVEL = 0.15


pygame.init()
window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Terrain Generator")

MOVE_DIST = 0.3
position = pygame.Vector2()
velocity = pygame.Vector2()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and tile_size >= 27: tile_size -= 2  # Zoom out
    if keys[pygame.K_e] and tile_size <= 49: tile_size += 2  # Zoom in

    if keys[pygame.K_UP] or keys[pygame.K_w]: velocity.y -= MOVE_DIST
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: velocity.y += MOVE_DIST
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: velocity.x -= MOVE_DIST
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: velocity.x += MOVE_DIST
    velocity *= 0.8

    if keys[pygame.K_SPACE]: position += pygame.Vector2(round(velocity.x), round(velocity.y)) * 2
    else: position += pygame.Vector2(round(velocity.x), round(velocity.y))

    # Include scroll
    for x in range(TILE_ITERS + 1):
        for y in range(TILE_ITERS + 1):
            currpos = [(x + position.x) / NOISE_CHANGE, (y + position.y) / NOISE_CHANGE]
            n1 = noise1(currpos)
            n2 = noise2(currpos)
            h = heatmap(currpos)
            n = (n1 + n2 + h * 0.7) * 0.6  # Also a bit of heatmap for more detail

            tile = [x * tile_size, y * tile_size, tile_size, tile_size]

            if n < SEA_LEVEL:
                diff = SEA_LEVEL - n
                pygame.draw.rect(window, (30, 152 - round(diff * 250), 255 - round(diff * 200)), tile)
            elif MOUNTAIN_LEVEL < n < SNOW_LEVEL:
                diff = SNOW_LEVEL - n
                pygame.draw.rect(window, (140 - round(diff * 210), 90, 80), tile)
            elif SNOW_LEVEL < n:
                diff = 1 - n + h
                change = round(diff * 60)
                pygame.draw.rect(window, (255 - change, 250 - change, 250 - change), tile)
            else:
                # Heatmap
                if h > DESERT_LEVEL:
                    # Desert
                    diff = 0.8 - h + n
                    change = round(diff * 90)
                    pygame.draw.rect(window, (255 - change, 220 - change, 170 - change), tile)
                else:
                    # Grass
                    diff = MOUNTAIN_LEVEL - n
                    pygame.draw.rect(window, (62, 220 - round(diff * 110), 59), tile)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
