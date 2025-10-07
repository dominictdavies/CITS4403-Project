import pygame
from src.model import InfectionModel

CELL_SIZE = 20
FPS = 5


def draw_model(screen: pygame.Surface, model: InfectionModel):
    screen.fill((0, 0, 0))

    for agent in model.agents:
        # Each agent has a .pos attribute: (x, y) in model.space coordinates
        x, y = agent.pos  # type: ignore

        # Convert to pixel coordinates
        px = int(x * CELL_SIZE)
        py = int(y * CELL_SIZE)

        # You can color agents by type or state if desired
        color = (0, 255, 0)  # green as a placeholder
        pygame.draw.circle(screen, color, (px, py), 5)


def run_simulation(model: InfectionModel):
    pygame.init()

    screen = pygame.display.set_mode(
        (model.width * CELL_SIZE, model.height * CELL_SIZE)
    )
    clock = pygame.time.Clock()

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
