import pygame
from src.model import InfectionModel

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
FPS = 10


def draw_model(screen, model):
    screen.fill((0, 0, 0))
    for (x, y), cell in model.grid.coord_iter():
        agents = cell[0]
        color = (0, 255, 0) if agents else (30, 30, 30)
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)


def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    clock = pygame.time.Clock()
    model = InfectionModel(
        N=80,
        width=50,
        height=50,
        speed=3.0,
        collision_radius=1.0,  # bounce only (small)
        contact_radius=6.0,  # infection proximity (large)
        infection_prob=0.5,
        initial_infected=2,
        seed=42,
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        model.step()
        draw_model(screen, model)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run_simulation()
