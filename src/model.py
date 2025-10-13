import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace

from utils.config import SimulationConfig

from .agents import Health, Person


def count_infected(m):
    return sum(
        1 for a in m.agents if isinstance(a, Person) and a.state == Health.INFECTED
    )


def count_susceptible(m):
    return sum(
        1 for a in m.agents if isinstance(a, Person) and a.state == Health.SUSCEPTIBLE
    )


def count_total(m):
    return sum(1 for _ in m.agents)


class InfectionModel(Model):
    """
    Continuous-space infection spread model with separated radii:

    - collision_radius: used only for velocity flip (collision proxy)
    - contact_radius:   used only for infection proximity

    Distancing scales contact_radius; hygiene scales frame_infection_prob.
    """

    def __init__(self, config: SimulationConfig):
        super().__init__(seed=config.seed)
        random.seed(config.seed)
        self.width = config.world.width
        self.height = config.world.height
        self.space = ContinuousSpace(self.width, self.height, torus=True)
        self.config = config

        # agents
        for i in range(config.population.num_people):
            state = Health.SUSCEPTIBLE
            if i < config.population.initial_infected:
                state = Health.INFECTED
            elif random.random() < max(
                0.0, min(1.0, config.population.vaccinated_rate)
            ):
                state = Health.VACCINATED

            a = Person(self, speed=config.world.speed, state=state)
            self.space.place_agent(
                a,
                (
                    random.uniform(0, config.world.width),
                    random.uniform(0, config.world.height),
                ),
            )

        # data
        self.datacollector = DataCollector(
            model_reporters={
                "Infected": count_infected,
                "Susceptible": count_susceptible,
                "Total": count_total,
            }
        )

        self.running = True

    def step(self):
        """Advance one tick and stop once no susceptibles remain."""
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")
        if all(
            isinstance(a, Person) and a.state != Health.SUSCEPTIBLE for a in self.agents
        ):
            self.running = False
