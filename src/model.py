from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from .agents import Person, Health
import random


# --- metrics for DataCollector ----------------------------------------------

def count_infected(m):
    return sum(
        1 for a in m.schedule.agents
        if isinstance(a, Person) and a.state == Health.INFECTED
    )

def count_susceptible(m):
    return sum(
        1 for a in m.schedule.agents
        if isinstance(a, Person) and a.state == Health.SUSCEPTIBLE
    )


class InfectionModel(Model):
    """
    Minimal infection spread model in continuous 2D space.

    Parameters
    ----------
    N : int
        Number of agents.
    width, height : float
        Size of the simulation box.
    speed : float
        Agent speed per step (units of space per tick).
    collision_radius : float
        Neighborhood radius used as a collision / contact proxy.
    infection_prob : float in [0, 1]
        Per-step infection probability upon contact with an infected agent.
    initial_infected : int
        Number of initially infected agents.
    vaccinated_rate : float in [0, 1]
        Fraction of agents initialized as vaccinated (reserved; optional).
    vaccinated_effect : float in [0, 1]
        Multiplicative reduction on infection probability for vaccinated.
    """

    def __init__(self, N=120, width=100, height=100,
                 speed=1.2, collision_radius=1.5,
                 infection_prob=0.25, initial_infected=3,
                 vaccinated_rate=0.0, vaccinated_effect=0.5):
        super().__init__()

        # Domain and scheduler
        self.width, self.height = width, height
        self.space = ContinuousSpace(width, height, torus=False)
        self.schedule = RandomActivation(self)

        # Model parameters
        self.collision_radius = collision_radius
        self.infection_prob = infection_prob
        self.vaccinated_effect = vaccinated_effect

        # Agent initialization
        for i in range(N):
            state = Health.SUSCEPTIBLE
            if i < initial_infected:
                state = Health.INFECTED
            elif random.random() < vaccinated_rate:
                state = Health.VACCINATED

            a = Person(i, self, speed=speed, state=state)
            self.schedule.add(a)
            self.space.place_agent(
                a, (random.uniform(0, width), random.uniform(0, height))
            )

        # Time-series collection for plots
        self.datacollector = DataCollector(model_reporters={
            "Infected": count_infected,
            "Susceptible": count_susceptible
        })

        self.running = True

    def step(self):
        """Advance the simulation by one tick and stop when no S remain."""
        self.datacollector.collect(self)
        self.schedule.step()

        # Termination: all agents are non-susceptible
        if all(
            isinstance(a, Person) and a.state != Health.SUSCEPTIBLE
            for a in self.schedule.agents
        ):
            self.running = False
