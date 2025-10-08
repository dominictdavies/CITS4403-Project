import numpy as np
import pandas as pd
import seaborn as sns
import mesa


class InfectionAgent(mesa.Agent):
    """An agent that may spread the infection."""

    def __init__(self, model):
        super().__init__(model)
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.1, 0.1])

    def move(self):
        self.position += self.velocity
        print(f"{self.unique_id!s}: Arrived at {self.position}")


class InfectionModel(mesa.Model):
    """A model with some number of infection agents."""

    def __init__(self, n, seed=None):
        super().__init__(seed=seed)
        self.num_agents = n
        InfectionAgent.create_agents(model=self, n=n)

    def step(self):
        """Advance the model by one step."""
        self.agents.shuffle_do("move")


if __name__ == "__main__":
    infection_model = InfectionModel(10)
    infection_model.step()
