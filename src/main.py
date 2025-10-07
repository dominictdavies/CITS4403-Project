"""Entry point for running the InfectionModel simulation."""

from src.model import InfectionModel
from src.visualisation import run_simulation


if __name__ == "__main__":
    model = InfectionModel(
        N=128,
        width=1280,
        height=1280,
        speed=1.0,
        collision_radius=0.1,  # TODO: Fix collision_radius
        contact_radius=10.0,
        infection_prob=0.5,
        initial_infected=1,
        seed=42,
    )

    run_simulation(model)
