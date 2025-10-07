import pygame
from src.model import InfectionModel

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
FPS = 10


def draw_model(screen, model):
    screen.fill((0, 0, 0))

    for agent in model.agents:
        # Each agent has a .pos attribute: (x, y) in model.space coordinates
        x, y = agent.pos

        # Convert to pixel coordinates
        px = int(x * CELL_SIZE)
        py = int(y * CELL_SIZE)

        # You can color agents by type or state if desired
        color = (0, 255, 0)  # green as a placeholder
        pygame.draw.circle(screen, color, (px, py), 5)


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
