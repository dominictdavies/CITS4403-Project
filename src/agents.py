from enum import Enum, auto
import math
import random
from mesa import Agent


class Health(Enum):
    """Finite states of an agent."""
    SUSCEPTIBLE = auto()
    INFECTED = auto()
    RECOVERED = auto()   # reserved
    VACCINATED = auto()  # reserved


class Person(Agent):
    """
    Moving point in continuous 2D space.
    - Constant-speed straight-line motion.
    - Specular reflection at boundaries.
    - Velocity flip on proximity-based collision.
    - Infection attempt on proximity to infected neighbors.
    """

    def __init__(self, model, speed=1.2, direction=None,
                 state=Health.SUSCEPTIBLE):
        super().__init__(model)
        self.speed = speed
        if direction is None:
            ang = random.uniform(0.0, 2.0 * math.pi)
            self.vx, self.vy = math.cos(ang), math.sin(ang)
        else:
            self.vx, self.vy = direction
        self.state = state

    # --- motion & collisions -------------------------------------------------
    def _reflect_on_edge(self, x, y):
        """Boundary reflection with strict in-bounds clamping."""
        xmin, ymin, xmax, ymax = 0.0, 0.0, self.model.width, self.model.height
        if x < xmin or x > xmax:
            self.vx *= -1.0
            x = min(max(x, xmin + 1e-6), xmax - 1e-6)
        if y < ymin or y > ymax:
            self.vy *= -1.0
            y = min(max(y, ymin + 1e-6), ymax - 1e-6)
        return x, y

    def _reflect_on_people(self, pos):
        """Collision proxy using collision_radius; flips velocity if any neighbor is within radius."""
        neighbors = self.model.space.get_neighbors(
            pos, self.model.collision_radius, include_center=False
        )
        if any(isinstance(o, Person) for o in neighbors):
            self.vx *= -1.0
            self.vy *= -1.0

    # --- infection -----------------------------------------------------------
    def _maybe_infect(self, pos):
        """Infection attempt for susceptible agents using contact_radius."""
        if self.state != Health.SUSCEPTIBLE:
            return
        neighbors = self.model.space.get_neighbors(
            pos, self.model.contact_radius, include_center=False
        )
        for other in neighbors:
            if isinstance(other, Person) and other.state == Health.INFECTED:
                p = self.model.infection_prob
                if self.state == Health.VACCINATED and self.model.vaccinated_effect:
                    p *= (1.0 - self.model.vaccinated_effect)
                if random.random() < p:
                    self.state = Health.INFECTED
                    break

    # --- step ----------------------------------------------------------------
    def step(self):
        """One tick: move, reflect, update infection state."""
        x, y = self.pos
        nx, ny = x + self.vx * self.speed, y + self.vy * self.speed
        nx, ny = self._reflect_on_edge(nx, ny)
        self._reflect_on_people((nx, ny))
        self.model.space.move_agent(self, (nx, ny))
        self._maybe_infect((nx, ny))
