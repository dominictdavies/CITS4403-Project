from enum import Enum, auto
import math
import random
from mesa import Agent


class Health(Enum):
    """Health state for a person agent."""
    SUSCEPTIBLE = auto()
    INFECTED = auto()
    RECOVERED = auto()   # reserved for future use
    VACCINATED = auto()  # reserved for future use


class Person(Agent):
    """
    Moving point in continuous 2D space.
    - Constant speed and straight-line motion.
    - Specular reflection on edges.
    - Simple velocity flip on close contact with any person (collision proxy).
    - Infection attempt when near an infected neighbor.
    """

    def __init__(self, unique_id, model, speed=1.2, direction=None,
                 state=Health.SUSCEPTIBLE):
        super().__init__(unique_id, model)
        self.speed = speed

        # Unit velocity vector
        if direction is None:
            ang = random.uniform(0.0, 2.0 * math.pi)
            self.vx, self.vy = math.cos(ang), math.sin(ang)
        else:
            self.vx, self.vy = direction

        self.state = state

    # --- motion & collisions -------------------------------------------------

    def _reflect_on_edge(self, x, y):
        """Reflect on box boundaries and clamp position within [0, W]x[0, H]."""
        xmin, ymin, xmax, ymax = 0.0, 0.0, self.model.width, self.model.height

        if x < xmin or x > xmax:
            self.vx *= -1.0
            x = min(max(x, xmin), xmax)

        if y < ymin or y > ymax:
            self.vy *= -1.0
            y = min(max(y, ymin), ymax)

        return x, y

    def _reflect_on_people(self, pos):
        """
        Naive person–person collision: if any neighbor is within collision radius,
        flip velocity vector (prevents long overlaps and creates 'bounce' effect).
        """
        neighbors = self.model.space.get_neighbors(
            pos, self.model.collision_radius, include_center=False
        )
        if any(isinstance(o, Person) for o in neighbors):
            self.vx *= -1.0
            self.vy *= -1.0

    # --- infection -----------------------------------------------------------

    def _maybe_infect(self, pos):
        """
        Try to infect a susceptible agent if an infected neighbor is nearby.
        Vaccination effectiveness (if used later) scales infection probability.
        """
        if self.state != Health.SUSCEPTIBLE:
            return

        neighbors = self.model.space.get_neighbors(
            pos, self.model.collision_radius, include_center=False
        )
        for other in neighbors:
            if isinstance(other, Person) and other.state == Health.INFECTED:
                p = self.model.infection_prob
                if self.state == Health.VACCINATED and self.model.vaccinated_effect:
                    p *= (1.0 - self.model.vaccinated_effect)
                if random.random() < p:
                    self.state = Health.INFECTED
                    break

    # --- Mesa step -----------------------------------------------------------

    def step(self):
        """Move, handle reflections, and perform infection attempt."""
        x, y = self.model.space.get_position(self)

        # Straight-line motion
        nx, ny = x + self.vx * self.speed, y + self.vy * self.speed

        # Reflect on edges and on close contact with people
        nx, ny = self._reflect_on_edge(nx, ny)
        self._reflect_on_people((nx, ny))

        # Commit new position
        self.model.space.move_agent(self, (nx, ny))

        # Infection check
        self._maybe_infect((nx, ny))
