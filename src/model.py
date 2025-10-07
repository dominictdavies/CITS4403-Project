from mesa import Model
from mesa.space import ContinuousSpace

from mesa.datacollection import DataCollector
from .agents import Person, Health
import random


def count_infected(m):
    return sum(1 for a in m.agents if isinstance(a, Person) and a.state == Health.INFECTED)

def count_susceptible(m):
    return sum(1 for a in m.agents if isinstance(a, Person) and a.state == Health.SUSCEPTIBLE)

def count_total(m):
    return sum(1 for _ in m.agents)


class InfectionModel(Model):
    """
    Continuous-space infection spread model with separated radii:

    - collision_radius: used only for velocity flip (collision proxy)
    - contact_radius:   used only for infection proximity

    Distancing scales contact_radius; hygiene scales infection_prob.
    """

    def __init__(self,
                 N=120, width=100, height=100,
                 speed=2.0,
                 collision_radius=1.0,
                 contact_radius=3.0,
                 infection_prob=0.35,
                 initial_infected=3,
                 vaccinated_rate=0.0,
                 vaccinated_effect=0.5,
                 hygiene_factor=1.0,
                 distancing_factor=1.0,
                 seed=None):
        super().__init__()
        if seed is not None:
            random.seed(seed)

        # domain & agent step
        self.width, self.height = width, height
        self.space = ContinuousSpace(width, height, torus=False)
        self.agents.shuffle_do("step")

        # parameters
        self.collision_radius = float(collision_radius)
        base_contact = float(contact_radius)
        self.contact_radius = base_contact * max(0.0, float(distancing_factor))

        self.base_infection_prob = infection_prob
        self.infection_prob = max(0.0, min(1.0, infection_prob * max(0.0, float(hygiene_factor))))
        self.vaccinated_effect = max(0.0, min(1.0, vaccinated_effect))

        # agents
        for i in range(N):
            state = Health.SUSCEPTIBLE
            if i < initial_infected:
                state = Health.INFECTED
            elif random.random() < max(0.0, min(1.0, vaccinated_rate)):
                state = Health.VACCINATED

            a = Person(self, speed=speed, state=state)
            self.space.place_agent(a, (random.uniform(0, width), random.uniform(0, height)))

        # data
        self.datacollector = DataCollector(model_reporters={
            "Infected": count_infected,
            "Susceptible": count_susceptible,
            "Total": count_total,
        })

        self.running = True

    def step(self):
        """Advance one tick and stop once no susceptibles remain."""
        self.datacollector.collect(self)
        self.agents.do("step")
        if all(isinstance(a, Person) and a.state != Health.SUSCEPTIBLE for a in self.agents):
            self.running = False
