import math
import random
from enum import Enum, auto

from mesa import Agent


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

    def __init__(self, model, speed=1.0, direction=None, state=Health.SUSCEPTIBLE):
        super().__init__(model)
        self.speed = speed
        if direction is None:
            ang = random.uniform(0.0, 2.0 * math.pi)
            self.vx, self.vy = math.cos(ang), math.sin(ang)
        else:
            self.vx, self.vy = direction
        self.state = state

    def _reflect_on_people(self):
        """Collision proxy using collision_radius; flips velocity if any neighbor is within radius."""
        neighbors = self.model.space.get_neighbors(
            self.pos, self.model.collision_radius, include_center=False
        )
        if any(isinstance(o, Person) for o in neighbors):
            self.vx *= -1.0
            self.vy *= -1.0

    def _maybe_infect(self, pos):
        """Infection attempt for susceptible agents using contact_radius."""
        if self.state == Health.INFECTED:
            return

        neighbors = self.model.space.get_neighbors(
            pos, self.model.contact_radius, include_center=False
        )
        for other in neighbors:
            if isinstance(other, Person) and other.state == Health.INFECTED:
                p = self.model.infection_prob

                if self.state == Health.RECOVERED and self.model.recovered_effect:
                    p *= 1.0 - self.model.recovered_effect
                elif self.state == Health.VACCINATED and self.model.vaccinated_effect:
                    p *= 1.0 - self.model.vaccinated_effect

                if random.random() < p:
                    self.state = Health.INFECTED
                    break

    def _maybe_recover(self):
        """Recover attempt for infected agents"""
        if (
            self.state == Health.INFECTED
            and random.random() < self.model.recover_prob_per_frame
        ):
            self.state = Health.RECOVERED

    def step(self):
        """One tick: move, reflect, update infection state."""
        self._reflect_on_people()
        x, y = self.pos
        nx, ny = x + self.vx * self.speed, y + self.vy * self.speed
        self.model.space.move_agent(self, (nx, ny))
        self._maybe_infect((nx, ny))
        self._maybe_recover()
