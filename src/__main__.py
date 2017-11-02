if __name__ == "__main__":
    import pygame
    import sys

    from src.res import Colors, Meta
    from src.gui import plot_coord

    run = True

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_mode((Meta.WIDTH, Meta.HEIGHT))
    screen = pygame.display.get_surface()

    world = pygame.image.load(Meta.WORLD_MAP)
    worldRect = world.get_rect()

    screen.fill(Colors.BLACK)
    screen.blit(world, worldRect)
    plot_coord(screen, Colors.WHITE, 49.2827, -123.1207)    # Vancouver, Canada
    plot_coord(screen, Colors.WHITE, 31.2304, 121.4737)     # Shanghai, China
    plot_coord(screen, Colors.WHITE, -33.8688, 151.2093)    # Sydney, Australia
    plot_coord(screen, Colors.WHITE, -22.9068, -43.1729)    # Rio de Janeiro, Brazil
    plot_coord(screen, Colors.WHITE, -33.9249, 18.4241)     # Cape Town, South Africa
    plot_coord(screen, Colors.WHITE, 51.5074, -0.1278)      # London, England
    pygame.display.flip()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(1000 / 30)
    else:
        print("Please run, do not import")
