"""Infection model using Mesa agent-based modelling framework."""

import random
import sys

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace

from utils.config import SimulationConfig

from .agents import Health, Person


def count_susceptible(model: Model):
    """Counts the number of agents that are currently susceptible"""
    return sum(
        1
        for a in model.agents
        if isinstance(a, Person) and a.state == Health.SUSCEPTIBLE
    )


def count_infected(model: Model):
    """Counts the number of agents that are currently infected"""
    return sum(
        1 for a in model.agents if isinstance(a, Person) and a.state == Health.INFECTED
    )


def count_recovered(model: Model):
    """Counts the number of agents that are currently recovered"""
    return sum(
        1 for a in model.agents if isinstance(a, Person) and a.state == Health.RECOVERED
    )


def count_vaccinated(model: Model):
    """Counts the number of agents that are currently vaccinated"""
    return sum(
        1
        for a in model.agents
        if isinstance(a, Person) and a.state == Health.VACCINATED
    )


def count_total(model: Model):
    """Counts the number of agents in the simulation"""
    return sum(1 for _ in model.agents)


class InfectionModel(Model):
    """
    Agent-based infection model in continuous 2D space.

    Attributes:
        width: Width of the simulation space.
        height: Height of the simulation space.
        space: Mesa ContinuousSpace with toroidal wrapping.
        config: SimulationConfig containing all model parameters.
        datacollector: Collects population counts at each time step.
        running: Whether the simulation should continue (stops when no susceptibles remain).
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
                "Susceptible": count_susceptible,
                "Infected": count_infected,
                "Recovered": count_recovered,
                "Vaccinated": count_vaccinated,
                "Total": count_total,
            }
        )

    def step(self):
        """Advance one tick and stop once no susceptibles remain."""
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")
        if count_infected(self) == 0:
            sys.exit(0)
