import pygame
from src.model import InfectionModel
from src.agents import Person, Health


def draw_model(screen: pygame.Surface, model: InfectionModel, scale: int):
    screen.fill((0, 0, 0))

    for agent in model.agents:
        if not isinstance(agent, Person):
            continue

        # Each agent has a .pos attribute: (x, y) in model.space coordinates
        x, y = agent.pos  # type: ignore

        # Convert to pixel coordinates
        px = int(x * scale)
        py = int(y * scale)

        # You can color agents by type or state if desired
        if agent.state == Health.SUSCEPTIBLE:
            color = (255, 255, 0)
        elif agent.state == Health.INFECTED:
            color = (255, 0, 0)
        elif agent.state == Health.RECOVERED:
            color = (128, 128, 128)
        elif agent.state == Health.VACCINATED:
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)

        pygame.draw.circle(screen, color, (px, py), 5)


def run_simulation(model: InfectionModel, fps: int = 5, scale: int = 20):
    pygame.init()

    screen = pygame.display.set_mode((model.width * scale, model.height * scale))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        model.step()
        draw_model(screen, model, scale)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
