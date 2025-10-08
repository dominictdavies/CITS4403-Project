"""Entry point for running the InfectionModel simulation."""

from src.model import InfectionModel
from src.visualisation import run_simulation

if __name__ == "__main__":
    model = InfectionModel(
        N=128,
        width=1280,
        height=1280,
        speed=1.0,
        collision_radius=10.0,
        contact_radius=20.0,
        infection_prob=0.5,
        vaccinated_effect=1.0,
        vaccinated_rate=0.2,
        initial_infected=1,
        seed=42,
    )

    run_simulation(model, fps=120)
