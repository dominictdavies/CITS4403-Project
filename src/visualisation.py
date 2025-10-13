"""Pygame-based visualisation for the InfectionModel simulation."""

# pylint: disable=no-member

import pygame

from src.agents import Health, Person
from src.model import InfectionModel


def draw_model(screen: pygame.Surface, model: InfectionModel, scale: int) -> None:
    """
    Render all agents in the InfectionModel onto the Pygame screen.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        model (InfectionModel): The simulation model containing agents and state.
        scale (int): Scaling factor to convert model coordinates to pixels.
    """

    screen.fill((0, 0, 0))

    for agent in model.agents:
        if not isinstance(agent, Person):
            continue

        # Convert agent position to pixel coordinates
        x, y = agent.pos  # type: ignore
        px = int(x * scale)
        py = int(y * scale)

        # Colour agents by health state
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


def is_simulation_running() -> bool:
    """
    Handle Pygame events and determine whether the simulation should continue.

    Returns:
        bool: True if the simulation should continue running, False if the
        user has requested to quit.
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def run_simulation(model: InfectionModel, fps: int = 30, scale: int = 1) -> None:
    """
    Run the InfectionModel simulation using a Pygame visualization loop.

    Args:
        model (InfectionModel): The simulation model to visualize and step.
        fps (int, optional): Target frames per second for the update loop.
            Defaults to 30.
        scale (int, optional): Scaling factor to convert model coordinates to
            pixels. Defaults to 1.
    """

    pygame.init()

    screen = pygame.display.set_mode((model.width * scale, model.height * scale))
    clock = pygame.time.Clock()

    while is_simulation_running():
        model.step()
        draw_model(screen, model, scale)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
