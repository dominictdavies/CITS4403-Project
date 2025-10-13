import math
import random
from enum import Enum, auto
from typing import TYPE_CHECKING, cast

from mesa import Agent
from mesa.space import FloatCoordinate

if TYPE_CHECKING:
    from model import InfectionModel


class Health(Enum):
    """Finite states of an agent."""

    SUSCEPTIBLE = auto()
    INFECTED = auto()
    RECOVERED = auto()
    VACCINATED = auto()


class Person(Agent):
    """
    Moving point in continuous 2D space.
    - Constant-speed straight-line motion.
    - Specular reflection at boundaries.
    - Velocity flip on proximity-based collision.
    - Infection attempt on proximity to infected neighbors.
    """

    def __init__(self, model, speed=3.0, direction=None, state=Health.SUSCEPTIBLE):
        super().__init__(model)

        self.world_config = self.infection_model.config.world
        self.disease_config = self.infection_model.config.disease
        self.population_config = self.infection_model.config.population

        self.speed = speed
        if direction is None:
            ang = random.uniform(0.0, 2.0 * math.pi)
            self.vx, self.vy = math.cos(ang), math.sin(ang)
        else:
            self.vx, self.vy = direction
        self.state = state

    @property
    def infection_model(self) -> "InfectionModel":
        return cast("InfectionModel", self.model)

    @property
    def float_pos(self) -> "FloatCoordinate":
        return cast("FloatCoordinate", self.pos)

    def _reflect_on_people(self):
        """Collision proxy using collision_radius; flips velocity if any neighbor is within radius."""
        neighbors = self.infection_model.space.get_neighbors(
            self.float_pos, self.world_config.collision_radius, include_center=False
        )
        if any(isinstance(o, Person) for o in neighbors):
            self.vx *= -1.0
            self.vy *= -1.0

    def _maybe_infect(self, pos):
        """Infection attempt for susceptible agents using contact_radius."""
        if self.state == Health.INFECTED:
            return

        neighbors = self.infection_model.space.get_neighbors(
            pos, self.disease_config.contact_radius, include_center=False
        )
        for other in neighbors:
            if isinstance(other, Person) and other.state == Health.INFECTED:
                p = self.disease_config.frame_infection_prob

                if (
                    self.state == Health.RECOVERED
                    and self.population_config.recovered_effect
                ):
                    p *= 1.0 - self.population_config.recovered_effect
                elif (
                    self.state == Health.VACCINATED
                    and self.population_config.vaccinated_effect
                ):
                    p *= 1.0 - self.population_config.vaccinated_effect

                if random.random() < p:
                    self.state = Health.INFECTED
                    break

    def _maybe_recover(self):
        """Recover attempt for infected agents"""

        if (
            self.state == Health.INFECTED
            and random.random() < self.disease_config.frame_recover_prob
        ):
            self.state = Health.RECOVERED

    def step(self):
        """One tick: move, reflect, update infection state."""
        self._reflect_on_people()
        x, y = tuple(self.float_pos)
        nx, ny = x + self.vx * self.speed, y + self.vy * self.speed
        self.infection_model.space.move_agent(self, (nx, ny))
        self._maybe_infect((nx, ny))
        self._maybe_recover()
